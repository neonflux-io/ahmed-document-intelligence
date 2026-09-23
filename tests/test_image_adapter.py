from pathlib import Path

from PIL import Image, ImageDraw

from app.documents.image_adapter import ImageDocumentAdapter


def test_image_adapter_reads_text():
    image_path = Path("data/test/sample_quotation.png")

    image = Image.new(
        "RGB",
        (1000, 400),
        "white",
    )

    draw = ImageDraw.Draw(image)

    draw.text(
        (50, 50),
        "Test Pharma Quotation",
        fill="black",
    )

    draw.text(
        (50, 120),
        "Product: Testamol 500",
        fill="black",
    )

    draw.text(
        (50, 190),
        "INN: Paracetamol",
        fill="black",
    )

    draw.text(
        (50, 260),
        "Price: 0.05 USD per tablet",
        fill="black",
    )

    image.save(image_path)

    adapter = ImageDocumentAdapter()

    assert adapter.supports(image_path)

    result = adapter.parse(image_path)

    assert result.source_document == "sample_quotation.png"
    assert result.document_type == "image"
    assert "Testamol" in result.raw_text