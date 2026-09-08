"""Caso de uso: Crear un nuevo estudiante."""
from src.application.dtos.student_dto import CreateStudentDTO, StudentResponseDTO
from src.domain.entities.student import Student
from src.domain.exceptions import DuplicateEmailError
from src.domain.ports.student_repository import StudentRepositoryPort


class CreateStudentUseCase:
    """Caso de uso responsable de registrar un nuevo estudiante."""

    def __init__(self, repository: StudentRepositoryPort):
        self.repository = repository

    def execute(self, dto: CreateStudentDTO) -> StudentResponseDTO:
        # Verificar unicidad del email
        normalized_email = dto.email.strip().lower() if dto.email else ""
        existing = self.repository.get_by_email(normalized_email)
        if existing:
            raise DuplicateEmailError(f"Ya existe un estudiante registrado con el correo '{normalized_email}'.")

        # Crear entidad de dominio (las validaciones de negocio ocurren aquí)
        student = Student(
            nombres=dto.nombres,
            apellidos=dto.apellidos,
            edad=dto.edad,
            telefono=dto.telefono,
            email=dto.email,
            status=dto.status,
        )

        saved = self.repository.save(student)

        return StudentResponseDTO(
            id=saved.id,
            nombres=saved.nombres,
            apellidos=saved.apellidos,
            edad=saved.edad,
            telefono=saved.telefono,
            email=saved.email,
            status=saved.status,
        )
