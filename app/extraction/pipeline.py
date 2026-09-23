from pathlib import Path

from app.documents.loader import DocumentLoader
from app.extraction.extractor import QuotationExtractor
from app.storage.csv import CSVStorage
from app.storage.sqlite import SQLiteStorage
from app.validation.confidence import ConfidenceScorer
from app.validation.validator import QuotationValidator


class DocumentProcessingPipeline:
    """Process one document from ingestion to human-review output."""

    def __init__(self) -> None:
        self.loader = DocumentLoader()
        self.extractor = QuotationExtractor()
        self.validator = QuotationValidator()
        self.confidence_scorer = ConfidenceScorer()

        self.sqlite_storage = SQLiteStorage()
        self.csv_storage = CSVStorage()

    def process(self, path: Path):
        document = self.loader.load(path)

        quotation = self.extractor.extract(document)

        quotation = self.validator.validate(
            quotation
        )

        quotation = self.confidence_scorer.score(
            quotation
        )

        self.sqlite_storage.save(quotation)
        self.csv_storage.save(quotation)

        return quotation