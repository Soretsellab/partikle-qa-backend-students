"""Data Transfer Objects (DTOs) para la capa de aplicación."""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class CreateStudentDTO:
    nombres: str
    apellidos: str
    edad: int
    telefono: str
    email: str
    status: str = "activo"


@dataclass
class UpdateStudentDTO:
    id: int
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    edad: Optional[int] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None


@dataclass
class StudentResponseDTO:
    id: int
    nombres: str
    apellidos: str
    edad: int
    telefono: str
    email: str
    status: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "edad": self.edad,
            "telefono": self.telefono,
            "email": self.email,
            "status": self.status,
        }


@dataclass
class PaginatedStudentsDTO:
    items: List[StudentResponseDTO]
    total: int
    page: int
    per_page: int
    total_pages: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "items": [item.to_dict() for item in self.items],
            "total": self.total,
            "page": self.page,
            "per_page": self.per_page,
            "total_pages": self.total_pages,
            "has_next": self.page < self.total_pages,
            "has_prev": self.page > 1,
        }
