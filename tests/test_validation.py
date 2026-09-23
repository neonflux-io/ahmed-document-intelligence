from app.models.quotation import Quotation, QuotationLine
from app.validation.confidence import ConfidenceScorer
from app.validation.validator import QuotationValidator


def test_low_confidence_requires_human_review():
    quotation = Quotation(
        quotation_id="TEST-001",
        source_document="test.json",
        lines=[
            QuotationLine(
                product_name="Test Product",
                source_document="test.json",
                uncertain_fields=["price"],
            )
        ],
    )

    validator = QuotationValidator()
    quotation = validator.validate(quotation)

    scorer = ConfidenceScorer()
    quotation = scorer.score(quotation)

    line = quotation.lines[0]

    assert line.confidence_level == "low"
    assert line.requires_human_review is True


def test_complete_line_has_high_confidence():
    quotation = Quotation(
        quotation_id="TEST-002",
        source_document="test.json",
        lines=[
            QuotationLine(
                product_name="Testamol 500",
                inn="Paracetamol",
                strength="500 mg",
                dosage_form="tablet",
                uom="tablet",
                price_per_uom=0.05,
                price_per_uom_basis="stated",
                currency="USD",
                source_document="test.json",
            )
        ],
    )

    validator = QuotationValidator()
    quotation = validator.validate(quotation)

    scorer = ConfidenceScorer()
    quotation = scorer.score(quotation)

    line = quotation.lines[0]

    assert line.confidence_level == "high"
    assert line.requires_human_review is False
    assert line.price_per_uom_basis == "stated"