import hashlib

from app.services.documents.loaders.pdf_loader import InvalidPdfError


class DocumentIngestionError(ValueError):
    """Raised when an uploaded document violates ingestion rules."""


class FileTooLargeError(DocumentIngestionError):
    """Raised when a PDF exceeds the configured size limit."""


class UnsupportedFileTypeError(DocumentIngestionError):
    """Raised when the uploaded file is not a PDF."""


class DocumentService:
    def __init__(self, *, repository, pdf_loader, max_pdf_size_bytes):
        self.repository = repository
        self.pdf_loader = pdf_loader
        self.max_pdf_size_bytes = max_pdf_size_bytes

    def ingest(self, *, filename, pdf_bytes):
        if not filename or not filename.lower().endswith(".pdf"):
            raise UnsupportedFileTypeError("Envie um arquivo com extensão .pdf.")
        if len(pdf_bytes) > self.max_pdf_size_bytes:
            raise FileTooLargeError("O PDF excede o limite configurado de tamanho.")

        try:
            extraction = self.pdf_loader.load(pdf_bytes)
        except InvalidPdfError as error:
            raise DocumentIngestionError(str(error)) from error

        return self.repository.add(
            filename=filename,
            extraction=extraction,
            file_size_bytes=len(pdf_bytes),
            sha256=hashlib.sha256(pdf_bytes).hexdigest(),
            original_pdf=pdf_bytes,
        )