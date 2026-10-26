# Contrato de la interfaz HTTP

Todas las rutas pertenecen a la misma instancia FastAPI. Los cuerpos y respuestas de datos
usan JSON. Los textos de error visibles para el usuario están en español. No hay autenticación
en esta versión; la instancia se usa de forma local para una sola persona.

## Página y recursos

- `GET /`: devuelve la página HTML principal.
- `GET /static/styles.css` y `GET /static/app.js`: devuelven los recursos de la interfaz.

## Materias

| Operación | Entrada | Éxito |
|-----------|---------|-------|
| `GET /api/materias` | Ninguna | `200`: lista de `{id, nombre, color}` en orden de creación. |
| `POST /api/materias` | `{nombre, color}` | `201`: materia creada. |

`nombre` se recorta y admite 1–80 caracteres. `color` admite `#RRGGBB`.
No se ofrecen rutas de edición ni borrado.

## Tareas

| Operación | Entrada | Éxito |
|-----------|---------|-------|
| `GET /api/tareas` | Consultas opcionales `materia_id` y `estado` | `200`: lista ordenada de tareas. |
| `POST /api/tareas` | `{materia_id, titulo, descripcion?, fecha_entrega}` | `201`: tarea creada. |
| `PATCH /api/tareas/{id}/estado` | `{completada: true/false}` | `200`: tarea actualizada. |

Cada tarea de respuesta contiene `id`, `materia_id`, `titulo`, `descripcion`
(`null` si no existe), `fecha_entrega` en `AAAA-MM-DD` y `completada`.
`estado` acepta `pendiente` o `completada`; los filtros omitidos muestran todos.
Si ambos filtros se envían, se aplican juntos. El orden es `fecha_entrega` y luego `id`,
ambos ascendentes. La API no guarda ni devuelve la etiqueta temporal.

`titulo` se recorta y admite 1–120 caracteres; `descripcion` se recorta y admite hasta
1000. `fecha_entrega` debe ser una fecha real; `materia_id` debe existir. Una fecha
pasada es válida. `completada` empieza en `false`.

## Errores

- `422`: entrada o filtro inválido, con `{error: mensaje_en_español}` que identifica el
  campo y, para longitudes, el límite. No se guardan cambios.
- `404`: tarea o materia indicada no existe, con `{error: mensaje_en_español}`.
- `500`: fallo de almacenamiento, con mensaje general en español; no se afirma que se
  haya guardado el cambio.

La interfaz muestra el mensaje de error y mantiene el formulario o estado previo para que
el estudiante pueda corregirlo. No se exponen rutas de eliminación.
