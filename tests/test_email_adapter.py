from pathlib import Path

from app.documents.email_adapter import EmailDocumentAdapter


def test_email_adapter_reads_email():
    email_path = Path("data/test/sample_quotation.eml")

    email_content = """From: supplier@example.com
To: buyer@example.com
Subject: Quotation - Test Pharma

Dear Buyer,

Please find our quotation below.

Product: Testamol 500
INN: Paracetamol
Price: 0.05 USD per tablet

Regards,
Test Pharma
"""

    email_path.write_text(
        email_content,
        encoding="utf-8",
    )

    adapter = EmailDocumentAdapter()

    assert adapter.supports(email_path)

    result = adapter.parse(email_path)

    assert result.source_document == "sample_quotation.eml"
    assert result.document_type == "email"
    assert "Testamol 500" in result.raw_text
    assert "Paracetamol" in result.raw_text
    assert "0.05 USD" in result.raw_text