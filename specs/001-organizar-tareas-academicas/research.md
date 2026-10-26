# Investigación y decisiones

## Persistencia sencilla

**Decisión**: Usar `sqlite3` de Python con consultas parametrizadas y un archivo local.
Activar `PRAGMA foreign_keys = ON` en cada conexión.

**Motivo**: Dos entidades y un único usuario no justifican un ORM. Los parámetros evitan
construir consultas con texto del usuario; las claves foráneas protegen la asociación.

**Alternativas consideradas**: Un ORM añade dependencias y capas; archivos JSON dificultan
la integridad de la relación y los filtros.

**Fuentes**: [Documentación de `sqlite3` de Python 3.12](https://docs.python.org/3.12/library/sqlite3.html) y
[claves foráneas de SQLite](https://www.sqlite.org/foreignkeys.html).

## Interfaz servida por FastAPI

**Decisión**: Servir `index.html` y los archivos CSS y JavaScript desde la misma aplicación
FastAPI que expone la API.

**Motivo**: Cumple la petición de un solo proyecto y evita un servidor o compilador de frontend.

**Alternativas consideradas**: Un servidor frontend separado agrega configuración sin aportar
valor a esta primera versión.

**Fuente**: [Archivos estáticos en FastAPI](https://fastapi.tiangolo.com/tutorial/static-files/).

## Urgencia y hora local

**Decisión**: Conservar solo la fecha civil de entrega. En el navegador, construir el inicio
del día siguiente con la zona horaria local, convertir ambos instantes a tiempo transcurrido
real y comparar la diferencia con 48 horas exactas.

**Motivo**: La especificación usa la hora local del dispositivo. El navegador ya conoce esa
zona y puede recalcular cuando cambie el reloj o la zona, sin enviar datos de zona al servidor.

**Alternativas consideradas**: Calcularlo en el servidor requiere transmitir y mantener una
zona horaria por solicitud; contar dos días de calendario incumple la aclaración sobre 48 horas
reales. El estado pendiente/completado sí se guarda; urgente/vencido se deriva cada vez.

## Pruebas de extremo a extremo

**Decisión**: Usar pytest para la API y `pytest-playwright` para
probar la interfaz JavaScript con un navegador real y tamaños de pantalla distintos.

**Motivo**: La constitución exige pruebas automatizadas de toda funcionalidad; las pruebas
solo de API no verificarían filtros, etiquetas temporales ni teclado en el navegador.

**Alternativas consideradas**: Comprobación manual única no cumple la constitución; adoptar
un framework de frontend solo para facilitar pruebas añade complejidad de producto.

**Fuentes**: [Pruebas en FastAPI](https://fastapi.tiangolo.com/tutorial/testing/),
[complemento oficial de Playwright para pytest](https://playwright.dev/python/docs/test-runners)
y [control del reloj en pruebas](https://playwright.dev/python/docs/clock).
