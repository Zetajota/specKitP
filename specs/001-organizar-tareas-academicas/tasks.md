# Tareas: Organización de tareas académicas

**Entrada**: Documentos de diseño en `specs/001-organizar-tareas-academicas/`.

**Prerrequisitos**: [plan.md](plan.md), [spec.md](spec.md), [data-model.md](data-model.md),
[contrato HTTP](contracts/api.md) y [quickstart.md](quickstart.md).

**Pruebas**: Obligatorias por la constitución; se escriben antes de la funcionalidad que comprueban.

**Organización**: Cada historia tiene sus pruebas y un incremento funcional demostrable.

## Formato: `[ID] [P?] [Historia] Descripción`

- `[P]`: puede hacerse en paralelo con otra tarea marcada en la misma etapa porque usa archivos distintos y no depende de trabajo inconcluso.
- `[US1]`, `[US2]`, `[US3]`: historia de usuario correspondiente.
- Todas las rutas son relativas a la raíz del proyecto.

## Fase 1: Preparación

**Objetivo**: Dejar instalable un único proyecto Python sin contenedores ni compilación de frontend.

- [X] T001 Crear `pyproject.toml` para Python 3.12 con FastAPI y Uvicorn; añadir dependencias de pruebas pytest, httpx y pytest-playwright y la configuración para descubrir `tests/`.
- [X] T002 Crear `app/__init__.py`, `app/main.py` y `app/static/index.html` como esqueleto mínimo de una sola aplicación que sirve la página desde FastAPI.
- [X] T003 Crear `tests/conftest.py` con una instancia de prueba, archivo SQLite temporal por prueba y servidor local para los recorridos de navegador, sin tocar el archivo de datos normal.

## Fase 2: Base común

**Objetivo**: Preparar almacenamiento e interfaz compartidos que requieren las tres historias.

**Puerta**: Terminar esta fase antes de implementar las historias.

- [X] T004 Crear `app/db.py` con conexión SQLite parametrizada, creación de tablas `materias` y `tareas`, clave foránea de tarea a materia y `PRAGMA foreign_keys = ON` por conexión; usar el `id` de tarea como orden de creación y no añadir borrado.
- [X] T005 Crear `app/validation.py` con constantes de límites, normalización de espacios y construcción de errores en español; dejar la validación definitiva antes de cada escritura.
- [X] T006 Configurar en `app/main.py` la ruta `GET /`, los recursos `/static/styles.css` y `/static/app.js`, y el manejador de errores de entrada con formato `{error: mensaje_en_español}`.
- [X] T007 [P] Crear `app/static/styles.css` con estilos base legibles, foco visible y distribución adaptable a celular y computadora; el color de materia debe ser auxiliar al texto.

## Fase 3: Historia de usuario 1 — Registrar materias y tareas (P1) 🎯 MVP

**Objetivo**: Registrar una materia y tareas asociadas y conservarlas entre sesiones.

**Prueba independiente**: Crear una materia y una tarea con y sin descripción, recargar la página
y comprobar que persisten; entradas inválidas no generan registros.

### Pruebas previas

- [X] T008 [P] [US1] Escribir en `tests/test_api.py` pruebas de `GET/POST /api/materias` y `POST /api/tareas`: nombre obligatorio de 1 a 80 caracteres, color `#RRGGBB`, título obligatorio de 1 a 120, descripción opcional de hasta 1000, recorte de espacios, fecha civil válida incluso pasada, materia existente, rechazo de tipos inválidos y mensajes 422/404 en español.
- [X] T009 [P] [US1] Escribir en `tests/test_browser.py` el recorrido de registrar materia y tareas con y sin descripción, estados vacíos, corrección tras error y conservación al recargar, en anchos de celular y computadora.

### Implementación

