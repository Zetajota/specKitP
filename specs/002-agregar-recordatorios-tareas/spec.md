# Especificación de la funcionalidad: Recordatorios de tareas pendientes

**Rama de la funcionalidad**: No creada

**Fecha de creación**: 2026-10-26

**Estado**: Borrador

**Descripción de origen**: El estudiante recibe una notificación un día antes de la fecha de entrega de cada tarea pendiente. El estudiante aclaró que basta con recibirla mientras la aplicación está abierta.

## Escenarios de usuario y pruebas *(obligatorio)*

### Historia de usuario 1: Recibir un recordatorio oportuno (prioridad: P1)

Como estudiante, quiero recibir un aviso de cada tarea pendiente el día anterior a su entrega para poder organizar el tiempo que me queda.

**Motivo de la prioridad**: Es el beneficio principal de la funcionalidad.

**Prueba independiente**: Preparar una tarea pendiente con entrega al día siguiente, mantener abierta la aplicación y comprobar que aparece un aviso visible con la tarea y su materia.

**Escenarios de aceptación**:

1. **Dado** que una tarea pendiente se entrega mañana, **cuando** comienza el día anterior a la entrega y la aplicación está abierta, **entonces** aparece un recordatorio con el título, la materia y la fecha de entrega.
2. **Dado** que abro la aplicación durante el día anterior a la entrega de una tarea pendiente, **cuando** se muestran mis tareas, **entonces** recibo el recordatorio aunque no tuviera la página abierta a medianoche.
3. **Dado** que varias tareas pendientes vencen mañana, **cuando** corresponde recordarlas, **entonces** recibo un aviso identificable para cada una.
4. **Dado** que no hay tareas pendientes con entrega mañana, **cuando** consulto la aplicación, **entonces** no recibo recordatorios.

---

### Historia de usuario 2: Evitar avisos repetidos o irrelevantes (prioridad: P2)

Como estudiante, quiero ver cada recordatorio una sola vez y no recibir avisos de tareas completadas para mantener útiles las notificaciones.

**Motivo de la prioridad**: Evita ruido y refuerza la confianza en los avisos.

**Prueba independiente**: Mostrar un recordatorio, recargar y volver a abrir la aplicación durante el mismo día; comprobar que no reaparece. Completar otra tarea antes del día de aviso y comprobar que no genera recordatorio.

**Escenarios de aceptación**:

1. **Dado** que ya se mostró el recordatorio de una tarea, **cuando** recargo o vuelvo a abrir la aplicación el mismo día, **entonces** no se repite.
2. **Dado** que completé una tarea antes del día de aviso, **cuando** llega el día anterior a su entrega, **entonces** no recibo un recordatorio de esa tarea.
3. **Dado** que una tarea ya está en su día de entrega o venció, **cuando** abro la aplicación, **entonces** no se emite un recordatorio tardío de «un día antes».

### Casos límite

- «Un día antes» significa el día calendario inmediatamente anterior a la fecha de entrega, desde las 00:00 hasta antes de las 00:00 del día de entrega, según la hora local del dispositivo.
- Si la aplicación permanece abierta cuando comienza ese día, el aviso aparece sin recargar la página; al volver a verla después de una suspensión, se vuelve a evaluar la fecha.
- Una tarea creada durante el día anterior a su entrega puede generar el aviso en esa misma sesión.
- Si el estudiante marca una tarea como completada antes de mostrarse el aviso, no se emite. Si la completa después de verlo, el aviso ya emitido no se repite.
- El aviso identifica la tarea por su título y materia, incluso si hay títulos repetidos.
- Si no se puede conservar la constancia de que se mostró un recordatorio, se informa del problema y no se afirma que el aviso quedó registrado.

## Requisitos *(obligatorio)*

### Requisitos funcionales

- **RF-001**: El sistema DEBE identificar las tareas pendientes cuya fecha de entrega es el día calendario siguiente al día local actual del dispositivo.
- **RF-002**: El sistema DEBE mostrar en la aplicación abierta un recordatorio por cada tarea identificada, con título, materia y fecha de entrega legibles.
- **RF-003**: El sistema DEBE evaluar los recordatorios al abrir la aplicación, al comenzar un nuevo día local mientras permanece abierta y al recuperar el foco.
- **RF-004**: El sistema DEBE conservar qué recordatorios ya se mostraron para no repetirlos al recargar o reabrir la aplicación durante el mismo día.
- **RF-005**: El sistema NO DEBE mostrar recordatorios de tareas completadas, de tareas cuyo día de entrega ya comenzó ni de tareas vencidas.
- **RF-006**: Los recordatorios DEBEN poder leerse y cerrarse mediante teclado y ser comprensibles sin depender del color, en celular y computadora.
- **RF-007**: El sistema DEBE informar en español cuando no pueda registrar que un recordatorio ya se mostró, sin afirmar que el registro fue exitoso.

### Entidades principales

- **Tarea existente**: aporta título, materia, fecha de entrega y estado pendiente o completada.
- **Constancia de recordatorio**: identifica la tarea y el día local para el que se mostró el aviso, con el fin de evitar repeticiones.

## Criterios de éxito *(obligatorio)*

### Resultados medibles

- **CE-001**: En pruebas de fechas, el 100 % de las tareas pendientes con entrega al día siguiente genera exactamente un recordatorio durante ese día mientras la aplicación está abierta.
- **CE-002**: El 100 % de las tareas completadas o fuera del día de recordatorio genera cero avisos.
- **CE-003**: Al recargar o reabrir la aplicación durante el mismo día, el 100 % de los recordatorios ya mostrados permanece sin repetirse.
- **CE-004**: El 100 % de los avisos contiene título, materia y fecha de entrega, y puede cerrarse con teclado en tamaños de celular y computadora.

## Suposiciones

- Esta funcionalidad amplía la aplicación de tareas académicas existente; no agrega cuentas ni sincronización entre dispositivos.
- «Notificación» significa un aviso visible dentro de la aplicación mientras está abierta. No se envían avisos del sistema, correos ni mensajes cuando está cerrada.
- La fecha y la hora local del dispositivo determinan el día de recordatorio; el plazo de entrega y la clasificación «urgente» existentes no cambian.
- Cada tarea recibe como máximo un recordatorio por su fecha de entrega actual. La primera versión no permite editar fechas de entrega, por lo que no se requiere un nuevo aviso por reprogramación.
