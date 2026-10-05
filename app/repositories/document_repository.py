from contextlib import contextmanager
from pathlib import Path
import sqlite3

from app.models.document import Document


class DocumentRepository:
    def __init__(self, database_path):
        self.database_path = Path(database_path)

    def initialize(self):
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    page_count INTEGER NOT NULL,
                    word_count INTEGER NOT NULL,
                    character_count INTEGER NOT NULL,
                    file_size_bytes INTEGER NOT NULL,
                    sha256 TEXT NOT NULL,
                    uploaded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    original_pdf BLOB NOT NULL,
                    extracted_text TEXT NOT NULL
                )
                """
            )

    def add(self, *, filename, extraction, file_size_bytes, sha256, original_pdf):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO documents (
                    filename, subject, summary, page_count, word_count,
                    character_count, file_size_bytes, sha256, original_pdf,
                    extracted_text
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    filename,
                    extraction.subject,
                    extraction.summary,
                    extraction.page_count,
                    extraction.word_count,
                    extraction.character_count,
                    file_size_bytes,
                    sha256,
                    original_pdf,
                    extraction.text,
                ),
            )
            document_id = cursor.lastrowid
        return self.get(document_id)

    def list_recent(self, limit=50):
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM documents ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [self._to_document(row) for row in rows]

    def get(self, document_id):
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM documents WHERE id = ?", (document_id,)
            ).fetchone()
        return self._to_document(row) if row else None

    @contextmanager
    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    @staticmethod
    def _to_document(row):
        return Document(
            id=row["id"],
            filename=row["filename"],
            subject=row["subject"],
            summary=row["summary"],
            page_count=row["page_count"],
            word_count=row["word_count"],
            character_count=row["character_count"],
            file_size_bytes=row["file_size_bytes"],
            sha256=row["sha256"],
            uploaded_at=row["uploaded_at"],
            original_pdf=row["original_pdf"],
            extracted_text=row["extracted_text"],
        )