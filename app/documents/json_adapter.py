import json
from pathlib import Path
from typing import Any

from app.documents.adapters import DocumentAdapter
from app.documents.base import NormalizedDocument


class JSONDocumentAdapter(DocumentAdapter):
    """Adapter for generic JSON quotation documents."""

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() == ".json"

    def parse(self, path: Path) -> NormalizedDocument:
        with path.open("r", encoding="utf-8") as file:
            data: Any = json.load(file)

        raw_text = json.dumps(data, indent=2, ensure_ascii=False)

        metadata = self._extract_metadata(data)

        return NormalizedDocument(
            source_document=path.name,
            document_type="json",
            raw_text=raw_text,
            metadata=metadata,
        )

    def _extract_metadata(self, data: Any) -> dict[str, Any]:
        """Extract useful top-level metadata without assuming a supplier schema."""

        if not isinstance(data, dict):
            return {}

        metadata: dict[str, Any] = {}

        for key, value in data.items():
            if isinstance(value, (str, int, float, bool)):
                metadata[key] = value

        return metadata