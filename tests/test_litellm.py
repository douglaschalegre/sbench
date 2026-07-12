from __future__ import annotations

from pathlib import Path

from sbench import litellm


def test_check_litellm_proxy_accepts_a_healthy_response(monkeypatch) -> None:
    captured = {}

    class Response:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return None

    def fake_urlopen(request, *, timeout):
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        return Response()

    monkeypatch.setattr(litellm, "urlopen", fake_urlopen)

    health = litellm.check_litellm_proxy(
        base_url="http://127.0.0.1:4100/v1",
        timeout_seconds=1.5,
    )

    assert health.available is True
    assert health.url == "http://127.0.0.1:4100/health/liveliness"
    assert captured == {
        "url": "http://127.0.0.1:4100/health/liveliness",
        "timeout": 1.5,
    }


def test_check_litellm_proxy_reports_connection_failures(monkeypatch) -> None:
    def fake_urlopen(request, *, timeout):
        raise ConnectionRefusedError("connection refused")

    monkeypatch.setattr(litellm, "urlopen", fake_urlopen)

    health = litellm.check_litellm_proxy(base_url="http://localhost:4000")

    assert health.available is False
    assert health.detail == "connection refused"
    assert "make litellm" in litellm.render_litellm_unavailable(health)


def test_check_litellm_proxy_loads_repo_environment(monkeypatch, tmp_path: Path) -> None:
    (tmp_path / ".env").write_text(
        "LITELLM_BASE_URL=http://proxy.example.test:4200\n",
        encoding="utf-8",
    )

    captured = {}

    class Response:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return None

    def fake_urlopen(request, *, timeout):
        captured["url"] = request.full_url
        return Response()

    monkeypatch.delenv("LITELLM_BASE_URL", raising=False)
    monkeypatch.setattr(litellm, "urlopen", fake_urlopen)

    health = litellm.check_litellm_proxy(repo_root=tmp_path)

    assert health.available is True
    assert captured["url"] == "http://proxy.example.test:4200/health/liveliness"
