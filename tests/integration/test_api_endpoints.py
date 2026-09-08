"""Pruebas de integración para la API REST de Estudiantes (/api/v1/students)."""
import pytest


class TestStudentApiEndpoints:
    """Validación exhaustiva de endpoints HTTP REST."""

    def test_create_student_success(self, client):
        payload = {
            "nombres": "Mateo",
            "apellidos": "Guzmán",
            "edad": 22,
            "telefono": "+573012345678",
            "email": "mateo.guzman@example.com",
            "status": "activo",
        }
        res = client.post("/api/v1/students", json=payload)
        assert res.status_code == 201
        data = res.get_json()
        assert data["success"] is True
        assert data["data"]["id"] is not None
        assert data["data"]["nombres"] == "Mateo"
        assert data["data"]["email"] == "mateo.guzman@example.com"

    def test_create_student_missing_fields_fails(self, client):
        payload = {"nombres": "Mateo"}
        res = client.post("/api/v1/students", json=payload)
        assert res.status_code == 400
        data = res.get_json()
        assert data["success"] is False
        assert "Campos requeridos faltantes" in data["error"]

    def test_create_student_invalid_body_fails(self, client):
        res = client.post("/api/v1/students", data="not json", content_type="text/plain")
        assert res.status_code == 400
        data = res.get_json()
        assert data["success"] is False

    def test_create_student_validation_error_invalid_email(self, client):
        payload = {
            "nombres": "Mateo",
            "apellidos": "Guzmán",
            "edad": 22,
            "telefono": "+573012345678",
            "email": "invalido-sin-arroba",
            "status": "activo",
        }
        res = client.post("/api/v1/students", json=payload)
        assert res.status_code == 400
        assert res.get_json()["success"] is False

    def test_create_student_duplicate_email_conflict(self, client):
        payload = {
            "nombres": "Mateo",
            "apellidos": "Guzmán",
            "edad": 22,
            "telefono": "+573012345678",
            "email": "duplicado@example.com",
            "status": "activo",
        }
        res1 = client.post("/api/v1/students", json=payload)
        assert res1.status_code == 201

        res2 = client.post("/api/v1/students", json=payload)
        assert res2.status_code == 409
        data = res2.get_json()
        assert data["success"] is False
        assert "Ya existe un estudiante" in data["error"]

    def test_get_student_by_id_success(self, client):
        create_res = client.post(
            "/api/v1/students",
            json={
                "nombres": "Lucía",
                "apellidos": "Torres",
                "edad": 21,
                "telefono": "3001112233",
                "email": "lucia.torres@example.com",
            },
        )
        student_id = create_res.get_json()["data"]["id"]

        get_res = client.get(f"/api/v1/students/{student_id}")
        assert get_res.status_code == 200
        assert get_res.get_json()["data"]["nombres"] == "Lucía"

    def test_get_student_by_id_not_found(self, client):
        res = client.get("/api/v1/students/99999")
        assert res.status_code == 404
        assert res.get_json()["success"] is False

    def test_list_students_paginated_and_filtered(self, client):
        # Insertar 3 estudiantes
        for i in range(1, 4):
            client.post(
                "/api/v1/students",
                json={
                    "nombres": f"Alumno {i}",
                    "apellidos": f"Test {i}",
                    "edad": 20 + i,
                    "telefono": f"300000000{i}",
                    "email": f"alumno{i}@example.com",
                    "status": "activo" if i <= 2 else "inactivo",
                },
            )

        # Listar activos
        res = client.get("/api/v1/students?status=activo&per_page=10")
        assert res.status_code == 200
        data = res.get_json()["data"]
        assert data["total"] == 2
        assert len(data["items"]) == 2

        # Búsqueda por texto
        res_search = client.get("/api/v1/students?search=Alumno 3")
        assert res_search.status_code == 200
        data_search = res_search.get_json()["data"]
        assert data_search["total"] == 1
        assert data_search["items"][0]["nombres"] == "Alumno 3"

    def test_list_students_invalid_query_params(self, client):
        res = client.get("/api/v1/students?page=abc")
        assert res.status_code == 400
        assert res.get_json()["success"] is False

    def test_update_student_success(self, client):
        create_res = client.post(
            "/api/v1/students",
            json={
                "nombres": "Camilo",
                "apellidos": "Sesto",
                "edad": 24,
                "telefono": "3004445566",
                "email": "camilo@example.com",
                "status": "activo",
            },
        )
        student_id = create_res.get_json()["data"]["id"]

        update_res = client.put(
            f"/api/v1/students/{student_id}",
            json={"edad": 25, "status": "inactivo"},
        )
        assert update_res.status_code == 200
        data = update_res.get_json()["data"]
        assert data["edad"] == 25
        assert data["status"] == "inactivo"
        assert data["nombres"] == "Camilo"

    def test_update_student_not_found(self, client):
        res = client.put("/api/v1/students/9999", json={"edad": 30})
        assert res.status_code == 404

    def test_update_student_validation_error(self, client):
        create_res = client.post(
            "/api/v1/students",
            json={
                "nombres": "Rosa",
                "apellidos": "Díaz",
                "edad": 20,
                "telefono": "3001112233",
                "email": "rosa@example.com",
            },
        )
        student_id = create_res.get_json()["data"]["id"]

        update_res = client.put(f"/api/v1/students/{student_id}", json={"edad": -10})
        assert update_res.status_code == 400

    def test_delete_student_success(self, client):
        create_res = client.post(
            "/api/v1/students",
            json={
                "nombres": "Para",
                "apellidos": "Borrar",
                "edad": 20,
                "telefono": "3001112233",
                "email": "borrar.api@example.com",
            },
        )
        student_id = create_res.get_json()["data"]["id"]

        delete_res = client.delete(f"/api/v1/students/{student_id}")
        assert delete_res.status_code == 200

        # Verificar que ya no existe
        get_res = client.get(f"/api/v1/students/{student_id}")
        assert get_res.status_code == 404

    def test_delete_student_not_found(self, client):
        res = client.delete("/api/v1/students/9999")
        assert res.status_code == 404

    def test_update_student_invalid_body_fails(self, client):
        res = client.put("/api/v1/students/1", data="not json", content_type="text/plain")
        assert res.status_code == 400

    def test_update_student_invalid_age_string(self, client):
        res = client.put("/api/v1/students/1", json={"edad": "invalido"})
        assert res.status_code == 400

    def test_update_student_duplicate_email_conflict(self, client):
        # Crear estudiante 1
        client.post("/api/v1/students", json={
            "nombres": "E1", "apellidos": "A1", "edad": 20, "telefono": "3001111111", "email": "e1@test.com"
        })
        # Crear estudiante 2
        res2 = client.post("/api/v1/students", json={
            "nombres": "E2", "apellidos": "A2", "edad": 20, "telefono": "3002222222", "email": "e2@test.com"
        })
        id2 = res2.get_json()["data"]["id"]

        # Intentar poner a estudiante 2 el email de estudiante 1
        res_update = client.put(f"/api/v1/students/{id2}", json={"email": "e1@test.com"})
        assert res_update.status_code == 409

    def test_not_found_handlers(self, client):
        api_res = client.get("/api/v1/ruta-inexistente")
        assert api_res.status_code == 404
        assert api_res.get_json()["success"] is False

        web_res = client.get("/ruta-web-inexistente")
        assert web_res.status_code == 404

