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
Cada registro cuenta con los siguientes campos:
- **`id`**: Entero autoincremental (Clave primaria).
- **`nombres`**: Texto no vacío (obligatorio).
- **`apellidos`**: Texto no vacío (obligatorio).
- **`edad`**: Entero positivo (entre 1 y 120 años).
- **`telefono`**: Texto con formato válido (7 a 20 dígitos/caracteres numéricos).
- **`email`**: Dirección de correo electrónico única y con formato válido.
- **`status`**: Estado del estudiante: `'activo'` o `'inactivo'`.

---

## ⚙️ Instalación y Configuración Local

### Prerrequisitos
- Python 3.10 o superior (verificado con Python 3.12).
- Gestor de paquetes `pip`.

### Paso 1: Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd Entrevista
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

La aplicación incluye un dashboard web responsivo estilizado con Tailwind CSS que permite:
- **Visualizar estudiantes** con sus datos y badges de estado (`activo` en verde, `inactivo` en gris).
- **Filtrar por estado** (`activo` / `inactivo` / todos).
- **Buscador en tiempo real** por nombres, apellidos o email.
- **Paginación de resultados** configurable con controles de navegación anterior/siguiente.
- **Modales integrados** para crear nuevo estudiante, editar información existente y confirmación de borrado.

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
  - `search`: Búsqueda textual en nombres, apellidos o email.

**Ejemplo de respuesta (200 OK):**
```json
{
  "success": true,
  "data": {
    "has_next": true,
    "has_prev": false,
    "items": [
      {
        "id": 1,
        "nombres": "Juan Carlos",
        "apellidos": "Pérez Gómez",
        "edad": 22,
        "telefono": "+573001234567",
        "email": "juan.perez@example.com",
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
  - `400 Bad Request`: Error de validación o campos faltantes.
  - `409 Conflict`: Correo electrónico ya registrado.

### 4. Actualizar Estudiante
- **Método:** `PUT`
- **URL:** `/api/v1/students/<id>`
- **Headers:** `Content-Type: application/json`
- **Cuerpo JSON (campos a actualizar):**
```json
{
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

## 🧪 Pruebas Automatizadas y QA

Para ejecutar la suite completa de pruebas unitarias y de integración junto con el informe de cobertura de código:

```bash
pytest --cov=src --cov-report=term-missing
```

Para generar además un reporte en HTML navegable:
```bash
pytest --cov=src --cov-report=html
```
*(El reporte se generará en la carpeta `htmlcov/index.html`)*.

---

## 📬 Contacto de Entrega
- Correo 1: `gerenciap@partikle.tech`
- Correo 2: `atrespalacios@partikle.tech`
