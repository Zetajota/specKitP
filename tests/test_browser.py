"""Recorridos del estudiante en un navegador real."""

import pytest
from playwright.sync_api import expect


@pytest.mark.parametrize("width,height", [(390, 844), (1280, 800)])
def test_registro_recarga_y_error(page, live_server, width, height):
    page.set_viewport_size({"width": width, "height": height})
    page.goto(live_server)
    expect(page.get_by_text("Aún no hay materias")).to_be_visible()
    page.get_by_label("Nombre de la materia").fill("Matemáticas")
    page.get_by_label("Color de la materia").fill("#2255aa")
    page.get_by_role("button", name="Guardar materia").click()
    page.get_by_label("Título de la tarea").fill("Leer capítulo")
    page.get_by_label("Fecha de entrega").fill("2026-10-27")
    page.get_by_role("button", name="Guardar tarea").click()
    expect(page.get_by_text("Leer capítulo")).to_be_visible()
    page.reload()
    expect(page.get_by_text("Leer capítulo")).to_be_visible()
    page.get_by_label("Título de la tarea").fill("X" * 121)
    page.get_by_role("button", name="Guardar tarea").click()
    expect(page.get_by_role("alert")).to_contain_text("120")
    assert page.get_by_label("Título de la tarea").input_value() == "X" * 121


def test_urgencia_y_vencimiento_en_limites(browser, live_server):
    context = browser.new_context(timezone_id="America/La_Paz")
    page = context.new_page()
    page.request.post(
        f"{live_server}/api/materias",
        data={"nombre": "Cálculo", "color": "#2255AA"},
    )
    page.request.post(
        f"{live_server}/api/tareas",
        data={"materia_id": 1, "titulo": "Examen", "fecha_entrega": "2026-10-27"},
    )
    page.clock.install(time="2026-10-26T03:00:00Z")
    page.clock.pause_at("2026-10-26T03:59:59.999Z")
    page.goto(live_server)
    row = page.get_by_text("Examen").locator("..")
    expect(row).not_to_contain_text("Urgente")
    page.clock.run_for(1)
    expect(row).to_contain_text("Urgente")
    page.clock.fast_forward("48:00:00")
    expect(row).to_contain_text("Vencida")
    expect(row).not_to_contain_text("Urgente")
    context.close()


def test_cambio_de_horario_no_equivale_a_dos_dias(browser, live_server):
    context = browser.new_context(timezone_id="America/New_York")
    page = context.new_page()
    page.request.post(
        f"{live_server}/api/materias",
        data={"nombre": "Historia", "color": "#2255AA"},
    )
    page.request.post(
        f"{live_server}/api/tareas",
        data={"materia_id": 1, "titulo": "Ensayo", "fecha_entrega": "2027-03-14"},
    )
    # El cambio a horario de verano ocurre el 14 de marzo de 2027.
    page.clock.set_fixed_time("2027-03-13T03:59:59Z")
    page.goto(live_server)
    row = page.get_by_text("Ensayo").locator("..")
    expect(row).not_to_contain_text("Urgente")
    page.clock.set_fixed_time("2027-03-13T04:00:00Z")
    page.reload()
    expect(page.get_by_text("Ensayo").locator("..")).to_contain_text("Urgente")
    context.close()


def test_completar_y_combinar_filtros(page, live_server):
    primera = page.request.post(
        f"{live_server}/api/materias",
        data={"nombre": "Física", "color": "#2255AA"},
    ).json()
    segunda = page.request.post(
        f"{live_server}/api/materias",
        data={"nombre": "Química", "color": "#336633"},
    ).json()
    page.request.post(
        f"{live_server}/api/tareas",
        data={"materia_id": primera["id"], "titulo": "Examen", "fecha_entrega": "2026-10-27"},
    )
    page.request.post(
        f"{live_server}/api/tareas",
        data={"materia_id": segunda["id"], "titulo": "Ensayo", "fecha_entrega": "2026-10-28"},
    )
    page.goto(live_server)
    page.get_by_role("button", name="Completar Examen").click()
    expect(page.get_by_text("Examen").locator("..")).to_contain_text("Completada")
    expect(page.get_by_text("Examen").locator("..")).not_to_contain_text("Urgente")
    expect(page.get_by_text("Examen").locator("..")).not_to_contain_text("Vencida")
    page.reload()
    expect(page.get_by_text("Examen").locator("..")).to_contain_text("Completada")
    page.get_by_label("Filtrar por materia").select_option(str(primera["id"]))
    page.get_by_label("Filtrar por estado").select_option("completada")
    expect(page.get_by_text("Examen")).to_be_visible()
    expect(page.get_by_text("Ensayo")).to_have_count(0)
    page.get_by_role("button", name="Volver a pendiente Examen").click()
    expect(page.get_by_text("Ninguna tarea coincide")).to_be_visible()
    page.get_by_role("button", name="Limpiar filtros").click()
    expect(page.get_by_text("Examen")).to_be_visible()
    expect(page.get_by_text("Ensayo")).to_be_visible()


@pytest.mark.parametrize("width,height", [(390, 844), (1280, 800)])
def test_teclado_etiquetas_y_ancho(page, live_server, width, height):
    page.set_viewport_size({"width": width, "height": height})
    page.goto(live_server)
    assert page.get_by_label("Nombre de la materia").is_visible()
    assert page.get_by_label("Color de la materia").is_visible()
    assert page.get_by_label("Filtrar por materia").is_visible()
    assert page.get_by_label("Filtrar por estado").is_visible()
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    page.get_by_label("Nombre de la materia").focus()
    page.keyboard.type("Literatura")
    page.keyboard.press("Tab")
    assert page.evaluate("document.activeElement.id") == "materia-color"
    assert page.evaluate(
        "getComputedStyle(document.activeElement).outlineWidth"
    ) != "0px"
    page.get_by_role("button", name="Guardar materia").focus()
    page.keyboard.press("Enter")
    expect(page.locator("#materias-list").get_by_text("Literatura")).to_be_visible()


def test_lista_de_cien_tareas_y_filtro_en_pantalla(page, live_server):
    materia_id = page.request.post(
        f"{live_server}/api/materias",
        data={"nombre": "Álgebra", "color": "#2255AA"},
    ).json()["id"]
    for index in range(100):
        page.request.post(
            f"{live_server}/api/tareas",
            data={
                "materia_id": materia_id,
                "titulo": f"Tarea {index:03d}",
                "fecha_entrega": f"2026-11-{(index % 28) + 1:02d}",
            },
        )
    page.goto(live_server)
    expect(page.locator("#tareas-list li")).to_have_count(100)
    page.get_by_label("Filtrar por estado").select_option("completada")
    expect(page.get_by_text("Ninguna tarea coincide")).to_be_visible()
    page.get_by_role("button", name="Limpiar filtros").click()
    expect(page.locator("#tareas-list li")).to_have_count(100)
