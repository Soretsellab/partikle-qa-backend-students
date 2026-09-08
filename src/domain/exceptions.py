"""Excepciones de dominio para la gestión de estudiantes."""


class DomainException(Exception):
    """Excepción base para errores de reglas de negocio en el dominio."""
    pass


class StudentValidationError(DomainException):
    """Lanzada cuando uno o varios atributos del estudiante no cumplen las reglas de negocio."""
    pass


class StudentNotFoundError(DomainException):
    """Lanzada cuando no se encuentra un estudiante por su identificador."""
    pass


class DuplicateEmailError(DomainException):
    """Lanzada cuando se intenta registrar o actualizar un estudiante con un correo ya existente."""
    pass
