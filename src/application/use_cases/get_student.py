"""Caso de uso: Consultar un estudiante por ID."""
from src.application.dtos.student_dto import StudentResponseDTO
from src.domain.exceptions import StudentNotFoundError
from src.domain.ports.student_repository import StudentRepositoryPort


class GetStudentUseCase:
    """Caso de uso responsable de obtener la información de un estudiante por su ID."""

    def __init__(self, repository: StudentRepositoryPort):
        self.repository = repository

    def execute(self, student_id: int) -> StudentResponseDTO:
        student = self.repository.get_by_id(student_id)
        if not student:
            raise StudentNotFoundError(f"Estudiante con ID {student_id} no encontrado.")

        return StudentResponseDTO(
            id=student.id,
            documento=student.documento,
            nombres=student.nombres,
            apellidos=student.apellidos,
            edad=student.edad,
            telefono=student.telefono,
            email=student.email,
            status=student.status,
        )
