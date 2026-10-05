from dataclasses import dataclass
from io import BytesIO
import re

from pypdf import PdfReader
from pypdf.errors import PdfReadError, PdfStreamError


class InvalidPdfError(ValueError):
    """Raised when a PDF cannot be read safely."""


@dataclass(frozen=True, slots=True)
class PdfExtraction:
    text: str
    page_count: int
    word_count: int
    character_count: int
    subject: str
    summary: str


class PdfLoader:
    SUMMARY_MAX_LENGTH = 360
    SUBJECT_MAX_LENGTH = 120

    def load(self, pdf_bytes):
        if not pdf_bytes:
            raise InvalidPdfError("O arquivo PDF está vazio.")

        try:
            reader = PdfReader(BytesIO(pdf_bytes), strict=False)
            if reader.is_encrypted:
                raise InvalidPdfError("PDF protegido por senha não é suportado.")
            page_texts = [page.extract_text() or "" for page in reader.pages]
        except InvalidPdfError:
            raise
        except (PdfReadError, PdfStreamError, ValueError, OSError) as error:
            raise InvalidPdfError("Não foi possível ler o PDF enviado.") from error

        text = "\n".join(page_texts).strip()
        words = re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE)
        paragraphs = [" ".join(line.split()) for line in text.splitlines() if line.strip()]
        subject = paragraphs[0][: self.SUBJECT_MAX_LENGTH] if paragraphs else "Não identificado"
        summary = " ".join(paragraphs[:3]) or "O PDF não contém texto extraível."
        if len(summary) > self.SUMMARY_MAX_LENGTH:
            summary = summary[: self.SUMMARY_MAX_LENGTH - 3].rstrip() + "..."

        return PdfExtraction(
            text=text,
            page_count=len(reader.pages),
            word_count=len(words),
            character_count=len(text),
            subject=subject,
            summary=summary,
        )