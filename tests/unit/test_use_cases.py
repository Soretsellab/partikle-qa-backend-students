"""Pruebas unitarias para los casos de uso de la capa de aplicación."""
from unittest.mock import MagicMock
import pytest

from src.application.dtos.student_dto import CreateStudentDTO, UpdateStudentDTO
from src.application.use_cases.create_student import CreateStudentUseCase
from src.application.use_cases.delete_student import DeleteStudentUseCase
from src.application.use_cases.get_student import GetStudentUseCase
from src.application.use_cases.list_students import ListStudentsUseCase
from src.application.use_cases.update_student import UpdateStudentUseCase
from src.domain.entities.student import Student
from src.domain.exceptions import (
    DuplicateDocumentoError,
    DuplicateEmailError,
    StudentNotFoundError,
    StudentValidationError,
)
from src.domain.ports.student_repository import StudentRepositoryPort


class TestCreateStudentUseCase:
    """Pruebas del caso de uso de registro de estudiantes."""

    def test_create_student_success(self):
        mock_repo = MagicMock(spec=StudentRepositoryPort)
        mock_repo.get_by_documento.return_value = None
        mock_repo.get_by_email.return_value = None

        def fake_save(student):
            student.id = 1
            return student

        mock_repo.save.side_effect = fake_save

        use_case = CreateStudentUseCase(mock_repo)
        dto = CreateStudentDTO("1118803077", "Carlos", "Gómez", 20, "3001234567", "carlos@example.com", "activo")
        result = use_case.execute(dto)

        assert result.id == 1
        assert result.documento == "1118803077"
        assert result.nombres == "Carlos"
        assert result.email == "carlos@example.com"
        mock_repo.get_by_documento.assert_called_once_with("1118803077")
        mock_repo.get_by_email.assert_called_once_with("carlos@example.com")
        mock_repo.save.assert_called_once()

    def test_create_student_duplicate_documento_raises_error(self):
        mock_repo = MagicMock(spec=StudentRepositoryPort)
        existing_student = Student(id=1, documento="1118803077", nombres="Existe", apellidos="Ya", edad=25, telefono="3001234567", email="otro@example.com")
        mock_repo.get_by_documento.return_value = existing_student

        use_case = CreateStudentUseCase(mock_repo)
        dto = CreateStudentDTO("1118803077", "Carlos", "Gómez", 20, "3001234567", "carlos@example.com", "activo")

        with pytest.raises(DuplicateDocumentoError, match="Ya existe un estudiante registrado con el documento"):
            use_case.execute(dto)

        mock_repo.save.assert_not_called()

    def test_create_student_duplicate_email_raises_error(self):
        mock_repo = MagicMock(spec=StudentRepositoryPort)
        mock_repo.get_by_documento.return_value = None
        existing_student = Student(id=1, documento="1017283940", nombres="Existe", apellidos="Ya", edad=25, telefono="3001234567", email="carlos@example.com")
        mock_repo.get_by_email.return_value = existing_student

        use_case = CreateStudentUseCase(mock_repo)
        dto = CreateStudentDTO("1118803077", "Carlos", "Gómez", 20, "3001234567", "carlos@example.com", "activo")

        with pytest.raises(DuplicateEmailError, match="Ya existe un estudiante registrado con el correo"):
            use_case.execute(dto)

        mock_repo.save.assert_not_called()


class TestGetStudentUseCase:
    """Pruebas del caso de uso de consulta de estudiante."""

    def test_get_student_success(self):
        mock_repo = MagicMock(spec=StudentRepositoryPort)
        student = Student(id=5, documento="1118803077", nombres="Marta", apellidos="López", edad=21, telefono="3101234567", email="marta@example.com")
        mock_repo.get_by_id.return_value = student

        use_case = GetStudentUseCase(mock_repo)
        result = use_case.execute(5)

        assert result.id == 5
        assert result.documento == "1118803077"
        assert result.nombres == "Marta"
        mock_repo.get_by_id.assert_called_once_with(5)

    def test_get_student_not_found_raises_error(self):
        mock_repo = MagicMock(spec=StudentRepositoryPort)
        mock_repo.get_by_id.return_value = None

        use_case = GetStudentUseCase(mock_repo)
        with pytest.raises(StudentNotFoundError, match="Estudiante con ID 99 no encontrado"):
            use_case.execute(99)


