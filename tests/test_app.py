from fastapi.testclient import TestClient

import app


client = TestClient(app.app)


class _SuccessResult:
    class _Document:
        @staticmethod
        def export_to_markdown() -> str:
            return "# ok"

    document = _Document()


class _SuccessConverter:
    @staticmethod
    def convert(_: str) -> _SuccessResult:
        return _SuccessResult()


class _FailConverter:
    @staticmethod
    def convert(_: str) -> _SuccessResult:
        raise RuntimeError("boom")


def test_healthz_returns_ok() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_convert_returns_markdown() -> None:
    old_converter = app.converter
    app.converter = _SuccessConverter()
    try:
        response = client.get("/convert", params={"url": "https://arxiv.org/pdf/1234.5678"})
    finally:
        app.converter = old_converter

    assert response.status_code == 200
    assert response.text == "# ok"
    assert response.headers["content-type"].startswith("text/markdown")


def test_convert_requires_url() -> None:
    response = client.get("/convert")
    assert response.status_code == 422


def test_convert_rejects_invalid_url() -> None:
    response = client.get("/convert", params={"url": "not-a-url"})
    assert response.status_code == 422


def test_convert_returns_502_on_conversion_failure() -> None:
    old_converter = app.converter
    app.converter = _FailConverter()
    try:
        response = client.get("/convert", params={"url": "https://arxiv.org/pdf/1234.5678"})
    finally:
        app.converter = old_converter

    assert response.status_code == 502
    assert "Conversion failed" in response.json()["detail"]
