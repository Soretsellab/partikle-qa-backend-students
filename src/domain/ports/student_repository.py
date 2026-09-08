"""Puerto secundario (SPI): Contrato de persistencia para Estudiantes."""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from src.domain.entities.student import Student


class StudentRepositoryPort(ABC):
    """Interfaz abstracta que define las operaciones de persistencia de Student."""

    @abstractmethod
    def save(self, student: Student) -> Student:
        """Persiste un nuevo estudiante y retorna la entidad con su ID asignado."""
        pass  # pragma: no cover

    @abstractmethod
    def get_by_id(self, student_id: int) -> Optional[Student]:
        """Obtiene un estudiante por su ID único."""
        pass  # pragma: no cover

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Student]:
        """Obtiene un estudiante por su dirección de correo electrónico."""
        pass  # pragma: no cover

    @abstractmethod
    def get_by_documento(self, documento: str) -> Optional[Student]:
        """Obtiene un estudiante por su documento de identidad único."""
        pass  # pragma: no cover


    @abstractmethod
    def list_all(
        self,
        filters: Optional[dict] = None,
        page: int = 1,
        per_page: int = 10,
    ) -> Tuple[List[Student], int]:
        """Lista estudiantes aplicando filtros opcionales y paginación.

        Retorna una tupla con la lista de estudiantes de la página actual y el total general.
        """
        pass  # pragma: no cover

    @abstractmethod
    def update(self, student: Student) -> Student:
        """Actualiza la información de un estudiante existente."""
        pass  # pragma: no cover

    @abstractmethod
    def delete(self, student_id: int) -> bool:
        """Elimina un estudiante por su ID único. Retorna True si fue eliminado."""
        pass  # pragma: no cover

