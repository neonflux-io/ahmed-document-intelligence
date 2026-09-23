from email import policy
from email.parser import BytesParser
from pathlib import Path

from bs4 import BeautifulSoup

from app.documents.adapters import DocumentAdapter
from app.documents.base import NormalizedDocument


class EmailDocumentAdapter(DocumentAdapter):
    """Adapter for .eml email documents."""

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() == ".eml"

    def parse(self, path: Path) -> NormalizedDocument:
        with path.open("rb") as file:
            message = BytesParser(policy=policy.default).parse(file)

        parts: list[str] = []

        subject = message.get("subject")
        sender = message.get("from")
        recipient = message.get("to")

        if subject:
            parts.append(f"Subject: {subject}")

        if sender:
            parts.append(f"From: {sender}")

        if recipient:
            parts.append(f"To: {recipient}")

        body = self._extract_body(message)

        if body:
            parts.append(body)

        raw_text = "\n\n".join(parts)

        warnings: list[str] = []

        if not body.strip():
            warnings.append("No email body text could be extracted.")

        return NormalizedDocument(
            source_document=path.name,
            document_type="email",
            raw_text=raw_text,
            metadata={
                "subject": subject,
                "from": sender,
                "to": recipient,
            },
            extraction_warnings=warnings,
        )

    def _extract_body(self, message) -> str:
        """Extract readable text from plain-text or HTML email bodies."""

        if message.is_multipart():
            plain_text: list[str] = []
            html_text: list[str] = []

            for part in message.walk():
                content_type = part.get_content_type()

                if content_type == "text/plain":
                    content = part.get_content()
                    if content.strip():
                        plain_text.append(content)

                elif content_type == "text/html":
                    content = part.get_content()
                    if content.strip():
                        html_text.append(content)

            if plain_text:
                return "\n\n".join(plain_text)

            if html_text:
                return "\n\n".join(
                    BeautifulSoup(html, "html.parser").get_text(
                        "\n", strip=True
                    )
                    for html in html_text
                )

            return ""

        content_type = message.get_content_type()
        content = message.get_content()

        if content_type == "text/html":
            return BeautifulSoup(
                content,
                "html.parser",
            ).get_text("\n", strip=True)

        return content