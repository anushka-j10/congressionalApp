"""Trusted language data; no notice contents or credentials are cached here."""
import json
import re
from datetime import date
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'languages'


@lru_cache(maxsize=1)
def all_languages():
    languages = {}
    for path in sorted(ROOT.glob('*.json')):
        if path.name.startswith('glossary_') or path.name == 'help.json':
            continue
        data = json.loads(path.read_text())
        if not re.fullmatch(r'[a-z]{2,3}(?:-[A-Za-z]{2})?', data['code']):
            raise ValueError('Invalid trusted language code')
        if data['direction'] not in {'ltr', 'rtl'} or len(data['months']) != 12:
            raise ValueError('Invalid trusted language configuration')
        languages[data['code']] = data
    english_keys = set(languages['en']['ui'])
    if any(set(cfg['ui']) != english_keys for cfg in languages.values()):
        raise ValueError('Language UI keys must match English')
    return languages


def language(code):
    return all_languages()[code]


def glossary(code):
    cfg = language(code)
    # Filename is trusted configuration, not a caller-provided path.
    path = ROOT / cfg['glossary_file']
    if path.parent != ROOT:
        raise ValueError('Invalid glossary path')
    return json.loads(path.read_text())


def message(code, key, **values):
    return language(code)['ui'][key].format(**values)


def display_date(value, code='en'):
    parsed = date.fromisoformat(value)
    cfg = language(code)
    return cfg['date_format'].format(day=parsed.day, month=cfg['months'][parsed.month - 1], year=parsed.year)


def public_languages():
    return {'languages': list(all_languages().values()), 'help': json.loads((ROOT/'help.json').read_text())}
