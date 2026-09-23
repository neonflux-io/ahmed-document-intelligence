from pathlib import Path

from app.documents.image_adapter import ImageDocumentAdapter


def test_poor_quality_ocr_is_flagged():
    path = Path(
        "data/input/scan_03_glare_partial_andina_p1.jpg"
    )

    adapter = ImageDocumentAdapter()

    result = adapter.parse(path)

    assert len(result.raw_text) < 100
    assert any(
        "very little text" in warning
        for warning in result.extraction_warnings
    )