"""Caso de uso: Listar estudiantes con filtros y paginación."""
import math
from typing import Optional

from src.application.dtos.student_dto import PaginatedStudentsDTO, StudentResponseDTO
from src.domain.ports.student_repository import StudentRepositoryPort


class ListStudentsUseCase:
    """Caso de uso responsable de listar estudiantes con filtrado y paginación."""

    def __init__(self, repository: StudentRepositoryPort):
        self.repository = repository

    def execute(
        self,
        filters: Optional[dict] = None,
        page: int = 1,
        per_page: int = 10,
    ) -> PaginatedStudentsDTO:
        # Normalizar parámetros de paginación
        current_page = max(1, page)
        items_per_page = max(1, min(100, per_page))

        students, total = self.repository.list_all(
            filters=filters or {},
            page=current_page,
            per_page=items_per_page,
        )

        total_pages = math.ceil(total / items_per_page) if total > 0 else 1

        items = [
            StudentResponseDTO(
                id=s.id,
                documento=s.documento,
                nombres=s.nombres,
                apellidos=s.apellidos,
                edad=s.edad,
                telefono=s.telefono,
                email=s.email,
                status=s.status,
            )
            for s in students
        ]

        return PaginatedStudentsDTO(
            items=items,
            total=total,
            page=current_page,
            per_page=items_per_page,
            total_pages=total_pages,
        )
