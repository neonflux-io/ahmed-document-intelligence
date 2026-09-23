import csv
from pathlib import Path

from app.models.quotation import Quotation


class CSVStorage:
    """Export quotation lines into a human-review CSV file."""

    def __init__(
        self,
        output_path: str = "output/quotations.csv",
    ) -> None:
        self.output_path = Path(output_path)

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(self, quotation: Quotation) -> None:
        fieldnames = [
            "quotation_id",
            "supplier",
            "quotation_date",
            "product_name",
            "inn",
            "strength",
            "dosage_form",
            "uom",
            "units_per_pack",
            "pack_description",
            "price_per_uom",
            "price_per_uom_basis",
            "price_per_pack",
            "price_per_pack_basis",
            "currency",
            "moq",
            "lead_time_days",
            "source_document",
            "confidence",
            "confidence_level",
            "requires_human_review",
            "uncertain_fields",
            "warnings",
        ]

        with self.output_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames,
            )

            writer.writeheader()

            for line in quotation.lines:
                writer.writerow(
                    {
                        "quotation_id": quotation.quotation_id,
                        "supplier": quotation.supplier,
                        "quotation_date": quotation.quotation_date,
                        "product_name": line.product_name,
                        "inn": line.inn,
                        "strength": line.strength,
                        "dosage_form": line.dosage_form,
                        "uom": line.uom,
                        "units_per_pack": line.units_per_pack,
                        "pack_description": line.pack_description,
                        "price_per_uom": line.price_per_uom,
                        "price_per_uom_basis": line.price_per_uom_basis,
                        "price_per_pack": line.price_per_pack,
                        "price_per_pack_basis": line.price_per_pack_basis,
                        "currency": line.currency,
                        "moq": line.moq,
                        "lead_time_days": line.lead_time_days,
                        "source_document": line.source_document,
                        "confidence": line.confidence,
                        "confidence_level": line.confidence_level,
                        "requires_human_review": (
                            line.requires_human_review
                        ),
                        "uncertain_fields": ", ".join(
                            line.uncertain_fields
                        ),
                        "warnings": " | ".join(
                            line.warnings
                        ),
                    }
                )