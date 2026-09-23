from pathlib import Path

from app.documents.loader import DocumentLoader


def test_sanova_json_contains_pack_price_without_stated_unit_price():
    path = Path(
        "data/input/sanova_offer_export_2026-08-03.json"
    )

    document = DocumentLoader().load(path)

    text = document.raw_text

    assert "Sanotri-TLD" in text

    assert '"units_per_pack": 90' in text
    assert '"price_per_pack": 3.15' in text

    assert "Unit prices not stated separately" in text