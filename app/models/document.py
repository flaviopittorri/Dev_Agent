from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Document:
    id: int
    filename: str
    subject: str
    summary: str
    page_count: int
    word_count: int
    character_count: int
    file_size_bytes: int
    sha256: str
    uploaded_at: str
    original_pdf: bytes = field(repr=False)
    extracted_text: str = field(repr=False)

    def to_metadata_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "subject": self.subject,
            "summary": self.summary,
            "page_count": self.page_count,
            "word_count": self.word_count,
            "character_count": self.character_count,
            "file_size_bytes": self.file_size_bytes,
            "sha256": self.sha256,
            "uploaded_at": self.uploaded_at,
        }