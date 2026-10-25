"""Proposed deterministic checks. Review the policies in DESIGN_NOTES.md."""

import re
import unicodedata
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from difflib import SequenceMatcher

from backend.extraction_models import CheckedField

# Unsupported signs are rejected, never removed to produce a positive amount.
AMOUNT_SIGNS = '-+−﹣－⁻₋–—'

MAX_AMOUNT = Decimal('1000000.00')  # Explicit conservative policy, not a legal limit.
MONTHS = {name: index for index, name in enumerate(
    ['january', 'february', 'march', 'april', 'may', 'june', 'july',
     'august', 'september', 'october', 'november', 'december'], 1)}
DATE_PATTERN = re.compile(
    r'(?<![\w/.-])(?:[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}|'
    r'[0-9]{1,2}[/.-][0-9]{1,2}[/.-][0-9]{4}|'
    r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|'
    r'Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
    r'\.?\s+[0-9]{1,2}(?:st|nd|rd|th)?(?:,\s*|\s+)[0-9]{4})(?![\w/-]|\.[0-9])', re.I)
WEEKDAY = re.compile(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+', re.I)
TIME_PATTERN = re.compile(r'(?<![\w:])(?:1[0-2]|0?[1-9])(?::[0-5][0-9])?\s*(?:AM|PM)\b', re.I)
ROOM_PATTERN = re.compile(r'\b(?:courtroom|room|suite)\s+[A-Za-z]?[0-9]+\b', re.I)
MONEY_PATTERN = re.compile(r'(?<!\w)\$\s*(?:[0-9]{1,3}(?:,[0-9]{3})+|[0-9]+)(?:\.[0-9]{2})?(?![\w,]|\.[0-9]|\s*[-+−])')
RELATIVE = re.compile(r'within\s+([0-9]{1,3})\s+(?:calendar\s+)?days?\s+(?:of|after)\s+'
                      r'(?:the\s+)?(?:issue date|date (?:above|of this notice))', re.I)


def normalized_with_positions(text):
    """Collapse whitespace/case while retaining offsets in the ORIGINAL string."""
    chars, positions = [], []
    for index, char in enumerate(text):
        for expanded in unicodedata.normalize('NFKC', char).casefold():
            expanded = ' ' if expanded.isspace() else expanded
            if expanded == ' ' and (not chars or chars[-1] == ' '):
                continue
            chars.append(expanded)
            positions.append(index)
    return ''.join(chars).rstrip(), positions


def normalize(text):
    return normalized_with_positions(text)[0].strip()


def digits(text):
    # Never equate O/0, l/1 or S/5, or drop leading zeroes.
    return re.findall(r'\d+', unicodedata.normalize('NFKC', text))


def whole_span(source, start, end):
    """A snippet must not cut a longer number/ID or hide a negative sign."""
    target = source[start:end]
    before, after = source[:start], source[end:]
    if start and target[0].isalnum() and source[start - 1].isalnum():
        return False
    if after and target[-1].isalnum() and after[0].isalnum():
        return False
    if target[-1].isdigit() and re.match(r'[.,][0-9]', after):
        return False
    sign_prefix = before.rstrip()
    if target[0].isdigit() and sign_prefix.endswith('$'):
        sign_prefix = sign_prefix[:-1].rstrip()
    if (target[0].isdigit() or target.startswith('$')) and sign_prefix.endswith(tuple(AMOUNT_SIGNS + '(')):
        return False
    money_candidate = '$' in target or re.fullmatch(r'[0-9][0-9,.]*', target)
    if money_candidate and after.lstrip().startswith(tuple(AMOUNT_SIGNS + ')')):
        return False
    if target[0].isdigit() and re.search(r'[0-9][.,]$', before):
        return False
    return True


def find_source(text, snippet):
    """Exact normalized match first; tightly bounded letter-only fuzz second."""
    if not snippet or not snippet.strip():
        return None
    source, positions = normalized_with_positions(text)
    target = normalize(snippet)
    index = source.find(target)
    while index >= 0:
        if whole_span(source, index, index + len(target)):
            return positions[index], positions[index + len(target) - 1] + 1
        index = source.find(target, index + 1)
    if len(target) < 12:
        return None  # Short fuzzy snippets can accidentally match unrelated text.
    tokens = list(re.finditer(r'\S+', source))
    width = len(target.split())
    best, best_ratio = None, 0.94
    for count in {max(1, width - 1), width, width + 1}:
        for offset in range(len(tokens) - count + 1):
            start, end = tokens[offset].start(), tokens[offset + count - 1].end()
            candidate = source[start:end]
            if not whole_span(source, start, end):
                continue
            if abs(len(candidate) - len(target)) > max(3, len(target) // 10):
                continue
            if digits(candidate) != digits(target):
                continue
            matcher = SequenceMatcher(None, target, candidate, autojunk=False)
            if matcher.quick_ratio() < best_ratio:
                continue
            ratio = matcher.ratio()
            if ratio >= best_ratio:
                best, best_ratio = (positions[start], positions[end - 1] + 1), ratio
    return best


def parse_date(value):
    """US month/day/year or ISO/year-first, with four-digit years only."""
    value = unicodedata.normalize('NFKC', value).strip()
    weekday = WEEKDAY.match(value)
    if weekday:
        value = value[weekday.end():]
    if not DATE_PATTERN.fullmatch(value):
        raise ValueError('Unsupported date')
    if re.fullmatch(r'[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}', value):
        year, month, day = map(int, value.split('-'))
    elif re.match(r'[0-9]', value):
        month, day, year = map(int, re.split(r'[/.-]', value))
    else:
        match = re.fullmatch(r'([A-Za-z]+)\.?\s+([0-9]{1,2})(?:st|nd|rd|th)?(?:,\s*|\s+)([0-9]{4})', value, re.I)
        label, day, year = match.groups()
        month = next(number for name, number in MONTHS.items() if name.startswith(label.lower().rstrip('.')))
        day, year = int(day), int(year)
    result = date(year, month, day)  # Rejects impossible/leap dates.
    if weekday and result.strftime('%A').casefold() != weekday[1].casefold():
        raise ValueError('Weekday differs from calendar date')
    return result


def one_date(snippet):
    matches = list(DATE_PATTERN.finditer(snippet))
    if len(matches) != 1:
        raise ValueError('Need one unambiguous date in its snippet')
    remainder = snippet[:matches[0].start()] + snippet[matches[0].end():]
    # A date may be printed in the same instruction as one positive amount and
    # a clock time. Ignore only complete typed tokens, never arbitrary digits.
    remainder = ROOM_PATTERN.sub('', TIME_PATTERN.sub('', MONEY_PATTERN.sub('', remainder)))
    if digits(remainder):
        raise ValueError('Other numbers make the date snippet ambiguous')
    prefix = snippet[:matches[0].start()]
    weekday = re.search(r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s*$', prefix, re.I)
    return parse_date((weekday[1] + ', ' if weekday else '') + matches[0].group())


def parse_amount(value):
    value = unicodedata.normalize('NFKC', value).strip()
    if not re.fullmatch(r'\$?\s*(?:[0-9]+|[0-9]{1,3}(?:,[0-9]{3})+)(?:\.[0-9]{2})?', value):
        raise ValueError('Unsupported amount')
    try:
        amount = Decimal(re.sub(r'[$,\s]', '', value))
    except InvalidOperation:
        raise ValueError('Unsupported amount') from None
    if not Decimal('0') <= amount <= MAX_AMOUNT:
        raise ValueError('Amount outside configured range')
    return amount.quantize(Decimal('0.01'))


def one_amount(snippet):
    snippet = unicodedata.normalize('NFKC', snippet)
    # Parentheses can mean an accounting negative; partial parentheses are also
    # ambiguous. Reject such evidence rather than stripping it or guessing.
    if '(' in snippet or ')' in snippet:
        raise ValueError('Parenthesized amount evidence is unsupported')
    # Broad capture keeps malformed/OCR-confused tokens intact so parsing rejects
    # them rather than accepting a shorter, apparently valid numeric substring.
    pattern = r'(?<!\w)(?:[-+]\s*)?[$S]\s*[-+]?\s*[0-9OIlS][0-9OIlS,.]*'
    matches = list(re.finditer(pattern, snippet))
    for match in matches:
        prefix = snippet[:match.start()].rstrip()
        suffix = snippet[match.end():].lstrip()
        if prefix.endswith(tuple(AMOUNT_SIGNS)) or suffix.startswith(tuple(AMOUNT_SIGNS)):
            raise ValueError('Amount sign context is unsupported')
    tokens = [match.group() for match in matches]
    remainder = re.sub(pattern, '', snippet)
    remainder = TIME_PATTERN.sub('', DATE_PATTERN.sub('', remainder))
    if tokens and digits(remainder):
        raise ValueError('Other numbers make the amount snippet ambiguous')
    if not tokens:
        labeled = re.fullmatch(r'\s*(?:(?:amount(?: due)?|balance(?: due)?)\s*:\s*)?(.+?)\s*', snippet, re.I)
        tokens = [labeled.group(1)] if labeled else []
    if len(tokens) != 1:
        raise ValueError('Need one amount in its snippet')
    return parse_amount(tokens[0])


def action_core(value):
    """Only optional introductory courtesy/modality may differ, never clauses."""
    return re.sub(r'^(?:please\s+|you must\s+)', '', normalize(value)).rstrip(' .!?')


def action_sentence(text, start, end):
    """Recover a copied action's sentence, including wrapped trailing clauses.

    English heuristic, bounded to avoid unbounded scans. A clipped model snippet
    is not trusted to define the sentence boundary. No content is auto-expanded.
    """
    left = text.rfind('\n', 0, start) + 1
    # Preserve a condition wrapped immediately before the copied action.
    for _ in range(3):
        previous_start = text.rfind('\n', 0, max(0, left - 1)) + 1
        previous = text[previous_start:max(0, left - 1)].strip()
        if left and previous and (previous.endswith(',') or
                (re.match(r'^(?:if|unless|otherwise|except|when)\b', previous, re.I) and not previous.endswith(('.', '!', '?'))) or
                re.search(r'\b(?:if|unless|otherwise|or|and|by|before|within)\s*$', previous, re.I)):
            left = previous_start
        else:
            break
    right = min(len(text), end + 2000)
    tail = text[end:right]
    boundary = re.search(r'\n\s*\n|\n\s*(?:Contact|Questions|Amount due|Deadline|Due date|Issued)\s*:', tail, re.I)
    if boundary:
        right = end + boundary.start()
    segment = text[left:right]
    masked = re.sub(r'\b(?:Mr|Mrs|Ms|Dr|St|ext)\.', lambda m: m[0][:-1] + '\u2024', segment, flags=re.I)
    stops = list(re.finditer(r'[.!?](?=\s|$)', masked))
    before = [m.end() for m in stops if left + m.end() <= start]
    after = [m.end() for m in stops if left + m.end() >= end]
    lo = before[-1] if before else 0
    hi = after[0] if after else len(segment)
    sentence = segment[lo:hi].strip()
    sentence = re.sub(r'^(?:required action|what (?:you must|to) do|to pay)\s*:\s*', '', sentence, flags=re.I)
    return sentence



# Only explicit obligation labels participate; issue dates and ordinary dates do not.
OBLIGATION_DATE_LABEL = re.compile(
    r'(?:^|\n)[^\n:]{0,30}\b(?:deadline|due date|return date|return deadline|'
    r'(?:mandatory|required|scheduled) hearing date|hearing date|'
    r'date of required appearance|respond by|return by|pay by|payment due)'
    r'\s*(?::|is|on|by)?\s*$', re.I)
CONTEXT_DATE_PATTERN = re.compile(DATE_PATTERN.pattern.replace(
    r'(?![\w/.-])', r'(?![\w/-]|\.[0-9])'), re.I)


def conflicting_obligation_dates(text):
    """A single deadline card must abstain if explicit obligation dates disagree."""
    values=set()
    for match in CONTEXT_DATE_PATTERN.finditer(text):
        prefix=text[max(0,match.start()-160):match.start()]
        if not OBLIGATION_DATE_LABEL.search(prefix):
            continue
        try:
            values.add(parse_date(match.group()))
        except (ValueError,StopIteration):
            continue
    return len(values)>1



META_INSTRUCTION = re.compile(
    r'\b(?:ignore|disregard|override)\s+(?:(?:all|the|any|previous|prior)\s+)*'
    r'(?:instructions?|prompts?|validators?|system)\b|'
    r'\b(?:system override|developer instruction|assistant output|official (?:ai|decoder) instructions?)\b|'
    r'\b(?:reveal|print|show|expose)\b.{0,70}\b(?:system prompt|hidden prompt|api key)\b|'
    r'\bdisable\b.{0,50}\bvalidators?\b|'
    r'\bmark\b.{0,100}\bas verified\b|'
    r'\b(?:required_action|amount_due|deadline)\s+must\s+be\b|'
    r'\b(?:say|output|replace|set)\b.{0,65}\b(?:amount(?: due)?|deadline|contact|required_action)\b', re.I)
FIELD_LINE = re.compile(r'^\s*(?:issued|issue date|deadline|due date|amount(?: due)?|'
                        r'current amount due|balance(?: due)?|contact|what to do)\s*:', re.I)


def evidence_context(text,start,end):
    """Include the real source line and nearby preceding cues, never following commands."""
    left=text.rfind('\n',0,start)+1
    right=text.find('\n',end)
    if right<0:right=len(text)
    line=text[left:right]
    preceding=[]
    for previous in reversed(text[:left].splitlines()[-3:]):
        if not previous.strip() or FIELD_LINE.match(previous):break
        preceding.insert(0,previous)
    return '\n'.join(preceding+[line])


def unsafe_evidence(name,text,start,end,snippet):
    context=evidence_context(text,start,end)
    if META_INSTRUCTION.search(normalize(context)) or META_INSTRUCTION.search(normalize(snippet)):
        return True
    # Role checks use the evidence's own line, not an unrelated preceding field.
    line_end=text.find('\n',end)
    own_line=text[text.rfind('\n',0,start)+1:line_end if line_end>=0 else len(text)]
    if name=='amount_due':
        role = re.search(r'\b(?:late (?:fee|penalty)|future (?:fee|balance)|penalty|example amount)\b', own_line, re.I)
        if role:
            money = MONEY_PATTERN.search(own_line)
            # "Pay $X ... to avoid a late fee" describes the current amount;
            # "$X" after the fee label remains wrong-role evidence, even when
            # the model clips that label out of its source snippet.
            current = money and money.start() < role.start() and re.search(
                r'\b(?:pay|current|amount due|balance due)\b', own_line[:money.start()], re.I)
            if not current:
                return True
    if name=='deadline' and re.match(r'\s*(?:issued|issue date|received|printed|date of (?:this )?notice)\s*:',own_line,re.I):
        return True
    return False


def checked_field(name, proposed, text, today):
    value, snippet = proposed.value, proposed.source_snippet
    if value is None:
        # A model's absence decision is not proof the document lacks the fact.
        return CheckedField(value=None, source_snippet=snippet, status='missing',
                            reason='The extractor did not find this field. Check the photo.')
    result = CheckedField(value=value, source_snippet=snippet, status='unverified',
                          reason='The value could not be checked against its source.')
    span = find_source(text, snippet)
    if not span or not value.strip():
        return result
    start, end = span
    result.source_start, result.source_end = span
    actual = text[start:end]
    if unsafe_evidence(name,text,start,end,snippet):
        result.reason = 'The source has conflicting field-role or instruction-like context. Check the original notice.'
        return result
    # Explicit labeled absence is different from an unparsable numeric proposal.
    # Require the phrase in BOTH the proposed snippet and the matched source.
    absence = r'(?:not specified|not stated|not provided|none|n/a)'
    labels = {'amount_due': r'(?:amount(?: due)?|balance(?: due)?)',
              'deadline': r'(?:deadline|due date)'}
    if name in labels and re.fullmatch(absence, normalize(value)):
        pattern = labels[name] + r'\s*:\s*' + re.escape(normalize(value)) + r'[.!]?'
        if re.fullmatch(pattern, normalize(snippet)) and re.fullmatch(pattern, normalize(actual)):
            result.value = None
            result.status = 'missing'
            result.reason = 'The confirmed source explicitly says this field is not stated.'
            return result
    if '[unreadable]' in actual.casefold() or '\ufffd' in actual:
        return result
    try:
        if name == 'deadline':
            if conflicting_obligation_dates(text):
                raise ValueError('Conflicting explicit obligation dates')
            if proposed.kind == 'absolute':
                if any(item is not None for item in [proposed.relative_days, proposed.anchor_date, proposed.anchor_source_snippet]):
                    raise ValueError('Conflicting deadline representation')
                deadline = parse_date(value)
                if deadline != one_date(snippet) or deadline != one_date(actual):
                    raise ValueError('Date differs from source')
            elif proposed.kind == 'relative':
                rule = RELATIVE.fullmatch(value.strip())
                if not rule or not 0 < int(rule[1]) <= 365 or proposed.relative_days != int(rule[1]):
                    raise ValueError('Unsupported relative deadline')
                # No fuzzy repair for the actual relative rule or its number.
                if normalize(value) not in normalize(snippet) or normalize(value) not in normalize(actual):
                    raise ValueError('Relative rule missing')
                anchor = find_source(text, proposed.anchor_source_snippet)
                if not anchor or not proposed.anchor_date:
                    raise ValueError('Missing anchor')
                anchor_text = text[anchor[0]:anchor[1]]
                if not re.search(r'\b(?:issued|issue date|date of (?:this )?notice)\s*:', anchor_text, re.I):
                    raise ValueError('Anchor is not explicitly an issue date')
                if unsafe_evidence('anchor',text,anchor[0],anchor[1],proposed.anchor_source_snippet):
                    raise ValueError('Instruction-like anchor evidence')
                origin = parse_date(proposed.anchor_date)
                if origin != one_date(proposed.anchor_source_snippet) or origin != one_date(anchor_text):
                    raise ValueError('Anchor date differs')
                deadline = origin + timedelta(days=proposed.relative_days)
                result.anchor_source_snippet = proposed.anchor_source_snippet
                result.anchor_start, result.anchor_end = anchor
            else:
                raise ValueError('Missing deadline kind')
            result.normalized_value = deadline.isoformat()
            result.days_remaining = (deadline - today).days
        elif name == 'amount_due':
            amount = parse_amount(value)
            if amount != one_amount(snippet) or amount != one_amount(actual):
                raise ValueError('Amount differs from source')
            result.normalized_value = format(amount, '.2f')
        else:
            # Text fields are copied, not paraphrased into claims by the model.
            target, source = normalize(value), normalize(snippet)
            index = source.find(target)
            if index < 0 or not whole_span(source, index, index + len(target)):
                raise ValueError('Text value is not a whole source phrase')
            # When fuzzy letters match, all numeric sequences still must agree.
            if digits(snippet) != digits(actual):
                raise ValueError('Source digits differ')
            if name == 'required_action':
                value_span = find_source(actual, value)
                if not value_span:
                    raise ValueError('Action not found in actual source')
                sentence = action_sentence(text, start + value_span[0], start + value_span[1])
                if action_core(value) != action_core(sentence):
                    result.reason = 'The action may omit a condition, alternative, or timing clause. Check the complete instruction.'
                    return result
        result.status = 'verified'
        result.reason = 'Matches the confirmed text. Check that this is the right fact on your original notice.'
    except (ValueError, StopIteration, OverflowError):
        pass  # Public reason is fixed; exception values never enter logs/responses.
    return result


def verify_notice(proposed, text, today):
    fields = {name: checked_field(name, getattr(proposed, name), text, today)
              for name in ['issuing_agency', 'deadline', 'amount_due', 'required_action', 'contact']}
    warnings = ['Verified means source-matched to your confirmed text, not independently authenticated or guaranteed to be the correct field.']
    for name in ['deadline', 'amount_due', 'required_action']:
        if fields[name].status != 'verified':
            warnings.append(name.replace('_', ' ').capitalize() + ': not verified. Check the original notice or ask someone for help.')
    return fields, warnings
