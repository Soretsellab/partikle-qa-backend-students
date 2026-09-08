# Parte 1: Respuestas Teóricas — Prueba Técnica Python (QA Backend)

Respuestas directas, claras y fundamentadas a las preguntas teóricas de la evaluación:

---

### 1. ¿Cuáles son los tipos de datos en Python?

En Python, los tipos de datos básicos y más utilizados se dividen en:

1. **Numéricos:**
   - `int`: Números enteros (ej. `25`, `-5`).
   - `float`: Números decimales (ej. `3.14`, `0.5`).
   - `complex`: Números complejos (ej. `2 + 3j`).

2. **Texto:**
   - `str`: Cadenas de caracteres / texto (ej. `"Samuel Ballesteros"`).

3. **Colecciones y Secuencias:**
   - `list`: Listas ordenadas que se pueden modificar (ej. `[1, 2, 3]`).
   - `tuple`: Tuplas ordenadas que no se pueden modificar (inmutables) (ej. `(10, 20)`).
   - `dict`: Diccionarios de clave-valor (ej. `{"nombre": "Samuel", "edad": 24}`).
   - `set`: Conjuntos de elementos únicos, sin duplicados ni orden fijo (ej. `{1, 2, 3}`).

4. **Booleanos:**
   - `bool`: Valores lógicos de verdad (`True` o `False`).

5. **Nulo:**
   - `None`: Representa la ausencia de valor.

---

### 2. ¿Para qué se usan los índices negativos en las secuencias?

Los índices negativos sirven para **acceder a los elementos de una lista, tupla o texto empezando a contar desde el final hacia el principio**, sin necesidad de calcular la longitud total de la secuencia.

- El índice `-1` es el **último** elemento.
- El índice `-2` es el **penúltimo** elemento.

**Ejemplo sencillo:**
```python
alumnos = ["Carlos", "María", "Samuel"]

print(alumnos[-1])   # Imprime: "Samuel" (el último)
print(alumnos[-2])   # Imprime: "María"  (el penúltimo)
```

**¿Por qué es útil?**
Hace el código más limpio y fácil de leer, evitando escribir `alumnos[len(alumnos) - 1]`.

---

### 3. ¿Qué son los docstrings?

Un **docstring** es un texto explicativo delimitado por triples comillas (`"""..."""`) que se coloca al principio de una función, clase o módulo para explicar **qué hace, qué parámetros recibe y qué devuelve**.

**¿En qué se diferencia de un comentario normal (`#`)?**
1. Un comentario `#` es ignorado por Python, mientras que el docstring se guarda en la memoria del programa (`__doc__`).
2. Se puede consultar en cualquier momento usando la función `help()` en consola.
3. Los editores de código (como VS Code) lo leen automáticamente para mostrar sugerencias y ayudas flotantes mientras programas.

**Ejemplo sencillo:**
```python
def calcular_promedio(nota1: float, nota2: float) -> float:
    """Calcula el promedio de dos notas numéricas."""
    return (nota1 + nota2) / 2
```

---

### 4. ¿Qué operador realiza la división hacia abajo (floor division)?

- `/`
- **`//`  <-- [RESPUESTA CORRECTA]**
- `%`
- Ninguna de las anteriores

**Explicación:**
- `/` realiza la división normal con decimales: `7 / 2` resulta `3.5`.
- **`//` realiza la división hacia abajo**: toma el resultado y se queda con el número entero inferior más cercano (`7 // 2` resulta `3`).
- `%` es el operador de residuo (módulo): entrega lo que sobra de la división (`7 % 2` resulta `1`).

---

### 5. Explique las ventajas y desventajas de Flask y Django

Flask y Django son los dos frameworks web más conocidos en Python, pero tienen filosofías opuestas:

- **Flask es un microframework ligero y flexible:** Te da solo lo básico (gestión de rutas y peticiones HTTP) y te deja libertad absoluta para elegir cómo organizar tu arquitectura y qué herramientas usar.
- **Django es un framework "con todo incluido" (*batteries included*):** Trae de fábrica base de datos (ORM), panel de administración, autenticación de usuarios y seguridad integrada.

#### Comparativa rápida:

| Característica | **Flask** | **Django** |
|---|---|---|
| **Enfoque** | Minimalista y flexible | Completo y estructurado |
| **Base de datos (ORM)** | No incluye (usas SQLite directo, SQLAlchemy, etc.) | Trae su propio ORM potente con migraciones |
| **Panel de Administración** | No incluye de serie | Incluido y listo para usar |
| **Curva de aprendizaje** | Rápido y sencillo para empezar | Más amplio por la cantidad de conceptos |

#### Ventajas y Desventajas:

**Flask:**
- *Ventaja:* Es muy liviano, rápido y te permite aplicar arquitecturas limpias o hexagonales sin atarte a estructuras impuestas.
- *Desventaja:* Si el proyecto crece, tienes que configurar y conectar manualmente la base de datos, la seguridad y las herramientas adicionales.

**Django:**
- *Ventaja:* Acelera el desarrollo en proyectos grandes porque ya tiene resuelta la autenticación, el panel de control y las migraciones de base de datos.
- *Desventaja:* Es más pesado, más rígido y resulta innecesariamente complejo para microservicios o APIs pequeñas.

