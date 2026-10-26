"""Recognize damaged timing tokens without repairing or inferring their values."""
import re
from datetime import date

DIGIT = r"[0-9OIlSBZC]"
# Include truncated years. A one-digit year must remain visible as uncertainty.
NUMERIC_DATE = re.compile(
    rf"(?<![\w/.-])(?:{DIGIT}{{4}}[ \t]*[-/.][ \t]*{DIGIT}{{1,2}}[ \t]*[-/.][ \t]*{DIGIT}{{1,2}}|"
    rf"{DIGIT}{{1,2}}[ \t]*[-/.][ \t]*{DIGIT}{{1,2}}[ \t]*[-/.][ \t]*{DIGIT}{{1,4}})(?![\w/-]|\.[0-9])")
DURATION = re.compile(
    rf"(?<![\w.])(?P<count>{DIGIT}{{1,4}})[\s|’'\"`-]*"
    r"(?:(?:calendar|business|working)[\s-]+)?(?:days?|hours?|weeks?|months?)(?!\w)", re.I)


def timing_issues(text):
    """Return literal source spans, never suggested corrections.

    Four-digit, calendar-valid dates are necessary, not proof of OCR accuracy.
    Numeric-looking letters beside a time unit are ambiguous even if two local
    OCR passes agree. English words such as 'five days' are not changed.
    """
    issues = []
    for match in NUMERIC_DATE.finditer(text):
        parts = re.split(r"\s*[-/.]\s*", match.group())
        try:
            if not all(part.isascii() and part.isdigit() for part in parts):
                raise ValueError
            if len(parts[0]) == 4:
                year, month, day = parts
            else:
                month, day, year = parts
            if len(year) != 4:
                raise ValueError
            date(int(year), int(month), int(day))
        except ValueError:
            issues.append({"kind": "date", "start": match.start(), "end": match.end()})
    for match in DURATION.finditer(text):
        if not match['count'].isascii() or not match['count'].isdigit():
            issues.append({"kind": "duration", "start": match.start(), "end": match.end()})
    return sorted(issues, key=lambda issue: issue['start'])
