from pathlib import Path

import fitz

from app.documents.pdf_adapter import PDFDocumentAdapter


def test_pdf_adapter_reads_text():
    pdf_path = Path("data/test/sample_quotation.pdf")

    document = fitz.open()

    page = document.new_page()

    page.insert_text(
        (72, 72),
        "Test Pharma Quotation\n"
        "Product: Testamol 500\n"
        "INN: Paracetamol\n"
        "Unit Price: 0.05 USD",
    )

    document.save(pdf_path)
    document.close()

    adapter = PDFDocumentAdapter()

    assert adapter.supports(pdf_path)

    result = adapter.parse(pdf_path)

    assert result.source_document == "sample_quotation.pdf"
    assert result.document_type == "pdf"
    assert "Testamol 500" in result.raw_text
    assert "Paracetamol" in result.raw_text