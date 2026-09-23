import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from app.documents.base import NormalizedDocument
from app.models.quotation import Quotation, QuotationLine


load_dotenv()


class ExtractionResult(BaseModel):
    """Structured result returned by the LLM."""

    supplier: str | None = None
    quotation_date: str | None = None
    currency: str | None = None

    lines: list[QuotationLine] = Field(
        default_factory=list
    )


class QuotationExtractor:
    """Extract structured quotation data from normalized documents."""

    def __init__(self) -> None:
        load_dotenv()

        use_mock = (
            os.getenv("USE_MOCK_LLM", "false").lower()
            == "true"
        )

        if use_mock:
            self.llm = None
            self.structured_llm = None
            self.use_mock = True
            return

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured. "
                "Add it to the local .env file."
            )

        self.llm = ChatOpenAI(
            model="gpt-5-mini",
            temperature=0,
            api_key=api_key,
        )

        self.structured_llm = self.llm.with_structured_output(
            ExtractionResult
        )

        self.use_mock = False

    def extract(
        self,
        document: NormalizedDocument,
    ) -> Quotation:

        if self.use_mock:
            return self._mock_extract(document)

        prompt = f"""
You are a document intelligence system extracting
pharmaceutical quotation information.

Extract information from the document below.

Rules:

1. Extract only information supported by the document.
2. Never invent missing values.
3. Preserve the original product name.
4. Extract the INN when present.
5. Preserve strength and dosage form separately when possible.
6. Distinguish price per UOM from price per pack.
7. Preserve the currency exactly.
8. Preserve ALL price tiers when they exist.
9. Preserve MOQ and lead time when available.
10. If a value is explicitly stated by the supplier,
    mark its price basis as "stated".
11. If a unit price must be calculated from a pack price,
    mark its price basis as "derived".
12. Never present a derived price as though the supplier
    explicitly stated it.
13. If the document contains a correction or superseding
    value, use the latest value as the final value.
14. For a corrected value, create evidence with:
    evidence_type = "correction"
    and preserve the earlier value in supersedes_value.
15. Add evidence for important extracted pricing fields.
16. If a value is uncertain, leave it null and add the
    field name to uncertain_fields.
17. Add warnings for contradictions, corrections,
    missing information, or unusual pricing situations.
18. source_document must be exactly:
    {document.source_document}

Document filename:
{document.source_document}

Document type:
{document.document_type}

Document content:
{document.raw_text}
"""

        result = self.structured_llm.invoke(prompt)

        quotation_lines: list[QuotationLine] = []

        for line in result.lines:
            line.source_document = document.source_document
            quotation_lines.append(line)

        quotation_id = document.metadata.get(
            "quotation_id",
            document.source_document,
        )

        quotation = Quotation(
            quotation_id=str(quotation_id),
            supplier=result.supplier,
            quotation_date=result.quotation_date,
            currency=result.currency,
            lines=quotation_lines,
            source_document=document.source_document,
        )

        return quotation

    def _mock_extract(
        self,
        document: NormalizedDocument,
    ) -> Quotation:
        """Create deterministic local output for development."""

        line = QuotationLine(
            product_name="Mock Extracted Product",
            inn=None,
            strength=None,
            dosage_form=None,
            uom=None,
            price_per_uom=None,
            price_per_uom_basis=None,
            price_per_pack=None,
            price_per_pack_basis=None,
            currency=None,
            source_document=document.source_document,
            uncertain_fields=[
                "product_name",
                "inn",
                "price",
            ],
            warnings=[
                "Mock extraction mode is enabled. "
                "This result must not be used as production data."
            ],
        )

        return Quotation(
            quotation_id=document.source_document,
            supplier="Mock Supplier",
            quotation_date=None,
            currency=None,
            lines=[line],
            source_document=document.source_document,
        )