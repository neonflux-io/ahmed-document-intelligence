from pathlib import Path

import pytesseract
from PIL import Image

from app.documents.adapters import DocumentAdapter
from app.documents.base import NormalizedDocument


class ImageDocumentAdapter(DocumentAdapter):
    """Adapter for image-based documents using OCR."""

    SUPPORTED_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".tif",
        ".tiff",
        ".bmp",
    }

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in self.SUPPORTED_EXTENSIONS

    def parse(self, path: Path) -> NormalizedDocument:
        image = Image.open(path)

        raw_text = pytesseract.image_to_string(
            image
        ).strip()

        warnings: list[str] = []

        character_count = len(raw_text)

        if character_count == 0:
            warnings.append(
                "OCR produced no readable text."
            )

        elif character_count < 100:
            warnings.append(
                "OCR produced very little text; "
                "document quality may be too poor for reliable extraction."
            )

        elif character_count < 500:
            warnings.append(
                "OCR output is short; "
                "some document content may have been missed."
            )

        return NormalizedDocument(
            source_document=path.name,
            document_type="image",
            raw_text=raw_text,
            extraction_warnings=warnings,
        )