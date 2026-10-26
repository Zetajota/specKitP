# Tareas: Recordatorios de tareas pendientes

**Entrada**: [spec.md](spec.md), [plan.md](plan.md), [data-model.md](data-model.md) y [contrato HTTP](contracts/api.md).

**Pruebas**: Obligatorias por la constitución. Las pruebas de cada historia se escriben y fallan antes de implementar esa historia.

## Formato: `[ID] [P?] [Historia] Descripción`

`[P]` indica archivos distintos sin dependencia inmediata; `[US1]` y `[US2]`
identifican la historia. Las rutas son relativas a la raíz del proyecto.

## Fase 1: Preparación

**Objetivo**: Confirmar que la aplicación base puede ampliarse sin afectar los recorridos existentes.

- [ ] T001 Ejecutar la suite base de Python 3.12 declarada en `pyproject.toml` y registrar el resultado inicial en `specs/002-agregar-recordatorios-tareas/quickstart.md`.

## Fase 2: Base común

**Objetivo**: Conservar constancias de recordatorio en la base local.

- [ ] T002 Escribir en `tests/test_api.py` una prueba que exija la constancia única por `(tarea_id, dia_local)`, fecha real `AAAA-MM-DD` y referencia a una tarea existente; comprobar que falla inicialmente.
- [ ] T003 Ampliar `app/db.py` con la tabla de constancias, clave foránea a `tareas.id` y unicidad por `(tarea_id, dia_local)`, manteniendo la inicialización de bases existentes.

## Fase 3: Historia de usuario 1 — Recibir un recordatorio oportuno (P1)

**Objetivo**: Mostrar un aviso de cada tarea pendiente con entrega mañana mientras la página está abierta.

**Prueba independiente**: Preparar tareas con entrega mañana, hoy y pasado mañana;
solo las primeras deben generar un aviso con título, materia y fecha, incluso al
cruzar medianoche con la página abierta.

### Pruebas previas

- [ ] T004 [P] [US1] Escribir en `tests/test_api.py` pruebas de `GET /api/recordatorios?dia_local=AAAA-MM-DD` para fecha válida, tareas pendientes que se entregan mañana, varias tareas, orden por identificador, respuesta vacía y error 422 en español.
- [ ] T005 [P] [US1] Escribir en `tests/test_browser.py` pruebas con reloj local controlado para aviso al abrir, tarea creada durante el día previo, cruce de medianoche y regreso al foco, con título, materia y fecha visibles.

### Implementación

- [ ] T006 [US1] Añadir a `app/validation.py` validación estricta de `dia_local` como fecha civil real `AAAA-MM-DD` y cálculo del día calendario siguiente.
- [ ] T007 [US1] Añadir a `app/db.py` consulta de tareas pendientes con entrega al día siguiente de `dia_local`, sin constancia previa, unidas al nombre de su materia y ordenadas por `tarea_id`.
- [ ] T008 [US1] Añadir a `app/main.py` `GET /api/recordatorios` con respuesta `tarea_id`, `titulo`, `materia` y `fecha_entrega`, y rechazo en español de fecha ausente o inválida.
- [X] T009 [US1] Añadir a `app/static/app.js` evaluación del día local al abrir, al llegar a medianoche y al recuperar el foco; solicitar y mostrar avisos elegibles. La confirmación persistente se integra en US2.
- [ ] T010 [US1] Añadir a `app/static/index.html` y `app/static/styles.css` una región de avisos legible, etiquetada, adaptable y con cierre por teclado, sin depender solo del color.
- [ ] T011 [US1] Ejecutar y corregir las pruebas de US1 en `tests/test_api.py` y `tests/test_browser.py` hasta que pasen sin romper la suite base.

## Fase 4: Historia de usuario 2 — Evitar avisos repetidos o irrelevantes (P2)

**Objetivo**: Registrar una sola emisión por tarea y día, y excluir tareas completadas o fuera de fecha.

**Prueba independiente**: Emitir un aviso, recargar y abrir otra pestaña; no debe
repetirse. Completar otra tarea antes de la emisión y comprobar que no aparece.

### Pruebas previas

- [ ] T012 [P] [US2] Escribir en `tests/test_api.py` pruebas de `POST /api/recordatorios/{tarea_id}/marcar`: `201` al registrar, `200` si ya existe o dejó de ser elegible, `404` si falta la tarea, `422` para identificador o día inválido y `500` en español ante fallo de almacenamiento.
- [ ] T013 [P] [US2] Escribir en `tests/test_browser.py` pruebas de ausencia de duplicados tras recarga y dos pestañas, exclusión de tareas completadas o vencidas y cierre del aviso mediante teclado en anchos de celular y computadora.

### Implementación

- [ ] T014 [US2] Añadir a `app/db.py` una operación atómica que compruebe tarea pendiente, entrega mañana y unicidad `(tarea_id, dia_local)` antes de registrar la constancia; devolver si se creó o ya existía.
- [ ] T015 [US2] Añadir a `app/main.py` `POST /api/recordatorios/{tarea_id}/marcar` con respuestas `201/200/404/422/500` y mensajes en español según `contracts/api.md`.
- [X] T016 [US2] Ajustar `app/static/app.js` para presentar un aviso solo tras `registrado: true`, evitar avisos tardíos, conservar el estado visual al recargar e informar fallos de registro sin afirmar éxito.
- [ ] T017 [US2] Ajustar `app/static/index.html` y `app/static/styles.css` para que varios avisos sean distinguibles y su control de cierre mantenga foco visible y lectura por teclado.
- [ ] T018 [US2] Ejecutar y corregir las pruebas de US2 en `tests/test_api.py` y `tests/test_browser.py` hasta que pasen junto a US1.

## Fase 5: Verificación y cierre

- [ ] T019 [P] Ampliar `tests/test_api.py` con 100 tareas y fallo de almacenamiento para confirmar selección, ausencia de duplicados y errores sin falso éxito.
- [ ] T020 [P] Ampliar `tests/test_browser.py` con pruebas de 100 tareas, avisos múltiples, foco, teclado y tamaños de celular y computadora para CE-001 a CE-004.
- [ ] T021 Actualizar `specs/002-agregar-recordatorios-tareas/quickstart.md` con comandos reales y resultados de la suite; ejecutar `python -m pytest` con Python 3.12 y corregir cualquier regresión en `app/` o `tests/`.

## Dependencias y orden

1. T001 confirma la línea base. T002 debe fallar antes de T003.
2. T003 prepara US1. T004 y T005 pueden escribirse en paralelo.
3. US1 se completa antes de US2 porque el registro de avisos utiliza su consulta
   y su interfaz. T012 y T013 pueden escribirse en paralelo.
4. T019 y T020 pueden avanzar en paralelo después de ambas historias; T021 cierra
   el trabajo con la suite completa.
5. Quien edite `app/db.py`, `app/main.py` o `app/static/app.js` integra sus cambios
   antes de que otra persona modifique el mismo archivo.

## Estrategia de entrega

El producto mínimo es US1 tras las fases 1 y 2. US2 añade la garantía de no repetir
avisos. Ninguna historia se considera terminada hasta que sus pruebas automatizadas
pasen y el aviso sea utilizable con teclado.
