# Constitución del proyecto académico de la UPB

## Principios fundamentales

### I. Simplicidad primero

Cada solución DEBE ser la mínima que satisfaga los requisitos actuales y funcione correctamente.
No se DEBEN añadir capas, dependencias ni funciones para necesidades hipotéticas (YAGNI).
Toda complejidad adicional DEBE justificarse con un requisito concreto.

### II. Pruebas obligatorias

Toda funcionalidad DEBE contar con pruebas automatizadas que cubran su comportamiento esperado
antes de considerarse terminada. Las pruebas pertinentes DEBEN ejecutarse y pasar antes de la
entrega. Esto permite verificar los resultados y detectar regresiones.

### III. Código legible

El código DEBE usar nombres claros y funciones pequeñas con una responsabilidad definida.
Las decisiones y comportamientos que no sean evidentes DEBEN documentarse cerca del código.
La legibilidad facilita la revisión y el mantenimiento del proyecto académico.

### IV. Validación de entradas

Todo dato proporcionado por el usuario DEBE validarse antes de procesarse. La validación DEBE
comprobar formato, tipo, límites y campos obligatorios según corresponda, y los datos inválidos
DEBEN producir un error comprensible sin continuar el procesamiento. Esto evita resultados
incorrectos y fallos evitables.

### V. Accesibilidad y diseño responsivo

Toda interfaz DEBE poder utilizarse en celular y computadora sin pérdida de funciones.
Los controles DEBEN ser accesibles mediante teclado, tener etiquetas comprensibles y mantener
un contraste y una presentación legibles en ambos tamaños de pantalla.

## Restricciones adicionales

La documentación del proyecto DEBE redactarse en español. Las dependencias y decisiones de
arquitectura DEBEN responder a requisitos actuales y quedar justificadas cuando añadan
complejidad. Los mensajes visibles para el usuario DEBEN ser claros y estar en español.

## Flujo de desarrollo

Antes de cerrar una funcionalidad, se DEBEN revisar sus requisitos, validar todas sus entradas,
ejecutar sus pruebas automatizadas y comprobar manualmente la interfaz en tamaños de celular y
computadora cuando corresponda. La revisión del cambio DEBE comprobar los cinco principios y
registrar cualquier incumplimiento antes de la entrega.

## Gobernanza

Esta constitución rige las especificaciones, los planes, las tareas y las revisiones del proyecto.
Toda enmienda DEBE documentar el cambio, su motivo y el impacto en los artefactos existentes;
DEBE ser aprobada por la persona responsable del proyecto antes de entrar en vigor.

La versión sigue el esquema MAYOR.MENOR.PARCHE: MAYOR para eliminar o redefinir principios de
forma incompatible; MENOR para añadir principios o ampliar obligaciones; PARCHE para aclaraciones
sin cambio normativo. Cada cambio DEBE actualizar la fecha de última modificación. En cada
entrega se DEBE comprobar el cumplimiento de esta constitución; las excepciones requieren una
enmienda aprobada.

**Versión**: 1.0.0 | **Ratificada**: 2026-10-26 | **Última modificación**: 2026-10-26
