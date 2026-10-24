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
    r'\.?\s+[0-9]{1,2}(?:st|nd|rd|th)?(?:,\s*|\s+)[0-9]{4})(?![\w/.-])', re.I)
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
    return date(year, month, day)  # Rejects impossible/leap dates.


def one_date(snippet):
    matches = list(DATE_PATTERN.finditer(snippet))
    if len(matches) != 1:
        raise ValueError('Need one unambiguous date in its snippet')
    if digits(snippet[:matches[0].start()] + snippet[matches[0].end():]):
        raise ValueError('Other numbers make the date snippet ambiguous')
    return parse_date(matches[0].group())


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
    if tokens and digits(re.sub(pattern, '', snippet)):
        raise ValueError('Other numbers make the amount snippet ambiguous')
    if not tokens:
        labeled = re.fullmatch(r'\s*(?:(?:amount(?: due)?|balance(?: due)?)\s*:\s*)?(.+?)\s*', snippet, re.I)
        tokens = [labeled.group(1)] if labeled else []
    if len(tokens) != 1:
        raise ValueError('Need one amount in its snippet')
    return parse_amount(tokens[0])


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
