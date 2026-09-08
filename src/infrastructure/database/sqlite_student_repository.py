"""Adaptador de persistencia: Implementación en SQLite3 del puerto StudentRepositoryPort."""
import sqlite3
from typing import List, Optional, Tuple

from src.domain.entities.student import Student
from src.domain.exceptions import DuplicateDocumentoError, DuplicateEmailError
from src.domain.ports.student_repository import StudentRepositoryPort
from src.infrastructure.database.db_connection import get_connection


class SqliteStudentRepository(StudentRepositoryPort):
    """Repositorio de estudiantes respaldado por SQLite3."""

    def __init__(self, db_path: Optional[str] = None, connection: Optional[sqlite3.Connection] = None):
        self._db_path = db_path
        self._connection = connection

    def _get_conn(self) -> sqlite3.Connection:
        if self._connection is not None:
            return self._connection
        return get_connection(self._db_path)

    def _row_to_entity(self, row: sqlite3.Row) -> Student:
        return Student(
            id=row["id"],
            documento=row["documento"],
            nombres=row["nombres"],
            apellidos=row["apellidos"],
            edad=row["edad"],
            telefono=row["telefono"],
            email=row["email"],
            status=row["status"],
        )

    def save(self, student: Student) -> Student:
        conn = self._get_conn()
        should_close = self._connection is None
        try:
            with conn:
                cursor = conn.execute(
                    """
                    INSERT INTO students (documento, nombres, apellidos, edad, telefono, email, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        student.documento,
                        student.nombres,
                        student.apellidos,
                        student.edad,
                        student.telefono,
                        student.email,
                        student.status,
                    ),
                )
                student.id = cursor.lastrowid
                return student
        except sqlite3.IntegrityError as e:
            err_msg = str(e)
            if "UNIQUE constraint failed: students.documento" in err_msg:
                raise DuplicateDocumentoError(f"Ya existe un estudiante con el documento '{student.documento}'.") from e
            if "UNIQUE constraint failed: students.email" in err_msg:
                raise DuplicateEmailError(f"Ya existe un estudiante con el correo '{student.email}'.") from e
            raise
        finally:
            if should_close:
                conn.close()

    def get_by_id(self, student_id: int) -> Optional[Student]:
        conn = self._get_conn()
        should_close = self._connection is None
        try:
            cursor = conn.execute("SELECT * FROM students WHERE id = ?;", (student_id,))
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None
        finally:
            if should_close:
                conn.close()

    def get_by_email(self, email: str) -> Optional[Student]:
        conn = self._get_conn()
        should_close = self._connection is None
        try:
            cursor = conn.execute(
                "SELECT * FROM students WHERE LOWER(email) = LOWER(?);",
                (email.strip(),),
            )
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None
        finally:
            if should_close:
                conn.close()

    def get_by_documento(self, documento: str) -> Optional[Student]:
        conn = self._get_conn()
        should_close = self._connection is None
        try:
            cursor = conn.execute(
                "SELECT * FROM students WHERE documento = ?;",
                (documento.strip(),),
            )
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None
        finally:
            if should_close:
                conn.close()

    def list_all(
        self,
        filters: Optional[dict] = None,
        page: int = 1,
        per_page: int = 10,
    ) -> Tuple[List[Student], int]:
        filters = filters or {}
        conn = self._get_conn()
        should_close = self._connection is None

        conditions = []
        params: List[object] = []

        # Filtro por estado ('activo' o 'inactivo')
        status = filters.get("status")
        if status and status.strip().lower() in ("activo", "inactivo"):
            conditions.append("status = ?")
            params.append(status.strip().lower())

        # Filtro de búsqueda por texto (en documento, nombres, apellidos o email)
        search = filters.get("search")
        if search and search.strip():
            term = f"%{search.strip()}%"
            conditions.append("(documento LIKE ? OR nombres LIKE ? OR apellidos LIKE ? OR email LIKE ?)")
            params.extend([term, term, term, term])

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        try:
            # 1. Total de registros que cumplen los filtros
            count_query = f"SELECT COUNT(*) AS total FROM students {where_clause};"
            cursor = conn.execute(count_query, params)
            total = cursor.fetchone()["total"]

            # 2. Registros paginados
            offset = (page - 1) * per_page
            select_query = f"""
                SELECT * FROM students
                {where_clause}
                ORDER BY id DESC
                LIMIT ? OFFSET ?;
            """
            cursor = conn.execute(select_query, params + [per_page, offset])
            rows = cursor.fetchall()
            students = [self._row_to_entity(r) for r in rows]

            return students, total
        finally:
            if should_close:
                conn.close()

    def update(self, student: Student) -> Student:
        conn = self._get_conn()
        should_close = self._connection is None
        try:
            with conn:
                conn.execute(
                    """
                    UPDATE students
                    SET documento = ?, nombres = ?, apellidos = ?, edad = ?, telefono = ?, email = ?, status = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?;
                    """,
                    (
                        student.documento,
                        student.nombres,
                        student.apellidos,
                        student.edad,
                        student.telefono,
                        student.email,
                        student.status,
                        student.id,
                    ),
                )
                return student
        except sqlite3.IntegrityError as e:
            err_msg = str(e)
            if "UNIQUE constraint failed: students.documento" in err_msg:
                raise DuplicateDocumentoError(f"Ya existe un estudiante con el documento '{student.documento}'.") from e
            if "UNIQUE constraint failed: students.email" in err_msg:
                raise DuplicateEmailError(f"Ya existe un estudiante con el correo '{student.email}'.") from e
            raise
        finally:
            if should_close:
                conn.close()

    def delete(self, student_id: int) -> bool:
        conn = self._get_conn()
        should_close = self._connection is None
        try:
            with conn:
                cursor = conn.execute("DELETE FROM students WHERE id = ?;", (student_id,))
                return cursor.rowcount > 0
        finally:
            if should_close:
                conn.close()
