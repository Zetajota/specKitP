# Contrato HTTP: Recordatorios

Las rutas amplían la aplicación FastAPI existente. Las respuestas usan JSON y los
mensajes de error visibles están en español.

## Consultar recordatorios

`GET /api/recordatorios?dia_local=AAAA-MM-DD`

- `dia_local` es obligatorio y debe ser una fecha civil real.
- Respuesta `200`: lista de tareas pendientes cuya `fecha_entrega` es el día
  siguiente y que no tienen constancia para `dia_local`.
- Cada elemento contiene `tarea_id`, `titulo`, `materia` y
  `fecha_entrega`. La lista se ordena por `tarea_id`.
- Una lista vacía significa que no hay avisos pendientes.

## Registrar antes de mostrar

`POST /api/recordatorios/{tarea_id}/marcar` con
`{ "dia_local": "AAAA-MM-DD" }`.

- `201` con `{ "registrado": true }`: se creó la constancia y la interfaz
  puede mostrar el aviso.
- `200` con `{ "registrado": false }`: ya había constancia o la tarea dejó
  de ser elegible; la interfaz no muestra un segundo aviso.
- `404`: la tarea no existe, con `{ "error": "..." }`.
- `422`: identificador o fecha inválidos, con `{ "error": "..." }`.
- `500`: fallo de almacenamiento, con `{ "error": "..." }`; la interfaz
  informa el problema sin afirmar que el aviso quedó registrado.

La operación de registro comprueba elegibilidad y unicidad en una sola transacción.
