"""Run with python -m pytest from the repository root."""

import json
from fastapi.testclient import TestClient
from backend.main import Settings, app

client = TestClient(app)


def test_health_contains_no_configuration(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "secret-test-value")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")
    settings = Settings.from_environment()
    assert settings.api_key == "secret-test-value"
    assert settings.model == "test-model"
    assert "secret-test-value" not in repr(settings)
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Hello from Notice Decoder!"}


def test_configuration_is_optional_in_milestone_zero(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    settings = Settings.from_environment()
    assert settings.api_key == settings.model == ""


def test_shell_and_manifest_assets_are_served():
    page = client.get("/")
    assert page.status_code == 200
    assert "not legal advice" in page.text
    manifest = client.get("/manifest.webmanifest")
    assert manifest.status_code == 200
    data = manifest.json()
    assert data["display"] == "standalone"
    for icon in data["icons"]:
        response = client.get(icon["src"])
        assert response.status_code == 200
        assert response.content.startswith(b"\x89PNG\r\n\x1a\n")
        size = int(icon["sizes"].split("x")[0])
        assert int.from_bytes(response.content[16:20], "big") == size
        assert int.from_bytes(response.content[20:24], "big") == size
    for path in ["/styles.css", "/app.js", "/sw.js"]:
        assert client.get(path).status_code == 200


def test_private_files_are_not_served():
    for path in ["/.env", "/.env.example", "/backend/main.py", "/.git/config"]:
        assert client.get(path).status_code == 404


def test_cache_allowlist_excludes_api():
    # Guard the privacy boundary: only static shell paths may be precached.
    script = client.get("/sw.js").text
    shell = json.loads(script.split("const SHELL = ", 1)[1].split(";", 1)[0])
    assert all(not path.startswith("/api") for path in shell)
    assert "!SHELL.includes(url.pathname)" in script


def test_public_assets_and_configuration_never_expose_credentials(monkeypatch):
    # Deliberately artificial credential: never load the real .env in tests.
    secret = 'synthetic-private-credential-for-boundary-test'
    monkeypatch.setattr(app.state, 'settings', Settings(secret, 'test-model'))
    script = client.get('/sw.js').text
    shell = json.loads(script.split('const SHELL = ', 1)[1].split(';', 1)[0])
    private = ['/.env', '/.env.example', '/%2eenv', '/..%2f.env', '/%2e%2e/.env', '/backend/main.py', '/.git/config']
    for path in ['/api/health', '/api/config', *shell, *private]:
        response = client.get(path)
        assert secret.encode() not in response.content
        assert secret not in str(response.headers)
        if path in private:
            assert response.status_code == 404
        if path.startswith('/api/'):
            assert response.headers['cache-control'] == 'no-store'
