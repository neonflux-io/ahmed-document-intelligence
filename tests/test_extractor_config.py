import pytest

from app.extraction.extractor import QuotationExtractor


def test_extractor_requires_api_key(monkeypatch):
    monkeypatch.delenv(
        "OPENAI_API_KEY",
        raising=False,
    )

    monkeypatch.setenv(
        "USE_MOCK_LLM",
        "false",
    )

    with pytest.raises(
        RuntimeError,
        match="OPENAI_API_KEY is not configured",
    ):
        QuotationExtractor()


def test_extractor_supports_mock_mode(monkeypatch):
    monkeypatch.delenv(
        "OPENAI_API_KEY",
        raising=False,
    )

    monkeypatch.setenv(
        "USE_MOCK_LLM",
        "true",
    )

    extractor = QuotationExtractor()

    assert extractor.use_mock is True
    assert extractor.structured_llm is None