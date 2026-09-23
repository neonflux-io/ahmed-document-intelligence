from abc import ABC, abstractmethod
from pathlib import Path

from app.documents.base import NormalizedDocument


class DocumentAdapter(ABC):
    """Base interface for all document format adapters."""

    @abstractmethod
    def supports(self, path: Path) -> bool:
        """Return True if this adapter can process the given file."""
        raise NotImplementedError

    @abstractmethod
    def parse(self, path: Path) -> NormalizedDocument:
        """Convert the source document into our common format."""
        raise NotImplementedError