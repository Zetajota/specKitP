# Guía de validación: Recordatorios

## Requisitos

La aplicación de tareas base debe estar instalada y funcionando según
[su guía](../001-organizar-tareas-academicas/quickstart.md). Las pruebas usan
Python 3.12, pytest y Chromium de Playwright.

## Recorridos que deben probarse

1. Crear una tarea pendiente con entrega mañana. Abrir la aplicación en el
   día anterior: aparece un aviso con título, materia y fecha.
2. Mantener la página abierta al cruzar medianoche local. El aviso aparece
   sin recargar. Repetir tras recuperar el foco.
3. Crear dos tareas con entrega mañana. Se muestra un aviso identificable
   para cada una.
4. Recargar y reabrir durante el mismo día. Los avisos ya mostrados no
   reaparecen; dos pestañas abiertas tampoco generan duplicados.
5. Completar una tarea antes del aviso. No se muestra. En el día de entrega
   o después tampoco se muestran avisos tardíos.
6. Simular un fallo de almacenamiento. Aparece un mensaje en español sin
   afirmar que se registró el recordatorio.
7. En tamaños de celular y computadora, comprobar lectura, anuncio y
   cierre de avisos mediante teclado.

La suite automatizada deberá pasar con `.\.venv\Scripts\python.exe -m pytest`
antes de considerar terminada la funcionalidad. Los datos y respuestas
esperados están en [modelo](data-model.md) y [contrato](contracts/api.md).
