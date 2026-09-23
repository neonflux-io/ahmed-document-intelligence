from typing import Any, TypedDict

from app.documents.base import NormalizedDocument
from app.models.quotation import Quotation


class AgentState(TypedDict, total=False):
    """Shared state passed between LangGraph nodes."""

    file_path: str

    document: NormalizedDocument

    quotation: Quotation | None

    errors: list[str]

    warnings: list[str]

    metadata: dict[str, Any]