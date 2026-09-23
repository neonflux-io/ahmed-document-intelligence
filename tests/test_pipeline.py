from pathlib import Path

from app.extraction.pipeline import DocumentProcessingPipeline


def test_pipeline_processes_real_json(monkeypatch, tmp_path):
    monkeypatch.setenv(
        "USE_MOCK_LLM",
        "true",
    )

    monkeypatch.setenv(
        "OPENAI_API_KEY",
        "",
    )

    monkeypatch.chdir(tmp_path)

    source_file = Path(
        "data/input/sanova_offer_export_2026-08-03.json"
    )

    # Copy the real assessment file into the temporary
    # test directory so the test does not modify the
    # project's real output files.
    source_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    original_file = Path(
        __file__
    ).parent.parent / "data" / "input" / (
        "sanova_offer_export_2026-08-03.json"
    )

    target_file = source_file

    target_file.write_bytes(
        original_file.read_bytes()
    )

    pipeline = DocumentProcessingPipeline()

    quotation = pipeline.process(
        target_file
    )

    assert quotation.source_document == (
        "sanova_offer_export_2026-08-03.json"
    )

    assert quotation.supplier == "Mock Supplier"

    assert len(quotation.lines) == 1

    assert quotation.lines[0].requires_human_review is True

    assert Path(
        "output/quotations.csv"
    ).exists()

    assert Path(
        "output/quotations.db"
    ).exists()