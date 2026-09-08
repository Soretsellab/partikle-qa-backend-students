"""Caso de uso: Eliminar un estudiante por ID."""
from src.domain.exceptions import StudentNotFoundError
from src.domain.ports.student_repository import StudentRepositoryPort


class DeleteStudentUseCase:
    """Caso de uso responsable de eliminar un estudiante del sistema."""

    def __init__(self, repository: StudentRepositoryPort):
        self.repository = repository

    def execute(self, student_id: int) -> bool:
        existing = self.repository.get_by_id(student_id)
        if not existing:
            raise StudentNotFoundError(f"Estudiante con ID {student_id} no encontrado.")

        return self.repository.delete(student_id)
