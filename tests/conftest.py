"""Configuración global y fixtures para la suite de pruebas pytest."""
import os
import sqlite3
import tempfile
import pytest

from src.application.dtos.student_dto import CreateStudentDTO
from src.application.use_cases.create_student import CreateStudentUseCase
from src.domain.entities.student import Student
from src.infrastructure.database.db_connection import init_db
from src.infrastructure.database.sqlite_student_repository import SqliteStudentRepository
from src.infrastructure.web.app import create_app


@pytest.fixture
def temp_db():
    """Crea una base de datos SQLite temporal en disco para pruebas aisladas."""
    fd, path = tempfile.mkstemp(suffix=".sqlite3")
    os.close(fd)
    init_db(path)
    yield path
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def sqlite_repo(temp_db):
    """Instancia del repositorio SQLite conectado a la base de datos de pruebas."""
    return SqliteStudentRepository(db_path=temp_db)


@pytest.fixture
def app(sqlite_repo):
    """Instancia de la aplicación Flask configurada para el entorno de pruebas."""
    application = create_app(
        repository=sqlite_repo,
        test_config={
            "TESTING": True,
            "SECRET_KEY": "test-secret-key",
        },
    )
    return application


@pytest.fixture
def client(app):
    """Cliente de pruebas HTTP de Flask."""
    return app.test_client()


@pytest.fixture
def sample_student_dto():
    """DTO de estudiante válido para pruebas."""
    return CreateStudentDTO(
        nombres="Ana María",
        apellidos="Gómez Restrepo",
        edad=23,
        telefono="+573001234567",
        email="ana.gomez@test.com",
        status="activo",
    )


@pytest.fixture
def seeded_repo(sqlite_repo, sample_student_dto):
    """Repositorio pre-poblado con un estudiante de prueba."""
    use_case = CreateStudentUseCase(sqlite_repo)
    use_case.execute(sample_student_dto)
    return sqlite_repo
