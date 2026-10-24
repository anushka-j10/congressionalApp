"""Deterministic numeric, date, glossary and warning checks; not semantic proof."""
import re
import unicodedata
from collections import Counter
from datetime import date
from difflib import SequenceMatcher

from backend.field_validation import DATE_PATTERN, parse_date, parse_amount
from backend.reader_tokens import MONEY
from backend.language_config import language, glossary, display_date

DATE_IN_TEXT = re.compile(DATE_PATTERN.pattern.replace(r'(?![\w/.-])', r'(?![\w/-]|\.[0-9])'), re.I)
PLACEHOLDER = re.compile(r'⟦ND_[0-9]+⟧')


def leaves(value, path=''):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from leaves(item, path + '.' + key)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from leaves(item, path + '.' + str(index))


def map_strings(value, function):
    if isinstance(value, str):
        return function(value)
    if isinstance(value, dict):
        return {key: map_strings(item, function) for key, item in value.items()}
    if isinstance(value, list):
        return [map_strings(item, function) for item in value]
    return value


def text_of(value):
    return '\n'.join(text for _, text in leaves(value))


def number_signature(text):
    return Counter(re.findall(r'\d+', unicodedata.normalize('NFKC', text)))


def canonicalize_dates(text):
    def replace(match):
        try:
            return display_date(parse_date(match.group()).isoformat())
        except (ValueError, StopIteration):
            return match.group()
    return DATE_IN_TEXT.sub(replace, text)


def date_pattern(code):
    cfg = language(code)
    pattern = re.escape(cfg['date_format'])
    pattern = pattern.replace(r'\{day\}', r'(?P<day>[0-9]{1,2})')
    pattern = pattern.replace(r'\{month\}', '(?P<month>' + '|'.join(re.escape(item) for item in cfg['months']) + ')')
    pattern = pattern.replace(r'\{year\}', r'(?P<year>[0-9]{4})')
    return re.compile(r'(?<!\w)' + pattern + r'(?!\w)', re.I)


def date_signature(text, code):
    cfg = language(code)
    months = {month.casefold():index+1 for index, month in enumerate(cfg['months'])}
    found = Counter()
    for match in date_pattern(code).finditer(text):
        try:
            value = date(int(match['year']), months[match['month'].casefold()], int(match['day']))
        except ValueError:
            return None
        found[value.isoformat()] += 1
    return found


def money_signature(text):
    values = Counter()
    for match in MONEY.finditer(text):
        try:
            values[str(parse_amount(match.group()))] += 1
        except ValueError:
            return None
    return values


def english_checks(candidate, template, verified_text):
    text, allowed = text_of(candidate), canonicalize_dates(verified_text)
    errors = []
    if not set(number_signature(text)) <= set(number_signature(allowed)):
        errors.append('extra_number')
    dates, allowed_dates = date_signature(text, 'en'), date_signature(allowed, 'en')
    if dates is None or not set(dates) <= set(allowed_dates or {}):
        errors.append('extra_or_invalid_date')
    money, allowed_money = money_signature(text), money_signature(allowed)
    if money is None or not set(money) <= set(allowed_money or {}):
        errors.append('extra_or_invalid_amount')
    if candidate['cards'] != template['cards']:
        errors.append('changed_card_fact_or_status')
    if candidate['confidence_notes'] != template['confidence_notes'] or candidate['disclaimer'] != template['disclaimer']:
        errors.append('changed_warning_or_disclaimer')
    for name in ['deadline_note', 'amount_note']:
        if number_signature(candidate[name]) != number_signature(template[name]):
            errors.append('changed_' + name)
        if name == 'deadline_note' and date_signature(candidate[name], 'en') != date_signature(template[name], 'en'):
            errors.append('changed_deadline_date')
    if any(not text.strip() for _, text in leaves(candidate)):
        errors.append('empty_text')
    return errors


def used_glossary(source, code):
    text = text_of(source)
    return [entry for entry in glossary(code)
            if re.search(r'(?<!\w)' + re.escape(entry['english']) + r'(?!\w)', text, re.I)]


