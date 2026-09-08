# Respuestas a las Preguntas Teóricas (Parte 1)

Candidato: Samuel Ballesteros  
Documento: 1118803077  
Teléfono: 3104512230  

A continuación comparto mis respuestas a las 5 preguntas teóricas de la prueba.

---

### 1. ¿Cuáles son los tipos de datos en Python?

En mi día a día con Python suelo trabajar con estos tipos de datos principales:

- Numéricos:
  - int: números enteros (por ejemplo 24 o -5).
  - float: números con decimales (por ejemplo 3.14).
  - complex: números complejos (por ejemplo 2 + 3j).
- Texto:
  - str: cadenas de caracteres o texto (por ejemplo "Samuel Ballesteros").
- Colecciones:
  - list: listas ordenadas y modificables (por ejemplo [1, 2, 3]).
  - tuple: tuplas ordenadas pero que no se pueden modificar una vez creadas (por ejemplo (10, 20)).
  - dict: diccionarios con pares clave-valor (por ejemplo {"nombre": "Samuel", "edad": 24}).
  - set: conjuntos de elementos únicos, sin orden ni duplicados.
- Booleanos:
  - bool: valores lógicos (True o False).
- Nulo:
  - None: representa la ausencia de un valor.

---

### 2. ¿Para qué se usan los índices negativos en las secuencias?

Los uso para acceder a los elementos de una lista, tupla o texto empezando a contar desde el final hacia adelante, sin necesidad de calcular cuántos elementos hay en total.

El índice -1 me devuelve el último elemento y el -2 el penúltimo.

Ejemplo:

```python
alumnos = ["Carlos", "María", "Samuel"]

print(alumnos[-1])  # Imprime "Samuel" (el último)
print(alumnos[-2])  # Imprime "María" (el penúltimo)
```

Me resulta muy práctico porque me evita tener que escribir `alumnos[len(alumnos) - 1]` y hace que el código sea más legible.

---

### 3. ¿Qué son los docstrings?

Son cadenas de texto entre comillas triples ("""...""") que coloco al principio de una función, clase o módulo para explicar qué hace, qué parámetros recibe y qué retorna.

A diferencia de un comentario normal con #:
1. El docstring no se borra al compilar; se guarda en memoria y lo puedo consultar en la consola con help() o accediendo al atributo __doc__.
2. Mi editor de código (como VS Code) lo lee automáticamente para mostrarme la documentación y las ayudas flotantes mientras escribo código.

Ejemplo:

```python
def calcular_promedio(nota1: float, nota2: float) -> float:
    """Calcula el promedio simple de dos notas."""
    return (nota1 + nota2) / 2
```

---

### 4. ¿Qué operador realiza la división hacia abajo (floor division)?

La respuesta correcta es //

La diferencia práctica con los otros operadores es:
- / hace una división regular y devuelve un flotante: 7 / 2 da 3.5.
- // hace la división entera o hacia abajo, quedándose con el entero inferior: 7 // 2 da 3.
- % calcula el residuo de la división: 7 % 2 da 1.

---

### 5. Explique las ventajas y desventajas de Flask y Django

He trabajado con ambos y la diferencia principal está en la filosofía y el alcance:

Flask:
Es un microframework muy liviano. Me da el control de las rutas y peticiones HTTP, y me da libertad total para decidir cómo estructurar el proyecto, qué base de datos usar y qué librerías conectar.
- Ventajas: Es rápido de inicializar, consume pocos recursos y es ideal cuando quiero implementar una arquitectura limpia o hexagonal sin que el framework me obligue a seguir sus convenciones.
- Desventajas: Al no traer casi nada integrado, si la aplicación crece me toca configurar o programar manualmente la autenticación, los formularios o las migraciones.

Django:
Es un framework completo ("con baterías incluidas"). Viene de fábrica con su propio ORM, panel de administración listo para producción, sistema de usuarios y seguridad.
- Ventajas: Acelera mucho el desarrollo de proyectos completos porque ya tiene resueltas la mayoría de necesidades comunes.
- Desventajas: Es más pesado, tiene una curva de aprendizaje más pronunciada y resulta rígido si quiero usar patrones desacoplados o si solo necesito una API pequeña.
