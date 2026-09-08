# Sistema de Registro de Estudiantes — Partikle (Python QA Backend)

Solución técnica para la prueba de evaluación **Python – QA Backend** de **Partikle**.

El proyecto implementa una **API REST** y un **Dashboard Web interactivo** para la gestión completa de estudiantes, desarrollado bajo los principios de **Arquitectura Limpia / Hexagonal (Ports & Adapters)**, persistencia pura en **SQLite3**, vistas con motor de plantillas **Jinja2** (con filtros y paginación) y una suite de pruebas automatizadas con **Pytest** (unitarias y de integración).

---

##  Contenido del Repositorio

- **`TEORIA.md`**: Respuestas técnicas detalladas y fundamentadas a las 5 preguntas de la **Parte 1 (Teoría)**.
- **`src/domain`**: Entidades e invariantes de negocio, excepciones y contratos de puertos (`StudentRepositoryPort`), totalmente desacoplados de frameworks.
- **`src/application`**: Casos de uso (CRUD, filtros, paginación) y Data Transfer Objects (DTOs).
- **`src/infrastructure`**: Adaptador de base de datos con `sqlite3` y adaptador web con **Flask**, controladores REST y vistas Jinja2.
- **`tests/`**: Suite exhaustiva de pruebas unitarias y de integración con `pytest` y `pytest-cov`.

---

## 🏛️ Arquitectura Hexagonal (Ports & Adapters)

El diseño del proyecto separa estrictamente la lógica del negocio de los detalles técnicos y frameworks externos:

```text
Entrevista/
├── TEORIA.md                  # Parte 1: Respuestas teóricas
├── README.md                  # Instrucciones de ejecución y documentación
├── requirements.txt           # Dependencias de producción y testing
├── pytest.ini                 # Configuración de pruebas
├── run.py                     # Entry point de la aplicación (incluye seed de prueba)
├── src/
│   ├── domain/                # NÚCLEO: Reglas de negocio e invariantes
│   │   ├── entities/          # Entidad Student con validaciones estrictas
│   │   ├── exceptions.py      # Jerarquía de excepciones de dominio
│   │   └── ports/             # Contratos de interfaces (StudentRepositoryPort)
│   ├── application/           # CASOS DE USO Y DTOs
│   │   ├── dtos/              # Objetos de transferencia de datos
│   │   └── use_cases/         # Create, Get, List, Update, Delete Student
│   └── infrastructure/        # ADAPTADORES EXTERNOS
│       ├── database/          # SQLite3: Conexión y repositorio concreto
│       └── web/               # Flask: Controladores API REST y Vistas Jinja2
│           └── templates/     # Plantillas HTML con Tailwind CSS
└── tests/                     # SUITE DE PRUEBAS (QA)
    ├── conftest.py            # Fixtures y base de datos en memoria para tests
    ├── unit/                  # Tests unitarios de dominio y casos de uso
    └── integration/           # Tests de integración de endpoints REST, vistas y SQLite
```

### Modelo de Datos del Estudiante
Cada registro cuenta con los siguientes campos validados a nivel de Dominio:
- **`id`**: Entero autoincremental (Clave primaria técnica en base de datos).
- **`documento`**: Documento de identidad / Cédula único (6 a 20 caracteres alfanuméricos, e.g. `1118803077`). **Identificador de negocio único**.
- **`nombres`**: Texto no vacío (obligatorio).
- **`apellidos`**: Texto no vacío (obligatorio).
- **`edad`**: Entero positivo (entre 1 y 120 años).
- **`telefono`**: Texto con formato válido (7 a 20 dígitos/caracteres numéricos).
- **`email`**: Dirección de correo electrónico única y con formato válido RFC.
- **`status`**: Estado del estudiante: `'activo'` o `'inactivo'`.

---

## 📋 Observación de Auditoría y Diseño: Identificador Único por Documento de Identidad

Durante la auditoría del sistema y modelado de dominio, se detectó un requerimiento esencial de integridad para aplicaciones académicas y de gestión estudiantil:

> **El problema de la homonimia y la trazabilidad:** En instituciones y registros estudiantiles es sumamente común la existencia de estudiantes con nombres y apellidos idénticos o muy similares (e.g. dos "Juan Pérez"). Confiar únicamente en un `id` interno autoincremental no permite al evaluador o usuario final validar inequívocamente a la persona en el mundo real, y el correo electrónico puede variar con el tiempo o ser compartido por apoderados.

### Solución Implementada:
1. **Identificador Natural de Negocio (`documento`):** Se introdujo el campo `documento` (Cédula de Ciudadanía / Documento de Identidad) con restricción `UNIQUE` indexada en base de datos (`idx_students_documento`) y validación estricta de formato en la entidad de dominio `Student`.
2. **Registro de Semilla con Documento Real:** Se configuró como primer registro de prueba en la base de datos el documento de identidad del candidato: **`1118803077`**, perteneciente a **Samuel Ballesteros** (Teléfono: `3104512230`), permitiendo validar inmediatamente búsquedas exactas, prevención de duplicados (`DuplicateDocumentoError` / HTTP 409 Conflict) y edición en la interfaz web.
3. **Búsqueda Multicriterio Optimizada:** La barra de búsqueda del Dashboard Web y el parámetro `search` de la API REST filtran de manera instantánea por **`documento`**, `nombres`, `apellidos` y `email`.

---

## ⚙️ Instalación y Configuración Local

