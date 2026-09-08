# Sistema de Registro de Estudiantes — Prueba Técnica Python QA Backend

Solución desarrollada por Samuel Ballesteros para la prueba técnica de Partikle.

Implementé una API REST y un panel web con Flask para la gestión de estudiantes, organizando el código bajo una arquitectura limpia / hexagonal (puertos y adaptadores). Para la persistencia utilicé SQLite3 nativo sin ORMs pesados, plantillas HTML con Jinja2 y Tailwind CSS para la interfaz, y una suite de pruebas con Pytest para asegurar la calidad de todo el flujo.

---

## Contenido del Repositorio

- `TEORIA.md`: Mis respuestas a las 5 preguntas teóricas de la Parte 1.
- `src/domain`: Entidades con sus reglas de validación, excepciones de negocio y la interfaz del repositorio (`StudentRepositoryPort`), sin dependencias de Flask ni SQLite.
- `src/application`: Casos de uso (crear, consultar, listar con paginación/filtros, actualizar y eliminar) y objetos de transferencia de datos (DTOs).
- `src/infrastructure`: Adaptador de base de datos con SQLite3 y adaptador web con Flask (controladores REST y vistas Jinja2).
- `tests/`: Pruebas unitarias y de integración realizadas con Pytest.
- `run.py`: Punto de entrada de la aplicación con datos iniciales de prueba.

---

## Arquitectura del Proyecto

Decidí estructurar el proyecto separando la lógica de negocio de los detalles técnicos y librerías externas:

```text
Entrevista/
├── TEORIA.md                  # Parte 1: Respuestas teóricas
├── README.md                  # Documentación del proyecto
├── requirements.txt           # Dependencias necesarias
├── pytest.ini                 # Configuración de pytest
├── run.py                     # Inicialización del servidor y datos iniciales
├── src/
│   ├── domain/                # Reglas de negocio puras
│   │   ├── entities/          # Entidad Student con validaciones
│   │   ├── exceptions.py      # Excepciones propias del dominio
│   │   └── ports/             # Interfaz del repositorio
│   ├── application/           # Casos de uso y DTOs
│   │   ├── dtos/              # Objetos para mover datos entre capas
│   │   └── use_cases/         # Lógica de cada operación (Create, Get, List, Update, Delete)
│   └── infrastructure/        # Adaptadores externos
│       ├── database/          # Conexión y consultas SQLite3
│       └── web/               # Controladores Flask (API REST y vistas Jinja2)
│           └── templates/     # Plantillas HTML
└── tests/                     # Suite de pruebas
    ├── conftest.py            # Fixtures y base de datos temporal
    ├── unit/                  # Pruebas unitarias de entidades y casos de uso
    └── integration/           # Pruebas de integración de la base de datos, API y vistas
```

### Campos del Estudiante

En la entidad de dominio definí y validé los siguientes datos:
- `id`: Entero autoincremental que uso como identificador técnico en la base de datos.
- `documento`: Cédula o documento de identidad único (entre 6 y 20 caracteres alfanuméricos). Es la clave de negocio principal.
- `nombres`: Texto obligatorio.
- `apellidos`: Texto obligatorio.
- `edad`: Entero entre 1 y 120 años.
- `telefono`: Entre 7 y 20 dígitos numéricos.
- `email`: Correo electrónico único con formato válido.
- `status`: Estado del estudiante, únicamente 'activo' o 'inactivo'.

---

## Observación de Auditoría: Identificador Único por Cédula

Durante el análisis del problema noté una situación recurrente en sistemas académicos: es muy común que existan estudiantes con nombres y apellidos idénticos (homonimia). Un `id` numérico interno solo sirve a nivel de base de datos, y el correo electrónico puede variar o ser compartido por padres de familia.

Por esta razón decidí implementar el campo `documento` (Cédula de Ciudadanía) con restricción `UNIQUE` e índice en SQLite. De esta forma:
1. Ningún estudiante puede registrarse dos veces con el mismo documento.
2. Si se intenta duplicar, el sistema lanza un error controlado (`DuplicateDocumentoError` / HTTP 409 Conflict).
3. La barra de búsqueda de la interfaz web y el parámetro `search` de la API permiten buscar directamente por número de cédula.

Para facilitar la revisión por parte del equipo evaluador, configuré en los datos iniciales de prueba mi propio número de documento: **`1118803077`**, a nombre de **Samuel Ballesteros** (Teléfono: `3104512230`), para que puedan probar de inmediato las búsquedas y la edición.

---

## Instalación y Ejecución

### Prerrequisitos
- Python 3.10 o superior (yo utilicé Python 3.12).
- pip instalado.

### 1. Clonar el repositorio
```bash
git clone https://github.com/Soretsellab/partikle-qa-backend-students.git
cd partikle-qa-backend-students
```

### 2. Crear y activar entorno virtual
En Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

En Linux o macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Iniciar la aplicación
```bash
python run.py
```

Al ejecutarlo por primera vez, el script crea automáticamente el archivo `students.db` con su tabla e índices, e inserta registros de ejemplo.

- Interfaz Web: http://127.0.0.1:5000
- Endpoint API REST: http://127.0.0.1:5000/api/v1/students

