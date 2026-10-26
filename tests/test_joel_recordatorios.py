"""Pruebas aisladas de la lógica de recordatorios de la interfaz."""

import json

from playwright.sync_api import expect


def mock_recordatorios(page, pendientes, registrar=None):
    """Simula el contrato HTTP mientras el backend está en desarrollo."""
    registrar = registrar or (lambda _identificador: (201, {"registrado": True}))
    consultas = []
    registros = []

    def consultar(route):
        consultas.append(route.request.url)
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(pendientes(route.request.url), ensure_ascii=False),
        )

    def marcar(route):
        registros.append(route.request.url)
        identificador = int(route.request.url.split("/api/recordatorios/")[1].split("/")[0])
        status, body = registrar(identificador)
        route.fulfill(
            status=status,
            content_type="application/json",
            body=json.dumps(body, ensure_ascii=False),
        )

    page.route("**/api/recordatorios?*", consultar)
    page.route("**/api/recordatorios/*/marcar", marcar)
    return consultas, registros


def candidato(identificador=7):
    return {
        "tarea_id": identificador,
        "titulo": "Examen de cálculo",
        "materia": "Matemáticas",
        "fecha_entrega": "2026-10-27",
    }


def test_joel_aviso_al_abrir_y_al_cruzar_medianoche(browser, live_server):
    context = browser.new_context(timezone_id="America/La_Paz")
    page = context.new_page()
    consultas, registros = mock_recordatorios(
        page,
        lambda url: [candidato()] if "dia_local=2026-10-26" in url else [],
    )
    page.clock.install(time="2026-10-26T03:00:00Z")
    page.clock.pause_at("2026-10-26T03:59:59.900Z")
    page.goto(live_server)
    expect(page.get_by_text("Examen de cálculo")).to_have_count(0)
    page.clock.run_for(100)
    expect(page.get_by_text("Examen de cálculo")).to_be_visible()
    expect(page.get_by_text("Matemáticas")).to_be_visible()
    expect(page.get_by_text("2026-10-27")).to_be_visible()
    assert any("dia_local=2026-10-26" in url for url in consultas)
    assert len(registros) == 1
    context.close()


def test_joel_no_duplica_al_recargar_y_respeta_el_registro(browser, live_server):
    context = browser.new_context(timezone_id="America/La_Paz")
    page = context.new_page()
    envios = 0

    def registrar(_identificador):
        nonlocal envios
        envios += 1
        return (201, {"registrado": True}) if envios == 1 else (200, {"registrado": False})

    _, registros = mock_recordatorios(page, lambda _url: [candidato()], registrar)
    page.clock.set_fixed_time("2026-10-26T16:00:00Z")
    page.goto(live_server)
    expect(page.get_by_text("Examen de cálculo")).to_be_visible()
    with page.expect_response(lambda response: "/api/recordatorios/7/marcar" in response.url):
        page.reload()
    expect(page.get_by_text("Examen de cálculo")).to_have_count(0)
    assert len(registros) == 2
    context.close()


def test_joel_fallo_de_registro_no_muestra_aviso(browser, live_server):
    context = browser.new_context(timezone_id="America/La_Paz")
    page = context.new_page()
    mock_recordatorios(
        page,
        lambda _url: [candidato()],
        lambda _identificador: (500, {"error": "No se pudo registrar el recordatorio."}),
    )
    page.clock.set_fixed_time("2026-10-26T16:00:00Z")
    page.goto(live_server)
    expect(page.get_by_role("alert")).to_contain_text("No se pudo registrar")
    expect(page.get_by_text("Examen de cálculo")).to_have_count(0)
    context.close()


def test_joel_revisa_al_recuperar_foco_y_descarta_aviso_tardio(browser, live_server):
    context = browser.new_context(timezone_id="America/La_Paz")
    page = context.new_page()
    consultas, registros = mock_recordatorios(
        page,
        lambda url: [candidato()] if "dia_local=2026-10-26" in url else [],
    )
    page.clock.set_fixed_time("2026-10-25T16:00:00Z")
    page.goto(live_server)
    expect(page.get_by_text("Examen de cálculo")).to_have_count(0)
    page.clock.set_fixed_time("2026-10-26T16:00:00Z")
    page.evaluate("window.dispatchEvent(new Event('focus'))")
    expect(page.get_by_text("Examen de cálculo")).to_be_visible()
    assert any("dia_local=2026-10-26" in url for url in consultas)
    assert len(registros) == 1
    context.close()


def test_joel_varios_avisos_y_cierre_por_teclado(browser, live_server):
    context = browser.new_context(timezone_id="America/La_Paz")
    page = context.new_page()
    segundo = {
        "tarea_id": 8,
        "titulo": "Trabajo de física",
        "materia": "Física",
        "fecha_entrega": "2026-10-27",
    }
    atrasado = {
        "tarea_id": 9,
        "titulo": "Aviso tardío",
        "materia": "Historia",
        "fecha_entrega": "2026-10-26",
    }
    _, registros = mock_recordatorios(
        page, lambda _url: [candidato(), segundo, atrasado]
    )
    page.clock.set_fixed_time("2026-10-26T16:00:00Z")
    page.goto(live_server)
    expect(page.locator("#recordatorios-list li")).to_have_count(2)
    expect(page.get_by_text("Aviso tardío")).to_have_count(0)
    close = page.get_by_role("button", name="Cerrar recordatorio de Examen de cálculo")
    close.focus()
    page.keyboard.press("Enter")
    expect(page.locator("#recordatorios-list li")).to_have_count(1)
    assert len(registros) == 2
    context.close()
