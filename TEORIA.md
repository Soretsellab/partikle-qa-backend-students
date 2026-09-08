# Parte 1: Respuestas Teóricas — Prueba Técnica Python (QA Backend)

A continuación se presentan las respuestas a las preguntas teóricas solicitadas en la evaluación:

---

### 1. ¿Cuáles son los tipos de datos en Python?

Python es un lenguaje fuertemente tipado y dinámico. Sus tipos de datos incorporados (*built-in types*) se agrupan según su naturaleza y mutabilidad:

1. **Numéricos (`Numeric Types`):**
   - `int`: Números enteros de precisión arbitraria (ej. `42`, `-10`).
   - `float`: Números de coma flotante de precisión doble según IEEE 754 (ej. `3.14159`, `1e-4`).
   - `complex`: Números complejos con parte real e imaginaria (ej. `2 + 3j`).

2. **Secuencias (`Sequence Types`):**
   - `str`: Secuencias inmutables de caracteres Unicode (ej. `"Backend"`).
   - `list`: Colección ordenada, heterogénea y **mutable** de elementos (ej. `[1, "QA", True]`).
   - `tuple`: Colección ordenada, heterogénea e **inmutable** (ej. `(10, 20)`).
   - `range`: Secuencia inmutable de números comúnmente usada en bucles iterativos (ej. `range(0, 10)`).

3. **Mapeos (`Mapping Types`):**
   - `dict`: Colección mutable de pares clave-valor indexados por claves hashables (ej. `{"id": 1, "status": "activo"}`).

4. **Conjuntos (`Set Types`):**
   - `set`: Colección mutable, no ordenada y sin duplicados de elementos hashables (ej. `{1, 2, 3}`).
   - `frozenset`: Versión inmutable y hashable de un `set`.

5. **Booleanos (`Boolean Type`):**
   - `bool`: Subtipo de `int` que representa valores de verdad lógica: `True` y `False`.

6. **Tipos Binarios (`Binary Types`):**
   - `bytes`: Secuencia inmutable de bytes (ej. `b"datos"`).
   - `bytearray`: Secuencia mutable de bytes.
   - `memoryview`: Permite acceder a la memoria de otros objetos binarios sin realizar copias.

7. **Nulo / Especial:**
   - `NoneType` (`None`): Representa la ausencia de valor o valor nulo de retorno.

---

### 2. ¿Para qué se usan los índices negativos en las secuencias?

En Python, los índices negativos permiten **acceder y rebanar (*slicing*) secuencias (cadenas, listas, tuplas) comenzando desde el final hacia el principio**, eliminando la necesidad de calcular manualmente `len(secuencia) - 1`.

- El índice `-1` referencia al **último elemento**.
- El índice `-2` referencia al **penúltimo elemento**, y así sucesivamente hasta `-len(secuencia)` que apunta al primer elemento.

**Ejemplo:**
```python
alumnos = ["Carlos", "María", "Andrés"]
print(alumnos[-1])  # "Andrés" (último)
print(alumnos[-2])  # "María"  (penúltimo)

# Slicing: Obtener los dos últimos elementos
print(alumnos[-2:])  # ['María', 'Andrés']

# Invertir una secuencia:
print(alumnos[::-1])  # ['Andrés', 'María', 'Carlos']
```

**Ventajas principales:**
- Mayor legibilidad del código (más idiomático o *Pythonic*).
- Menor probabilidad de errores por desfase de índice (*off-by-one errors*).
- Eficiencia computacional al evitar consultas previas a la longitud de la colección.

---

### 3. ¿Qué son los docstrings?

Los **docstrings** (*documentation strings*) son literales de cadena de texto (generalmente delimitados por triples comillas `"""` o `'''`) situados como la **primera declaración** dentro de la definición de un módulo, función, método o clase.

Su propósito es proporcionar documentación interna estructurada sobre el comportamiento, parámetros, valores de retorno y excepciones del elemento.

**Características clave:**
1. A diferencia de los comentarios regulares (`#`), los docstrings no son descartados por el intérprete: se compilan en bytecode y se almacenan en el atributo especial `__doc__` del objeto.
2. Son accesibles en tiempo de ejecución mediante la función integrada `help()` o introspección (`objeto.__doc__`).
3. Son interpretados por herramientas automatizadas de documentación (Sphinx, MkDocs, pydoc) y por entornos de desarrollo para autocompletado y tipado.
4. Siguen estándares de la comunidad como **PEP 257** y formatos estándar (Google Style, NumPy, Sphinx).

