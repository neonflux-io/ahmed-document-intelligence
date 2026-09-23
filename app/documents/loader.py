from pathlib import Path

from app.documents.adapters import DocumentAdapter
from app.documents.base import NormalizedDocument
from app.documents.registry import get_default_adapters


class DocumentLoader:
    """Selects the appropriate adapter for an input document."""

    def __init__(
        self,
        adapters: list[DocumentAdapter] | None = None,
    ) -> None:
        self.adapters = (
            adapters
            if adapters is not None
            else get_default_adapters()
        )

    def load(self, path: Path) -> NormalizedDocument:
        for adapter in self.adapters:
            if adapter.supports(path):
                return adapter.parse(path)

        raise ValueError(
            f"Unsupported document type: {path.suffix}"
        )