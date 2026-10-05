from flask import Blueprint, current_app, jsonify, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from app.services.documents.document_service import (
    DocumentIngestionError,
    FileTooLargeError,
)

document_blueprint = Blueprint("documents", __name__)


@document_blueprint.get("/")
def dashboard():
    return _render_dashboard()


@document_blueprint.get("/api/documents")
def list_documents():
    documents = _document_service().repository.list_recent()
    return jsonify(documents=[document.to_metadata_dict() for document in documents])


@document_blueprint.post("/documents")
@document_blueprint.post("/api/documents")
def upload_document():
    uploaded_file = request.files.get("file")
    filename = secure_filename(uploaded_file.filename) if uploaded_file else ""
    if not filename:
        return _upload_error("Selecione um arquivo PDF.", 400)

    try:
        document = _document_service().ingest(
            filename=filename,
            pdf_bytes=uploaded_file.read(),
        )
    except FileTooLargeError as error:
        return _upload_error(str(error), 413)
    except DocumentIngestionError as error:
        return _upload_error(str(error), 400)

    if _is_api_request():
        return jsonify(document=document.to_metadata_dict()), 201
    return redirect(url_for("documents.dashboard"))


@document_blueprint.get("/api/documents/<int:document_id>")
def get_document(document_id):
    document = _document_service().repository.get(document_id)
    if document is None:
        return jsonify(error="Documento não encontrado."), 404
    return jsonify(document=document.to_metadata_dict())


def _document_service():
    return current_app.extensions["document_service"]


def _is_api_request():
    return request.path.startswith("/api/")


def _upload_error(message, status_code):
    if _is_api_request():
        return jsonify(error=message), status_code
    return _render_dashboard(error=message), status_code


def _render_dashboard(error=None):
    documents = _document_service().repository.list_recent()
    return render_template(
        "dashboard.html",
        documents=documents,
        error=error,
        database_path=str(current_app.config["DATABASE_PATH"]),
        total_pages=sum(document.page_count for document in documents),
        total_words=sum(document.word_count for document in documents),
    )