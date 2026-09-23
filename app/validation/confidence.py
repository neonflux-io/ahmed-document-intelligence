from app.models.quotation import Quotation


class ConfidenceScorer:
    """Calculate confidence and identify records requiring review."""

    def score(self, quotation: Quotation) -> Quotation:
        for line in quotation.lines:
            score = 1.0

            if not line.product_name:
                score -= 0.20

            if not line.inn:
                score -= 0.10

            if (
                line.price_per_uom is None
                and line.price_per_pack is None
                and not line.price_tiers
            ):
                score -= 0.25

            if not line.currency:
                score -= 0.15

            score -= min(
                len(line.uncertain_fields) * 0.05,
                0.20,
            )

            score -= min(
                len(line.warnings) * 0.05,
                0.20,
            )

            score = max(0.0, min(1.0, score))

            line.confidence = round(score, 2)

            if score >= 0.85:
                line.confidence_level = "high"
            elif score >= 0.65:
                line.confidence_level = "medium"
            else:
                line.confidence_level = "low"

            line.requires_human_review = (
                line.confidence_level == "low"
                or bool(line.uncertain_fields)
                or bool(line.warnings)
            )

        if quotation.lines:
            quotation.confidence = round(
                sum(line.confidence for line in quotation.lines)
                / len(quotation.lines),
                2,
            )
        else:
            quotation.confidence = 0.0

        if quotation.confidence >= 0.85:
            quotation.confidence_level = "high"
        elif quotation.confidence >= 0.65:
            quotation.confidence_level = "medium"
        else:
            quotation.confidence_level = "low"

        return quotation