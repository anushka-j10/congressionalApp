"""Compare readers on frozen fixtures; keep transcript and candidate metrics separate."""

import argparse
import importlib
import hashlib
import json
import platform
import re
import subprocess
import sys
import time
import unicodedata
from collections import Counter
from dataclasses import asdict, dataclass
from decimal import Decimal
from difflib import SequenceMatcher
from pathlib import Path

from dotenv import load_dotenv

from backend.images import normalize_image
from backend.main import Settings
from backend.readers import ReaderError, TesseractReader, VisionReader
from backend.preprocessed_reader import PREPROCESSING, PreprocessedReader
from backend.hybrid_reader import HybridReader

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".heic", ".heif", ".webp"}
CONDITIONS = ("clean", "degraded", "handwriting", "legacy_m1")
DATE_RE = re.compile(r"(?<!\w)(?:\d{4}[ \t]*[-/.][ \t]*\d{1,2}[ \t]*[-/.][ \t]*\d{1,2}|\d{1,2}[ \t]*[-/.][ \t]*\d{1,2}[ \t]*[-/.][ \t]*\d{2,4})(?!\w)")
MONTH_RE = re.compile(r"(?i)(?<!\w)(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?[ \t]+\d{1,2}(?:st|nd|rd|th)?(?:[ \t]*,[ \t]*|[ \t]+)\d{4}(?!\w)")
MONEY_RE = re.compile(r"(?<![\w.])\$[ \t]*\d+(?:[ \t]*,[ \t]*\d{3})*(?:[ \t]*\.[ \t]*\d{2})?(?!\w|[.,]\w)")
DECIMAL_RE = re.compile(r"(?<![\w.])(?:\$[ \t]*)?\d+(?:[ \t]*,[ \t]*\d{3})*[ \t]*\.[ \t]*\d{2}(?!\w|\.\w)")
ID_RE = re.compile(r"(?im)^[ \t]*(?:Reference|Case(?:[ \t]*(?:No\.?|Number))?|ID|Citation|Ticket|Account)(?:[ \t]*(?:No\.?|Number))?[ \t]*[:#][ \t]*(?P<value>[A-Z0-9]+(?:[ \t]*[-/._][ \t]*[A-Z0-9]+)*)")


@dataclass(frozen=True)
class KeyToken:
    kind: str
    value: str


@dataclass(frozen=True)
class Sample:
    image: Path
    truth: Path
    condition: str
    variant: str


def normalized_text(text):
    """Ignore layout whitespace, but preserve spelling, case, and all digits."""
    return " ".join(unicodedata.normalize("NFKC", text).split())


def edit_distance(left, right):
    """Exact Levenshtein distance in linear memory; insert/delete/substitute cost 1."""
    if len(left) < len(right):
        left, right = right, left
    previous = list(range(len(right) + 1))
    for i, a in enumerate(left, 1):
        row = [i]
        for j, b in enumerate(right, 1):
            row.append(min(row[-1] + 1, previous[j] + 1, previous[j - 1] + (a != b)))
        previous = row
    return previous[-1]


def normalize_token(kind, value):
    value = unicodedata.normalize("NFKC", value)
    if kind == "amount":
        return format(Decimal(re.sub(r"[\s,$]", "", value)), ".2f")
    # Cosmetic separators and letter case may differ; never repair OCR digits.
    return re.sub(r"[\s,./_-]", "", value).casefold()


def key_tokens(text):
    text = unicodedata.normalize("NFKC", text)
    dates = [KeyToken("date", match.group()) for pattern in (DATE_RE, MONTH_RE) for match in pattern.finditer(text)]
    money = [KeyToken("amount", match.group()) for match in MONEY_RE.finditer(text)]
    ids = [KeyToken("id", match.group("value")) for match in ID_RE.finditer(text) if any(char.isdigit() for char in match.group("value"))]
    return dates + money + ids


