"""New synthetic receipt photos + deterministic faulty-OCR regressions.

No real notice image, transcript, identity, or held-out input is used. The
controlled transcript cases are simulated OCR failures, not claimed OCR output.
Run from the repository root: python results/phone-reading-fix/receipt_repro.py
"""
import io
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from PIL import Image, ImageDraw, ImageFilter
from eval.generate_samples import load_font
from backend.images import normalize_image
from backend.preprocessed_reader import PreprocessedReader
from backend.readers import quality_warnings
from backend.ocr_safety import timing_issues
from backend.field_validation import checked_field
from backend.extraction_models import ProposedField

OUT = Path(__file__).resolve().parent
BASE = 'eccb39bcd3d683eb4bc357dc8dd52895790ac4f0'
old = {'__name__': 'before_phone_fix'}
exec(compile(subprocess.check_output(['git', 'show', BASE + ':backend/field_validation.py'], cwd=ROOT),
             'before_phone_fix.py', 'exec'), old)

lines = [
    'SYNTHETIC TEST ONLY - NOT A REAL TICKET',
    'INVENTED RIVER DEMONSTRATION COURT',
    'COMPLAINT AND SUMMONS',
    'Reference: SYNTHETIC-PHONE-701',
    '100 Example Lane, Demo Town, ZZ 00000',
    'Contact: Fictional Review Office',
    'Vehicle: TEST-ONLY     Color: GRAY',
    'Offense: Fictional restricted parking',
    'Issued: 11/04/2027    Time: 10:25 AM',
    'Amount due: $146.00    Due date: 11/29/2027',
    '1. PLEA OF NOT GUILTY',
    'If you dispute this synthetic charge, notify',
    'the office at least 7 days prior to the pay',
    'by date listed on this ticket.',
    '2. APPEARANCE',
    'The office will provide a hearing date.',
    'Never send payment for this test notice.',
]


def photo(degraded):
    page = Image.new('RGB', (820, 1120), '#faf9f6')
    draw = ImageDraw.Draw(page)
    for i, line in enumerate(lines):
        y = 65 + i * 52
        draw.text((35, y), line, font=load_font(size=27 if i < 3 else 26), fill='#181818')
        if i in (2, 8, 9):
            draw.line((28, y + 43, 790, y + 43), fill='#4b4b4b', width=2)
    if degraded:
        # A fold and tilted, compressed, narrow receipt. These are new pixels,
        # not a derivative of a resident's photograph.
        draw.line((30, 370, 790, 395), fill='#d1d0cc', width=3)
        page = page.resize((530, 724)).filter(ImageFilter.GaussianBlur(0.35))
        page = page.resize((820, 1120)).rotate(4, Image.Resampling.BICUBIC, expand=True, fillcolor='#393c40')
    background = Image.new('RGB', (1100, 1450), '#393c40')
    background.paste(page, ((1100 - page.width)//2, (1450 - page.height)//2))
    out = io.BytesIO()
    background.save(out, 'JPEG', quality=42 if degraded else 92)
    return out.getvalue()


photos = []
for variant in ('clean', 'angled-compressed'):
    raw = photo(variant != 'clean')
    (OUT / ('synthetic-receipt-' + variant + '.jpg')).write_bytes(raw)
    reading = PreprocessedReader().read(normalize_image(raw))
    (OUT / ('synthetic-receipt-' + variant + '-ocr.txt')).write_text(reading.text + '\n')
    checks = {'amount': '$146.00' in reading.text, 'complete_due_date': '11/29/2027' in reading.text,
              'complete_timing': bool(re.search(r'at least\s+7\s+days', reading.text))}
    photos.append({'variant': variant, 'key_token_checks': checks,
                   'passed': sum(checks.values()), 'total': len(checks),
                   'timing_issues': timing_issues(reading.text), 'warnings': quality_warnings(reading.text)})

cases = [
    ('clean_duration', 'If you dispute this charge, notify the office at least 7 days before payment.', 'verified'),
    ('letter_for_digit', 'If you dispute this charge, notify the office at least S days before payment.', 'unverified'),
    ('wrapped_punctuation', 'If you dispute this charge, notify the office at least’’S |\ndays before payment.', 'unverified'),
    ('mixed_duration', 'File a response within 3C days of receipt.', 'unverified'),
    ('one_digit_year', 'Pay the current balance by 11/29/2.', 'unverified'),
    ('three_digit_year', 'Pay the current balance by 11/29/202.', 'unverified'),
    ('impossible_date', 'Pay the current balance by 02/30/2027.', 'unverified'),
    ('valid_date', 'Pay the current balance by 11/29/2027.', 'verified'),
]
controls = []
for name, source, expected in cases:
    proposal = ProposedField(value=source, source_snippet=source)
    before = old['checked_field']('required_action', proposal, source, date(2027, 11, 1))
    after = checked_field('required_action', proposal, source, date(2027, 11, 1))
    controls.append({'case': name, 'simulated_ocr': source, 'expected_status': expected,
                     'before': before.model_dump(), 'after': after.model_dump(),
                     'pass': after.status == expected})
result = {'baseline_commit': BASE, 'synthetic_only': True, 'model_calls': 0,
          'tesseract_version': subprocess.check_output(['tesseract', '--version'], text=True).splitlines()[0],
          'photo_ocr': photos, 'controlled_failures': controls,
          'limits': 'New development regressions, not the exact iPhone file or an independent held-out evaluation. '
                    'A calendar-valid but wrong OCR number can still evade these checks.'}
(OUT / 'receipt-reproduction.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'photos': photos, 'control_passes': sum(c['pass'] for c in controls), 'control_total': len(controls),
                  'before_unsafe_actions_verified': sum(c['before']['status']=='verified' and c['expected_status']=='unverified' for c in controls),
                  'after_unsafe_actions_verified': sum(c['after']['status']=='verified' and c['expected_status']=='unverified' for c in controls)}, indent=2))
assert all(c['pass'] for c in controls)
