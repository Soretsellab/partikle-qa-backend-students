"""Punto de entrada principal para ejecutar el servidor Flask."""
import os
import sys

# Asegurar que la raíz del proyecto esté en el PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.application.dtos.student_dto import CreateStudentDTO
from src.application.use_cases.create_student import CreateStudentUseCase
from src.infrastructure.web.app import create_app


def seed_sample_data(app):
    """Inserta datos de prueba iniciales si la base de datos está vacía."""
    with app.app_context():
        repo = app.config["STUDENT_REPOSITORY"]
        students, total = repo.list_all(page=1, per_page=1)
        if total == 0:
            samples = [
                CreateStudentDTO("1118803077", "Samuel", "Ballesteros", 24, "3104512230", "samuel.ballesteros@example.com", "activo"),
                CreateStudentDTO("1017283940", "Juan Carlos", "Pérez Gómez", 22, "+573001234568", "juan.perez@example.com", "activo"),
                CreateStudentDTO("1028394051", "María Alejandra", "Gómez López", 24, "+573109876543", "maria.gomez@example.com", "activo"),
                CreateStudentDTO("1039405162", "Carlos Andrés", "Rodríguez Ruiz", 26, "+573204567890", "carlos.rodriguez@example.com", "inactivo"),
                CreateStudentDTO("1040516273", "Ana Sofía", "Martínez Castro", 21, "+573155551234", "ana.martinez@example.com", "activo"),
                CreateStudentDTO("1051627384", "Diego Fernando", "Morales Toro", 23, "+573178889900", "diego.morales@example.com", "activo"),
                CreateStudentDTO("1062738495", "Laura Camila", "Valencia Díaz", 20, "+573187776655", "laura.valencia@example.com", "inactivo"),
                CreateStudentDTO("1073849506", "Sebastián", "Herrera Cano", 25, "+573012223344", "sebastian.herrera@example.com", "activo"),
                CreateStudentDTO("1084950617", "Valentina", "Ospina Ríos", 22, "+573114445566", "valentina.ospina@example.com", "activo"),
            ]
            use_case = CreateStudentUseCase(repo)
            for sample in samples:
                use_case.execute(sample)
            print("[INFO] Datos iniciales de demostración insertados con éxito.")


if __name__ == "__main__":
    app = create_app()
    seed_sample_data(app)
    port = int(os.environ.get("PORT", 5000))
    print(f" Servidor iniciado en http://127.0.0.1:{port}")
    print(f" API REST disponible en http://127.0.0.1:{port}/api/v1/students")
    app.run(host="0.0.0.0", port=port, debug=True)
