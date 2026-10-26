# Plan de trabajo del equipo: Recordatorios

**Equipo**: Abner, Joel, Mati y Erick.

**Alcance disponible**: Las 38 tareas de la aplicación de tareas académicas están
cerradas. Las 21 tareas abiertas de [recordatorios](tasks.md) son el trabajo de
desarrollo que se reparte aquí. La prueba de uso CE-001 de la primera funcionalidad
continúa pendiente como evaluación con estudiantes, separada de este desarrollo.

## Responsables y entregables

| Persona | Tareas principales | Archivos bajo su responsabilidad | Revisión cruzada |
|---------|--------------------|----------------------------------|------------------|
| **Mati** | T001, T002, T004, T005, T012, T013, T019 y T020 | `tests/test_api.py`, `tests/test_browser.py` | Revisa el comportamiento de API y los límites de fechas con Abner. |
| **Abner** | T003, T006, T007, T008, T014 y T015 | `app/db.py`, `app/validation.py`, `app/main.py` | Revisa el contrato consumido por la interfaz con Joel. |
| **Joel** | T009, T011, T016 y T018 | `app/static/app.js`; integración y pruebas de cada historia | Revisa el flujo visible y la ausencia de duplicados con Mati. |
| **Erick** | T010, T017 y T021 | `app/static/index.html`, `app/static/styles.css`, `quickstart.md` | Revisa accesibilidad, textos y resultados finales con Joel. |

Cada tarea tiene una persona responsable. Una tarea solo se marca completa cuando
su prueba pertinente pasa y la revisión cruzada no encuentra un requisito pendiente.

## Secuencia y coordinación

| Etapa | Trabajo y dependencia | Resultado para integrar |
|-------|------------------------|-------------------------|
| 1. Línea base | Mati ejecuta T001; escribe T002 antes de que Abner empiece T003. | Suite base y prueba nueva fallida por la ausencia de constancias. |
| 2. Historia 1 | Mati escribe T004 y T005. Abner implementa T006–T008; Joel T009; Erick T010. Joel cierra T011. | Un aviso legible de cada tarea pendiente con entrega mañana. |
| 3. Historia 2 | Mati escribe T012 y T013. Abner implementa T014–T015; Joel T016; Erick T017. Joel cierra T018. | Ausencia de duplicados y exclusión de tareas no elegibles. |
| 4. Cierre | Mati realiza T019–T020; Erick actualiza la guía y ejecuta T021 con el equipo. | Suite completa verde con Python 3.12 y guía reproducible. |

## Forma de integrar

- Cada persona trabaja en una rama propia derivada de `main`, por ejemplo
  `feature/002-abner-api`, `feature/002-mati-pruebas`,
  `feature/002-joel-interfaz` y `feature/002-erick-ux`.
- Los cambios de prueba de Mati se integran antes de la implementación que
  verifican. Abner y Joel acuerdan los nombres del contrato antes de tocar
  `app/main.py` o `app/static/app.js`.
- Nadie integra su propia revisión: otra persona comprueba el requisito,
  las pruebas y el contenido en español. La revisión final incluye los cinco
  principios de la constitución.
- Antes de cada push, se sigue [AGENTS.md](../../AGENTS.md) y se ejecuta
  `scripts/verificar-antes-de-push.ps1`. Una rama atrasada se integra,
  se resuelven sus conflictos y se repiten las pruebas antes de publicar.

## Criterios de cierre

1. T001–T021 están marcadas como completadas en `tasks.md`.
2. Las pruebas de API y navegador pasan con Python 3.12; no hay regresiones
   de las tareas académicas existentes.
3. Los avisos funcionan al abrir, a medianoche y al volver al foco, se
   registran una sola vez y pueden cerrarse con teclado.
4. La guía documenta la ejecución y las limitaciones de avisos solo con
   la aplicación abierta.
