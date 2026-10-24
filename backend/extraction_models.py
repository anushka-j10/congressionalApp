"""Proposed schema for student review; model output never controls field status."""

from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

DocType = Literal['parking_ticket', 'court_notice', 'utility_bill', 'school_letter', 'unknown']


class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)


class ExtractRequest(StrictModel):
    text: str = Field(min_length=1, max_length=30000)
    doc_type: DocType
    text_confirmed: Literal[True]

    @field_validator('text_confirmed', mode='before')
    @classmethod
    def require_real_confirmation(cls, value):
        if value is not True:
            raise ValueError('Explicit boolean confirmation required')
        return value


class ProposedField(StrictModel):
    # Required nullable keys distinguish a deliberate null from broken JSON.
    value: Optional[str] = Field(max_length=2000)
    source_snippet: Optional[str] = Field(max_length=1200)


class ProposedDeadline(ProposedField):
    kind: Optional[Literal['absolute', 'relative']]
    relative_days: Optional[int]
    anchor_date: Optional[str] = Field(max_length=100)
    anchor_source_snippet: Optional[str] = Field(max_length=1200)


class ProposedNotice(StrictModel):
    issuing_agency: ProposedField
    deadline: ProposedDeadline
    amount_due: ProposedField
    required_action: ProposedField
    contact: ProposedField


# Separate types allow future student-owned, document-specific rules. Shared core
# fields currently have the same meaning; these classes do not invent extra data.
class ParkingTicket(ProposedNotice):
    doc_type: Literal['parking_ticket']


class CourtNotice(ProposedNotice):
    doc_type: Literal['court_notice']


class UtilityBill(ProposedNotice):
    doc_type: Literal['utility_bill']


class SchoolLetter(ProposedNotice):
    doc_type: Literal['school_letter']


NOTICE_MODELS = {'parking_ticket': ParkingTicket, 'court_notice': CourtNotice,
                 'utility_bill': UtilityBill, 'school_letter': SchoolLetter}


class CheckedField(StrictModel):
    value: Optional[str]
    source_snippet: Optional[str]
    status: Literal['verified', 'unverified', 'missing']
    reason: str
    source_start: Optional[int] = None
    source_end: Optional[int] = None
    normalized_value: Optional[str] = None
    days_remaining: Optional[int] = None
    anchor_source_snippet: Optional[str] = None
    anchor_start: Optional[int] = None
    anchor_end: Optional[int] = None