- [X] T010 [US1] Implementar en `app/validation.py` la validación de materia: nombre de 1 a 80 caracteres después de recortar espacios y color obligatorio `#RRGGBB`; rechazar entradas de tipo incorrecto.
- [X] T011 [US1] Implementar en `app/validation.py` la validación de tarea: `materia_id` entero existente, título de 1 a 120 caracteres, descripción opcional de hasta 1000 tras recortar espacios y fecha real `AAAA-MM-DD`, incluida una fecha pasada; una descripción vacía se convierte en ausente.
- [X] T012 [US1] Implementar en `app/db.py` inserción y consulta de materias y tareas con consultas parametrizadas, `completada = false` al crear, relación íntegra y conservación tras cerrar y reabrir la aplicación.
- [X] T013 [US1] Implementar en `app/main.py` `GET /api/materias`, `POST /api/materias`, `POST /api/tareas` y una primera `GET /api/tareas` sin filtros, con respuestas y errores del contrato; no exponer rutas de edición o borrado.
- [X] T014 [US1] Completar en `app/static/index.html` formularios etiquetados de materia y tarea, selector de materia, lista de tareas y mensajes para ausencia de materias o tareas.
- [X] T015 [US1] Implementar en `app/static/app.js` solicitudes a la API, presentación de materias y tareas, guardado sin duplicación, mensajes de error en español y conservación del formulario ante un fallo.
- [X] T016 [US1] Ajustar `app/static/styles.css` para que formularios y lista sean legibles en celular y computadora, con controles alcanzables por teclado y texto de materia siempre visible.
- [X] T017 [US1] Ejecutar `tests/test_api.py` y `tests/test_browser.py` para el recorrido US1 y corregir en `app/validation.py`, `app/db.py`, `app/main.py` o `app/static/` hasta que pasen sus pruebas.

**Punto de control**: US1 funciona sin las etiquetas temporales ni los filtros de US2 y US3.

## Fase 4: Historia de usuario 2 — Reconocer tareas próximas y vencidas (P2)

**Objetivo**: Ordenar las tareas por entrega y distinguir urgentes y vencidas con la hora local.

**Prueba independiente**: Con tareas preparadas, comprobar el orden y las etiquetas en el
instante anterior, exacto y posterior a los límites de 48 horas y vencimiento.

### Pruebas previas

- [X] T018 [P] [US2] Ampliar `tests/test_api.py` con fechas desordenadas y empates para exigir `GET /api/tareas` por `fecha_entrega` ascendente y luego `id` ascendente, sin estado temporal persistido.
- [X] T019 [P] [US2] Ampliar `tests/test_browser.py` con reloj controlado y zona local para comprobar tareas normales, urgentes, vencidas y completadas; cubrir exactamente 48 horas antes, inicio del día siguiente, cambio de horario, actualización con la lista abierta y etiquetas de texto además del color.

### Implementación

- [X] T020 [US2] Ajustar `app/db.py` y `app/main.py` para entregar `GET /api/tareas` ordenado por `fecha_entrega` y luego `id`, conservando las fechas como días civiles y sin guardar «urgente» o «vencida».
- [X] T021 [US2] Implementar en `app/static/app.js` el inicio local del día siguiente a `fecha_entrega`; clasificar una tarea pendiente como urgente desde 48 horas reales antes de ese instante y vencida desde ese instante, sin etiquetas temporales para una completada.
- [X] T022 [US2] Implementar en `app/static/app.js` el recálculo de etiquetas al abrir la lista, al recuperar el foco y al cruzar un límite temporal mientras la página sigue abierta; no equiparar 48 horas reales con dos días de calendario.
- [X] T023 [US2] Ajustar `app/static/styles.css` y `app/static/index.html` para destacar vencidas y urgentes con texto y señales visuales que no dependan solo del color de la materia.
- [X] T024 [US2] Ejecutar las pruebas US2 de `tests/test_api.py` y `tests/test_browser.py` y corregir `app/db.py`, `app/main.py` o `app/static/` hasta que pasen.

**Punto de control**: US2 clasifica y ordena tareas existentes sin necesitar filtros.

## Fase 5: Historia de usuario 3 — Completar y filtrar tareas (P3)

**Objetivo**: Cambiar el estado de una tarea y combinar filtros por materia y estado.

**Prueba independiente**: Completar y reabrir una tarea; filtrar por materia, por estado y
ambos a la vez; limpiar filtros y conservar el estado al recargar.

### Pruebas previas

- [X] T025 [P] [US3] Ampliar `tests/test_api.py` para `PATCH /api/tareas/{id}/estado` con booleano obligatorio, persistencia y 404, y para `GET /api/tareas?materia_id=&estado=` con filtros aislados/combinados, valores inválidos 422 y orden estable.
- [X] T026 [P] [US3] Ampliar `tests/test_browser.py` para completar y reabrir tareas, eliminar etiquetas temporales al completar, recalcular al volver a pendiente, combinar y limpiar filtros y mostrar un mensaje cuando no haya coincidencias.

### Implementación

