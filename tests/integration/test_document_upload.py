import sqlite3
from io import BytesIO

import pytest
from pypdf.errors import PdfReadError

from app import create_app
from app.services.documents.loaders import pdf_loader


class FakePage:
    def extract_text(self):
        return "Inteligência Artificial Generativa\nModelos podem apoiar a criação de conteúdo didático."


class FakeReader:
    def __init__(self, stream, strict=False):
        if not stream.read().startswith(b"%PDF-"):
            raise PdfReadError("Invalid PDF header")
        self.is_encrypted = False
        self.pages = [FakePage()]


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(pdf_loader, "PdfReader", FakeReader)
    app = create_app(
        {
            "TESTING": True,
            "DATABASE_PATH": tmp_path / "documents.db",
            "MAX_PDF_SIZE_BYTES": 100,
            "MAX_CONTENT_LENGTH": 1024,
        }
    )
    return app.test_client(), tmp_path / "documents.db"


def test_upload_persists_pdf_and_dashboard_shows_document(client):
    test_client, database_path = client
    original_pdf = b"%PDF-1.4 sample document"

    response = test_client.post(
        "/api/documents",
        data={"file": (BytesIO(original_pdf), "generative-ai.pdf")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 201
    metadata = response.json["document"]
    assert metadata["filename"] == "generative-ai.pdf"
    assert metadata["subject"] == "Inteligência Artificial Generativa"
    assert metadata["page_count"] == 1
    assert metadata["word_count"] == 11
    assert metadata["file_size_bytes"] == len(original_pdf)

    with sqlite3.connect(database_path) as connection:
        stored_pdf, extracted_text = connection.execute(
            "SELECT original_pdf, extracted_text FROM documents WHERE id = ?",
            (metadata["id"],),
        ).fetchone()
    assert stored_pdf == original_pdf
    assert "criação de conteúdo didático" in extracted_text

    dashboard = test_client.get("/")
    assert dashboard.status_code == 200
    assert b"generative-ai.pdf" in dashboard.data
    assert "Inteligência Artificial Generativa" in dashboard.get_data(as_text=True)
    assert b"SQLite" in dashboard.data


@pytest.mark.parametrize(
    ("filename", "pdf_bytes", "expected_status"),
    [
        ("notes.txt", b"plain text", 400),
        ("broken.pdf", b"not a pdf", 400),
        ("large.pdf", b"x" * 101, 413),
    ],
)
def test_upload_rejects_unsupported_invalid_and_oversized_files(
    client, filename, pdf_bytes, expected_status
):
    test_client, database_path = client

    response = test_client.post(
        "/api/documents",
        data={"file": (BytesIO(pdf_bytes), filename)},
        content_type="multipart/form-data",
    )

    assert response.status_code == expected_status
    with sqlite3.connect(database_path) as connection:
        document_count = connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    assert document_count == 0


def test_html_upload_redirects_to_dashboard(client):
    test_client, _database_path = client

    response = test_client.post(
        "/documents",
        data={"file": (BytesIO(b"%PDF-1.4 sample"), "aula.pdf")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")