def matching_occurrences(token, output):
    """Count a token's literal normalized value anywhere, with whole-token bounds."""
    output = unicodedata.normalize("NFKC", output)
    if token.kind == "amount":
        matches = {match.span(): match.group() for pattern in (MONEY_RE, DECIMAL_RE) for match in pattern.finditer(output)}
        # Two patterns can see the same amount. Deduplicate by end position.
        return len({end for (_, end), value in matches.items()
                    if normalize_token("amount", value) == normalize_token("amount", token.value)})
    runs = re.findall(r"[A-Za-z]+|\d+", token.value)
    joiner = r"[\s,./_-]*"
    pattern = r"(?<![A-Za-z0-9])" + joiner.join(re.escape(run) for run in runs) + r"(?![A-Za-z0-9])"
    return len(re.findall(pattern, output, flags=re.IGNORECASE))


def score_text(truth, output):
    expected, actual = normalized_text(truth), normalized_text(output)
    if not expected:
        raise ValueError("Ground truth must contain text")
    edits = edit_distance(expected, actual)
    tokens = key_tokens(truth)
    groups = Counter((token.kind, normalize_token(token.kind, token.value)) for token in tokens)
    representatives = {(token.kind, normalize_token(token.kind, token.value)): token for token in tokens}
    missing = []
    matched = 0
    for key, count in groups.items():
        token = representatives[key]
        hits = min(count, matching_occurrences(token, output))
        matched += hits
        if hits < count:
            # Candidates are what OCR actually returned, not invented corrections.
            observed = [item for item in key_tokens(output) if item.kind == token.kind]
            if token.kind == "amount":
                observed += [KeyToken("amount", match.group()) for match in DECIMAL_RE.finditer(output)]
            candidates = sorted({item.value for item in observed}, key=lambda value: SequenceMatcher(
                None, normalize_token(token.kind, token.value), normalize_token(token.kind, value)).ratio(), reverse=True)[:3]
            missing.append({**asdict(token), "missing_occurrences": count - hits, "observed_candidates": candidates})
    return {"character_edits": edits, "ground_truth_characters": len(expected),
            "cer": edits / len(expected), "key_tokens": len(tokens), "key_tokens_matched": matched,
            "key_token_recall": matched / len(tokens) if tokens else None,
            "target_tokens": [asdict(token) for token in tokens], "missed_tokens": missing}


def score_shown_candidates(truth, reviews):
    """One-to-one credit for correct literal values in the UI's candidate payload."""
    targets = key_tokens(truth)
    edges = []
    for token in targets:
        expected = normalize_token(token.kind, token.value)
        options = []
        for index, review in enumerate(reviews):
            if review["kind"] != token.kind:
                continue
            for candidate in review["candidates"]:
                try:
                    same = normalize_token(token.kind, candidate["value"]) == expected
                except Exception:
                    same = False
                if same:
                    options.append(index)
                    break
        edges.append(options)
    # A review group may represent at most one correct target occurrence, even
    # if its two alternatives happen to equal two distinct ground-truth values.
    owners = {}
    def assign(target_index, visited):
        for review_index in edges[target_index]:
            if review_index in visited:
                continue
            visited.add(review_index)
            if review_index not in owners or assign(owners[review_index], visited):
                owners[review_index] = target_index
                return True
        return False
    for index in range(len(targets)):
        assign(index, set())
    matched_indices = set(owners.values())
    return {"candidate_key_tokens_matched": len(matched_indices),
            "candidate_key_token_recall": len(matched_indices) / len(targets) if targets else None,
            "candidate_missed_tokens": [asdict(token) for index, token in enumerate(targets) if index not in matched_indices]}


class MemoryReader:
    """Per-run RAM-only memoization avoids paying for the same vision call twice."""
    def __init__(self, reader):
        self.reader = reader
        self.name = reader.name
        self.cache = {}

    def read(self, image_bytes):
        key = hashlib.sha256(image_bytes).digest()
        if key not in self.cache:
            self.cache[key] = self.reader.read(image_bytes)
        return self.cache[key]


