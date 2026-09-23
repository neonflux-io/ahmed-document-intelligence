from pathlib import Path

from app.models.quotation import Quotation, QuotationLine
from app.storage.csv import CSVStorage


def test_csv_storage_creates_review_file(tmp_path):
    output_file = tmp_path / "quotations.csv"

    quotation = Quotation(
        quotation_id="TEST-CSV-001",
        supplier="Test Pharma",
        quotation_date="2026-09-23",
        currency="USD",
        source_document="test.json",
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
                source_document="test.json",
                confidence=0.95,
                confidence_level="high",
                requires_human_review=False,
            )
        ],
    )

    storage = CSVStorage(str(output_file))
    storage.save(quotation)

    assert output_file.exists()

    content = output_file.read_text(
        encoding="utf-8"
    )

    assert "Testamol 500" in content
    assert "Paracetamol" in content
    assert "0.05" in content
    assert "high" in content