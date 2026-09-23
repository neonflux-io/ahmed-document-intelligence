from pathlib import Path

from app.documents.json_adapter import JSONDocumentAdapter


def test_json_adapter_reads_document():
    path = Path("data/test/sample_quotation.json")

    adapter = JSONDocumentAdapter()

    assert adapter.supports(path)

    document = adapter.parse(path)

    assert document.source_document == "sample_quotation.json"
    assert document.document_type == "json"
    assert "Testamol 500" in document.raw_text
    assert "Paracetamol" in document.raw_text