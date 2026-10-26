# Modelo de datos: Constancia de recordatorio

## Relación con la tarea existente

Se reutilizan `tareas.id`, `tareas.materia_id`, `tareas.titulo`,
`tareas.fecha_entrega` y `tareas.completada`. La materia aporta el nombre
que aparece en el aviso.

## Constancia

| Campo | Tipo lógico | Reglas |
|-------|-------------|--------|
| tarea_id | Identificador entero | Obligatorio; referencia una tarea existente. |
| dia_local | Fecha civil | Obligatoria en formato `AAAA-MM-DD`; día en que se mostró el aviso. |

La pareja `(tarea_id, dia_local)` es única. Solo se crea si la tarea sigue pendiente
y su fecha de entrega es el día calendario siguiente a `dia_local`.
No se borra ni se edita en esta versión.

## Transiciones

- **Elegible**: tarea pendiente, entrega mañana y sin constancia para hoy.
- **Registrado**: se creó la constancia; solo entonces se muestra el aviso.
- **No elegible**: tarea completada, entrega en otro día o constancia ya existente.

Un registro repetido devuelve «ya registrado» sin crear otro. El cierre visual
del aviso no cambia su constancia.
