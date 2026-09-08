"""Pruebas de integración para el adaptador SqliteStudentRepository."""
import pytest

from src.domain.entities.student import Student
from src.domain.exceptions import DuplicateEmailError
from src.infrastructure.database.sqlite_student_repository import SqliteStudentRepository


class TestSqliteStudentRepository:
    """Pruebas sobre operaciones de base de datos con SQLite3."""

    def test_save_and_get_by_id(self, sqlite_repo: SqliteStudentRepository):
        student = Student(
            nombres="Pedro",
            apellidos="Alvarado",
            edad=21,
            telefono="+573100000000",
            email="pedro@test.com",
            status="activo",
        )
        saved = sqlite_repo.save(student)
        assert saved.id is not None

        retrieved = sqlite_repo.get_by_id(saved.id)
        assert retrieved is not None
        assert retrieved.id == saved.id
        assert retrieved.nombres == "Pedro"
        assert retrieved.email == "pedro@test.com"

    def test_save_duplicate_email_raises_duplicate_email_error(self, sqlite_repo: SqliteStudentRepository):
        s1 = Student(nombres="Pedro", apellidos="A", edad=21, telefono="3100000000", email="repeat@test.com")
        s2 = Student(nombres="Pablo", apellidos="B", edad=22, telefono="3100000001", email="repeat@test.com")
        sqlite_repo.save(s1)

        with pytest.raises(DuplicateEmailError):
            sqlite_repo.save(s2)

    def test_get_by_email_case_insensitive(self, sqlite_repo: SqliteStudentRepository):
        student = Student(nombres="Lucía", apellidos="Méndez", edad=24, telefono="3150000000", email="lucia@test.com")
        sqlite_repo.save(student)

        found = sqlite_repo.get_by_email("LUCIA@TEST.COM")
        assert found is not None
        assert found.email == "lucia@test.com"

    def test_list_all_with_filters_and_pagination(self, sqlite_repo: SqliteStudentRepository):
        # Insertar varios estudiantes
        for i in range(1, 11):
            sqlite_repo.save(
                Student(
                    nombres=f"Estudiante {i}",
                    apellidos=f"Apellido {i}",
                    edad=20 + i,
                    telefono=f"30010000{i:02d}",
                    email=f"estudiante{i}@test.com",
                    status="activo" if i % 2 == 0 else "inactivo",
                )
            )

        # 1. Paginación
        items_page1, total = sqlite_repo.list_all(page=1, per_page=4)
        assert total == 10
        assert len(items_page1) == 4

        items_page3, _ = sqlite_repo.list_all(page=3, per_page=4)
        assert len(items_page3) == 2

        # 2. Filtro por status
        activos, total_activos = sqlite_repo.list_all(filters={"status": "activo"}, page=1, per_page=10)
        assert total_activos == 5
        assert all(s.status == "activo" for s in activos)

        # 3. Filtro por búsqueda textual
        search_res, total_search = sqlite_repo.list_all(filters={"search": "Estudiante 10"})
        assert total_search == 1
        assert search_res[0].nombres == "Estudiante 10"

    def test_update_student(self, sqlite_repo: SqliteStudentRepository):
        student = sqlite_repo.save(
            Student(nombres="Felipe", apellidos="Ríos", edad=23, telefono="3102223344", email="felipe@test.com")
        )
        student.edad = 25
        student.status = "inactivo"
        student.nombres = "Felipe Andrés"

        updated = sqlite_repo.update(student)
        assert updated.edad == 25
        assert updated.status == "inactivo"

        reloaded = sqlite_repo.get_by_id(student.id)
        assert reloaded.nombres == "Felipe Andrés"
        assert reloaded.edad == 25
        assert reloaded.status == "inactivo"

    def test_delete_student(self, sqlite_repo: SqliteStudentRepository):
        student = sqlite_repo.save(
            Student(nombres="Borrar", apellidos="Me", edad=20, telefono="3000000000", email="borrame@test.com")
        )
        assert sqlite_repo.delete(student.id) is True
        assert sqlite_repo.get_by_id(student.id) is None
        assert sqlite_repo.delete(student.id) is False
