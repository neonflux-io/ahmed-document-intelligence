from app.documents.adapters import DocumentAdapter
from app.documents.email_adapter import EmailDocumentAdapter
from app.documents.image_adapter import ImageDocumentAdapter
from app.documents.json_adapter import JSONDocumentAdapter
from app.documents.pdf_adapter import PDFDocumentAdapter


def get_default_adapters() -> list[DocumentAdapter]:
    """Return all supported document adapters."""

    return [
        JSONDocumentAdapter(),
        PDFDocumentAdapter(),
        EmailDocumentAdapter(),
        ImageDocumentAdapter(),
    ]