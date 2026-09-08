"""Entidad de Dominio: Student."""
from dataclasses import dataclass
import re
from typing import Optional

from src.domain.exceptions import StudentValidationError

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
PHONE_REGEX = re.compile(r"^\+?[0-9\s\-()]{7,20}$")
VALID_STATUSES = {"activo", "inactivo"}


@dataclass
class Student:
    """Entidad que representa a un estudiante en el sistema."""
    nombres: str
    apellidos: str
    edad: int
    telefono: str
    email: str
    status: str = "activo"
    id: Optional[int] = None

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Valida las reglas de negocio e invariantes del estudiante."""
        if not self.nombres or not self.nombres.strip():
            raise StudentValidationError("El campo 'nombres' es obligatorio y no puede estar vacío.")
        self.nombres = self.nombres.strip()

        if not self.apellidos or not self.apellidos.strip():
            raise StudentValidationError("El campo 'apellidos' es obligatorio y no puede estar vacío.")
        self.apellidos = self.apellidos.strip()

        if not isinstance(self.edad, int) or isinstance(self.edad, bool):
            raise StudentValidationError("El campo 'edad' debe ser un número entero.")
        if self.edad <= 0 or self.edad > 120:
            raise StudentValidationError("La edad debe ser un número positivo coherente (entre 1 y 120 años).")

        if not self.telefono or not self.telefono.strip():
            raise StudentValidationError("El campo 'telefono' es obligatorio.")
        self.telefono = self.telefono.strip()
        if not PHONE_REGEX.match(self.telefono):
            raise StudentValidationError("El formato del teléfono es inválido. Debe contener entre 7 y 20 dígitos.")

        if not self.email or not self.email.strip():
            raise StudentValidationError("El campo 'email' es obligatorio.")
        self.email = self.email.strip().lower()
        if not EMAIL_REGEX.match(self.email):
            raise StudentValidationError(f"El correo '{self.email}' no tiene un formato válido.")

        if not self.status or self.status.strip().lower() not in VALID_STATUSES:
            raise StudentValidationError("El campo 'status' debe ser exactamente 'activo' o 'inactivo'.")
        self.status = self.status.strip().lower()

    def to_dict(self) -> dict:
        """Convierte la entidad a un diccionario serializable."""
        return {
            "id": self.id,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "edad": self.edad,
            "telefono": self.telefono,
            "email": self.email,
            "status": self.status,
        }
