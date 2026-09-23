from pathlib import Path

import pymupdf
import pytesseract
from PIL import Image

from app.documents.adapters import DocumentAdapter
from app.documents.base import NormalizedDocument


class PDFDocumentAdapter(DocumentAdapter):
    """Adapter for text-based and scanned PDF documents."""

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() == ".pdf"

    def parse(self, path: Path) -> NormalizedDocument:
        document = pymupdf.open(path)

        pages: list[str] = []
        warnings: list[str] = []

        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            if text:
                pages.append(text)
                continue

            # No embedded text was found.
            # Render the page and use OCR instead.
            try:
                pixmap = page.get_pixmap(
                    matrix=pymupdf.Matrix(2, 2)
                )

                image = Image.frombytes(
                    "RGB",
                    [pixmap.width, pixmap.height],
                    pixmap.samples,
                )

                ocr_text = pytesseract.image_to_string(
                    image
                ).strip()

                if ocr_text:
                    pages.append(ocr_text)
                    warnings.append(
                        f"Page {page_number} required OCR."
                    )
                else:
                    warnings.append(
                        f"Page {page_number} contained no "
                        "extractable text after OCR."
                    )

            except Exception as exc:
                warnings.append(
                    f"OCR failed on page {page_number}: {exc}"
                )

        document.close()

        raw_text = "\n\n".join(pages)

        if not raw_text:
            warnings.append(
                "No text could be extracted from the PDF."
            )

        return NormalizedDocument(
            source_document=path.name,
            document_type="pdf",
            raw_text=raw_text,
            extraction_warnings=warnings,
        )