**Ejemplo:**
```python
def calcular_promedio(calificaciones: list[float]) -> float:
    """Calcula la media aritmética de una lista de calificaciones.

    Args:
        calificaciones (list[float]): Lista con las notas numéricas.

    Returns:
        float: Promedio redondeado a dos decimales.

    Raises:
        ValueError: Si la lista de calificaciones está vacía.
    """
    if not calificaciones:
        raise ValueError("La lista de calificaciones no puede estar vacía.")
    return round(sum(calificaciones) / len(calificaciones), 2)
```

---

### 4. ¿Qué operador realiza la división hacia abajo (floor division)?

- `/`
- **`//`  <-- [RESPUESTA CORRECTA]**
- `%`
- Ninguna de las anteriores

**Explicación:**
El operador `//` realiza la **división entera / división hacia abajo (*floor division*)**, truncando el resultado al número entero menor o igual más cercano (redondeo hacia el infinito negativo, equivalente a `math.floor(a / b)`).
- `7 / 2` produce `3.5` (división flotante estándar).
- `7 // 2` produce `3`.
- `-7 // 2` produce `-4` (confirma que redondea hacia abajo, no trunca simplemente hacia cero).
- `%` corresponde al operador de módulo (residuo de la división).

---

### 5. Explique las ventajas y desventajas de Flask y Django

Tanto Flask como Django son los dos frameworks web más consolidados en el ecosistema Python, pero obedecen a filosofías de diseño distintas:

| Criterio | **Flask** (Microframework) | **Django** ("Batteries Included") |
| :--- | :--- | :--- |
| **Filosofía** | Minimalista, no obstinado (*unopinionated*), flexible y extensible. | Monolítico, obstinado (*opinionated*), todo incluido de fábrica. |
| **ORM** | No incluye ORM por defecto (libertad para usar SQLAlchemy, Peewee, SQLite nativo, etc.). | ORM propio muy potente, acoplado al framework con soporte de migraciones automáticas. |
| **Panel Admin** | No incluye (debe integrarse con Flask-Admin o desarrollarse). | Panel de administración autogenerado listo para producción. |
| **Autenticación** | No incluye nativamente (se usan extensiones como Flask-Login o Flask-JWT-Extended). | Sistema completo de usuarios, roles, permisos y hashing de contraseñas de serie. |
| **Curva de Aprendizaje**| Baja al inicio; se requiere mayor experiencia para diseñar arquitecturas escalables. | Media/Alta al inicio debido a su volumen de convenciones y abstracciones. |

#### Ventajas y Desventajas de Flask
- **Ventajas:**
  - **Gran flexibilidad arquitectónica:** Ideal para implementar arquitecturas limpias, hexagonales, microservicios y APIs ligeras sin forzar patrones ajenos.
  - **Bajo consumo de recursos y ligereza:** Se carga rápido y solo ejecuta el código estrictamente necesario.
  - **Total libertad de herramientas:** Permite elegir las librerías de persistencia, validación y serialización según las necesidades del proyecto.
- **Desventajas:**
  - **Mayor esfuerzo inicial en proyectos complejos:** Las funcionalidades como autenticación, migraciones, validación y seguridad avanzada deben configurarse o implementarse manualmente.
  - **Riesgo de falta de estandarización:** Equipos sin directrices claras pueden estructurar proyectos de formas heterogéneas.

#### Ventajas y Desventajas de Django
- **Ventajas:**
  - **Desarrollo rápido (Time-to-Market):** Provee de fábrica ORM, motor de migraciones, panel de administración, CSRF protection, autenticación y formularios.
  - **Estandarización:** La estructura común facilita la incorporación de nuevos desarrolladores a equipos grandes.
  - **Comunidad y ecosistema maduro:** Gran cantidad de paquetes listos para usar (`django-rest-framework`, `django-allauth`, etc.).
- **Desventajas:**
  - **Rigidez arquitectónica:** Intentar implementar patrones desacoplados (como arquitectura hexagonal pura) resulta costoso y contraproducente debido al fuerte acoplamiento del ORM y los modelos de Django.
  - **Sobrecarga innecesaria para microservicios simples:** Incluye muchos componentes que no son necesarios cuando solo se requiere una API o servicio liviano.
