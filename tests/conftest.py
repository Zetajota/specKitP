"""Aislamiento de datos y servidor de pruebas."""

import socket
import threading
import time

import pytest
import uvicorn
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def application(tmp_path):
    return create_app(tmp_path / "tareas.sqlite3")


@pytest.fixture
def client(application):
    with TestClient(application) as test_client:
        yield test_client


@pytest.fixture
def live_server(application):
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    config = uvicorn.Config(application, host="127.0.0.1", port=port, log_level="error")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    for _ in range(100):
        if server.started:
            break
        time.sleep(0.05)
    if not server.started:
        raise RuntimeError("No se pudo iniciar el servidor de pruebas.")
    yield f"http://127.0.0.1:{port}"
    server.should_exit = True
    thread.join(timeout=5)