---

## Interfaz Web

Diseñé una interfaz sencilla y responsiva utilizando plantillas Jinja2 y Tailwind CSS. En ella implementé:
- Listado de estudiantes con badge de estado (verde para activo, gris para inactivo).
- Filtro por estado (todos, activos, inactivos).
- Buscador en tiempo real por documento, nombres, apellidos o correo.
- Paginación con botones de página anterior y siguiente.
- Modales para registrar nuevos estudiantes, editar registros existentes y confirmar la eliminación.

---

## Documentación de la API REST

Todas las respuestas están estructuradas en formato JSON.

### 1. Listar estudiantes
- Método: `GET`
- URL: `/api/v1/students`
- Parámetros opcionales en la URL:
  - `page`: Número de página (por defecto 1).
  - `per_page`: Cantidad por página (por defecto 10).
  - `status`: Filtrar por 'activo' o 'inactivo'.
  - `search`: Buscar por documento, nombres, apellidos o email.

Ejemplo de respuesta (200 OK):
```json
{
  "success": true,
  "data": {
    "has_next": false,
    "has_prev": false,
    "items": [
      {
        "id": 1,
        "documento": "1118803077",
        "nombres": "Samuel",
        "apellidos": "Ballesteros",
        "edad": 24,
        "telefono": "3104512230",
        "email": "samuel.ballesteros@example.com",
        "status": "activo"
      }
    ],
    "page": 1,
    "per_page": 10,
    "total": 8,
    "total_pages": 1
  }
}
```

### 2. Consultar un estudiante por ID
- Método: `GET`
- URL: `/api/v1/students/<id>`
- Respuestas: `200 OK` si se encuentra, `404 Not Found` si no existe.

### 3. Crear un estudiante
- Método: `POST`
- URL: `/api/v1/students`
- Headers: `Content-Type: application/json`
- Cuerpo JSON:
```json
{
  "documento": "1098765432",
  "nombres": "Camila",
  "apellidos": "Sánchez",
  "edad": 23,
  "telefono": "3119876543",
  "email": "camila.sanchez@example.com",
  "status": "activo"
}
```
- Códigos de respuesta:
  - `201 Created`: Creado con éxito.
  - `400 Bad Request`: Si faltan campos o alguno no cumple las validaciones de formato.
  - `409 Conflict`: Si el documento o el correo ya están registrados.

### 4. Actualizar un estudiante
- Método: `PUT`
- URL: `/api/v1/students/<id>`
- Headers: `Content-Type: application/json`
- Cuerpo JSON (envío únicamente los campos que quiero modificar):
```json
{
  "edad": 25,
  "status": "inactivo"
}
```
- Códigos de respuesta: `200 OK`, `400 Bad Request`, `404 Not Found`, `409 Conflict`.

### 5. Eliminar un estudiante
- Método: `DELETE`
- URL: `/api/v1/students/<id>`
- Códigos de respuesta: `200 OK`, `404 Not Found`.

---

## Pruebas Automatizadas y Cobertura

Escribí una suite de 95 pruebas automáticas combinando pruebas unitarias (para las validaciones de la entidad y la lógica de los casos de uso) y pruebas de integración (para verificar los endpoints de la API, las vistas web y las consultas a SQLite).

Para correr las pruebas y ver el reporte de cobertura en consola:
```bash
pytest --cov=src --cov-report=term-missing
```

Resumen de cobertura obtenido:

| Módulo | Cobertura | Descripción |
|---|---|---|
| `src/domain/entities/student.py` | 100% | Validaciones de formato, documento, edad, teléfono, correo |
| `src/domain/exceptions.py` | 100% | Excepciones personalizadas |
| `src/domain/ports/student_repository.py` | 100% | Definición del puerto del repositorio |
| `src/application/dtos/student_dto.py` | 100% | Transferencia de datos |
| `src/application/use_cases/*` | 100% | Todos los casos de uso (crear, listar, consultar, editar, borrar) |
| `src/infrastructure/database/db_connection.py` | 100% | Creación de base de datos e índices |
| `src/infrastructure/database/sqlite_student_repository.py` | 92% | Consultas SQL y filtros de búsqueda |
| `src/infrastructure/web/controllers/student_api_controller.py` | 98% | Endpoints REST y manejo de códigos HTTP |
| `src/infrastructure/web/controllers/student_view_controller.py` | 100% | Vistas Jinja2, modales y formularios |
| **Total del proyecto** | **97%** | **95 pruebas pasadas en total** |

Si se desea generar el reporte en formato HTML para revisarlo en el navegador:
```bash
pytest --cov=src --cov-report=html
```
El reporte se guarda en la carpeta `htmlcov/index.html`.

---

## Información del Candidato

- Nombre: Samuel Ballesteros
- Documento de Identidad: 1118803077
- Teléfono: 3104512230
- Repositorio en GitHub: https://github.com/Soretsellab/partikle-qa-backend-students

---

## Contacto de Entrega

- Gerencia de Proyectos: `gerenciap@partikle.tech`
- Evaluación Técnica: `atrespalacios@partikle.tech`