def translation_checks(source, translated, code, fixed_notes=None):
    errors = []
    left, right = dict(leaves(source)), dict(leaves(translated))
    if set(left) != set(right):
        return ['changed_structure']
    for path, original in left.items():
        target = right[path]
        if number_signature(original) != number_signature(target):
            errors.append('number_preservation')
        if date_signature(original, 'en') != date_signature(target, code):
            errors.append('date_preservation')
        if money_signature(original) != money_signature(target):
            errors.append('amount_preservation')
        # Month names must be spelled out, not ambiguous numeric date formats.
        if re.search(r'(?<!\w)[0-9]{1,4}[/.-][0-9]{1,2}[/.-][0-9]{1,4}(?!\w)', target):
            errors.append('numeric_date_format')
        if not target.strip():
            errors.append('empty_text')
    target_text = unicodedata.normalize('NFKC', text_of(translated)).casefold()
    for entry in used_glossary(source, code):
        if unicodedata.normalize('NFKC', entry['translation']).casefold() not in target_text:
            errors.append('glossary')
    if translated['disclaimer'] != language(code)['ui']['disclaimer']:
        errors.append('disclaimer')
    if fixed_notes is not None and translated['confidence_notes'] != fixed_notes:
        errors.append('warning_preservation')
    return sorted(set(errors))


def protect(source, code):
    """Protect dates atomically, then money/compound IDs/numbers, per leaf."""
    replacements = {}
    def guard(text):
        if PLACEHOLDER.search(text):
            raise ValueError('Reserved token in source')
        def replace(match, value=None):
            token = f'⟦ND_{len(replacements)}⟧'
            replacements[token] = value if value is not None else match.group()
            return token
        def date_replace(match):
            iso = parse_date(match.group()).isoformat()
            return replace(match, display_date(iso, code))
        text = date_pattern('en').sub(date_replace, text)
        # Skip existing placeholders by alternation in every subsequent pass.
        for pattern in [MONEY.pattern, r'(?<!\w)[A-Za-z0-9]+(?:[-/.][A-Za-z0-9]+)+(?!\w)', r'[0-9]+']:
            regex = re.compile(PLACEHOLDER.pattern + '|' + pattern)
            def substitute(match):
                if PLACEHOLDER.fullmatch(match.group()):
                    return match.group()
                if not any(char.isdigit() for char in match.group()):
                    return match.group()
                return replace(match)
            text = regex.sub(substitute, text)
        return text
    return map_strings(source, guard), replacements


def restore(source, proposed, replacements):
    a, b = dict(leaves(source)), dict(leaves(proposed))
    if set(a) != set(b):
        raise ValueError('Changed structure')
    for path in a:
        if Counter(PLACEHOLDER.findall(a[path])) != Counter(PLACEHOLDER.findall(b[path])):
            raise ValueError('Changed protected facts')
    def replace(text):
        return PLACEHOLDER.sub(lambda match: replacements[match.group()], text)
    return map_strings(proposed, replace)


def back_translation_check(source, back, statuses):
    back = map_strings(back, canonicalize_dates)
    checks = translation_checks(source, back, 'en', source['confidence_notes'])
    scores = []
    for name, status in statuses.items():
        if status != 'verified' or name in {'deadline','amount_due'}:
            continue
        a, b = source['cards'][name].casefold(), back['cards'][name].casefold()
        score = SequenceMatcher(None, a, b, autojunk=False).ratio()
        scores.append(score)
        if score < .65:
            checks.append('key_fact_back_translation')
    return {'passed':not checks, 'checks':sorted(set(checks)),
            'minimum_text_similarity':round(min(scores), 4) if scores else None}


def neutral_dates(text, code):
    """Normalize supported date spellings before comparing numeric facts."""
    invalid = False
    cfg = language(code)
    months = {month.casefold(): index+1 for index, month in enumerate(cfg['months'])}
    def replace(match):
        nonlocal invalid
        try:
            parsed = date(int(match['year']), months[match['month'].casefold()], int(match['day']))
            return display_date(parsed.isoformat(), 'en')
        except ValueError:
            invalid = True
            return match.group()
    return canonicalize_dates(date_pattern(code).sub(replace, text)), invalid


def plain_translation_checks(source, target, code):
    """Numeric correctness is separate from the required month-name formatting."""
    original, invalid_source = neutral_dates(source, 'en')
    normalized, invalid_target = neutral_dates(target, code)
    return {
        'numbers':number_signature(original)==number_signature(normalized),
        'dates':not invalid_source and not invalid_target and date_signature(original,'en')==date_signature(normalized,'en'),
        'amounts':money_signature(source)==money_signature(target),
        'glossary':all(item['translation'].casefold() in target.casefold() for item in used_glossary(source,code)),
        'disclaimer':message_for_disclaimer(code) in target,
        'no_numeric_dates':not bool(re.search(r'(?<!\w)[0-9]{1,4}[/.-][0-9]{1,2}[/.-][0-9]{1,4}(?!\w)',target)),
    }


def message_for_disclaimer(code):
    return language(code)['ui']['disclaimer']
