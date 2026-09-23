from pathlib import Path

from app.documents.loader import DocumentLoader


def test_all_real_documents_can_be_loaded():
    input_dir = Path("data/input")

    loader = DocumentLoader()

    files = sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file()
    )

    assert len(files) == 8

    for path in files:
        document = loader.load(path)

        assert document.source_document == path.name
        assert document.document_type in {
            "pdf",
            "json",
            "email",
            "image",
        }

        assert document.raw_text.strip()