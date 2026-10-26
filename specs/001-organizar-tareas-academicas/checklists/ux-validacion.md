# Checklist de experiencia de usuario y validación de datos: Organización de tareas académicas

**Propósito**: Revisar la claridad, integridad y coherencia de los requisitos de experiencia de usuario y validación de datos.
**Fecha de creación**: 2026-10-26
**Funcionalidad**: [Especificación](../spec.md)

**Nota**: Este checklist revisa la calidad de los requisitos escritos, no la implementación.
**Responsable de revisión**: La persona revisora marca `[x]` solo cuando determina que el criterio de calidad del requisito está satisfecho.
**Significado de la marca**: `[x]` indica revisión satisfactoria del requisito; no significa que la funcionalidad esté implementada.

## Integridad de los recorridos de uso

- [ ] CHK001 ¿Están definidos los pasos y resultados esperados para registrar una materia, crear una tarea, consultarla y completarla? [Integridad, Espec. §Historias de usuario 1–3]
- [ ] CHK002 ¿Se especifican estados vacíos distintos para ausencia de materias, ausencia de tareas y filtros sin resultados, con una acción útil cuando corresponde? [Cobertura, Espec. §Casos límite]
- [ ] CHK003 ¿Se describe cómo conserva el estudiante los datos ingresados y corrige el formulario después de un rechazo o fallo de guardado? [Brecha, Espec. §RF-003 y RF-011]
- [ ] CHK004 ¿Se define qué información de materia, fecha, estado y descripción necesita cada tarea en el listado para que el estudiante pueda decidir qué atender? [Brecha, Espec. §Historia de usuario 2]
- [ ] CHK005 ¿Son coherentes los requisitos de filtros combinados, limpieza de filtros y orden de tareas en todos los escenarios? [Coherencia, Espec. §RF-005 y RF-010]
- [ ] CHK006 ¿Queda claro que una materia no se puede borrar en esta versión y que las tareas conservan su asociación? [Alcance, Espec. §RF-014 y Suposiciones]

## Claridad, accesibilidad y adaptación de la interfaz

- [ ] CHK007 ¿Se distinguen «vencida», «urgente», «normal» y «completada» con términos y prioridades visuales no ambiguos? [Claridad, Espec. §RF-006–RF-009]
- [ ] CHK008 ¿Se exige identificar urgencia y vencimiento mediante texto además de color, incluso cuando el color elegido para una materia sea parecido al indicador de estado? [Cobertura, Espec. §RF-008]
- [ ] CHK009 ¿Están descritos los requisitos de etiquetas, foco visible y uso por teclado para formularios, filtros y control de completado? [Cobertura, Espec. §RF-012]
- [ ] CHK010 ¿Se especifican criterios verificables de legibilidad y ausencia de pérdida de funciones en tamaños de celular y computadora? [Medibilidad, Espec. §RF-012 y CE-005]
- [ ] CHK011 ¿Se define cómo se comunica un error o cambio de estado a quien usa tecnologías de asistencia? [Brecha, Espec. §RF-011 y RF-012]
- [ ] CHK012 ¿Se indica si la lista debe reflejar un cambio de urgencia o vencimiento mientras permanece abierta, sin exigir una acción del estudiante? [Claridad, Espec. §RF-007]

## Reglas de entrada y mensajes de validación

- [ ] CHK013 ¿Se identifican los campos obligatorios y opcionales de materias y tareas, incluida la necesidad de una materia existente? [Integridad, Espec. §RF-001–RF-002]
- [ ] CHK014 ¿Son explícitos los límites de 80, 120 y 1000 caracteres y el momento en que se cuentan tras recortar espacios extremos? [Claridad, Espec. §RF-001–RF-003 y Casos límite]
- [ ] CHK015 ¿Se especifica el tratamiento de textos vacíos o formados solo por espacios y de una descripción opcional vacía? [Cobertura, Espec. §RF-003 y Casos límite]
- [ ] CHK016 ¿Está definido el formato admitido para el color y el resultado esperado ante un valor inválido? [Claridad, Espec. §RF-001 y Modelo de datos]
- [ ] CHK017 ¿Está definido qué constituye una fecha de entrega válida, incluida la aceptación de fechas pasadas y el rechazo de fechas inexistentes? [Claridad, Espec. §RF-002 y Casos límite]
- [ ] CHK018 ¿Están definidos los resultados para tipos de dato incorrectos, referencias de materia inexistentes y valores de filtro no admitidos? [Cobertura, Espec. §RF-003 y Contrato HTTP]
- [ ] CHK019 ¿Exigen los requisitos mensajes de error en español que identifiquen el campo y el límite incumplido, sin afirmar que se guardó un cambio fallido? [Coherencia, Espec. §RF-003 y RF-011]
- [ ] CHK020 ¿Se establece que toda entrada se valida antes de guardarse, aunque la interfaz ya haya dado una advertencia? [Cobertura, Espec. §RF-003 y Plan §Comprobación de la constitución]

## Fechas límite y criterios de aceptación

- [ ] CHK021 ¿Se define sin ambigüedad el instante en que una tarea pasa a urgente y luego a vencida según la hora local del dispositivo? [Claridad, Espec. §RF-006–RF-007]
- [ ] CHK022 ¿Se cubren el instante exacto de 48 horas, el inicio del día siguiente y los cambios de horario local como límites distintos? [Casos límite, Espec. §Casos límite]
- [ ] CHK023 ¿Queda claro que una tarea completada no recibe etiquetas temporales y que estas se recalculan al volver a pendiente? [Coherencia, Espec. §RF-009 e Historia de usuario 3]
- [ ] CHK024 ¿Permiten CE-001 a CE-005 evaluar de forma objetiva la facilidad de uso, la clasificación temporal, la conservación de datos y la adaptación de pantalla? [Medibilidad, Espec. §Criterios de éxito]

## Notas

- Marcar `[x]` solo después de revisar el requisito correspondiente.
- Mantener sin marcar los puntos que requieren aclaración o corrección.
- `/speckit-implement` puede leer este estado como control, pero no debe cambiar las marcas.
- [requirements.md](requirements.md) conserva su ciclo de revisión independiente.
- Registrar hallazgos junto al punto correspondiente.
