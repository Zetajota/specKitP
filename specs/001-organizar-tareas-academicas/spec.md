# Especificación de la funcionalidad: Organización de tareas académicas

**Rama de la funcionalidad**: No creada

**Fecha de creación**: 2026-10-26

**Estado**: Borrador

**Descripción de origen**: Aplicación para estudiantes de la UPB que permite registrar materias, crear tareas con fecha de entrega, consultar prioridades, completar tareas y filtrarlas, sin inicio de sesión.

## Aclaraciones

### Sesión 2026-10-26

- Pregunta: ¿Se podrán borrar materias y qué ocurrirá con sus tareas? → Respuesta: No se podrán borrar materias en esta versión; sus tareas permanecen asociadas.
- Pregunta: ¿Qué límites máximos tendrán el nombre de la materia, el título y la descripción de la tarea? → Respuesta: 80, 120 y 1000 caracteres, respectivamente.
- Pregunta: ¿Desde qué momento se calcula el plazo de 48 horas para mostrar «urgente»? → Respuesta: Se cuentan 48 horas reales hacia atrás desde el inicio del día siguiente al de entrega, según la hora local del dispositivo.

## Escenarios de usuario y pruebas *(obligatorio)*

### Historia de usuario 1: Registrar materias y tareas (prioridad: P1)

Como estudiante, quiero registrar mis materias y sus tareas para reunir mis pendientes académicos en un solo lugar.

**Motivo de la prioridad**: Sin materias ni tareas no existe una lista útil de pendientes.

**Prueba independiente**: Registrar una materia y una tarea asociada, cerrar y volver a abrir la aplicación y comprobar que ambas siguen disponibles.

**Escenarios de aceptación**:

1. **Dado** que no hay materias, **cuando** registro una con nombre y color válidos, **entonces** aparece en la lista de materias y puedo asignarle tareas.
2. **Dado** que existe una materia, **cuando** creo una tarea con título y fecha de entrega válidos, con o sin descripción, **entonces** la tarea aparece asociada a esa materia.
3. **Dado** que un campo obligatorio está vacío o contiene solo espacios, **cuando** intento guardar, **entonces** veo un mensaje claro y no se crea el registro.
4. **Dado** que ya guardé materias y tareas, **cuando** cierro y vuelvo a abrir la aplicación en el mismo dispositivo, **entonces** las encuentro con sus datos y estados conservados.
5. **Dado** que el nombre, el título o la descripción excede su límite, **cuando** intento guardar, **entonces** veo el límite permitido y el registro no se guarda.

---

### Historia de usuario 2: Reconocer tareas próximas y vencidas (prioridad: P2)

Como estudiante, quiero ver mis tareas ordenadas por entrega y distinguir las urgentes y vencidas para decidir qué atender primero.

**Motivo de la prioridad**: La prioridad temporal convierte la lista de tareas en una herramienta de organización.

**Prueba independiente**: Crear tareas con fechas pasadas, dentro y fuera de las próximas 48 horas, y verificar su orden y clasificación.

**Escenarios de aceptación**:

1. **Dado** que hay tareas con distintas fechas, **cuando** consulto la lista, **entonces** aparecen de la fecha de entrega más próxima a la más lejana.
2. **Dado** que una tarea pendiente terminó su día de entrega, **cuando** consulto la lista, **entonces** se destaca como «vencida».
3. **Dado** que faltan 48 horas reales o menos para el inicio del día siguiente al de entrega de una tarea pendiente, **cuando** consulto la lista, **entonces** aparece como «urgente», salvo que ya esté vencida.
4. **Dado** que una tarea está completada, **cuando** consulto la lista, **entonces** se identifica como completada y no se presenta como urgente ni vencida.

---

### Historia de usuario 3: Completar y filtrar tareas (prioridad: P3)

Como estudiante, quiero marcar tareas como completadas y filtrar por materia o estado para revisar solo los pendientes relevantes.

**Motivo de la prioridad**: Facilita el seguimiento diario cuando la lista crece.

**Prueba independiente**: Completar una tarea y verificar los filtros por materia, por estado y combinados.

**Escenarios de aceptación**:

1. **Dado** que una tarea está pendiente, **cuando** la marco como completada, **entonces** su estado cambia y se conserva al volver a abrir la aplicación.
2. **Dado** que una tarea está completada, **cuando** la marco como pendiente, **entonces** vuelve a aparecer entre las tareas pendientes y se recalcula su condición temporal.
3. **Dado** que existen tareas de varias materias, **cuando** selecciono una materia, **entonces** solo veo sus tareas.
4. **Dado** que existen tareas pendientes y completadas, **cuando** selecciono un estado, **entonces** solo veo las tareas de ese estado.
5. **Dado** que selecciono materia y estado, **cuando** consulto la lista, **entonces** se aplican ambos filtros a la vez; al limpiar los filtros vuelvo a ver todas las tareas.

### Casos límite

