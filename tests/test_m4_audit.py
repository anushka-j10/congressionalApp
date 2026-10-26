"""Milestone 4 verification proofs; synthetic data, no API calls or held-out reads."""
from datetime import date
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from backend.extraction import ExtractionResult
from backend.extraction_models import ParkingTicket, ProposedField, ProposedDeadline
from backend.field_validation import checked_field
from backend.main import app, get_extractor, get_today


@pytest.mark.parametrize('name',['issuing_agency','deadline','amount_due','required_action','contact'])
def test_absent_source_snippet_can_never_verify(name):
    text='SYNTHETIC INFORMATION PAGE\nThere are no payment or response instructions.'
    values={'issuing_agency':('Invented Agency','Issued by Invented Agency'),
            'deadline':('2028-04-14','Deadline: April 14, 2028'),
            'amount_due':('$26.45','Amount due: $26.45'),
            'required_action':('Mail the response.','Mail the response.'),
            'contact':('Example Support Desk','Contact: Example Support Desk')}
    value,snippet=values[name]
    data={'value':value,'source_snippet':snippet}
    if name=='deadline':
        data.update(kind='absolute',relative_days=None,anchor_date=None,anchor_source_snippet=None)
    proposed=(ProposedDeadline if name=='deadline' else ProposedField)(**data)
    result=checked_field(name,proposed,text,date(2028,3,2))
    assert result.status=='unverified'
    assert result.source_start is None and result.source_end is None
    assert result.normalized_value is None


def proposal(deadline=None):
    absent={'value':None,'source_snippet':None}
    return ParkingTicket.model_validate({'doc_type':'parking_ticket',
        'issuing_agency':absent,'amount_due':absent,'required_action':absent,'contact':absent,
        'deadline':deadline or {**absent,'kind':None,'relative_days':None,'anchor_date':None,'anchor_source_snippet':None}})


def extract(proposed,text):
    stub=SimpleNamespace(extract=lambda *args:ExtractionResult(proposed,{},1))
    app.dependency_overrides[get_extractor]=lambda:stub
    app.dependency_overrides[get_today]=lambda:date(2028,3,2)
    try:
        with TestClient(app) as client:
            response=client.post('/api/extract',json={'text':text,'doc_type':'parking_ticket','text_confirmed':True,'amounts_confirmed':False})
            assert response.status_code==200
            return response.json()
    finally:
        app.dependency_overrides.clear()


def test_notice_with_no_deadline_does_not_infer_one_from_issued_date():
    text='SYNTHETIC INFORMATION NOTICE\nIssued: March 2, 2028\nThis page is for your records only.'
    result=extract(proposal(),text)
    assert result['fields']['deadline']['status']=='missing'
    assert result['fields']['deadline']['value'] is None
    assert result['fields']['deadline']['normalized_value'] is None
    assert result['fields']['deadline']['days_remaining'] is None


def test_bad_model_cannot_promote_issue_date_to_a_missing_deadline():
    text='SYNTHETIC INFORMATION NOTICE\nIssued: March 2, 2028\nThis page is for your records only.'
    wrong={'value':'March 2, 2028','source_snippet':'Issued: March 2, 2028','kind':'absolute',
           'relative_days':None,'anchor_date':None,'anchor_source_snippet':None}
    field=extract(proposal(wrong),text)['fields']['deadline']
    assert field['status']=='unverified' and field['normalized_value'] is None


def test_all_absent_fields_stay_missing_without_added_values():
    result=extract(proposal(),'SYNTHETIC ANNOUNCEMENT\nThis page is informational only.')
    assert all(field['status']=='missing' and field['value'] is None for field in result['fields'].values())
