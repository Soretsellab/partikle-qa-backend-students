"""Controlador de vistas web con plantillas Jinja2 para la gestión de estudiantes."""
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from src.application.dtos.student_dto import CreateStudentDTO, UpdateStudentDTO
from src.application.use_cases.create_student import CreateStudentUseCase
from src.application.use_cases.delete_student import DeleteStudentUseCase
from src.application.use_cases.get_student import GetStudentUseCase
from src.application.use_cases.list_students import ListStudentsUseCase
from src.application.use_cases.update_student import UpdateStudentUseCase
from src.domain.exceptions import (
    DuplicateDocumentoError,
    DuplicateEmailError,
    StudentNotFoundError,
    StudentValidationError,
)

student_view_bp = Blueprint("student_views", __name__)


def _get_repository():
    return current_app.config["STUDENT_REPOSITORY"]


@student_view_bp.route("/", methods=["GET"])
@student_view_bp.route("/students", methods=["GET"])
def index():
    """Página principal con listado, buscador, filtros y paginación."""
    try:
        page = max(1, int(request.args.get("page", 1)))
        per_page = max(1, min(100, int(request.args.get("per_page", 10))))
    except ValueError:
        page, per_page = 1, 10

    search = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()

    filters = {}
    if search:
        filters["search"] = search
    if status in ("activo", "inactivo"):
        filters["status"] = status

    use_case = ListStudentsUseCase(_get_repository())
    paginated = use_case.execute(filters=filters, page=page, per_page=per_page)

    return render_template(
        "students/index.html",
        paginated=paginated,
        search=search,
        status=status,
    )


@student_view_bp.route("/students/create", methods=["POST"])
def create_student():
    """Crear estudiante desde formulario web."""
    documento = request.form.get("documento", "")
    nombres = request.form.get("nombres", "")
    apellidos = request.form.get("apellidos", "")
    edad_raw = request.form.get("edad", "")
    telefono = request.form.get("telefono", "")
    email = request.form.get("email", "")
    status = request.form.get("status", "activo")

    try:
        edad = int(edad_raw)
        dto = CreateStudentDTO(
            documento=documento,
            nombres=nombres,
            apellidos=apellidos,
            edad=edad,
            telefono=telefono,
            email=email,
            status=status,
        )
        use_case = CreateStudentUseCase(_get_repository())
        use_case.execute(dto)
        flash("Estudiante creado con éxito.", "success")
    except (StudentValidationError, DuplicateEmailError, DuplicateDocumentoError, ValueError) as e:
        flash(f"Error al crear estudiante: {str(e)}", "error")

    return redirect(url_for("student_views.index"))


@student_view_bp.route("/students/<int:student_id>/edit", methods=["POST"])
def update_student(student_id: int):
    """Actualizar estudiante desde formulario web."""
    documento = request.form.get("documento")
    nombres = request.form.get("nombres")
    apellidos = request.form.get("apellidos")
    edad_raw = request.form.get("edad")
    telefono = request.form.get("telefono")
    email = request.form.get("email")
    status = request.form.get("status")

    try:
        edad = int(edad_raw) if edad_raw else None
        dto = UpdateStudentDTO(
            id=student_id,
            documento=documento,
            nombres=nombres,
            apellidos=apellidos,
            edad=edad,
            telefono=telefono,
            email=email,
            status=status,
        )
        use_case = UpdateStudentUseCase(_get_repository())
        use_case.execute(dto)
        flash("Estudiante actualizado con éxito.", "success")
    except (StudentValidationError, DuplicateEmailError, DuplicateDocumentoError, StudentNotFoundError, ValueError) as e:
        flash(f"Error al actualizar estudiante: {str(e)}", "error")

    return redirect(url_for("student_views.index"))


@student_view_bp.route("/students/<int:student_id>/delete", methods=["POST"])
def delete_student(student_id: int):
    """Eliminar estudiante desde formulario web."""
    try:
        use_case = DeleteStudentUseCase(_get_repository())
        use_case.execute(student_id)
        flash("Estudiante eliminado correctamente.", "success")
    except StudentNotFoundError as e:
        flash(f"Error al eliminar: {str(e)}", "error")

    return redirect(url_for("student_views.index"))
