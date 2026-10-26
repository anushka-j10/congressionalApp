"""Real middleware controls with synthetic notices; no provider calls or secrets."""
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.deployment import DeploymentPolicy, AnalysisBudget

ORIGIN = 'https://notice-decoder.example'


@pytest.fixture
def deployed(monkeypatch):
    policy = DeploymentPolicy(True, ORIGIN, per_minute=3, per_hour=5)
    monkeypatch.setattr(app.state, 'deployment', policy)
    monkeypatch.setattr(app.state, 'analysis_budget', AnalysisBudget(policy))
    with TestClient(app) as client:
        yield client


@pytest.mark.parametrize('origin', ['http://bad.example', 'null', ORIGIN + '.evil', ORIGIN + '/'])
def test_foreign_origin_rejected_before_processing(deployed, origin):
    response = deployed.post('/api/read', headers={'Origin': origin}, content=b'PRIVATE SYNTHETIC NOTICE')
    assert response.status_code == 403
    assert 'PRIVATE' not in response.text
    assert 'access-control-allow-origin' not in response.headers
    assert response.headers['cache-control'] == 'no-store'
    assert app.state.analysis_budget.active == 0
    assert not app.state.analysis_budget.minute


def test_exact_cors_origin_and_preflight(deployed):
    response = deployed.options('/api/extract', headers={'Origin': ORIGIN,
        'Access-Control-Request-Method': 'POST', 'Access-Control-Request-Headers': 'content-type,x-notice-language'})
    assert response.status_code == 200
    assert response.headers['access-control-allow-origin'] == ORIGIN
    assert response.headers['vary'] == 'Origin'
    assert response.headers['access-control-allow-methods'] == 'POST'
    assert not app.state.analysis_budget.minute
    assert deployed.options('/api/extract', headers={'Origin': ORIGIN,
        'Access-Control-Request-Method': 'POST', 'Access-Control-Request-Headers': 'x-unapproved'}).status_code == 403
    assert deployed.options('/api/extract', headers={'Origin': ORIGIN,
        'Access-Control-Request-Method': 'DELETE'}).status_code == 403


def test_limit_shared_across_analysis_routes_and_not_bypassable_by_forwarded_ip(deployed):
    for path in ['/api/read', '/api/extract', '/api/explain']:
        response = deployed.post(path, content=b'bad', headers={'Origin': ORIGIN})
        assert response.status_code in {400, 415, 422}
        assert response.headers['access-control-allow-origin'] == ORIGIN
    response = deployed.post('/api/extract', headers={'Origin': ORIGIN, 'X-Forwarded-For': '192.0.2.99'})
    assert response.status_code == 429 and response.headers['retry-after'] == '60'
    assert response.headers['cache-control'] == 'no-store'
    assert app.state.analysis_budget.active == 0
    assert deployed.get('/api/health').status_code == 200
    assert deployed.get('/manifest.webmanifest').status_code == 200


def test_originless_requests_still_rate_limited(deployed):
    for _ in range(3):
        assert deployed.post('/api/read').status_code == 415
    assert deployed.post('/api/read/').status_code == 429


def test_budget_minute_hour_concurrency_and_expiry():
    now = [0]
    policy = DeploymentPolicy(True, ORIGIN, per_minute=2, per_hour=3, concurrent=1)
    budget = AnalysisBudget(policy, lambda: now[0])
    assert budget.acquire()
    assert not budget.acquire()  # A busy request is not charged another slot.
    budget.release()
    assert budget.acquire()
    budget.release()
    assert not budget.acquire()
    now[0] = 60
    assert budget.acquire()
    budget.release()
    now[0] = 120
    assert not budget.acquire()  # Hourly budget remains active after minute reset.
    now[0] = 3600
    assert budget.acquire()
    budget.release()


@pytest.mark.parametrize('origin', ['', 'http://notice.example', 'https://notice.example/',
    'https://notice.example/path', 'https://u:p@notice.example', 'https://notice.example?key=x'])
def test_production_requires_exact_https_origin(monkeypatch, origin):
    monkeypatch.setenv('APP_ENV', 'production')
    monkeypatch.setenv('PUBLIC_ORIGIN', origin)
    monkeypatch.delenv('RENDER_EXTERNAL_URL', raising=False)
    with pytest.raises(ValueError, match='HTTPS PUBLIC_ORIGIN'):
        DeploymentPolicy.from_environment()


def test_render_auto_enables_protection_and_uses_injected_url(monkeypatch):
    monkeypatch.delenv('APP_ENV', raising=False)
    monkeypatch.delenv('PUBLIC_ORIGIN', raising=False)
    monkeypatch.setenv('RENDER', 'true')
    monkeypatch.setenv('RENDER_EXTERNAL_URL', ORIGIN)
    assert DeploymentPolicy.from_environment() == DeploymentPolicy(True, ORIGIN)
