from pathlib import Path

from app.documents.loader import DocumentLoader


def test_novara_email_contains_price_correction():
    path = Path(
        "data/input/RE_RFQ-2026-0244_Novara_quotation.eml"
    )

    loader = DocumentLoader()

    document = loader.load(path)

    text = document.raw_text.lower()

    assert "azimax 250" in text

    assert "0.128 per tablet" in text

    assert "0.134 per tablet" in text

    assert "correction on line 1" in text

    assert "lines 2 and 3 are" in text
    assert "unchanged." in text