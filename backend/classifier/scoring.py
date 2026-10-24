"""Deterministic, conservative classification; confidence is a heuristic."""

import re
from dataclasses import dataclass
from math import isfinite

from .signals import SIGNALS

MIN_SCORE = 3.0
MIN_RELATIVE_MARGIN = 0.25


@dataclass
class Classification:
    doc_type: str
    confidence: float
    signals: list[str]


def classify(text, rules=None) -> Classification:
    rules = SIGNALS if rules is None else rules
    scores = {}
    matched = {}
    for kind, signals in rules.items():
        scores[kind] = 0.0
        matched[kind] = []
        for signal in signals:
            if not isfinite(signal.weight) or signal.weight <= 0:
                raise ValueError("Signal weights must be positive finite numbers")
            if re.search(signal.pattern, text, flags=re.IGNORECASE):
                scores[kind] += signal.weight
                matched[kind].append(f"{kind}: {signal.label} (+{signal.weight:g})")
    ranked = sorted(scores, key=scores.get, reverse=True)
    if not ranked or scores[ranked[0]] == 0:
        return Classification("unknown", 0.0, [])
    best = scores[ranked[0]]
    runner_up = scores[ranked[1]] if len(ranked) > 1 else 0.0
    margin = (best - runner_up) / best
    confidence = round(min(0.99, best / (best + MIN_SCORE) * margin), 3)
    evidence = [entry for kind in ranked for entry in matched[kind]]
    if best < MIN_SCORE or margin < MIN_RELATIVE_MARGIN:
        return Classification("unknown", min(0.49, confidence), evidence)
    return Classification(ranked[0], confidence, evidence)
