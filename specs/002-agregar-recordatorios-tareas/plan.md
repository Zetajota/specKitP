# Plan de implementación: Recordatorios de tareas pendientes

**Rama de referencia**: `002-agregar-recordatorios-tareas` | **Fecha**: 2026-10-26 | **Especificación**: [spec.md](spec.md)

## Resumen

Añadir avisos dentro de la aplicación durante el día calendario anterior a la entrega de
cada tarea pendiente. El navegador determina el día local y comprueba los avisos al abrir,
al llegar a medianoche y al recuperar el foco. FastAPI y SQLite conservan una constancia
por tarea y día para evitar duplicados entre recargas. No se agregan servicios externos,
cuentas ni notificaciones cuando la página está cerrada.

## Contexto técnico

**Lenguaje y versión**: Python 3.12 y JavaScript, HTML y CSS sin frameworks.

**Dependencias principales**: FastAPI y Uvicorn ya instalados; `sqlite3` de Python.

**Almacenamiento**: El archivo SQLite existente, con una tabla adicional de constancias.

**Pruebas**: pytest, `httpx` y `pytest-playwright` ya configurados.

**Plataforma de destino**: La aplicación web local existente, en celular y computadora.

**Tipo de proyecto**: Un solo proyecto; ampliación de `app/` y `tests/`.

**Objetivos de rendimiento**: Consultar y mostrar recordatorios para 100 tareas durante
el inicio o regreso a la página sin bloquear los controles de tareas.

**Restricciones**: Un usuario por instancia; español en avisos y documentos; sin avisos
fuera de la aplicación abierta; exactamente un aviso por tarea y día de recordatorio.

**Escala y alcance**: Hasta 100 tareas como volumen de aceptación; no se editan fechas
de entrega en esta versión.

## Comprobación de la constitución

*Puerta de entrada revisada antes y después del diseño: conforme.*

| Principio | Aplicación al diseño |
|-----------|----------------------|
| Simplicidad primero | Una tabla nueva y dos operaciones HTTP; se reutilizan las rutas, estilos y pruebas existentes. |
| Pruebas obligatorias | Las pruebas de API y navegador preceden cada cambio y cubren fechas, duplicados, estados y teclado. |
| Código legible | Nombres claros y funciones pequeñas; se documenta el límite de medianoche local. |
| Validación de entradas | El día local y el identificador de tarea se validan antes de consultar o guardar. |
| Accesible y responsivo | Avisos con texto, control de cierre por teclado y región anunciable en ambas pantallas. |

## Estructura del proyecto

### Documentación de esta funcionalidad

```text
specs/002-agregar-recordatorios-tareas/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── api.md
└── tasks.md
```

### Código fuente afectado

```text
app/
├── db.py
├── main.py
├── validation.py
└── static/
    ├── index.html
    ├── styles.css
    └── app.js
tests/
├── test_api.py
└── test_browser.py
```

**Decisión de estructura**: Se amplían los archivos existentes para mantener un solo
proyecto pequeño. No se añade un proceso de fondo, otro servidor ni un framework web.

## Flujo de aviso

1. El navegador calcula el día calendario local actual y solicita las tareas pendientes
   que se entregan al día siguiente y todavía no tienen constancia.
2. Antes de mostrar cada aviso, solicita registrar su constancia. La operación es atómica:
   solo una pestaña recibe la confirmación para mostrar ese aviso.
3. El aviso indica título, materia y fecha de entrega. Se puede cerrar con teclado.
4. Al comenzar un nuevo día local y al recuperar el foco, se repite la evaluación.
5. Si guardar la constancia falla, se muestra un error en español y no se presenta el
   recordatorio como registrado. No se inventa un aviso cuando la página está cerrada.

## Verificación posterior al diseño

El modelo y el contrato conservan las reglas de la especificación: día local anterior,
solo tareas pendientes, ausencia de duplicados y avisos accesibles. Las pruebas previstas
cubren los casos de medianoche, reapertura y varias tareas. No quedan decisiones
técnicas sin resolver para generar las tareas.