def discover_samples(root):
    samples, problems = [], []
    for condition in CONDITIONS:
        folder = root if condition == "legacy_m1" else root / condition
        if not folder.exists():
            continue
        for image in sorted(folder.iterdir()):
            if image.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            options = [image.with_suffix(".txt"), image.with_name(image.stem + ".gt.txt")]
            available = [path for path in options if path.is_file()]
            if len(available) != 1:
                problems.append(f"{condition}/{image.name}: provide exactly one same-stem .txt or .gt.txt ground truth")
                continue
            truth = available[0]
            if not truth.read_text(encoding="utf-8").strip():
                problems.append(f"{condition}/{image.name}: ground truth is empty")
                continue
            variant = image.stem.split("__", 1)[1] if condition == "degraded" and "__" in image.stem else condition
            samples.append(Sample(image, truth, condition, variant))
        # Flag orphan truths rather than quietly treating missing images as tested.
        image_stems = {path.stem for path in folder.iterdir() if path.suffix.lower() in IMAGE_SUFFIXES}
        for truth in folder.glob("*.txt"):
            stem = truth.stem.removesuffix(".gt")
            if stem not in image_stems:
                problems.append(f"{condition}/{truth.name}: missing image")
    return samples, problems


def evaluate_reader(reader, samples):
    rows = []
    for sample_index, sample in enumerate(samples, 1):
        start = time.monotonic()
        error = None
        try:
            # Preserve the M1 production normalization, rather than giving OCR
            # larger or otherwise improved input only in the evaluation harness.
            reading = reader.read(normalize_image(sample.image.read_bytes()))
            output = reading.text
            warnings = reading.warnings
            reviews = reading.token_reviews
        except Exception:
            # Count a failed reading as empty output; never log provider bodies.
            output, warnings, reviews, error = "", [], [], "read_failed"
        truth = sample.truth.read_text(encoding="utf-8")
        result = score_text(truth, output)
        if reader.name == "hybrid":
            result.update(score_shown_candidates(truth, reviews))
            result["candidate_reviews"] = reviews
        rows.append({"sample": sample.image.stem, "condition": sample.condition,
                     "variant": sample.variant, "reader": reader.name,
                     "seconds": round(time.monotonic() - start, 3), "error": error,
                     "warnings_count": len(warnings), **result})
        if sample_index % 8 == 0 or sample_index == len(samples):
            print(f"reader={reader.name} completed={sample_index}/{len(samples)}", file=sys.stderr, flush=True)
    return rows


def summarize(rows, condition):
    selected = [row for row in rows if row["condition"] == condition]
    chars = sum(row["ground_truth_characters"] for row in selected)
    tokens = sum(row["key_tokens"] for row in selected)
    matched = sum(row["key_tokens_matched"] for row in selected)
    return {"condition": condition, "samples": len(selected),
            "cer": sum(row["character_edits"] for row in selected) / chars if chars else None,
            "key_token_recall": matched / tokens if tokens else None,
            "matched": matched, "key_tokens": tokens,
            "errors": sum(row["error"] is not None for row in selected),
            "candidate_key_token_recall": sum(row.get("candidate_key_tokens_matched", 0) for row in selected) / tokens
                if tokens and any("candidate_key_token_recall" in row for row in selected) else None}


def print_table(reports):
    print(f"{'reader':<14} {'condition':<12} {'n':>3} {'CER':>8} {'text recall':>12} {'shown-candidate recall':>23} {'matched':>9} {'errors':>7}")
    print("-" * 106)
    for report in reports:
        for row in report["conditions"]:
            cer = f"{row['cer']:.2%}" if row["cer"] is not None else "N/A"
            recall = f"{row['key_token_recall']:.2%}" if row["key_token_recall"] is not None else "N/A"
            candidate = f"{row['candidate_key_token_recall']:.2%}" if row["candidate_key_token_recall"] is not None else "N/A"
            print(f"{report['reader']:<14} {row['condition']:<12} {row['samples']:>3} {cer:>8} {recall:>12} {candidate:>23} {row['matched']:>3}/{row['key_tokens']:<5} {row['errors']:>5}")
        if report.get("not_run_reason"):
            print("  NOT RUN: " + report["not_run_reason"])
    print("CER: lower is better. Key-token recall: higher is better. N/A is not a pass.")
    print("Hybrid CER/text recall score its local transcript; candidate recall scores only values shown for review.")


