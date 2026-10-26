"""Render recorded results only. No network, model calls, or answer-key edits."""
from collections import Counter
from html import escape
import json
from pathlib import Path
from .run import OUT, DATA, load_corpus

# Post-run qualitative review, not replacements for the frozen scorer or key.
REVIEW = {
 ('CT_02','clean','required_action'): ('supported_extra_text','Complete keyed action plus the printed mailing destination; strict scorer overcounts this as wrong.'),
 ('CT_02','degraded','required_action'): ('supported_extra_text','Complete keyed action plus printed mailing destination, with final comma instead of period.'),
 ('ME_01','clean','required_action'): ('ocr_word_error','OCR changed fine to tine and registration to registraticn; copied as verified.'),
 ('ME_01','clean','contact'): ('wrong_contact','The email ends in .ccm instead of the printed .com. It is also displayed in the English explanation.'),
 ('ME_02','clean','required_action'): ('ocr_word_error','OCR changed money to moncy; constraints are otherwise retained.'),
 ('ME_02','degraded','required_action'): ('omitted_constraints','Verified action omits the printed no-cards and do-not-mail-cash sentences. The money-order option remains, but the mailing restriction is lost.'),
 ('NH_01','degraded','required_action'): ('supported_extra_text','Adds the printed agency-response timeline and possible later decision; no invented resident deadline in this action.'),
 ('NH_02','clean','contact'): ('label_only','Correct phone digits with the printed Questions label. Strict mismatch, not a wrong number.'),
 ('NY_01','clean','required_action'): ('corrupted_timing','Verified action says 3C days instead of 30. The separate deadline field is unverified, but that does not suppress this action.'),
 ('PA_01','clean','contact'): ('ocr_word_error','Correct printed URL prefixed by OCR garbage ss; URL itself is intact.'),
 ('PA_01','degraded','contact'): ('supported_extra_text','Both printed contact channels preserved, but combined differently from the predeclared aliases.'),
 ('PA_02','clean','deadline'): ('conditional_deadline_policy','Printed November 5 payment date is real; the key requires abstention because contesting has a different deadline. This is loss of conditional context, not an invented date.'),
 ('PA_02','degraded','deadline'): ('conditional_deadline_policy','Same conditional-context failure: a single verified deadline cannot represent both payment and hearing-request branches.'),
 ('RI_02','degraded','contact'): ('label_only','Correct phone digits with Questions label; harmless strict-format failure.'),
 ('VT_01','clean','deadline'): ('wrong_year','OCR anchor changes 2026 to 2926. Validator computes and verifies November 25, 2926; English repeats it.'),
 ('VT_01','clean','required_action'): ('ocr_word_error','OCR changes ticket to Licket; action remains understandable but is not an exact reproduction.'),
 ('VT_02','clean','deadline'): ('inclusive_count_bug','Printed rule counts October 26 as day 1. November 8 is day 14, but validator verifies November 9.'),
 ('VT_02','clean','required_action'): ('ocr_word_error','OCR changes citation to citahon; the day-1 condition is preserved in the action despite wrong date calculation.'),
 ('VT_02','degraded','deadline'): ('inclusive_count_bug','Validator again verifies November 9 instead of November 8. OCR additionally misreads day 1 as day I.'),
 ('VT_02','degraded','required_action'): ('corrupted_timing','The printed day 1 becomes day I and remains verified. This reinforces the need to verify the counting convention against the image.'),
 ('VT_02','degraded','contact'): ('ocr_word_error','Street is misread as Suect; address number, street name, city, state and ZIP remain intact.'),
}

def frac(n,d):return f'{n}/{d} ({100*n/d:.2f}%)' if d else 'N/A (0/0)'
def metric(x):return frac(x['n'],x['d'])
def cell(x):return str(x).replace('|','\\|').replace('\n',' ')

