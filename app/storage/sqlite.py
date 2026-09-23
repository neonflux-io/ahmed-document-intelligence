import json
import sqlite3
from pathlib import Path

from app.models.quotation import Quotation


class SQLiteStorage:
    """Persist quotation results for human review."""

    def __init__(self, database_path: str = "output/quotations.db") -> None:
        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._create_tables()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)

    def _create_tables(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS quotations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quotation_id TEXT,
                    supplier TEXT,
                    quotation_date TEXT,
                    currency TEXT,
                    source_document TEXT,
                    confidence REAL,
                    confidence_level TEXT,
                    warnings TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS quotation_lines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quotation_id INTEGER,
                    product_name TEXT,
                    inn TEXT,
                    strength TEXT,
                    dosage_form TEXT,
                    uom TEXT,
                    units_per_pack REAL,
                    pack_description TEXT,
                    price_per_uom REAL,
                    price_per_pack REAL,
                    currency TEXT,
                    price_tiers TEXT,
                    moq REAL,
                    lead_time_days INTEGER,
                    source_document TEXT,
                    confidence REAL,
                    confidence_level TEXT,
                    uncertain_fields TEXT,
                    warnings TEXT,
                    evidence TEXT,
                    FOREIGN KEY (quotation_id)
                        REFERENCES quotations(id)
                )
                """
            )

    def save(self, quotation: Quotation) -> None:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO quotations (
                    quotation_id,
                    supplier,
                    quotation_date,
                    currency,
                    source_document,
                    confidence,
                    confidence_level,
                    warnings
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    quotation.quotation_id,
                    quotation.supplier,
                    quotation.quotation_date,
                    quotation.currency,
                    quotation.source_document,
                    quotation.confidence,
                    quotation.confidence_level,
                    json.dumps(quotation.warnings),
                ),
            )

            quotation_db_id = cursor.lastrowid

            for line in quotation.lines:
                connection.execute(
                    """
                    INSERT INTO quotation_lines (
                        quotation_id,
                        product_name,
                        inn,
                        strength,
                        dosage_form,
                        uom,
                        units_per_pack,
                        pack_description,
                        price_per_uom,
                        price_per_pack,
                        currency,
                        price_tiers,
                        moq,
                        lead_time_days,
                        source_document,
                        confidence,
                        confidence_level,
                        uncertain_fields,
                        warnings,
                        evidence
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        quotation_db_id,
                        line.product_name,
                        line.inn,
                        line.strength,
                        line.dosage_form,
                        line.uom,
                        line.units_per_pack,
                        line.pack_description,
                        line.price_per_uom,
                        line.price_per_pack,
                        line.currency,
                        json.dumps(
                            [
                                tier.model_dump()
                                for tier in line.price_tiers
                            ]
                        ),
                        line.moq,
                        line.lead_time_days,
                        line.source_document,
                        line.confidence,
                        line.confidence_level,
                        json.dumps(line.uncertain_fields),
                        json.dumps(line.warnings),
                        json.dumps(
                            [
                                evidence.model_dump()
                                for evidence in line.evidence
                            ]
                        ),
                    ),
                )