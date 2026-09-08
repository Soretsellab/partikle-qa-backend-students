"""Pruebas de integración para las vistas HTML con plantillas Jinja2."""
import pytest


class TestStudentViewEndpoints:
    """Validación de las rutas web y renderizado de plantillas."""

    def test_index_view_renders_ok(self, client):
        res = client.get("/")
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Directorio de Estudiantes" in html
        assert "Partikle Academy" in html
        assert "Documento" in html

    def test_create_student_via_form_redirects_and_renders(self, client):
        form_data = {
            "documento": "1118803077",
            "nombres": "Estudiante",
            "apellidos": "Formulario",
            "edad": "23",
            "telefono": "+573009990011",
            "email": "form.student@example.com",
            "status": "activo",
        }
        res = client.post("/students/create", data=form_data, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Estudiante creado con éxito." in html
        assert "Estudiante Formulario" in html
        assert "1118803077" in html

    def test_create_student_via_form_invalid_shows_flash_error(self, client):
        form_data = {
            "documento": "1118803077",
            "nombres": "Estudiante",
            "apellidos": "Invalido",
            "edad": "-5",
            "telefono": "123",
            "email": "not-an-email",
            "status": "activo",
        }
        res = client.post("/students/create", data=form_data, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Error al crear estudiante:" in html

    def test_create_student_via_form_duplicate_documento_shows_flash_error(self, client):
        form_data1 = {
            "documento": "1118803077",
            "nombres": "Estudiante Uno",
            "apellidos": "Formulario",
            "edad": "23",
            "telefono": "+573009990011",
            "email": "form.uno@example.com",
            "status": "activo",
        }
        client.post("/students/create", data=form_data1, follow_redirects=True)

        form_data2 = {
            "documento": "1118803077",
            "nombres": "Estudiante Dos",
            "apellidos": "Formulario",
            "edad": "24",
            "telefono": "+573009990012",
            "email": "form.dos@example.com",
            "status": "activo",
        }
        res = client.post("/students/create", data=form_data2, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Ya existe un estudiante registrado con el documento" in html

    def test_edit_student_via_form_redirects_and_updates(self, client):
        # Crear primero vía API
        create_res = client.post(
            "/api/v1/students",
            json={
                "documento": "1118803077",
                "nombres": "Original",
                "apellidos": "Nombre",
                "edad": 20,
                "telefono": "3001112233",
                "email": "edit.view@example.com",
            },
        )
        student_id = create_res.get_json()["data"]["id"]

        # Enviar formulario de edición
        update_data = {
            "documento": "1118803999",
            "nombres": "Modificado",
            "apellidos": "Nombre",
            "edad": "25",
            "telefono": "3001112233",
            "email": "edit.view@example.com",
            "status": "inactivo",
        }
        res = client.post(f"/students/{student_id}/edit", data=update_data, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Estudiante actualizado con éxito." in html
        assert "Modificado Nombre" in html
        assert "1118803999" in html

    def test_delete_student_via_form_redirects(self, client):
        # Crear primero vía API
        create_res = client.post(
            "/api/v1/students",
            json={
                "documento": "1118803077",
                "nombres": "Eliminar",
                "apellidos": "Vista",
                "edad": 22,
                "telefono": "3001112233",
                "email": "delete.view@example.com",
            },
        )
        student_id = create_res.get_json()["data"]["id"]

        # Enviar POST de eliminación
        res = client.post(f"/students/{student_id}/delete", follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Estudiante eliminado correctamente." in html

    def test_view_filter_and_pagination(self, client):
        res = client.get("/students?search=test&status=activo&page=1&per_page=5")
        assert res.status_code == 200

    def test_view_invalid_pagination_params_fallback(self, client):
        res = client.get("/students?page=invalido&per_page=otro")
        assert res.status_code == 200

    def test_view_edit_non_existent_student_shows_error(self, client):
        res = client.post("/students/99999/edit", data={"documento": "1118803077", "nombres": "X", "edad": "20"}, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Error al actualizar estudiante:" in html

    def test_view_delete_non_existent_student_shows_error(self, client):
        res = client.post("/students/99999/delete", follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Error al eliminar:" in html

