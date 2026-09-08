"""Punto de entrada principal para ejecutar el servidor Flask."""
import os
import sys

# Asegurar que la raíz del proyecto esté en el PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.application.dtos.student_dto import CreateStudentDTO
from src.application.use_cases.create_student import CreateStudentUseCase
from src.infrastructure.web.app import create_app


NOMBRES_SEED = [
    "Juan", "Carlos", "Andrés", "Alejandro", "Mateo", "Santiago", "Sebastián", "Diego", "Felipe", "Camilo",
    "Daniel", "Nicolás", "David", "Gabriel", "Samuel", "Lucas", "Tomás", "Manuel", "Julián", "Esteban",
    "María", "Camila", "Valentina", "Sofía", "Mariana", "Daniela", "Laura", "Paula", "Lucía", "Isabella",
    "Natalia", "Gabriela", "Andrea", "Carolina", "Sara", "Manuela", "Juliana", "Salomé", "Valeria", "Catalina"
]

APELLIDOS_SEED = [
    "Gómez", "Rodríguez", "Pérez", "González", "García", "Martínez", "López", "Hernández", "Sánchez", "Ramírez",
    "Torres", "Flores", "Díaz", "Vásquez", "Castro", "Morales", "Álvarez", "Romero", "Gutiérrez", "Suárez",
    "Rojas", "Navarro", "Mendoza", "Ortiz", "Silva", "Vargas", "Castillo", "Jiménez", "Moreno", "Ríos",
    "Restrepo", "Ospina", "Cano", "Mejía", "Jaramillo", "Duque", "Valencia", "Cardona", "Herrera", "Zapata"
]


def _clean_accent(text: str) -> str:
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn").lower()


def seed_sample_data(app):
    """Inserta datos de prueba iniciales (250 estudiantes) si la base de datos está vacía."""
    with app.app_context():
        repo = app.config["STUDENT_REPOSITORY"]
        students, total = repo.list_all(page=1, per_page=1)
        if total == 0:
            use_case = CreateStudentUseCase(repo)

            # 1. Registro principal: Samuel Ballesteros
            use_case.execute(
                CreateStudentDTO("1118803077", "Samuel", "Ballesteros", 24, "3104512230", "samuel.ballesteros@example.com", "activo")
            )

            # 2. Generar 249 estudiantes adicionales con datos realistas
            prefixes = ["300", "310", "320", "315", "301", "312", "314", "318"]
            for i in range(2, 251):
                nom = NOMBRES_SEED[(i * 7) % len(NOMBRES_SEED)]
                ape1 = APELLIDOS_SEED[(i * 11) % len(APELLIDOS_SEED)]
                ape2 = APELLIDOS_SEED[(i * 13) % len(APELLIDOS_SEED)]
                doc = f"10{i:08d}"
                edad = 18 + (i % 26)
                tel = f"{prefixes[(i * 3) % len(prefixes)]}{1000000 + (i * 37) % 8999999}"
                email = f"{_clean_accent(nom)}.{_clean_accent(ape1)}.{i}@correo.edu.co"
                status = "activo" if i % 4 != 0 else "inactivo"

                use_case.execute(
                    CreateStudentDTO(doc, nom, f"{ape1} {ape2}", edad, tel, email, status)
                )

            print(f"[INFO] Se insertaron 250 estudiantes iniciales para pruebas realistas de paginación.")


if __name__ == "__main__":
    app = create_app()
    seed_sample_data(app)
    port = int(os.environ.get("PORT", 5000))
    print(f" Servidor iniciado en http://127.0.0.1:{port}")
    print(f" API REST disponible en http://127.0.0.1:{port}/api/v1/students")
    app.run(host="0.0.0.0", port=port, debug=True)
