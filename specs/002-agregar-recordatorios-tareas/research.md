# Investigación y decisiones

## Día de recordatorio

**Decisión**: El navegador obtiene la fecha calendario local. El servidor usa esa fecha
para seleccionar tareas con entrega al día siguiente.

**Motivo**: La especificación usa la hora local del dispositivo. Pasar solo el día
calendario evita confundir «un día antes» con un intervalo de 24 horas.

**Alternativas consideradas**: Contar 24 horas desde el plazo de entrega produciría
avisos en el mismo día de entrega; depender de la zona del servidor podría diferir
de la del estudiante.

## Constancia sin duplicados

**Decisión**: Guardar en SQLite una constancia única por tarea y día local. El servidor
registra la constancia antes de que la interfaz muestre el aviso.

**Motivo**: Un registro único impide repetir el aviso tras recargar y evita que dos
pestañas abiertas muestren el mismo recordatorio.

**Alternativas consideradas**: Guardarlo solo en la memoria de la página se perdería al
recargar. Guardarlo solo en el navegador podría duplicar avisos en otro navegador
del mismo dispositivo.

## Entrega visible

**Decisión**: Usar un aviso dentro de la página con texto y control de cierre.

**Motivo**: El estudiante pidió avisos solo mientras la aplicación está abierta y el
proyecto mantiene un solo proceso local.

**Alternativas consideradas**: Notificaciones del sistema, correo y servicios de
fondo quedan fuera de la especificación.
