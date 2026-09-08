"""Controlador REST API para la gestión de estudiantes."""
from flask import Blueprint, current_app, jsonify, request

from src.application.dtos.student_dto import CreateStudentDTO, UpdateStudentDTO
from src.application.use_cases.create_student import CreateStudentUseCase
from src.application.use_cases.delete_student import DeleteStudentUseCase
from src.application.use_cases.get_student import GetStudentUseCase
from src.application.use_cases.list_students import ListStudentsUseCase
from src.application.use_cases.update_student import UpdateStudentUseCase
from src.domain.exceptions import DuplicateEmailError, StudentNotFoundError, StudentValidationError

student_api_bp = Blueprint("student_api", __name__, url_prefix="/api/v1/students")


def _get_repository():
    return current_app.config["STUDENT_REPOSITORY"]


@student_api_bp.route("", methods=["GET"])
def list_students():
    """Listar estudiantes con filtros y paginación."""
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
    except ValueError:
        return jsonify({"success": False, "error": "Los parámetros 'page' y 'per_page' deben ser enteros."}), 400

    filters = {
        "status": request.args.get("status"),
        "search": request.args.get("search"),
    }

    use_case = ListStudentsUseCase(_get_repository())
    result = use_case.execute(filters=filters, page=page, per_page=per_page)

    return jsonify({"success": True, "data": result.to_dict()}), 200


@student_api_bp.route("/<int:student_id>", methods=["GET"])
def get_student(student_id: int):
    """Consultar un estudiante por ID."""
    use_case = GetStudentUseCase(_get_repository())
    try:
        result = use_case.execute(student_id)
        return jsonify({"success": True, "data": result.to_dict()}), 200
    except StudentNotFoundError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@student_api_bp.route("", methods=["POST"])
def create_student():
    """Crear un nuevo estudiante."""
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return jsonify({"success": False, "error": "Cuerpo de solicitud inválido o ausente (se espera formato JSON)."}), 400

    required_fields = ["nombres", "apellidos", "edad", "telefono", "email"]
    missing = [field for field in required_fields if field not in body]
    if missing:
        return jsonify({"success": False, "error": f"Campos requeridos faltantes: {', '.join(missing)}"}), 400

    try:
        dto = CreateStudentDTO(
            nombres=str(body.get("nombres", "")),
            apellidos=str(body.get("apellidos", "")),
            edad=int(body.get("edad")) if body.get("edad") is not None else -1,
            telefono=str(body.get("telefono", "")),
            email=str(body.get("email", "")),
            status=str(body.get("status", "activo")),
        )
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "El campo 'edad' debe ser un número entero válido."}), 400

    use_case = CreateStudentUseCase(_get_repository())
    try:
        result = use_case.execute(dto)
        return jsonify({
            "success": True,
            "message": "Estudiante registrado exitosamente.",
            "data": result.to_dict(),
        }), 201
    except StudentValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except DuplicateEmailError as e:
        return jsonify({"success": False, "error": str(e)}), 409


@student_api_bp.route("/<int:student_id>", methods=["PUT"])
def update_student(student_id: int):
    """Actualizar un estudiante existente."""
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return jsonify({"success": False, "error": "Cuerpo de solicitud inválido o ausente (se espera formato JSON)."}), 400

    edad_val = None
    if "edad" in body:
        try:
            edad_val = int(body["edad"])
        except (ValueError, TypeError):
            return jsonify({"success": False, "error": "El campo 'edad' debe ser un número entero válido."}), 400

    dto = UpdateStudentDTO(
        id=student_id,
        nombres=body.get("nombres"),
        apellidos=body.get("apellidos"),
        edad=edad_val,
        telefono=body.get("telefono"),
        email=body.get("email"),
        status=body.get("status"),
    )

    use_case = UpdateStudentUseCase(_get_repository())
    try:
        result = use_case.execute(dto)
        return jsonify({
            "success": True,
            "message": "Estudiante actualizado exitosamente.",
            "data": result.to_dict(),
        }), 200
    except StudentNotFoundError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except StudentValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except DuplicateEmailError as e:
        return jsonify({"success": False, "error": str(e)}), 409


@student_api_bp.route("/<int:student_id>", methods=["DELETE"])
def delete_student(student_id: int):
    """Eliminar un estudiante por ID."""
    use_case = DeleteStudentUseCase(_get_repository())
    try:
        use_case.execute(student_id)
        return jsonify({"success": True, "message": f"Estudiante con ID {student_id} eliminado exitosamente."}), 200
    except StudentNotFoundError as e:
        return jsonify({"success": False, "error": str(e)}), 404
