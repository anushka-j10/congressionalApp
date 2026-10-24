"""STUDENT OWNED: fill these lists with your own tested signals and weights."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Signal:
    label: str
    pattern: str  # Python regular expression, matched case-insensitively.
    weight: float  # Positive evidence weight; a signal scores once per document.


# TODO(student): add Signal(label=..., pattern=..., weight=...) entries below.
# Keep this empty until YOU write the real lists. See toy tests for syntax.
SIGNALS: dict[str, tuple[Signal, ...]] = {
    "parking_ticket": (),  # TODO(student)
    "court_notice": (),    # TODO(student)
    "utility_bill": (),    # TODO(student)
    "school_letter": (),   # TODO(student)
}