def run(root, names, factories=()):
    settings = Settings.from_environment()
    samples, problems = discover_samples(root)
    if problems:
        raise ValueError("Fix dataset pairs before measuring:\n" + "\n".join(problems))
    if not any(sample.condition in {"clean", "degraded"} for sample in samples):
        raise ValueError("No printed measurement samples found; generate the reader corpus first")
    local = MemoryReader(PreprocessedReader(settings.tesseract_command))
    vision = MemoryReader(VisionReader(settings.api_key, settings.model)) if settings.api_key and settings.model else None
    unavailable_reason = "OPENAI_API_KEY and OPENAI_MODEL are not both configured"
    if vision and any(name in {"vision", "hybrid"} for name in names):
        try:
            # This first real result stays in RAM for the later vision/hybrid
            # rows, so it is not an extra paid request.
            vision.read(normalize_image(samples[0].image.read_bytes()))
        except ReaderError as exc:
            unavailable_reason = str(exc)  # ReaderError messages are fixed/public-safe.
            vision.cache.clear()
            vision = None
    available = {"tesseract": TesseractReader(settings.tesseract_command), "preprocessed": local,
                 "vision": vision, "hybrid": HybridReader(local, vision) if vision else None}
    readers = []
    for name in names:
        readers.append((name, available[name]))
    for spec in factories:
        module, function = spec.split(":", 1)
        reader = getattr(importlib.import_module(module), function)()
        readers.append((reader.name, reader))
    reports = []
    for name, reader in readers:
        rows = evaluate_reader(reader, samples) if reader else []
        conditions = [summarize(rows, condition) for condition in CONDITIONS]
        printed = [row for row in rows if row["condition"] in {"clean", "degraded"}]
        count = sum(row["key_tokens"] for row in printed)
        matched = sum(row["key_tokens_matched"] for row in printed)
        recall = matched / count if count else None
        candidate_matched = sum(row.get("candidate_key_tokens_matched", 0) for row in printed)
        candidate_recall = candidate_matched / count if count and name == "hybrid" else None
        gate_recall = candidate_recall if name == "hybrid" else recall
        reports.append({"reader": name, "conditions": conditions, "samples": rows,
                        "printed_key_recall": recall,
                        "printed_candidate_key_recall": candidate_recall,
                        "printed_threshold_met": gate_recall >= 0.95 if gate_recall is not None else None,
                        "not_run_reason": None if reader else unavailable_reason})
    # Do not keep full transcriptions beyond this comparison run.
    local.cache.clear()
    if vision:
        vision.cache.clear()
    try:
        version = subprocess.run([settings.tesseract_command, "--version"], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, timeout=5, check=False).stdout.decode().splitlines()[0]
    except (OSError, subprocess.SubprocessError, IndexError):
        version = "unavailable"
    repository = Path(__file__).resolve().parents[1]
    fingerprints = {str(path.relative_to(repository)): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in [repository / name for name in ("backend/readers.py", "backend/images.py", "backend/main.py", "frontend/image-prep.js", "backend/preprocessed_reader.py", "backend/hybrid_reader.py", "backend/reader_tokens.py")]}
    corpus_manifest = root.parent / "reader-corpus.json"
    return {"stage": "A2 comparison; production reader selection and Part B gate pending",
            "python_version": platform.python_version(), "tesseract_version": version,
            "production_fingerprints": fingerprints,
            "corpus_manifest_sha256": hashlib.sha256(corpus_manifest.read_bytes()).hexdigest() if corpus_manifest.exists() else None,
            "settings": {"normalization": "unchanged M1 EXIF transpose; <=1600px; JPEG quality 90",
                         "tesseract_language": "eng", "tesseract_psm": 3,
                         "vision_model": settings.model or None, "preprocessing": PREPROCESSING,
                         "cache_policy": "per-run RAM only; component results reused by hybrid"},
            "reports": reports}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent / "samples")
    parser.add_argument("--readers", nargs="+", choices=("tesseract", "preprocessed", "vision", "hybrid"), default=["tesseract", "preprocessed", "vision", "hybrid"])
    parser.add_argument("--factory", action="append", default=[], help="Trusted local module:zero_argument_factory returning any TextReader")
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "reports/reader-comparison.json")
    options = parser.parse_args()
    if options.env_file:
        load_dotenv(options.env_file, override=False)
    try:
        result = run(options.root, options.readers, options.factory)
    except (ValueError, OSError) as error:
        parser.exit(2, str(error) + "\n")
    options.output.parent.mkdir(parents=True, exist_ok=True)
    options.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print_table(result["reports"])
    print("Formal gate: PENDING reader selection and review. No extraction has been started.")
