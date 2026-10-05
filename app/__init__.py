import os
from pathlib import Path

from flask import Flask, request
from werkzeug.exceptions import RequestEntityTooLarge

from app.controllers.document_controller import document_blueprint
from app.repositories.document_repository import DocumentRepository
from app.services.documents.document_service import DocumentService
from app.services.documents.loaders.pdf_loader import PdfLoader

DEFAULT_MAX_PDF_SIZE_BYTES = 20 * 1024 * 1024


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE_PATH=os.environ.get("DATABASE_PATH", "generated/documents.db"),
        MAX_PDF_SIZE_BYTES=DEFAULT_MAX_PDF_SIZE_BYTES,
        MAX_CONTENT_LENGTH=DEFAULT_MAX_PDF_SIZE_BYTES + 64 * 1024,
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", "local-development-only"),
    )
    if test_config:
        app.config.update(test_config)

    repository = DocumentRepository(Path(app.config["DATABASE_PATH"]))
    repository.initialize()
    app.extensions["document_service"] = DocumentService(
        repository=repository,
        pdf_loader=PdfLoader(),
        max_pdf_size_bytes=app.config["MAX_PDF_SIZE_BYTES"],
    )
    app.register_blueprint(document_blueprint)

    @app.errorhandler(RequestEntityTooLarge)
    def handle_request_too_large(_error):
        if request.path.startswith("/api/"):
            return {"error": "O upload excede o limite permitido."}, 413
        return "O upload excede o limite permitido.", 413

    return app