- Si no hay materias, se muestra un estado vacío con una acción para registrar la primera.
- Si no hay tareas o ningún resultado coincide con los filtros, se muestra un mensaje claro sin inventar resultados.
- Una tarea debe tener una materia existente; si esta no está disponible, se impide guardarla y se informa el motivo.
- Una fecha de entrega pasada se acepta para registrar pendientes atrasados.
- Durante el día de entrega, la tarea aún no está vencida; vence en el instante en que comienza el día siguiente según la hora local del dispositivo.
- En el instante exacto de 48 horas reales antes del inicio del día siguiente al de entrega, la tarea pendiente se considera urgente; un instante antes no lo es.
- La clasificación se recalcula al consultar la lista y al cruzar un límite de urgencia o vencimiento mientras la lista está abierta. Los cambios de horario local no convierten las 48 horas reales en dos días de calendario.
- Si dos tareas tienen la misma fecha de entrega, conservan el orden en que fueron creadas.
- Los campos de texto se validan tras quitar espacios al inicio y al final; una descripción vacía equivale a no proporcionar descripción.
- Los límites de caracteres se aplican después de quitar los espacios al inicio y al final; el valor exacto del límite se acepta y uno mayor se rechaza.
- Si no se puede conservar un cambio, se informa del error y no se presenta como guardado.

## Requisitos *(obligatorio)*

### Requisitos funcionales

- **RF-001**: El estudiante DEBE poder registrar una materia con nombre de 1 a 80 caracteres y un color válido.
- **RF-002**: El estudiante DEBE poder crear una tarea asociada a una materia existente, con título de 1 a 120 caracteres, fecha de entrega válida y descripción opcional de hasta 1000 caracteres.
- **RF-003**: El sistema DEBE quitar espacios al inicio y al final de los campos de texto, validar todos los datos proporcionados por el estudiante antes de guardarlos y mostrar errores comprensibles en español que indiquen el límite incumplido.
- **RF-004**: El sistema DEBE conservar materias, tareas y estados para el mismo usuario en el mismo dispositivo entre sesiones.
- **RF-005**: El sistema DEBE mostrar las tareas ordenadas por fecha de entrega ascendente; en caso de empate, por orden de creación.
- **RF-006**: El sistema DEBE clasificar una tarea pendiente como «vencida» desde el inicio del día siguiente al de entrega, según la hora local del dispositivo.
- **RF-007**: El sistema DEBE clasificar una tarea pendiente como «urgente» desde el instante situado 48 horas reales antes del inicio del día siguiente al de entrega hasta ese inicio, sin incluirlo; DEBE recalcular la clasificación al consultar la lista y al cruzar ese límite mientras permanezca abierta.
- **RF-008**: El sistema DEBE destacar visualmente las tareas vencidas y urgentes e identificar cada condición también con texto, sin depender solo del color.
- **RF-009**: El estudiante DEBE poder cambiar una tarea entre pendiente y completada; las completadas no DEBEN recibir etiquetas de urgencia o vencimiento.
- **RF-010**: El estudiante DEBE poder filtrar tareas por una materia, por estado pendiente o completado, y combinar ambos filtros; también DEBE poder limpiar los filtros.
- **RF-011**: El sistema DEBE mostrar estados vacíos y errores de guardado comprensibles.
- **RF-012**: La interfaz DEBE permitir completar los flujos principales en celular y computadora, con controles identificables, navegación por teclado y texto legible.
- **RF-013**: La primera versión DEBE funcionar para un solo usuario por dispositivo, sin registro ni inicio de sesión.
- **RF-014**: La primera versión NO DEBE ofrecer la opción de borrar materias; las tareas conservan su materia asociada.

### Entidades principales

- **Materia**: asignatura del estudiante, identificada por un nombre de 1 a 80 caracteres y un color; agrupa tareas.
- **Tarea**: pendiente académico con título de 1 a 120 caracteres, descripción opcional de hasta 1000 caracteres, fecha de entrega, materia asociada, estado pendiente o completada y orden de creación.

## Criterios de éxito *(obligatorio)*

### Resultados medibles

- **CE-001**: Al menos 9 de cada 10 estudiantes de una prueba de uso pueden registrar una materia y su primera tarea en menos de 3 minutos, sin ayuda.
- **CE-002**: En una lista de 100 tareas, la vista ordenada y los filtros muestran el resultado esperado en el 100 % de los casos de aceptación.
- **CE-003**: En pruebas de fechas límite, el 100 % de las tareas pendientes se clasifica correctamente como vencida, urgente o normal.
- **CE-004**: El 100 % de las materias, tareas y estados guardados sigue disponible después de cerrar y volver a abrir la aplicación en el mismo dispositivo, mientras sus datos locales permanezcan intactos.
- **CE-005**: Los flujos de registrar, consultar, completar y filtrar tareas se pueden terminar en una pantalla de celular y otra de computadora, usando teclado cuando corresponda, sin pérdida de funciones.

## Suposiciones

- La fecha de entrega indica un día, sin hora específica; su plazo termina al comenzar el día siguiente según la hora local del dispositivo.
- Los datos pertenecen a una sola persona y permanecen en el dispositivo; no se sincronizan entre dispositivos.
- Se permite registrar tareas con fechas pasadas para organizar pendientes atrasados.
- En esta versión no se incluyen edición ni eliminación de materias o tareas, recordatorios, colaboración ni integración con sistemas de la UPB.
- No se requieren servicios externos para los flujos descritos.
