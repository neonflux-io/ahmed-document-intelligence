from app.models.quotation import QuotationLine


def test_stated_unit_price_is_preserved():
    line = QuotationLine(
        product_name="Test Product",
        price_per_uom=0.05,
        price_per_uom_basis="stated",
        currency="USD",
        source_document="test.json",
    )

    assert line.price_per_uom == 0.05
    assert line.price_per_uom_basis == "stated"


def test_derived_unit_price_is_distinguished():
    line = QuotationLine(
        product_name="Test Product",
        units_per_pack=90,
        price_per_pack=3.15,
        price_per_pack_basis="stated",
        price_per_uom=0.035,
        price_per_uom_basis="derived",
        currency="EUR",
        source_document="test.json",
    )

    assert line.price_per_pack == 3.15
    assert line.price_per_pack_basis == "stated"

    assert line.price_per_uom == 0.035
    assert line.price_per_uom_basis == "derived"