class TestListStudentsUseCase:
    """Pruebas del caso de uso de listado con paginación y filtros."""

    def test_list_students_paginated(self):
        mock_repo = MagicMock(spec=StudentRepositoryPort)
        students = [
            Student(id=1, documento="1118803077", nombres="A", apellidos="B", edad=20, telefono="3001234567", email="a@a.com"),
            Student(id=2, documento="1028394051", nombres="C", apellidos="D", edad=22, telefono="3007654321", email="c@c.com"),
        ]
        mock_repo.list_all.return_value = (students, 15)

        use_case = ListStudentsUseCase(mock_repo)
        result = use_case.execute(filters={"status": "activo"}, page=2, per_page=2)

        assert result.page == 2
        assert result.per_page == 2
        assert result.total == 15
        assert result.total_pages == 8
        assert len(result.items) == 2
        assert result.items[0].id == 1
        assert result.items[0].documento == "1118803077"
        assert result.to_dict()["has_next"] is True
        assert result.to_dict()["has_prev"] is True

    def test_list_students_empty(self):
        mock_repo = MagicMock(spec=StudentRepositoryPort)
        mock_repo.list_all.return_value = ([], 0)

        use_case = ListStudentsUseCase(mock_repo)
        result = use_case.execute()

        assert result.total == 0
        assert result.total_pages == 1
        assert len(result.items) == 0


class TestUpdateStudentUseCase:
    """Pruebas del caso de uso de actualización de estudiante."""

    def test_update_student_success(self):
        mock_repo = MagicMock(spec=StudentRepositoryPort)
        original = Student(id=1, documento="1118803077", nombres="Juan", apellidos="Pérez", edad=20, telefono="3001234567", email="juan@example.com", status="activo")
        mock_repo.get_by_id.return_value = original
        mock_repo.get_by_documento.return_value = None
        mock_repo.get_by_email.return_value = None
        mock_repo.update.side_effect = lambda s: s

        use_case = UpdateStudentUseCase(mock_repo)
        dto = UpdateStudentDTO(id=1, edad=21, status="inactivo")
        result = use_case.execute(dto)

        assert result.edad == 21
        assert result.status == "inactivo"
        assert result.nombres == "Juan"
        assert result.documento == "1118803077"
        mock_repo.update.assert_called_once()

    def test_update_student_not_found(self):
        mock_repo = MagicMock(spec=StudentRepositoryPort)
        mock_repo.get_by_id.return_value = None

        use_case = UpdateStudentUseCase(mock_repo)
        dto = UpdateStudentDTO(id=42, edad=25)

        with pytest.raises(StudentNotFoundError):
            use_case.execute(dto)

    def test_update_student_documento_conflict(self):
        mock_repo = MagicMock(spec=StudentRepositoryPort)
        original = Student(id=1, documento="1118803077", nombres="Juan", apellidos="Pérez", edad=20, telefono="3001234567", email="juan@example.com")
        another = Student(id=2, documento="9998887776", nombres="Carlos", apellidos="Ruiz", edad=22, telefono="3101234567", email="carlos@example.com")
        mock_repo.get_by_id.return_value = original
        mock_repo.get_by_documento.return_value = another

        use_case = UpdateStudentUseCase(mock_repo)
        dto = UpdateStudentDTO(id=1, documento="9998887776")

        with pytest.raises(DuplicateDocumentoError, match="Ya existe un estudiante registrado con el documento"):
            use_case.execute(dto)

    def test_update_student_email_conflict(self):
        mock_repo = MagicMock(spec=StudentRepositoryPort)
        original = Student(id=1, documento="1118803077", nombres="Juan", apellidos="Pérez", edad=20, telefono="3001234567", email="juan@example.com")
        another = Student(id=2, documento="9998887776", nombres="María", apellidos="Gómez", edad=22, telefono="3101234567", email="maria@example.com")
        mock_repo.get_by_id.return_value = original
        mock_repo.get_by_email.return_value = another

        use_case = UpdateStudentUseCase(mock_repo)
        dto = UpdateStudentDTO(id=1, email="maria@example.com")

        with pytest.raises(DuplicateEmailError, match="Ya existe un estudiante registrado"):
            use_case.execute(dto)


class TestDeleteStudentUseCase:
    """Pruebas del caso de uso de eliminación."""

    def test_delete_student_success(self):
        mock_repo = MagicMock(spec=StudentRepositoryPort)
        student = Student(id=3, documento="1118803077", nombres="Andrés", apellidos="Diaz", edad=24, telefono="3001112233", email="andres@test.com")
        mock_repo.get_by_id.return_value = student
        mock_repo.delete.return_value = True

        use_case = DeleteStudentUseCase(mock_repo)
        result = use_case.execute(3)

        assert result is True
        mock_repo.delete.assert_called_once_with(3)

    def test_delete_student_not_found(self):
        mock_repo = MagicMock(spec=StudentRepositoryPort)
        mock_repo.get_by_id.return_value = None

        use_case = DeleteStudentUseCase(mock_repo)
        with pytest.raises(StudentNotFoundError):
            use_case.execute(99)
