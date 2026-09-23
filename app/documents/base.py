from typing import Any

from pydantic import BaseModel, Field


class ExtractedTable(BaseModel):
    headers: list[str] = Field(default_factory=list)
    rows: list[list[Any]] = Field(default_factory=list)


class NormalizedDocument(BaseModel):
    source_document: str
    document_type: str

    raw_text: str = ""

    tables: list[ExtractedTable] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    extraction_warnings: list[str] = Field(default_factory=list)