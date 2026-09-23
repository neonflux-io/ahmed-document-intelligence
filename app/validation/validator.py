from app.models.quotation import Quotation


class QuotationValidator:
    """Run deterministic validation checks on extracted quotations."""

    def validate(self, quotation: Quotation) -> Quotation:
        warnings = list(quotation.warnings)

        if not quotation.lines:
            warnings.append("No quotation lines were extracted.")

        for index, line in enumerate(quotation.lines, start=1):
            if not line.product_name:
                line.uncertain_fields.append("product_name")
                warnings.append(
                    f"Line {index}: product name is missing."
                )

            if not line.source_document:
                line.uncertain_fields.append("source_document")
                warnings.append(
                    f"Line {index}: source document is missing."
                )

            if not line.currency:
                line.uncertain_fields.append("currency")
                warnings.append(
                    f"Line {index}: currency is missing."
                )

            if (
                line.price_per_uom is None
                and line.price_per_pack is None
                and not line.price_tiers
            ):
                line.uncertain_fields.append("price")
                warnings.append(
                    f"Line {index}: no price was extracted."
                )

            if line.price_per_uom is not None and line.price_per_uom < 0:
                line.warnings.append(
                    "Price per UOM cannot be negative."
                )

            if (
                line.price_per_pack is not None
                and line.price_per_pack < 0
            ):
                line.warnings.append(
                    "Price per pack cannot be negative."
                )

            for tier in line.price_tiers:
                if tier.price < 0:
                    line.warnings.append(
                        "Tier price cannot be negative."
                    )

                if (
                    tier.min_quantity is not None
                    and tier.max_quantity is not None
                    and tier.min_quantity > tier.max_quantity
                ):
                    line.warnings.append(
                        "Tier minimum quantity is greater than "
                        "maximum quantity."
                    )

        quotation.warnings = warnings

        return quotation