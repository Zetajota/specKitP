"""Aplicación HTTP y página principal."""

import sqlite3
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.db import (
    add_materia, add_tarea, init_db, list_materias, list_recordatorios, list_tareas,
    mark_recordatorio, materia_exists, set_tarea_estado,
)
from app.validation import (
    InputError, positive_id, validate_dia_local, validate_materia, validate_tarea,
)

STATIC_DIR = Path(__file__).parent / "static"
DEFAULT_DB = Path(__file__).parent.parent / "data" / "tareas.sqlite3"


def create_app(db_path: Path | None = None) -> FastAPI:
    database = Path(db_path) if db_path is not None else DEFAULT_DB
    init_db(database)
    application = FastAPI(title="Tareas académicas UPB")
    application.state.db_path = database
    application.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @application.exception_handler(InputError)
    async def input_error(_request: Request, error: InputError) -> JSONResponse:
        return JSONResponse({"error": error.message}, status_code=error.status_code)

    @application.exception_handler(RequestValidationError)
    async def request_error(_request: Request, _error: RequestValidationError) -> JSONResponse:
        return JSONResponse({"error": "La solicitud contiene datos inválidos."}, status_code=422)

    @application.exception_handler(sqlite3.Error)
    async def storage_error(_request: Request, _error: sqlite3.Error) -> JSONResponse:
        return JSONResponse({"error": "No se pudo guardar o consultar la información."}, status_code=500)

    @application.get("/", include_in_schema=False)
    def home() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    async def payload_from(request: Request) -> dict:
        try:
            payload = await request.json()
        except ValueError as error:
            raise InputError("La solicitud debe contener datos JSON válidos.") from error
        if not isinstance(payload, dict):
            raise InputError("La solicitud debe contener un objeto de datos.")
        return payload

    @application.get("/api/materias")
    def get_materias() -> list[dict]:
        return list_materias(database)

    @application.post("/api/materias", status_code=201)
    async def post_materia(request: Request) -> dict:
        return add_materia(database, validate_materia(await payload_from(request)))

    @application.get("/api/tareas")
    def get_tareas(materia_id: str | None = None, estado: str | None = None) -> list[dict]:
        parsed_id = None
        if materia_id is not None:
            if not materia_id.isdecimal():
                raise InputError("Materia: el filtro debe ser un entero positivo.")
            parsed_id = positive_id(int(materia_id), "Materia")
        if estado not in (None, "pendiente", "completada"):
            raise InputError("Estado: usa pendiente o completada.")
        completed = None if estado is None else estado == "completada"
        return list_tareas(database, parsed_id, completed)

    @application.post("/api/tareas", status_code=201)
    async def post_tarea(request: Request) -> dict:
        data = validate_tarea(await payload_from(request))
        if not materia_exists(database, data["materia_id"]):
            raise InputError("La materia indicada no existe.", status_code=404)
        return add_tarea(database, data)

    @application.patch("/api/tareas/{tarea_id}/estado")
    async def patch_tarea_estado(tarea_id: int, request: Request) -> dict:
        positive_id(tarea_id, "Tarea")
        body = await payload_from(request)
        completed = body.get("completada")
        if not isinstance(completed, bool):
            raise InputError("Estado de la tarea: debe ser verdadero o falso.")
        updated = set_tarea_estado(database, tarea_id, completed)
        if updated is None:
            raise InputError("La tarea indicada no existe.", status_code=404)
        return updated

    @application.get("/api/recordatorios")
    def get_recordatorios(dia_local: str | None = None) -> list[dict]:
        if dia_local is None:
            raise InputError("Día local: el parámetro es obligatorio.")
        local_day, due_day = validate_dia_local(dia_local)
        return list_recordatorios(database, local_day, due_day)

    @application.post("/api/recordatorios/{tarea_id}/marcar")
    async def post_recordatorio(tarea_id: str, request: Request) -> JSONResponse:
        if not tarea_id.isdecimal():
            raise InputError("Tarea: debe ser un entero positivo.")
        parsed_id = positive_id(int(tarea_id), "Tarea")
        body = await payload_from(request)
        if "dia_local" not in body:
            raise InputError("Día local: el campo es obligatorio.")
        local_day, due_day = validate_dia_local(body["dia_local"])
        recorded = mark_recordatorio(database, parsed_id, local_day, due_day)
        if recorded is None:
            raise InputError("La tarea indicada no existe.", status_code=404)
        return JSONResponse({"registrado": recorded}, status_code=201 if recorded else 200)

    return application


app = create_app()
