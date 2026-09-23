from typing import Any
from pydantic import BaseModel, Field


class Evidence(BaseModel):
    field: str
    value: Any
    source_document: str
    location: str | None = None
    extraction_method: str | None = None
    evidence_type: str = "stated"
    supersedes_value: Any | None = None
    notes: str | None = None

class PriceTier(BaseModel):
    min_quantity: int | None = None
    max_quantity: int | None = None
    price: float
    currency: str
    price_basis: str

class QuotationLine(BaseModel):
    product_name: str | None = None
    inn: str | None = None
    strength: str | None = None
    dosage_form: str | None = None

    uom: str | None = None
    units_per_pack: float | None = None
    pack_description: str | None = None

    price_per_uom: float | None = None
    price_per_uom_basis: str | None = None

    price_per_pack: float | None = None
    price_per_pack_basis: str | None = None

    currency: str | None = None

    price_tiers: list[PriceTier] = Field(default_factory=list)

    moq: float | None = None
    lead_time_days: int | None = None

    source_document: str

    confidence: float = 0.0
    confidence_level: str = "low"

    uncertain_fields: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    requires_human_review: bool = False
    evidence: list[Evidence] = Field(default_factory=list)


class Quotation(BaseModel):
    quotation_id: str
    supplier: str | None = None
    quotation_date: str | None = None
    currency: str | None = None

    lines: list[QuotationLine] = Field(default_factory=list)

    source_document: str

    confidence: float = 0.0
    confidence_level: str = "low"

    warnings: list[str] = Field(default_factory=list)