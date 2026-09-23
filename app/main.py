import sys
from pathlib import Path

from app.extraction.pipeline import DocumentProcessingPipeline


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage: python -m app.main <document_path>"
        )
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    try:
        pipeline = DocumentProcessingPipeline()

        quotation = pipeline.process(file_path)

    except Exception as exc:
        print(f"Processing failed: {exc}")
        sys.exit(1)

    print()
    print("Extraction completed.")
    print(f"Source: {quotation.source_document}")
    print(f"Supplier: {quotation.supplier}")
    print(f"Confidence: {quotation.confidence}")
    print(f"Confidence level: {quotation.confidence_level}")
    print(f"Lines extracted: {len(quotation.lines)}")

    print()
    print("Review status:")

    for line in quotation.lines:
        print(
            f"- {line.product_name}: "
            f"review={line.requires_human_review}"
        )

        if line.warnings:
            for warning in line.warnings:
                print(f"  Warning: {warning}")

    print()
    print("Outputs:")
    print("- output/quotations.db")
    print("- output/quotations.csv")


if __name__ == "__main__":
    main()