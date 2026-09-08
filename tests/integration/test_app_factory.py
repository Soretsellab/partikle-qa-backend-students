"""Pruebas para la factoría de aplicaciones y configuración por defecto."""
import os
import tempfile
import pytest

from src.infrastructure.web.app import create_app
from run import seed_sample_data


def test_create_app_default():
    """Verifica que create_app funcione con la base de datos por defecto o archivo temporal."""
    fd, path = tempfile.mkstemp(suffix=".sqlite3")
    os.close(fd)
    try:
        app = create_app(test_config={"TESTING": True, "DB_PATH": path})
        assert app is not None
        assert "STUDENT_REPOSITORY" in app.config
        # Ejecutar seed sobre la app recién creada
        seed_sample_data(app)
        # Segunda ejecución no debe duplicar datos
        seed_sample_data(app)
    finally:
        if os.path.exists(path):
            os.remove(path)
