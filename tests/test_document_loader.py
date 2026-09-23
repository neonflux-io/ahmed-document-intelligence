from pathlib import Path
from app.documents.loader import DocumentLoader


def test_loader_selects_json_adapter():
    loader = DocumentLoader()
    path = Path("data/test/sample_quotation.json")
    document = loader.load(path)
    assert document.document_type == "json"


def test_loader_selects_pdf_adapter():
    loader = DocumentLoader()
    path = Path("data/test/sample_quotation.pdf")
    document = loader.load(path)
    assert document.document_type == "pdf"

def test_loader_selects_email_adapter():
    loader = DocumentLoader()
    path = Path("data/test/sample_quotation.eml")
    document = loader.load(path)
    assert document.document_type == "email"


def test_loader_selects_image_adapter():
    loader = DocumentLoader()

    path = Path("data/test/sample_quotation.png")

    document = loader.load(path)

    assert document.document_type == "image"