### Prerrequisitos
- Python 3.10 o superior (verificado con Python 3.12).
- Gestor de paquetes `pip`.

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/Soretsellab/partikle-qa-backend-students.git
cd partikle-qa-backend-students
```

### Paso 2: Crear y activar entorno virtual (Recomendado)
- **En Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
- **En Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## 🚀 Ejecución de la Aplicación

Para iniciar el servidor de desarrollo:
```bash
python run.py
```

Al iniciar por primera vez, el sistema creará automáticamente la base de datos `students.db` con sus índices e insertará **datos de prueba iniciales** para facilitar la evaluación inmediata:

- **Panel Web / Dashboard (Jinja2):** [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **API REST Endpoint:** [http://127.0.0.1:5000/api/v1/students](http://127.0.0.1:5000/api/v1/students)

---

## 🖥️ Interfaz Web (Plantillas Jinja2)

La aplicación incluye un dashboard web interactivo y responsivo estilizado con Tailwind CSS que permite:
- **Visualizar estudiantes** con su documento de identidad, datos personales y badges de estado (`activo` en verde, `inactivo` en gris).
- **Filtrar por estado** (`activo` / `inactivo` / todos).
- **Buscador en tiempo real** por **documento de identidad**, nombres, apellidos o email.
- **Paginación de resultados** configurable con controles de navegación anterior/siguiente.
- **Modales funcionales e integrados** para crear nuevo estudiante, editar información existente (con prellenado seguro mediante atributos `data-*`) y confirmación modal de borrado.

---

## 📡 Documentación de la API REST

Todos los endpoints retornan respuestas con formato JSON estándar.

### 1. Listar Estudiantes (con paginación y filtros)
- **Método:** `GET`
- **URL:** `/api/v1/students`
- **Parámetros Query (opcionales):**
  - `page`: Número de página (default: 1).
  - `per_page`: Elementos por página (default: 10, max: 100).
  - `status`: Filtrar por estado (`activo` o `inactivo`).
  - `search`: Búsqueda textual por **documento**, nombres, apellidos o email.

**Ejemplo de respuesta (200 OK):**
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

### 2. Consultar Estudiante por ID
- **Método:** `GET`
- **URL:** `/api/v1/students/<id>`
- **Respuesta:** `200 OK` si existe, `404 Not Found` si no existe.

### 3. Crear Estudiante
- **Método:** `POST`
- **URL:** `/api/v1/students`
- **Headers:** `Content-Type: application/json`
- **Cuerpo JSON:**
```json
{
  "documento": "1118803077",
  "nombres": "Camila",
  "apellidos": "Sánchez",
  "edad": 23,
  "telefono": "+573119876543",
  "email": "camila.sanchez@example.com",
  "status": "activo"
}
```
- **Códigos de estado:**
  - `201 Created`: Creado exitosamente.
  - `400 Bad Request`: Error de validación o campos faltantes (e.g. documento inválido).
  - `409 Conflict`: Documento de identidad o correo electrónico ya registrado.

### 4. Actualizar Estudiante
- **Método:** `PUT`
- **URL:** `/api/v1/students/<id>`
- **Headers:** `Content-Type: application/json`
- **Cuerpo JSON (campos a actualizar opcionales):**
```json
{
  "documento": "1118803077",
  "edad": 24,
  "status": "inactivo"
}
```
- **Códigos de estado:** `200 OK`, `400 Bad Request`, `404 Not Found`, `409 Conflict`.

### 5. Eliminar Estudiante
- **Método:** `DELETE`
- **URL:** `/api/v1/students/<id>`
- **Códigos de estado:** `200 OK` (o confirmación), `404 Not Found`.

---

## 🧪 Pruebas Automatizadas y Cobertura QA

La suite cuenta con **95 pruebas automatizadas** (unitarias y de integración) con una **cobertura global del 97%**:

```bash
pytest --cov=src --cov-report=term-missing
```

| Módulo | Cobertura | Descripción |
|---|---|---|
| `src/domain/entities/student.py` | **100%** | Invariantes, tipos, validación de documento, email, teléfono, edad |
| `src/domain/exceptions.py` | **100%** | Excepciones de negocio (`DuplicateDocumentoError`, etc.) |
| `src/domain/ports/student_repository.py` | **100%** | Contrato de interfaz del repositorio |
| `src/application/dtos/student_dto.py` | **100%** | DTOs de transferencia y serialización |
| `src/application/use_cases/*` | **100%** | Todos los casos de uso (Create, Get, List, Update, Delete) |
| `src/infrastructure/database/db_connection.py` | **100%** | Esquema DDL, índices y conexiones seguras |
| `src/infrastructure/database/sqlite_student_repository.py` | **92%** | Persistencia SQL, consultas parametrizadas y filtros |
| `src/infrastructure/web/controllers/student_api_controller.py` | **98%** | Endpoints REST, códigos HTTP y serialización de errores |
| `src/infrastructure/web/controllers/student_view_controller.py` | **100%** | Flujo completo de vistas Jinja2, filtros y modales |
| **TOTAL** | **97%** | **95 tests PASSED** |

Para generar un reporte en HTML navegable:
```bash
pytest --cov=src --cov-report=html
```
*(El reporte se generará en la carpeta `htmlcov/index.html`)*.

---

## 👤 Información del Candidato
- **Nombre:** Samuel Ballesteros
- **Documento de Identidad:** `1118803077`
- **Teléfono de Contacto:** `3104512230`
- **Repositorio Público GitHub:** [https://github.com/Soretsellab/partikle-qa-backend-students](https://github.com/Soretsellab/partikle-qa-backend-students)

---

## 📬 Contacto de Entrega (Evaluadores Partikle)
- **Gerencia de Proyectos:** `gerenciap@partikle.tech`
- **Evaluación Técnica:** `atrespalacios@partikle.tech`
