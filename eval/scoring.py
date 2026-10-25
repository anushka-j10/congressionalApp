"""Codex-generated PROPOSED scorer for student review; independent of validators."""
import re
import unicodedata
from collections import Counter
from datetime import datetime
from decimal import Decimal, InvalidOperation
from statistics import mean,pstdev,median
import math
from eval.protocol import FIELDS

VERSION='proposed-reliability-v3'
CRITICAL=('deadline','amount_due','required_action')


def text(value):
    return ' '.join(unicodedata.normalize('NFKC',str(value)).casefold().split()).rstrip(' .')


def canonical(name,value):
    if value is None:return None
    value=unicodedata.normalize('NFKC',str(value)).strip()
    if name in {'amount_due','deadline'} and text(value) in {'not specified','not stated','not provided','none','n/a','no payment is requested','no payment requested','no deadline is stated','no return deadline is stated'}:
        return None
    if name=='amount_due' and re.fullmatch(r'not (?:stated|specified|provided)[;,.]\s*(?:fines?|fees?|costs?)\b[a-z\s,()\-]*\b(?:determined|decided|set)\b[a-z\s,()\-]*[.]?',value,re.I):
        return None  # Explicit absence plus a non-numeric future-determination explanation.
    if name=='amount_due':
        if not re.fullmatch(r'\$?\s*[0-9]+(?:,[0-9]{3})*(?:\.[0-9]{1,2})?',value):return text(value)
        try:return format(Decimal(value.replace('$','').replace(',','').strip()),'.2f')
        except InvalidOperation:return text(value)
    if name=='deadline':
        weekday=re.match(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+',value,re.I)
        candidate=value[weekday.end():] if weekday else value
        candidate=re.sub(r'\s+(?:at\s+)?(?:1[0-2]|0?[1-9])(?::[0-5][0-9])?\s*(?:AM|PM)$','',candidate,flags=re.I)
        for pattern in ['%Y-%m-%d','%m/%d/%Y','%B %d, %Y','%B %d %Y','%b %d, %Y']:
            try:
                parsed=datetime.strptime(candidate.rstrip(' .'),pattern).date()
                if weekday and parsed.strftime('%A').casefold()!=weekday[1].casefold():return text(value)
                return parsed.isoformat()
            except ValueError:pass
    return text(value)


def equivalent(name,left,right):
    """Bounded equivalence, not an LLM judge or unrestricted paraphrase credit.

    Dropping a courtesy/modality prefix cannot drop the rest of an instruction.
    Timings, alternatives, amounts and destinations must remain identical.
    """
    if name=='required_action' and left is not None and right is not None:
        core=lambda value:re.sub(r'^(?:please\s+|you must\s+)','',text(value))
        return core(left)==core(right)
    return canonical(name,left)==canonical(name,right)


def score_field(name,truth,expected_state,field,aliases=(),unavailable=False):
    candidate=field.get('normalized_value') or field.get('value')
    status=field.get('status','missing')
    correct=(canonical(name,candidate)==canonical(name,truth) or
             candidate is not None and any(canonical(name,candidate)==canonical(name,alias) for alias in aliases))
    if expected_state=='ambiguous':correct=candidate is None
    if unavailable:correct=False
    equivalent_correct=(equivalent(name,candidate,truth) or candidate is not None and any(equivalent(name,candidate,alias) for alias in aliases))
    if expected_state=='ambiguous':equivalent_correct=candidate is None
    if unavailable:equivalent_correct=False
    wrong=not correct
    return {'expected':truth,'expected_state':expected_state,'got':candidate,'canonical_got':canonical(name,candidate),'status':status,
        'correct_value_present':correct and expected_state=='present',
        'usable_verified_correct':correct and expected_state=='present' and status=='verified',
        'wrong':wrong,'false_verified':wrong and status=='verified' and not unavailable,
        'flagged_wrong':wrong and status in {'missing','unverified'} and not unavailable,
        'abstain_when_truth_exists':expected_state=='present' and status in {'missing','unverified'} and not unavailable,
        'correct_to_say_missing':expected_state=='missing' and canonical(name,candidate) is None and (status=='missing' or candidate is not None) and not unavailable,
        'unavailable':unavailable,
        'exact_wording_match':text(candidate)==text(truth) if candidate is not None and truth is not None else candidate is truth,
        'equivalent_value_present':equivalent_correct and expected_state=='present',
        'equivalence_false_verified':not equivalent_correct and status=='verified' and not unavailable}


def score_row(row):
    result={}
    for mode in ['B1','B2','full']:
        method=row.get('methods',{}).get(mode,{})
        unavailable=bool(row.get('error') or method.get('error'))
        result[mode]={name:score_field(name,row['expected'][name],row['expected_state'][name],
            method.get('fields',{}).get(name,{}),row.get('expected_aliases',{}).get(name,()),unavailable)
            for name in FIELDS}
    return result


def fraction(n,d):return {'n':n,'d':d,'rate':n/d if d else None}


def aggregate(records,mode,names=FIELDS):
    fields=[row['scores'][mode][name] for row in records for name in names]
    counts=Counter()
    for value in fields:
        for key in ['correct_value_present','usable_verified_correct','wrong','false_verified','flagged_wrong',
                    'abstain_when_truth_exists','correct_to_say_missing','unavailable',
                    'equivalent_value_present','equivalence_false_verified']:
            counts[key]+=bool(value[key])
        counts['truth_present']+=value['expected_state']=='present'
        counts['truth_missing']+=value['expected_state']=='missing'
        counts['verified_outputs']+=value['status']=='verified' and not value['unavailable']
    return {'opportunities':len(fields),'counts':dict(counts),
        'field_accuracy':fraction(counts['correct_value_present'],counts['truth_present']),
        'usable_verified_accuracy':fraction(counts['usable_verified_correct'],counts['truth_present']),
        'false_verified_rate':fraction(counts['false_verified'],len(fields)),
        'wrong_among_verified':fraction(counts['false_verified'],counts['verified_outputs']),
        'flagged_correctly_rate':fraction(counts['flagged_wrong'],counts['wrong']-counts['unavailable']),
        'abstain_when_truth_exists':fraction(counts['abstain_when_truth_exists'],counts['truth_present']),
        'correct_to_say_missing':fraction(counts['correct_to_say_missing'],counts['truth_missing']),
        'unavailable_rate':fraction(counts['unavailable'],len(fields)),
        'limited_equivalence_accuracy':fraction(counts['equivalent_value_present'],counts['truth_present']),
        'limited_equivalence_false_verified_rate':fraction(counts['equivalence_false_verified'],len(fields))}


def summarize(records):
    for row in records:row['scores']=score_row(row)
    summary={}
    for mode in ['B1','B2','full']:
        headline=aggregate(records,mode,CRITICAL)
        summary[mode]={'headline_critical':headline,'all_fields':aggregate(records,mode),
            'per_field':{name:aggregate(records,mode,[name]) for name in FIELDS}}
        repeated=[]
        for rep in sorted({row['repetition'] for row in records}):
            result=aggregate([row for row in records if row['repetition']==rep],mode,CRITICAL)
            repeated.append({'repetition':rep,'false_verified':result['false_verified_rate'],
                             'field_accuracy':result['field_accuracy']})
        values=[item['false_verified']['rate'] for item in repeated if item['false_verified']['rate'] is not None]
        summary[mode]['repeats']=repeated
        summary[mode]['false_verified_variance']={'mean':mean(values) if values else None,
             'population_stddev':pstdev(values) if values else None,'min':min(values) if values else None,
             'max':max(values) if values else None}
    return summary


def display(rate):
    return f"{rate['n']}/{rate['d']} ({100*rate['rate']:.1f}%)" if rate['rate'] is not None else 'N/A'



def usage_cost(usage,rates):
    total=usage.get('input_tokens',0);cached=min(total,usage.get('cached_input_tokens',0))
    return ((total-cached)*rates['usd_per_million_input']+cached*rates['usd_per_million_cached_input']+
            usage.get('output_tokens',0)*rates['usd_per_million_output'])/1_000_000


def method_usage(row,mode):
    baseline=Counter(row.get('methods',{}).get('B1',{}).get('usage',{}))
    language=Counter(row.get('language_usage_including_B1',{}))
    remaining=language-baseline
    extraction=Counter(row.get('extraction_usage',{}))
    if mode=='B1':return baseline
    if mode=='B2':return remaining if row.get('selected_type')=='unknown' else extraction
    return Counter() if row.get('selected_type')=='unknown' else extraction+remaining


def markdown(report):
    lines=['# M4 '+report['set']+' evaluation — '+report['status'],'',
      'Run date: '+report['run_date']+'; today: '+report['config']['today']+'; model: `'+report['config']['model']+'`.',
      'Temperature: '+str(report['config']['temperature'])+'; reasoning: '+report['config']['reasoning_effort']+'; scorer: '+VERSION+'.',
      'Records: '+str(len(report['records']))+'/'+str(report['planned_records'])+' (clean/degraded × repeats; correlated synthetic layouts).','',
      '**Headline: wrong Verified deadlines, amounts or actions per critical-field opportunity.**',
      'Also report wrong among Verified outputs, since abstention changes coverage. Exact-copy text scoring can count a valid paraphrase wrong; inspect failures.',
      'Truth-present accuracy excludes ambiguous/absent fields; false-verification opportunities include them. Thus 100% accuracy does not imply zero unsafe claims.','',
      '| Method | False-verified (critical) | Wrong among Verified | Field accuracy (truth present) | Usable verified accuracy | Flagged wrong | Unavailable |',
      '| --- | --- | --- | --- | --- | --- | --- |']
    if report['config'].get('protocol',{}).get('amount_review'):
        lines[9:9]=['Human amount review is NOT simulated. Amounts and money-bearing actions remain unverified by default; evaluate coverage as well as false-verification. Agreement between OCR passes is not proof of correctness.','']
    for mode,section in report['summary'].items():
        d=section['headline_critical']
        lines.append('| '+mode+' | '+' | '.join(display(d[key]) for key in ['false_verified_rate','wrong_among_verified','field_accuracy','usable_verified_accuracy','flagged_correctly_rate','unavailable_rate'])+' |')
    lines+=['','## Limited equivalence alongside strict scoring','',
      'Dates normalize supported weekday/time notation independently of production validators. Actions only tolerate a leading Please or You must; omitted timing, conditions, numbers or alternatives still fail. No free-form paraphrase or contact truncation is credited. Historical v2 results are not rewritten.',
      '', '| Method | Critical strict false-verified | Critical limited-equivalence false-verified | Limited-equivalence present accuracy |',
      '| --- | --- | --- | --- |']
    for mode,section in report['summary'].items():
        d=section['headline_critical']
        lines.append('| '+mode+' | '+' | '.join(display(d[key]) for key in ['false_verified_rate','limited_equivalence_false_verified_rate','limited_equivalence_accuracy'])+' |')
    lines+=['','## Per-field counts','', '| Method | Field | Accuracy | False-verified | Abstain when truth exists | Correct missing |', '| --- | --- | --- | --- | --- | --- |']
    for mode,section in report['summary'].items():
        for name,d in section['per_field'].items():
            lines.append('| '+mode+' | '+name+' | '+' | '.join(display(d[key]) for key in ['field_accuracy','false_verified_rate','abstain_when_truth_exists','correct_to_say_missing'])+' |')
    lines+=['','## Repeated-run variance','', '| Method | Run | False-verified (critical) | Accuracy |','| --- | --- | --- | --- |']
    for mode,section in report['summary'].items():
        for rep in section['repeats']:lines.append('| '+mode+' | '+str(rep['repetition'])+' | '+display(rep['false_verified'])+' | '+display(rep['field_accuracy'])+' |')
        var=section['false_verified_variance'];lines+=['',mode+' population standard deviation: '+str(var['population_stddev'])+'.','']
    lines+=['## Translation','', '| Method | Language | Number checks | Glossary checks | English fallback | Unavailable |', '| --- | --- | --- | --- | --- | --- |']
    for mode in ['B1','full']:
        for code in report['config']['languages']:
            n=len(report['records']);numbers=glossary=fallback=unavailable=0
            for row in report['records']:
                method=row.get('methods',{}).get(mode,{})
                if mode=='B1':
                    checks=method.get('translation',{}).get(code)
                    if checks is None:unavailable+=1;continue
                    numbers+=bool(checks.get('numbers'));glossary+=bool(checks.get('glossary'))
                else:
                    output=method.get('explanations',{}).get(code,{})
                    if not output or output.get('error'):unavailable+=1;continue
                    meta=output['translation'];fallback+=bool(meta['fallback_to_english'])
                    numbers+=bool(meta.get('static_messages_only')) or (not meta['fallback_to_english'] and bool(meta.get('checks',{}).get('numbers')))
                    glossary+=bool(meta.get('static_messages_only')) or (not meta['fallback_to_english'] and bool(meta.get('checks',{}).get('glossary')))
            lines.append('| '+mode+' | '+code+' | '+f'{numbers}/{n} | {glossary}/{n} | '+(f'{fallback}/{n}' if mode=='full' else 'N/A')+f' | {unavailable}/{n} |')
    rates=report.get('cost_basis') or report['config'].get('cost',{})
    if rates.get('status')=='standard_rate_estimate':
        lines+=['','## Latency and approximate model cost','', '| Method | Latency p50 (s) | Latency p95 (s) | Mean model USD / notice |','| --- | --- | --- | --- |']
        for mode in ['B1','B2','full']:
            values=sorted(row['methods'][mode]['latency_ms']/1000 for row in report['records'] if mode in row.get('methods',{}) and 'latency_ms' in row['methods'][mode])
            costs=[usage_cost(method_usage(row,mode),rates) for row in report['records']]
            if values:lines.append(f'| {mode} | {median(values):.2f} | {values[math.ceil(.95*len(values))-1]:.2f} | {mean(costs):.6f} |')
        lines+=['', 'p50 uses median; p95 uses nearest rank. Full runs both languages sequentially, B1 generates both in one call, and B2 has no language stage. Local/parallel resource contention affects timings.',
          'Cost uses actual reported tokens at [documented standard rates]('+rates['source']+') checked '+rates['checked_date']+'. Shared B2/full proposals are not two paid requests. These are hypothetical per-method costs, not values to sum as actual experiment spend.',
          rates['limitations']]
    lines+=['','B1 translates the whole OCR notice; full translates verified summaries. These are different scopes; glossary passes can be vacuous.',
      'Full translation success does not repair a wrongly selected Verified field. No native-speaker or physical-phone claim.',
      'B2 reuses the same raw proposal as full; it has no independent language stage.','',
      'Automatic classification is recorded separately; fixture type is explicitly selected, OCR text is confirmed unchanged by the harness.',
      'Multi-page sample uses page 1 only because the existing app accepts one photo; additional-page coverage is not simulated.',
      'Actual token usage is retained; failed-call unreported usage is unknown, never guessed.',
      ('No heldout data is included.' if report['set']!='heldout' else 'Frozen heldout attempt; no retry or post-test tuning.'),
      'A partial report or a failed provider call is never labeled a completed experiment.',
      'Scoring v2 recognizes explicit numeric-field absence claims and declared contact-name aliases. Static all-missing language bundles pass vacuous numeric/glossary checks.']
    return '\n'.join(lines)+'\n'
