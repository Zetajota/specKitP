# Guía de arranque y validación

## Requisitos previos

- Python 3.12 disponible como `py -3.12` en Windows.
- Dependencias declaradas en `pyproject.toml`.
- Para pruebas de navegador, instalación de Chromium de Playwright.

## Preparación y ejecución

Desde la raíz del proyecto, en PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e '.[test]'
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Abrir `http://127.0.0.1:8000/` en el navegador del mismo dispositivo. El archivo de datos
local se crea en `data/tareas.sqlite3` al iniciar la aplicación. Cada instalación usa su
propio archivo; no se sincroniza con otros dispositivos. Una instancia expuesta por red
compartiría sus datos con todos los dispositivos que la visiten y queda fuera del alcance
de esta primera versión.

## Pruebas automatizadas

En otra terminal de PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Las pruebas usarán archivos SQLite temporales. Deben cubrir los contratos de
[la API](contracts/api.md), los límites del [modelo](data-model.md), la conservación entre
sesiones y los recorridos del navegador. Una funcionalidad no se cierra si falla una prueba.
Si Playwright informa que falta Chromium, ejecutar de nuevo
`.\.venv\Scripts\python.exe -m playwright install chromium`.

## Comprobación funcional

1. Registrar una materia con nombre y color; crear una tarea con y otra sin descripción.
   Cerrar y volver a abrir la página: ambas deben seguir presentes.
2. Intentar guardar textos de 81, 121 y 1001 caracteres, una fecha inválida y una materia
   inexistente. Deben aparecer errores en español y no deben crearse registros.
3. Preparar tareas vencidas, dentro del límite exacto de 48 horas y fuera de él. Verificar
   orden, etiquetas con texto y ausencia de etiquetas temporales al completarlas.
4. Filtrar por materia y estado, combinar ambos filtros y limpiarlos. Marcar una tarea como
   completada y volver a dejarla pendiente.
5. Repetir los flujos en vista de celular y computadora; comprobar teclado, etiquetas,
   legibilidad y ausencia de funciones ocultas. La evaluación de 9 de 10 estudiantes en
   menos de tres minutos se realiza como prueba de uso separada.

Los detalles de datos y respuestas están en [modelo](data-model.md) y
[contrato HTTP](contracts/api.md).

## Estado de verificación

El 2026-10-26 se ejecutó `python -m pytest -q -p no:cacheprovider` con Python 3.12.15:
**13 pruebas superadas**. La suite cubre CE-002 con 100 tareas, orden y filtros;
CE-003 con límites exactos, vencimiento y cambio de horario; CE-004 con reapertura
de la aplicación usando el mismo archivo SQLite; y CE-005 con recorridos de teclado
y anchos de celular y computadora en Chromium.

CE-001 queda pendiente: requiere una prueba de uso con al menos diez estudiantes,
en la que nueve completen el registro de materia y tarea en menos de tres minutos
sin ayuda. Los tamaños de pantalla se probaron en navegador; no se realizó una
prueba en un teléfono físico.
