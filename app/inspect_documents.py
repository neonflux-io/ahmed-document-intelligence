from pathlib import Path

from app.documents.loader import DocumentLoader


def main() -> None:
    input_dir = Path("data/input")

    loader = DocumentLoader()

    for path in sorted(input_dir.iterdir()):
        if not path.is_file():
            continue

        print("=" * 80)
        print(f"FILE: {path.name}")

        try:
            document = loader.load(path)

            print(f"TYPE: {document.document_type}")
            print(f"TEXT LENGTH: {len(document.raw_text)}")

            if document.extraction_warnings:
                print("WARNINGS:")
                for warning in document.extraction_warnings:
                    print(f"  - {warning}")
            else:
                print("WARNINGS: none")

            print()
            print("TEXT PREVIEW:")
            print(document.raw_text[:1500])

        except Exception as exc:
            print(f"ERROR: {exc}")

        print()


if __name__ == "__main__":
    main()