- [X] T027 [US3] Implementar en `app/db.py` cambio de `completada` entre verdadero y falso y consulta de tareas con filtros combinables `materia_id` y estado, conservando orden por fecha e `id`.
- [X] T028 [US3] Implementar en `app/main.py` `PATCH /api/tareas/{id}/estado` con `{completada: true/false}` y ampliar `GET /api/tareas` para filtros válidos `pendiente` y `completada`, con errores 404/422 en español.
- [X] T029 [US3] Añadir en `app/static/index.html` control etiquetado de completado, filtros de materia y estado y acción de limpiar filtros; mantener navegación por teclado.
- [X] T030 [US3] Implementar en `app/static/app.js` cambio de estado, filtros combinados, limpieza, actualización de lista y mensaje para cero coincidencias, sin presentar como guardado un cambio fallido.
- [X] T031 [US3] Ejecutar las pruebas US3 de `tests/test_api.py` y `tests/test_browser.py` y corregir `app/db.py`, `app/main.py` o `app/static/` hasta que pasen.

**Punto de control**: Las tres historias funcionan y pueden demostrarse por separado con datos preparados.

## Fase 6: Revisión final

**Objetivo**: Comprobar los criterios transversales y dejar instrucciones de ejecución.

- [X] T032 [P] Ampliar `tests/test_api.py` con 100 tareas para comprobar orden y combinación de filtros, y con fallo de almacenamiento para comprobar que no se comunica éxito falso.
- [X] T033 [P] Ampliar `tests/test_browser.py` con recorridos de teclado, etiquetas accesibles, mensajes y anchos de celular/computadora para CE-005.
- [X] T034 Actualizar `specs/001-organizar-tareas-academicas/quickstart.md` con comandos definitivos de instalación, ejecución y pruebas; documentar que cada instancia usa un archivo local y que una instancia expuesta a otros dispositivos compartiría datos.
- [X] T035 Ejecutar toda la suite con `python -m pytest` y seguir `specs/001-organizar-tareas-academicas/quickstart.md`; registrar en ese archivo los resultados de CE-002 a CE-005 y la prueba de uso pendiente o realizada para CE-001.

## Dependencias y orden de ejecución

- **Preparación → Base común**: T001–T003 antes de T004–T007.
- **Base común → US1**: T004–T007 antes de T008–T017.
- **US1 → US2 y US3**: ambas usan materias y tareas existentes; pueden desarrollarse después de
  US1 con archivos separados o una secuencia coordinada. Sus pruebas son independientes con
  datos de prueba preparados.
- **US2 y US3 → Revisión final**: T032–T035 requieren los tres recorridos disponibles.
- **Dentro de cada historia**: escribir pruebas y observar que fallan; después validar,
  almacenar, exponer la API e integrar la interfaz; cerrar solo con pruebas que pasen.

## Oportunidades de trabajo en paralelo

- **US1**: T008 y T009 se pueden escribir en paralelo porque usan `tests/test_api.py` y
  `tests/test_browser.py` respectivamente.
- **US2**: T018 y T019 se pueden escribir en paralelo por la misma separación de archivos.
- **US3**: T025 y T026 se pueden escribir en paralelo por la misma separación de archivos.
- **Revisión final**: T032 y T033 se pueden escribir en paralelo. T007 puede avanzar junto
  con T005–T006 si la estructura de T002 ya está creada.
- Los cambios posteriores en `app/main.py`, `app/db.py` o `app/static/app.js` se
  coordinan en secuencia para evitar conflictos.

## Estrategia de entrega

1. Completar preparación y base común.
2. Entregar US1 como producto mínimo: registro, lista y conservación, con pruebas verdes.
3. Añadir US2 y verificar por separado orden y límites de tiempo.
4. Añadir US3 y verificar por separado estado y filtros.
5. Ejecutar revisión final, comprobar la constitución y usar la guía de arranque.

Las tareas marcadas `[P]` no dependen entre sí dentro de su etapa. Ninguna historia se
considera terminada sin sus pruebas automatizadas.

## Fase 7: Convergencia

- [X] T036 Completar en `app/static/app.js`, `app/static/styles.css` y `tests/test_browser.py` la clasificación y presentación de urgente/vencida, incluidos los límites de 48 horas reales, según RF-006, RF-007 y RF-008 (missing).
- [X] T037 Completar en `app/db.py`, `app/main.py`, `app/static/index.html`, `app/static/app.js`, `tests/test_api.py` y `tests/test_browser.py` el cambio de estado y los filtros combinados según RF-009 y RF-010 (missing).
- [X] T038 Completar en `tests/test_api.py` y `tests/test_browser.py` la comprobación de 100 tareas, fallos de almacenamiento, teclado y tamaños de pantalla según CE-002 y CE-005 (partial).
