from app.models.quotation import PriceTier, QuotationLine


def test_tiered_pricing_is_preserved():
    line = QuotationLine(
        product_name="Panadel 500",
        currency="ZAR",
        source_document="ubuntu.json",
        price_tiers=[
            PriceTier(
                min_quantity=100,
                max_quantity=999,
                price=41.5,
                currency="ZAR",
                price_basis="per_pack",
            ),
            PriceTier(
                min_quantity=1000,
                max_quantity=4999,
                price=37.9,
                currency="ZAR",
                price_basis="per_pack",
            ),
            PriceTier(
                min_quantity=5000,
                max_quantity=None,
                price=34.2,
                currency="ZAR",
                price_basis="per_pack",
            ),
        ],
    )

    assert len(line.price_tiers) == 3

    assert line.price_tiers[0].price == 41.5
    assert line.price_tiers[1].price == 37.9
    assert line.price_tiers[2].price == 34.2

    assert line.price_tiers[0].min_quantity == 100
    assert line.price_tiers[1].min_quantity == 1000
    assert line.price_tiers[2].min_quantity == 5000