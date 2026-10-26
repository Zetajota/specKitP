"""Contrato y conservación de materias y tareas."""

import sqlite3

from fastapi.testclient import TestClient

from app.main import create_app


def materia(client, nombre="Matemáticas", color="#2255AA"):
    response = client.post("/api/materias", json={"nombre": nombre, "color": color})
    assert response.status_code == 201, response.text
    return response.json()


def tarea(client, materia_id, titulo="Leer capítulo", descripcion=None, fecha="2026-10-27"):
    response = client.post(
        "/api/tareas",
        json={
            "materia_id": materia_id,
            "titulo": titulo,
            "descripcion": descripcion,
            "fecha_entrega": fecha,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def test_registro_y_conservacion(client, application):
    asignatura = materia(client, "  Matemáticas  ")
    assert asignatura["nombre"] == "Matemáticas"
    primera = tarea(client, asignatura["id"], "  Leer capítulo  ", "  páginas 1 a 3  ")
    segunda = tarea(client, asignatura["id"], "Resolver ejercicios", "   ", "2026-10-20")
    assert primera["titulo"] == "Leer capítulo"
    assert primera["descripcion"] == "páginas 1 a 3"
    assert primera["completada"] is False
    assert segunda["descripcion"] is None
    assert len(client.get("/api/tareas").json()) == 2
    with TestClient(create_app(application.state.db_path)) as reopened:
        assert reopened.get("/api/materias").json() == [asignatura]
        assert [item["id"] for item in reopened.get("/api/tareas").json()] == [
            segunda["id"],
            primera["id"],
        ]


def test_limites_y_datos_invalidos(client):
    asignatura = materia(client, "M" * 80)
    for payload in [
        {"nombre": " ", "color": "#2255AA"},
        {"nombre": "M" * 81, "color": "#2255AA"},
        {"nombre": 14, "color": "#2255AA"},
        {"nombre": "Historia", "color": "azul"},
    ]:
        response = client.post("/api/materias", json=payload)
        assert response.status_code == 422
        assert "error" in response.json()
    tarea(client, asignatura["id"], "T" * 120, "D" * 1000)
    invalidas = [
        ({"titulo": " "}, 422),
        ({"titulo": "T" * 121}, 422),
        ({"descripcion": "D" * 1001}, 422),
        ({"fecha_entrega": "2026-02-30"}, 422),
        ({"fecha_entrega": "ayer"}, 422),
        ({"materia_id": 9999}, 404),
        ({"materia_id": "uno"}, 422),
    ]
    base = {
        "materia_id": asignatura["id"],
        "titulo": "Trabajo",
        "descripcion": None,
        "fecha_entrega": "2026-10-27",
    }
    for update, status in invalidas:
        response = client.post("/api/tareas", json={**base, **update})
        assert response.status_code == status
        assert response.json()["error"]
    assert len(client.get("/api/tareas").json()) == 1


def test_orden_por_fecha_y_creacion(client):
    asignatura = materia(client)
    tarde = tarea(client, asignatura["id"], "Tarde", fecha="2026-11-02")
    primero = tarea(client, asignatura["id"], "Primero", fecha="2026-10-27")
    segundo = tarea(client, asignatura["id"], "Segundo", fecha="2026-10-27")
    items = client.get("/api/tareas").json()
    assert [item["id"] for item in items] == [
        primero["id"], segundo["id"], tarde["id"]
    ]
    assert all("urgente" not in item and "vencida" not in item for item in items)


def test_estado_y_filtros_combinados(client, application):
    primera_materia = materia(client, "Física")
    segunda_materia = materia(client, "Química")
    primera = tarea(client, primera_materia["id"], "Uno")
    segunda = tarea(client, primera_materia["id"], "Dos")
    tarea(client, segunda_materia["id"], "Tres")
    response = client.patch(
        f"/api/tareas/{segunda['id']}/estado", json={"completada": True}
    )
    assert response.status_code == 200
    assert response.json()["completada"] is True
    filtradas = client.get(
        f"/api/tareas?materia_id={primera_materia['id']}&estado=completada"
    )
    assert [item["id"] for item in filtradas.json()] == [segunda["id"]]
    assert [item["id"] for item in client.get("/api/tareas?estado=pendiente").json()] == [
        primera["id"], 3
    ]
    assert len(client.get(f"/api/tareas?materia_id={segunda_materia['id']}").json()) == 1
    with TestClient(create_app(application.state.db_path)) as reopened:
        assert reopened.get(f"/api/tareas?estado=completada").json()[0]["id"] == segunda["id"]
    assert client.patch(
        f"/api/tareas/{segunda['id']}/estado", json={"completada": False}
    ).json()["completada"] is False
    assert client.get("/api/tareas?estado=completada").json() == []
    for path in [
        "/api/tareas?estado=otro",
        "/api/tareas?materia_id=abc",
        "/api/tareas?materia_id=0",
    ]:
        assert client.get(path).status_code == 422
    assert client.patch("/api/tareas/9999/estado", json={"completada": True}).status_code == 404
    assert client.patch(
        f"/api/tareas/{primera['id']}/estado", json={"completada": "sí"}
    ).status_code == 422


def test_cien_tareas_y_error_de_almacenamiento(client, monkeypatch):
    asignatura = materia(client)
    for index in range(100):
        tarea(
            client,
            asignatura["id"],
            f"Tarea {index}",
            fecha=f"2026-11-{(index % 28) + 1:02d}",
        )
    items = client.get(f"/api/tareas?materia_id={asignatura['id']}&estado=pendiente").json()
    assert len(items) == 100
    assert [item["fecha_entrega"] for item in items] == sorted(
        item["fecha_entrega"] for item in items
    )

    def fail_storage(*_args, **_kwargs):
        raise sqlite3.OperationalError("fallo interno")

    monkeypatch.setattr("app.main.add_tarea", fail_storage)
    response = client.post(
        "/api/tareas",
        json={
            "materia_id": asignatura["id"],
            "titulo": "No guardada",
            "fecha_entrega": "2026-11-01",
        },
    )
    assert response.status_code == 500
    assert "No se pudo guardar" in response.json()["error"]
    assert len(client.get("/api/tareas").json()) == 100
