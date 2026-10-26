# Plan de implementación: Organización de tareas académicas

**Rama**: `001-organizar-tareas-academicas` | **Fecha**: 2026-10-26 | **Especificación**: [spec.md](spec.md)

**Entrada**: Especificación de la funcionalidad en `specs/001-organizar-tareas-academicas/spec.md`.

## Resumen

Construir una aplicación de una sola instancia para un estudiante por dispositivo. FastAPI
servirá la página y los archivos estáticos, además de una API pequeña para materias y tareas.
SQLite conservará los datos. JavaScript mostrará, filtrará y clasificará las tareas según la
hora local del navegador. Las pruebas con pytest cubrirán la API y los recorridos de la interfaz.

## Contexto técnico

**Lenguaje y versión**: Python 3.12; HTML, CSS y JavaScript sin frameworks.

**Dependencias principales**: FastAPI, Uvicorn; biblioteca estándar `sqlite3`.

**Almacenamiento**: Un archivo SQLite local por instancia; archivo separado para cada prueba.

**Pruebas**: pytest, `httpx` para `TestClient` y `pytest-playwright`
para los flujos reales del navegador.

**Plataforma de destino**: Aplicación web servida localmente; interfaz adaptable a navegadores
de celular y computadora. Cada instalación mantiene su propio archivo de datos.

**Tipo de proyecto**: Una aplicación web monolítica pequeña, sin Docker ni microservicios.

**Objetivos de rendimiento**: Listado y filtros perceptiblemente inmediatos con 100 tareas;
los recorridos principales deben cumplir los criterios CE-001 a CE-005 de la especificación.

**Restricciones**: Un usuario por instancia, sin cuentas; mensajes y documentos en español;
sin edición ni eliminación en esta versión; misma procedencia para interfaz y API.

**Escala y alcance**: Un estudiante, materias y hasta 100 tareas como volumen de aceptación;
una página principal y tres operaciones de escritura: crear materia, crear tarea y cambiar estado.

## Comprobación de la constitución

*Puerta de entrada evaluada antes de la investigación y repetida después del diseño: conforme.*

| Principio | Decisión verificable |
|-----------|----------------------|
| Simplicidad primero | Un solo proyecto; `sqlite3` directo, sin ORM, contenedores ni servicios adicionales. |
| Pruebas obligatorias | pytest cubre validaciones, almacenamiento, fechas límite, filtros y recorridos de interfaz antes del cierre. |
| Código legible | Archivos pequeños, nombres claros y comentarios solo para el cálculo temporal y otras decisiones no evidentes. |
| Validación de entradas | FastAPI valida en el servidor todos los cuerpos y filtros; la interfaz muestra errores en español. |
| Accesible y responsivo | Etiquetas visibles, estados expresados con texto, teclado y comprobación en tamaños de celular y computadora. |

No se detectan incumplimientos que requieran excepción. La dependencia de pruebas de navegador
se justifica por la obligación de probar automáticamente la funcionalidad visible de JavaScript.

## Estructura del proyecto

### Documentación de esta funcionalidad

```text
specs/001-organizar-tareas-academicas/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── api.md
└── checklists/
    └── requirements.md
```

`tasks.md` se generará en la siguiente fase con `/speckit-tasks`.

### Código fuente previsto

```text
app/
├── __init__.py
├── main.py
├── db.py
├── validation.py
└── static/
    ├── index.html
    ├── styles.css
    └── app.js
tests/
├── conftest.py
├── test_api.py
└── test_browser.py
pyproject.toml
```

**Decisión de estructura**: `main.py` define rutas y sirve la interfaz; `db.py` abre
conexiones y ejecuta consultas parametrizadas; `validation.py` concentra límites y reglas
compartidas por las rutas. `app.js` gestiona el estado de la página y la clasificación
temporal. No se añaden capas de repositorio, servicios ni compilación de frontend.

## Diseño de interacción y datos

- La interfaz solicita materias y tareas a la API de la misma instancia. Solo el servidor
  guarda datos; el navegador no mantiene una segunda copia persistente.
- La lista llega ordenada por `fecha_entrega` y orden de creación. Los filtros de materia
  y estado se combinan mediante parámetros de consulta; la interfaz permite limpiarlos.
- El navegador usa su hora local para obtener el inicio del día siguiente a cada fecha de
  entrega. Una tarea pendiente es urgente desde 48 horas reales antes de ese instante y
  vencida desde ese instante. Las completadas no reciben esas etiquetas.
- La interfaz recalcula etiquetas al cargar, al cambiar tareas o filtros, al recuperar el
  foco y al alcanzar el siguiente límite temporal mientras la página permanece abierta.
- El archivo SQLite se crea al iniciar la aplicación. Las claves foráneas se activan en
  cada conexión; la relación tarea → materia impide referencias inexistentes.
- La instancia se ejecuta para un solo estudiante y se recomienda enlazarla a
  `127.0.0.1`. Si se expone a otros dispositivos, todos verán el mismo archivo; ese
  despliegue compartido queda fuera de la primera versión.
- Un manejador de errores de validación de FastAPI transforma los rechazos de la API
  en el formato y los mensajes en español definidos en el contrato HTTP.

## Verificación posterior al diseño

Los artefactos de investigación, modelo, contrato y arranque mantienen los cinco principios:
no introducen funciones fuera del alcance, definen validación antes del guardado, fijan pruebas
automatizadas para cada recorrido y especifican la comprobación responsiva y accesible.
Las decisiones de almacenamiento y tiempo no dejan aclaraciones pendientes.
