from io import BytesIO

import pytest
from pypdf import PdfWriter

from app.services.documents.loaders import pdf_loader
from app.services.documents.loaders.pdf_loader import InvalidPdfError, PdfLoader


class FakePage:
    def __init__(self, text):
        self.text = text

    def extract_text(self):
        return self.text


class FakeReader:
    def __init__(self, _stream, strict=False):
        self.is_encrypted = False
        self.pages = [
            FakePage("Inteligência Artificial Generativa\nConteúdo para professores."),
            FakePage("Aplicações e limitações."),
        ]


def test_load_extracts_text_and_dashboard_metadata(monkeypatch):
    monkeypatch.setattr(pdf_loader, "PdfReader", FakeReader)

    result = PdfLoader().load(b"%PDF-1.4 test")

    assert result.subject == "Inteligência Artificial Generativa"
    assert result.page_count == 2
    assert result.word_count == 9
    assert result.character_count == len(result.text)
    assert "Aplicações e limitações." in result.summary


@pytest.mark.parametrize("pdf_bytes", [b"", b"not a pdf"])
def test_load_rejects_empty_and_malformed_files(pdf_bytes):
    with pytest.raises(InvalidPdfError):
        PdfLoader().load(pdf_bytes)


def test_load_rejects_encrypted_pdf(monkeypatch):
    class EncryptedReader(FakeReader):
        def __init__(self, _stream, strict=False):
            self.is_encrypted = True
            self.pages = []

    monkeypatch.setattr(pdf_loader, "PdfReader", EncryptedReader)

    with pytest.raises(InvalidPdfError, match="protegido por senha"):
        PdfLoader().load(b"%PDF-1.4 encrypted")


def test_load_reads_a_real_pdf_without_extractable_text():
    pdf_buffer = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.write(pdf_buffer)

    result = PdfLoader().load(pdf_buffer.getvalue())

    assert result.page_count == 1
    assert result.word_count == 0
    assert result.subject == "Não identificado"