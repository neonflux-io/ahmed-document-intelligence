from app.documents.base import NormalizedDocument
from app.extraction.extractor import (
    ExtractionResult,
    QuotationExtractor,
)
from app.models.quotation import QuotationLine


class FakeStructuredLLM:
    def invoke(self, prompt: str) -> ExtractionResult:
        return ExtractionResult(
            supplier="Test Pharma",
            quotation_date="2026-09-23",
            currency="USD",
            lines=[
                QuotationLine(
                    product_name="Testamol 500",
                    inn="Paracetamol",
                    strength="500 mg",
                    dosage_form="tablet",
                    uom="tablet",
                    price_per_uom=0.05,
                    price_per_uom_basis="stated",
                    currency="USD",
                    source_document="sample_quotation.json",
                )
            ],
        )


def test_extractor_builds_quotation(monkeypatch):
    monkeypatch.setenv(
        "OPENAI_API_KEY",
        "test-key",
    )

    monkeypatch.setenv(
        "USE_MOCK_LLM",
        "false",
    )

    extractor = QuotationExtractor()

    extractor.structured_llm = FakeStructuredLLM()

    document = NormalizedDocument(
        source_document="sample_quotation.json",
        document_type="json",
        raw_text=(
            "Product: Testamol 500\n"
            "INN: Paracetamol\n"
            "Price: 0.05 USD per tablet"
        ),
    )

    quotation = extractor.extract(document)

    assert quotation.supplier == "Test Pharma"
    assert quotation.currency == "USD"
    assert len(quotation.lines) == 1

    line = quotation.lines[0]

    assert line.product_name == "Testamol 500"
    assert line.price_per_uom == 0.05
    assert line.price_per_uom_basis == "stated"
    assert line.source_document == "sample_quotation.json"