"""Application Factory para Flask con inyección de dependencias."""
import os
from typing import Optional

from flask import Flask, jsonify

from src.domain.ports.student_repository import StudentRepositoryPort
from src.infrastructure.database.db_connection import init_db
from src.infrastructure.database.sqlite_student_repository import SqliteStudentRepository
from src.infrastructure.web.controllers.student_api_controller import student_api_bp
from src.infrastructure.web.controllers.student_view_controller import student_view_bp


def create_app(
    repository: Optional[StudentRepositoryPort] = None,
    test_config: Optional[dict] = None,
) -> Flask:
    """Crea y configura una instancia de la aplicación Flask."""
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    )

    # Configuración base
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "partikle-qa-secret-key-2026"),
        DB_PATH=os.environ.get("DB_PATH", None),
    )

    if test_config:
        app.config.update(test_config)

    # Inyección de dependencias (Repository Port)
    if repository is not None:
        app.config["STUDENT_REPOSITORY"] = repository
    else:
        db_path = app.config.get("DB_PATH")
        init_db(db_path)
        app.config["STUDENT_REPOSITORY"] = SqliteStudentRepository(db_path=db_path)

    # Registro de Blueprints
    app.register_blueprint(student_api_bp)
    app.register_blueprint(student_view_bp)

    # Manejador global de 404 para API
    @app.errorhandler(404)
    def handle_404(e):
        from flask import request
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "error": "Recurso no encontrado."}), 404
        return "Página no encontrada", 404

    # Manejador global de 500 para API
    @app.errorhandler(500)
    def handle_500(e):
        from flask import request
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "error": "Error interno del servidor."}), 500
        return "Error interno del servidor", 500

    return app
