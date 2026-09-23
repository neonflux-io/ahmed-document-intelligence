from app.models.quotation import Evidence, QuotationLine


def test_price_correction_preserves_previous_value():
    line = QuotationLine(
        product_name="Azimax 250",
        currency="EUR",
        price_per_uom=0.134,
        price_per_uom_basis="stated",
        source_document="novara.eml",
        warnings=[
            "A later price supersedes the earlier quoted price."
        ],
        evidence=[
            Evidence(
                field="price_per_uom",
                value=0.134,
                source_document="novara.eml",
                location="correction section",
                extraction_method="llm",
                evidence_type="correction",
                supersedes_value=0.128,
                notes=(
                    "Later supplier communication "
                    "supersedes the earlier price."
                ),
            )
        ],
    )

    assert line.price_per_uom == 0.134
    assert line.price_per_uom_basis == "stated"

    assert len(line.evidence) == 1

    evidence = line.evidence[0]

    assert evidence.evidence_type == "correction"
    assert evidence.value == 0.134
    assert evidence.supersedes_value == 0.128