def main():
    m,items=load_corpus()
    report=json.loads((OUT/'results.json').read_text());rows=report['records'];s=report['summary']
    actual={(r['sample'],r['variant'],n) for r in rows for n,v in r['scores']['full'].items() if v['false_verified']}
    assert actual==set(REVIEW),'Review must cover every strict false-verification'
    reviews=[dict(sample=k[0],variant=k[1],field=k[2],category=v[0],note=v[1]) for k,v in REVIEW.items()]
    (OUT/'qualitative-review.json').write_text(json.dumps({'post_hoc':True,'author':'Codex; not independent human adjudication',
        'scores_changed':False,'reviews':reviews},indent=2)+'\n')
    direct=sum(c['route_id'] is not None for c in items)
    lines=['# Northeast parking-notice stress test','',
        '**Result: FAIL for unattended reliability. The run completed, but unsafe verified outputs remain.**','',
        'Two researched synthetic notices per state (CT, ME, MA, NH, NJ, NY, PA, RI, VT), each clean and degraded: **18 source notices / 36 image runs**. These are exploratory assistant-authored tests, not independent held-out evidence.','',
        'Sources checked October 26, 2026. Only the two Pennsylvania layouts were reconstructed after visual inspection of official sample tickets; the other sixteen are content reconstructions from official instructions, not exact replicas of unseen forms. All case identities/dates/sums are synthetic; public issuer/contact names are retained. Pittsburgh uses a historical 2018 sample.','',
        '## Results','',
        '| Measure | Recorded result |','| --- | --- |',
        f'| Strict case PASS | {frac(s["case_pass"],len(rows))} |',
        f'| Strict case FAIL | {frac(len(rows)-s["case_pass"],len(rows))} |',
        f'| Correct extracted values where truth is present | {metric(s["all_fields"]["field_accuracy"])} |',
        f'| Correct values including expected missing/ambiguous | {frac(s["all_opportunity_correct"],s["all_opportunity_total"])} |',
        f'| Strict false-verified, all four fields | {metric(s["all_fields"]["false_verified_rate"])} |',
        f'| Strict false-verified, deadline/amount/action | {metric(s["critical"]["false_verified_rate"])} |',
        f'| Strict mismatches among verified fields | {metric(s["all_fields"]["wrong_among_verified"])} |',
        f'| MISSING or unverified, all field opportunities | {frac(s["missing_or_unverified"],s["all_opportunity_total"])} |',
        f'| Abstain when truth is present | {metric(s["all_fields"]["abstain_when_truth_exists"])} |',
        f'| Correct AND verified where truth is present | {metric(s["all_fields"]["usable_verified_accuracy"])} |',
        f'| Correct missing (no value supplied) | {metric(s["all_fields"]["correct_to_say_missing"])} |',
        f'| Pipeline unavailable | {metric(s["all_fields"]["unavailable_rate"])} |','',
        '**Interpretation:** PASS means the four scored fields match the declared key (or its predeclared aliases) and the English explanation stage returns. It does not require every field to be verified. In particular, human amount confirmation was not simulated: all thirty present amounts remain unverified/missing by design.','',
        'The strict scorer checks normalized values, copied actions and declared contact aliases. It counts harmless extra source text/labels as failures. Six of the 21 strict false-verifications are supported extra text or label-only differences; they remain in the published counts. Other differences include minor OCR misspellings, conditional-deadline representation limits, and real wrong dates/contacts. Do not interpret 21/144 as 21 independently adjudicated harmful errors.','',
        'ME_02 correctly withholds a calendar date for its unsupported hours/weekend rule, but strict value scoring still marks its retained unverified rule wrong because the key is null. Similarly, safe refusal to normalize a relative deadline counts against coverage. Neither is a verified invented date.','',
        '## Highest-priority findings','',
        '1. **Date verification can preserve catastrophic OCR errors:** VT_01 clean verifies and displays November 25, **2926**, from a misread issue-year anchor. Expected: November 25, 2026.',
        '2. **Inclusive counting is wrong:** VT_02 clean and degraded verify November **9**, although counting October 26 as day 1 makes the printed rule end November **8**.',
        '3. **Contacts and timing inside actions inherit OCR errors:** ME_01 clean verifies `.ccm` instead of `.com`; NY_01 clean verifies `3C days` instead of `30 days` even while the standalone deadline is unverified.',
        '4. **Complete instructions are not guaranteed:** ME_02 degraded drops the no-card/do-not-mail-cash sentences from its verified action.',
        '5. **Conditional dates lose context:** PA_02 selects the real payment date as a single verified deadline despite a different contest deadline. The key explicitly requires abstention; this is a representation/policy failure rather than a fabricated date.',
        '6. **Automatic classification is still unconfigured:** all 36 readings report unknown; this run explicitly selected parking_ticket. Issuing-agency strings also contain OCR corruption; agency is preserved in raw outputs but excluded from the historical four-field metric.','',
        'The English guard passed in all 36 runs with model-generated explanations and no reported guard failures. That checks consistency with extracted fields, not the truth of those fields: the bad year/date/contact survive into displayed English.','',
        '## Field results','', '| Field | Correct / truth present | Strict false-verified / all cases | Abstain / truth present |', '| --- | --- | --- | --- |']
    for name,stats in s['per_field'].items():lines.append('| '+name+' | '+' | '.join(metric(stats[k]) for k in ['field_accuracy','false_verified_rate','abstain_when_truth_exists'])+' |')
    lines+=['','## By state','', '| State | Cases passing | Value accuracy (present) | Strict false-verified |', '| --- | --- | --- | --- |']
    for state,stats in s['per_state'].items():
        subset=[r for r in rows if r['state']==state]
        lines.append(f'| {state} | {sum(r["case_pass"] for r in subset)}/{len(subset)} | {metric(stats["field_accuracy"])} | {metric(stats["false_verified_rate"])} |')
    lines+=['','## Clean versus degraded','', '| Variant | Value accuracy (present) | Strict false-verified |', '| --- | --- | --- |']
    for name,stats in s['per_variant'].items():lines.append(f'| {name} | {metric(stats["field_accuracy"])} | {metric(stats["false_verified_rate"])} |')
    lines+=['','Degradation sometimes changes OCR in a helpful direction; these correlated samples and one repetition do not establish that poor photos perform better.','',
        '## Each case','', '| Case | Issuer | Clean | Degraded | Routing with explicit state/issuer choice |', '| --- | --- | --- | --- | --- |']
    for c in items:
        subset={r['variant']:r for r in rows if r['sample']==c['id']}
        outcome=lambda v:'PASS' if subset[v]['case_pass'] else 'FAIL'
        lines.append(f'| {c["id"]} | {c["issuer"]} | {outcome("clean")} | {outcome("degraded")} | '+('Official route: '+c['route_id'] if c['route_id'] else 'Unlisted issuer: fallback, no payment link')+' |')
    lines+=['',f'Routing checks pass for **18/18** declared selections: **{direct}/18** have a bundled route and **{18-direct}/18** correctly fall back. The route checks execute the frontend selector function, not the external payment service. A person supplies the issuer; no OCR-based jurisdiction identification is claimed. Maine Capitol Police is not silently sent to the municipal portal, and Kingston is not sent to NYC.','',
        '## Reproduction and evidence','',
        f'- Base application commit: `{report["commit"]}`; application SHA-256: `{report["application_sha256"]}`. Backend/frontend files were unchanged throughout the run.',
        f'- Corpus manifest SHA-256 before calls: `{report["manifest_sha256"]}`. All image/answer hashes still match.',
        f'- Started `{report["started_at"]}`; finished `{report["completed_at"]}`.',
        '- Local preprocessed reader; pinned `gpt-5.4-mini-2026-03-17` (the README/render.yaml model); temperature 0, reasoning none; reference date October 26, 2026; two workers; one measurement per image. These are pinned evaluation settings; HTTP/browser provider defaults were not measured. The ignored local env uses the unversioned `gpt-5.4-mini` alias, which this run does not override.',
        '- Direct production component calls: image normalization → local OCR → extraction → deterministic validators → English explanation. No mocked reader or extractor. HTTP/CORS, deployed URL, mobile interaction, Spanish/Tagalog and read-aloud were not part of this stress run.',
        '- OCR was confirmed unchanged; parking_ticket selected explicitly. No amount checkbox or human correction simulated. All fields, source snippets, raw OCR, proposals, explanation and token usage are retained in [results.json](results.json).',
        '- [All failed cases in full](FAILURE_DETAILS.md), [qualitative review](qualitative-review.json), [visual gallery and provenance](gallery.html), [frozen manifest](../../eval/northeast_stress/corpus/manifest.json).',
        '- Regression checks: **430 Python tests pass**, one existing Starlette/AnyIO deprecation warning; **60 JavaScript tests pass**. See [Python log](pytest.txt) and [JavaScript log](node.txt).',
        '- Original held-out corpus, results and eval-freeze tag were neither rerun nor edited. This set cannot replace that independent evaluation. No production bug fixes or deployment are included.',
        '- API key loaded only inside the process, sent only to the configured OpenAI API by existing clients, and checked against serialized synthetic results before writing. Keys, headers and provider error bodies are never logged. Synthetic test images/text are intentionally saved by this opt-in evaluation tool, not by the production upload path.','',
        'Exact commands, run from the repository:','', '```sh',
        '../../work/m4-audit-venv/bin/python -m eval.northeast_stress.build',
        '../../work/m4-audit-venv/bin/python -m eval.northeast_stress.run --dry-run',
        '../../work/m4-audit-venv/bin/python -m eval.northeast_stress.run > ../../work/northeast-stress-run.log 2>&1',
        '../../work/m4-audit-venv/bin/python -m pytest -q > results/northeast-stress/pytest.txt 2>&1',
        '/opt/homebrew/bin/node --test tests/*.mjs > results/northeast-stress/node.txt 2>&1',
        '../../work/m4-audit-venv/bin/python -m eval.northeast_stress.report', '```','',
        'The build command refuses to overwrite an existing corpus; the live runner refuses a second run into the existing result directory. `--resume` processes only unfinished cases after matching hashes. On a new machine use the project dependencies plus python-dotenv (also used by the existing eval runner), Tesseract and a TrueType font. Report generation is offline and may be repeated.','',
        '## Source provenance','',
        'Each source describes a sample form or a local process. Synthetic case dates and amounts must not be used as real legal/payment guidance.','']
    for c in items:
        lines += [f'### {c["id"]}: {c["issuer"]}', '', c['source_basis'], '',
            *[f'- [Official source {i+1}]({url})' for i,url in enumerate(c['sources'])], '']
    (OUT/'REPORT.md').write_text('\n'.join(lines).rstrip()+'\n')
    details=['# Full failure records','', 'Original strict scores are retained; review notes do not change them. All content below is synthetic.','']
    for r in rows:
        if r['case_pass']:continue
        c=next(c for c in items if c['id']==r['sample'])
        details += [f'## {r["sample"]} — {r["variant"]}', '',
            f'[Input image](../../eval/northeast_stress/corpus/{r["input_image"]})','',
            '### Every strict field mismatch','']
        for name,value in r['scores']['full'].items():
            if not value['wrong']:continue
            details += [f'**{name}**: {value["status"]}; false-verified={value["false_verified"]}',
                '', 'Expected: `'+str(value['expected'])+'`', '', 'Observed: `'+str(value['got'])+'`','']
            review=REVIEW.get((r['sample'],r['variant'],name))
            if review:details += ['Review: '+review[1],'']
        details += ['### Visible source text','', '```text',c['visible_text'],'```','',
            '### Full OCR text','', '```text',r.get('reading',{}).get('text','UNAVAILABLE'),'```','',
            '### Complete proposed and checked fields','', '```json',json.dumps({'proposal':r.get('proposal'),
                'extraction':r.get('extraction')},indent=2,ensure_ascii=False),'```','',
            '### Complete displayed explanation','', '```json',json.dumps(r.get('explanation'),indent=2,ensure_ascii=False),'```','']
    (OUT/'FAILURE_DETAILS.md').write_text('\n'.join(details).rstrip()+'\n')
    html=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
        '<title>Northeast synthetic parking corpus</title><style>body{font:17px/1.5 system-ui;max-width:1200px;margin:auto;padding:24px;background:#fafafa;color:#181818}a{color:#174c82}section{border-top:2px solid #ccc;padding:24px 0}.images{display:grid;grid-template-columns:1fr 1fr;gap:20px}img{max-width:100%;max-height:700px;object-fit:contain;border:1px solid #ccc;background:white}figure{margin:0}details{margin:16px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere}table{border-collapse:collapse;width:100%}td,th{padding:8px;text-align:left;border:1px solid #ccc}@media(max-width:600px){.images{grid-template-columns:1fr}}</style>',
        '<h1>Northeast parking stress test</h1><p>18 synthetic notices, 36 images. These are not payable notices. Case details are invented; sources and limits are listed below.</p>',
        '<p><a href="REPORT.md">Results report</a> · <a href="FAILURE_DETAILS.md">Full failures</a></p>']
    for c in items:
        html += [f'<section><h2>{escape(c["id"])} — {escape(c["issuer"])}</h2><p>{escape(c["source_basis"])}</p>', '<div class="images">']
        for v in c['variants']:
            r=next(r for r in rows if r['sample']==c['id'] and r['variant']==v['name'])
            src='../../eval/northeast_stress/corpus/'+v['image']
            html += [f'<figure><a href="{src}"><img loading="lazy" src="{src}" alt="Synthetic {escape(c["id"])} {v["name"]} notice"></a><figcaption>{v["name"]}: {"PASS" if r["case_pass"] else "FAIL"} (strict key)</figcaption>',
                '<details><summary>Recorded fields and explanation</summary><pre>'+escape(json.dumps({'fields':r['extraction']['fields'],'english':r['explanation']['english']},indent=2,ensure_ascii=False))+'</pre></details></figure>']
        html+=['</div><details><summary>Answer key declared before the run</summary><pre>'+escape(json.dumps(c['expected'],indent=2))+'</pre></details><ul>']
        html += ['<li><a href="'+escape(url,quote=True)+'">Official source '+str(i+1)+'</a></li>' for i,url in enumerate(c['sources'])]
        html += ['</ul></section>']
    html+=['</html>'];(OUT/'gallery.html').write_text('\n'.join(html)+'\n')
    print('Wrote REPORT.md, FAILURE_DETAILS.md, gallery.html and qualitative-review.json from the saved run.')

if __name__=='__main__':main()
