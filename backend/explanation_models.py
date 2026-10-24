"""Strict language bundles; statuses remain outside model-generated text."""
from typing import Optional
from pydantic import Field, model_validator
from backend.extraction_models import StrictModel, CheckedField, DocType

FIELD_NAMES = ('issuing_agency','deadline','amount_due','required_action','contact')


class CardTexts(StrictModel):
    issuing_agency: str = Field(max_length=2500)
    deadline: str = Field(max_length=2500)
    amount_due: str = Field(max_length=2500)
    required_action: str = Field(max_length=2500)
    contact: str = Field(max_length=2500)


class Explanation(StrictModel):
    summary: str = Field(max_length=2500)
    what_happened: str = Field(max_length=2500)
    what_to_do: list[str] = Field(max_length=8)
    deadline_note: str = Field(max_length=2500)
    amount_note: str = Field(max_length=2500)
    confidence_notes: list[str] = Field(max_length=8)
    cards: CardTexts
    disclaimer: str = Field(max_length=500)

    @model_validator(mode='after')
    def bounded_lists(self):
        if any(len(item) > 2500 for item in self.what_to_do + self.confidence_notes):
            raise ValueError('Language text too long')
        return self


class ExplainRequest(StrictModel):
    doc_type: DocType
    fields: dict[str, CheckedField]
    today: str = Field(pattern=r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
    receipt: str = Field(max_length=100)
    language: str = Field(min_length=2, max_length=8)

    @model_validator(mode='after')
    def exact_fields(self):
        if set(self.fields) != set(FIELD_NAMES):
            raise ValueError('Unexpected fields')
        return self


class PlainTranslation(StrictModel):
    text: str = Field(max_length=50000)
