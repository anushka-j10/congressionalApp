"""Locate OCR candidates for cross-reader comparison, never field verification."""

import re
import unicodedata
from decimal import Decimal, InvalidOperation
from difflib import SequenceMatcher

# Keep common OCR letter/digit confusions as literal candidates, not corrections.
DIGIT = r"[0-9OIlS]"
DATE = re.compile(rf"(?<!\w)(?:{DIGIT}{{4}}[ \t]*[-/.][ \t]*{DIGIT}{{1,2}}[ \t]*[-/.][ \t]*{DIGIT}{{1,2}}|{DIGIT}{{1,2}}[ \t]*[-/.][ \t]*{DIGIT}{{1,2}}[ \t]*[-/.][ \t]*{DIGIT}{{2,4}})(?!\w)")
MONTH_DATE = re.compile(rf"(?i)(?<!\w)(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?[ \t]+{DIGIT}{{1,2}}(?:st|nd|rd|th)?(?:[ \t]*,[ \t]*|[ \t]+){DIGIT}{{4}}(?!\w)")
MONEY = re.compile(rf"(?<![\w.])(?:[-+][ \t]*)?\$[ \t]*(?:[-+][ \t]*)?{DIGIT}+(?:[ \t]*,[ \t]*{DIGIT}{{3}})*(?:[ \t]*\.[ \t]*{DIGIT}{{2}})?(?!\w|[.,]\w)")
LABELED_MONEY = re.compile(rf"(?im)\b(?:amount(?:[ \t]+due)?|balance(?:[ \t]+due)?)[ \t]*:[ \t]*(?P<value>(?:[-+][ \t]*)?\$?[ \t]*(?:[-+][ \t]*)?{DIGIT}+(?:[ \t]*,[ \t]*{DIGIT}{{3}})*(?:\.{DIGIT}{{2}})?)(?!\w|[.,]\w)")
IDENTIFIER = re.compile(r"(?im)^[ \t]*(?:Reference|Case(?:[ \t]*(?:No\.?|Number))?|ID|Citation|Ticket|Account)(?:[ \t]*(?:No\.?|Number))?[ \t]*[:#][ \t]*(?P<value>[A-Z0-9]+(?:[ \t]*[-/._][ \t]*[A-Z0-9]+)*)")


def normalize_candidate(kind, value):
    value = unicodedata.normalize("NFKC", value)
    if kind == "amount":
        compact = re.sub(r"[\s,$]", "", value)
        try:
            return format(Decimal(compact), ".2f")
        except InvalidOperation:
            return compact.casefold()
    return re.sub(r"[\s,./_-]", "", value).casefold()


def candidates(text, reader):
    found = []
    patterns = [("date", DATE, None), ("date", MONTH_DATE, None),
                ("amount", MONEY, None), ("amount", LABELED_MONEY, "value"),
                ("id", IDENTIFIER, "value")]
    seen = set()
    for kind, pattern, group in patterns:
        for match in pattern.finditer(text):
            start, end = match.span(group) if group else match.span()
            if (kind, end) in seen:
                continue
            seen.add((kind, end))
            value = text[start:end]
            if not any(char.isdigit() for char in value):
                continue
            found.append({"kind": kind, "value": value, "normalized": normalize_candidate(kind, value),
                          "reader": reader, "start": start, "end": end})
    return sorted(found, key=lambda item: item["start"])


def compare_candidates(local_text, other_text, local_reader, other_reader):
    left = candidates(local_text, local_reader)
    right = candidates(other_text, other_reader)
    key = lambda item: (item["kind"], item["normalized"])
    alignment = SequenceMatcher(a=[key(item) for item in left],
                                b=[key(item) for item in right], autojunk=False)
    reviews = []
    for tag, i, j, k, m in alignment.get_opcodes():
        if tag == "equal":
            for a, b in zip(left[i:j], right[k:m]):
                reviews.append({"kind": a["kind"], "status": "agreed", "candidates": [a, b]})
        else:
            # Pair only by kind within the unmatched block. These are OCR choices,
            # not claims that a particular date is a deadline or issue date.
            for kind in ("date", "amount", "id"):
                a = [item for item in left[i:j] if item["kind"] == kind]
                b = [item for item in right[k:m] if item["kind"] == kind]
                for index in range(max(len(a), len(b))):
                    values = ([a[index]] if index < len(a) else []) + ([b[index]] if index < len(b) else [])
                    reviews.append({"kind": kind, "status": "disputed", "candidates": values})
    return reviews
