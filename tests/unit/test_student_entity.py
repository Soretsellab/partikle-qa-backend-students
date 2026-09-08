"""Pruebas unitarias para la entidad de dominio Student y sus invariantes de negocio."""
import pytest

from src.domain.entities.student import Student
from src.domain.exceptions import StudentValidationError


class TestStudentEntity:
    """Suite de pruebas unitarias sobre reglas de negocio del Estudiante."""

    def test_create_valid_student_success(self):
        """Verifica la creación exitosa de un estudiante con atributos válidos."""
        student = Student(
            documento="  1118803077  ",
            nombres="  Carlos Alberto  ",
            apellidos="  Pérez López  ",
            edad=25,
            telefono="+573112345678",
            email="  CARLOS.PEREZ@example.com  ",
            status="activo",
        )
        assert student.documento == "1118803077"
        assert student.nombres == "Carlos Alberto"
        assert student.apellidos == "Pérez López"
        assert student.edad == 25
        assert student.telefono == "+573112345678"
        assert student.email == "carlos.perez@example.com"
        assert student.status == "activo"
        assert student.id is None

    @pytest.mark.parametrize(
        "empty_doc",
        ["", "   ", None],
    )
    def test_documento_empty_raises_validation_error(self, empty_doc):
        """Debe fallar si el documento está vacío o es nulo."""
        with pytest.raises(StudentValidationError, match="El campo 'documento' es obligatorio"):
            Student(
                documento=empty_doc,  # type: ignore
                nombres="Carlos",
                apellidos="Pérez",
                edad=20,
                telefono="3001234567",
                email="test@example.com",
            )

    @pytest.mark.parametrize(
        "invalid_doc",
        ["123", "ab", "doc@invalid!", "1" * 25, "12 34 56"],
    )
    def test_documento_invalid_format_raises_validation_error(self, invalid_doc):
        """Debe fallar si el documento no tiene formato alfanumérico entre 6 y 20 caracteres."""
        with pytest.raises(StudentValidationError, match="entre 6 y 20 caracteres"):
            Student(
                documento=invalid_doc,
                nombres="Carlos",
                apellidos="Pérez",
                edad=20,
                telefono="3001234567",
                email="test@example.com",
            )

    @pytest.mark.parametrize(
        "empty_names",
        ["", "   ", None],
    )
    def test_nombres_empty_raises_validation_error(self, empty_names):
        """Debe fallar si los nombres están vacíos o son solo espacios."""
        with pytest.raises(StudentValidationError, match="El campo 'nombres' es obligatorio"):
            Student(
                documento="1118803077",
                nombres=empty_names,  # type: ignore
                apellidos="Pérez",
                edad=20,
                telefono="3001234567",
                email="test@example.com",
            )

    @pytest.mark.parametrize(
        "empty_apellidos",
        ["", "   ", None],
    )
    def test_apellidos_empty_raises_validation_error(self, empty_apellidos):
        """Debe fallar si los apellidos están vacíos."""
        with pytest.raises(StudentValidationError, match="El campo 'apellidos' es obligatorio"):
            Student(
                documento="1118803077",
                nombres="Carlos",
                apellidos=empty_apellidos,  # type: ignore
                edad=20,
                telefono="3001234567",
                email="test@example.com",
            )

    @pytest.mark.parametrize(
        "invalid_age",
        [0, -5, -1, 121, 200],
    )
    def test_invalid_age_raises_validation_error(self, invalid_age):
        """Debe fallar si la edad es menor o igual a 0 o mayor a 120."""
        with pytest.raises(StudentValidationError, match="La edad debe ser un número positivo coherente"):
            Student(
                documento="1118803077",
                nombres="Carlos",
                apellidos="Pérez",
                edad=invalid_age,
                telefono="3001234567",
                email="test@example.com",
            )

    @pytest.mark.parametrize(
        "invalid_type_age",
        ["veinte", True, 20.5, None],
    )
    def test_invalid_age_type_raises_validation_error(self, invalid_type_age):
        """Debe fallar si la edad no es estrictamente un número entero."""
        with pytest.raises(StudentValidationError, match="El campo 'edad' debe ser un número entero"):
            Student(
                documento="1118803077",
                nombres="Carlos",
                apellidos="Pérez",
                edad=invalid_type_age,  # type: ignore
                telefono="3001234567",
                email="test@example.com",
            )

    @pytest.mark.parametrize(
        "invalid_phone",
        ["123", "abc", "tel-12345", "", "  "],
    )
    def test_invalid_phone_raises_validation_error(self, invalid_phone):
        """Debe fallar si el formato del teléfono no contiene longitud y caracteres válidos."""
        with pytest.raises(StudentValidationError):
            Student(
                documento="1118803077",
                nombres="Carlos",
                apellidos="Pérez",
                edad=20,
                telefono=invalid_phone,
                email="test@example.com",
            )

    @pytest.mark.parametrize(
        "invalid_email",
        ["correo_sin_arroba", "@sinusuario.com", "usuario@", "usuario@dominio", "usuario@.com", "", "   "],
    )
    def test_invalid_email_raises_validation_error(self, invalid_email):
        """Debe fallar si el formato del correo no es válido."""
        with pytest.raises(StudentValidationError):
            Student(
                documento="1118803077",
                nombres="Carlos",
                apellidos="Pérez",
                edad=20,
                telefono="3001234567",
                email=invalid_email,
            )

    @pytest.mark.parametrize(
        "invalid_status",
        ["pendiente", "eliminado", "activo_temporal", "suspendido", "", "123"],
    )
    def test_invalid_status_raises_validation_error(self, invalid_status):
        """Debe fallar si el estado no es 'activo' o 'inactivo'."""
        with pytest.raises(StudentValidationError, match="El campo 'status' debe ser exactamente"):
            Student(
                documento="1118803077",
                nombres="Carlos",
                apellidos="Pérez",
                edad=20,
                telefono="3001234567",
                email="test@example.com",
                status=invalid_status,
            )

    def test_to_dict_serialization(self):
        """Verifica la correcta conversión de la entidad a diccionario."""
        student = Student(
            id=1,
            documento="1118803077",
            nombres="Laura",
            apellidos="Restrepo",
            edad=22,
            telefono="+573009998877",
            email="laura@example.com",
            status="inactivo",
        )
        data = student.to_dict()
        assert data == {
            "id": 1,
            "documento": "1118803077",
            "nombres": "Laura",
            "apellidos": "Restrepo",
            "edad": 22,
            "telefono": "+573009998877",
            "email": "laura@example.com",
            "status": "inactivo",
        }
