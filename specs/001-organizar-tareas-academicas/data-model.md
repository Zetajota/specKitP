# Modelo de datos

## Materia

| Campo | Tipo lógico | Reglas |
|-------|-------------|--------|
| id | Identificador entero | Se asigna al crear; clave primaria. |
| nombre | Texto | Obligatorio, de 1 a 80 caracteres tras quitar espacios extremos. |
| color | Texto | Obligatorio, formato `#RRGGBB`. Es un apoyo visual; el nombre siempre es visible. |

Se permiten nombres repetidos: cada materia se identifica por `id`. No existe operación de
edición o eliminación en esta versión.

## Tarea

| Campo | Tipo lógico | Reglas |
|-------|-------------|--------|
| id | Identificador entero | Se asigna al crear; clave primaria y orden de creación. |
| materia_id | Identificador entero | Obligatorio; referencia una materia existente. |
| titulo | Texto | Obligatorio, de 1 a 120 caracteres tras quitar espacios extremos. |
| descripcion | Texto opcional | Hasta 1000 caracteres; vacío tras quitar espacios se guarda como ausente. |
| fecha_entrega | Fecha civil | Obligatoria, formato `AAAA-MM-DD`; se permiten fechas pasadas. |
| completada | Booleano | Inicialmente falso; único estado que se conserva. |

La relación es una materia con cero o más tareas; cada tarea pertenece a una materia.
La clave foránea se comprueba en SQLite y en la validación de la operación de creación.
No hay borrado en esta versión.

## Estados derivados

- **Completada**: `completada = verdadero`; sin etiqueta temporal.
- **Vencida**: tarea pendiente y momento actual igual o posterior al inicio local del día
  siguiente a `fecha_entrega`.
- **Urgente**: tarea pendiente y momento actual dentro del intervalo que empieza 48 horas
  reales antes de ese inicio y termina justo antes de él.
- **Normal**: tarea pendiente que no está vencida ni urgente.

El orden de la lista es `fecha_entrega` ascendente y luego `id` ascendente. Los filtros
por `materia_id` y `completada` se aplican juntos cuando ambos están presentes.

## Validación y errores

El servidor recorta espacios extremos y verifica tipo, longitud, color, fecha y referencias.
La interfaz puede repetir estas comprobaciones para dar respuesta inmediata, pero el servidor
es la autoridad antes de guardar. Un error de validación deja los datos sin cambios y
devuelve un mensaje legible en español. Los cambios de estado alternan entre pendiente y
completada; no hay estados intermedios.
