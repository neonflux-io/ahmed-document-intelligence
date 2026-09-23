from pathlib import Path

from app.documents.loader import DocumentLoader


def test_ubuntu_json_preserves_tiered_pricing():
    path = Path(
        "data/input/ubuntu_health_price_list_Q3-2026.json"
    )

    document = DocumentLoader().load(path)

    text = document.raw_text

    assert "Panadel 500" in text

    assert '"min_packs": 100' in text
    assert '"max_packs": 999' in text
    assert '"price_per_pack": 41.5' in text

    assert '"min_packs": 1000' in text
    assert '"max_packs": 4999' in text
    assert '"price_per_pack": 37.9' in text

    assert '"min_packs": 5000' in text
    assert '"price_per_pack": 34.2' in text