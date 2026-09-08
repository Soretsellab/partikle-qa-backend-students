"""Caso de uso: Actualizar un estudiante existente."""
from src.application.dtos.student_dto import StudentResponseDTO, UpdateStudentDTO
from src.domain.entities.student import Student
from src.domain.exceptions import DuplicateEmailError, StudentNotFoundError
from src.domain.ports.student_repository import StudentRepositoryPort


class UpdateStudentUseCase:
    """Caso de uso responsable de actualizar la información de un estudiante."""

    def __init__(self, repository: StudentRepositoryPort):
        self.repository = repository

    def execute(self, dto: UpdateStudentDTO) -> StudentResponseDTO:
        existing = self.repository.get_by_id(dto.id)
        if not existing:
            raise StudentNotFoundError(f"Estudiante con ID {dto.id} no encontrado.")

        # Si se actualiza el correo, comprobar que no esté en uso por otro estudiante
        new_email = dto.email.strip().lower() if dto.email is not None else existing.email
        if new_email != existing.email:
            other = self.repository.get_by_email(new_email)
            if other and other.id != existing.id:
                raise DuplicateEmailError(f"Ya existe un estudiante registrado con el correo '{new_email}'.")

        # Construir nueva entidad con campos actualizados o existentes
        updated_student = Student(
            id=existing.id,
            nombres=dto.nombres if dto.nombres is not None else existing.nombres,
            apellidos=dto.apellidos if dto.apellidos is not None else existing.apellidos,
            edad=dto.edad if dto.edad is not None else existing.edad,
            telefono=dto.telefono if dto.telefono is not None else existing.telefono,
            email=new_email,
            status=dto.status if dto.status is not None else existing.status,
        )

        saved = self.repository.update(updated_student)

        return StudentResponseDTO(
            id=saved.id,
            nombres=saved.nombres,
            apellidos=saved.apellidos,
            edad=saved.edad,
            telefono=saved.telefono,
            email=saved.email,
            status=saved.status,
        )
