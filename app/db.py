"""Acceso directo a SQLite para una instancia local."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


@contextmanager
def connection(db_path: Path) -> Iterator[sqlite3.Connection]:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    database = sqlite3.connect(db_path)
    database.row_factory = sqlite3.Row
    database.execute("PRAGMA foreign_keys = ON")
    try:
        yield database
        database.commit()
    except Exception:
        database.rollback()
        raise
    finally:
        database.close()


def init_db(db_path: Path) -> None:
    with connection(db_path) as database:
        database.executescript(
            """
            CREATE TABLE IF NOT EXISTS materias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                color TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                materia_id INTEGER NOT NULL REFERENCES materias(id),
                titulo TEXT NOT NULL,
                descripcion TEXT,
                fecha_entrega TEXT NOT NULL,
                completada INTEGER NOT NULL DEFAULT 0 CHECK (completada IN (0, 1))
            );
            CREATE TABLE IF NOT EXISTS constancias_recordatorio (
                tarea_id INTEGER NOT NULL REFERENCES tareas(id),
                dia_local TEXT NOT NULL,
                PRIMARY KEY (tarea_id, dia_local)
            );
            """
        )


def list_recordatorios(
    db_path: Path, dia_local: str, fecha_entrega: str
) -> list[dict]:
    """Lista tareas elegibles que aún no tienen constancia para el día local."""
    with connection(db_path) as database:
        rows = database.execute(
            """
            SELECT t.id AS tarea_id, t.titulo, m.nombre AS materia, t.fecha_entrega
            FROM tareas AS t
            JOIN materias AS m ON m.id = t.materia_id
            LEFT JOIN constancias_recordatorio AS c
                ON c.tarea_id = t.id AND c.dia_local = ?
            WHERE t.completada = 0 AND t.fecha_entrega = ? AND c.tarea_id IS NULL
            ORDER BY t.id ASC
            """,
            (dia_local, fecha_entrega),
        ).fetchall()
        return [dict(row) for row in rows]


def mark_recordatorio(
    db_path: Path, tarea_id: int, dia_local: str, fecha_entrega: str
) -> bool | None:
    """Registra atómicamente un aviso elegible. None indica que no existe la tarea."""
    with connection(db_path) as database:
        database.execute("BEGIN IMMEDIATE")
        task = database.execute(
            "SELECT completada, fecha_entrega FROM tareas WHERE id = ?", (tarea_id,)
        ).fetchone()
        if task is None:
            return None
        if task["completada"] or task["fecha_entrega"] != fecha_entrega:
            return False
        cursor = database.execute(
            """
            INSERT OR IGNORE INTO constancias_recordatorio (tarea_id, dia_local)
            VALUES (?, ?)
            """,
            (tarea_id, dia_local),
        )
        return cursor.rowcount == 1


def materia_exists(db_path: Path, materia_id: int) -> bool:
    with connection(db_path) as database:
        return database.execute(
            "SELECT 1 FROM materias WHERE id = ?", (materia_id,)
        ).fetchone() is not None


def list_materias(db_path: Path) -> list[dict]:
    with connection(db_path) as database:
        rows = database.execute("SELECT id, nombre, color FROM materias ORDER BY id").fetchall()
        return [dict(row) for row in rows]


def add_materia(db_path: Path, data: dict) -> dict:
    with connection(db_path) as database:
        cursor = database.execute(
            "INSERT INTO materias (nombre, color) VALUES (?, ?)",
            (data["nombre"], data["color"]),
        )
        return {"id": cursor.lastrowid, **data}


def task_dict(row: sqlite3.Row) -> dict:
    item = dict(row)
    item["completada"] = bool(item["completada"])
    return item


def add_tarea(db_path: Path, data: dict) -> dict:
    with connection(db_path) as database:
        cursor = database.execute(
            """
            INSERT INTO tareas (materia_id, titulo, descripcion, fecha_entrega)
            VALUES (?, ?, ?, ?)
            """,
            (data["materia_id"], data["titulo"], data["descripcion"], data["fecha_entrega"]),
        )
        row = database.execute(
            "SELECT * FROM tareas WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return task_dict(row)


def list_tareas(
    db_path: Path, materia_id: int | None = None, completada: bool | None = None
) -> list[dict]:
    conditions = []
    parameters = []
    if materia_id is not None:
        conditions.append("materia_id = ?")
        parameters.append(materia_id)
    if completada is not None:
        conditions.append("completada = ?")
        parameters.append(int(completada))
    where = f" WHERE {' AND '.join(conditions)}" if conditions else ""
    with connection(db_path) as database:
        rows = database.execute(
            "SELECT * FROM tareas" + where + " ORDER BY fecha_entrega ASC, id ASC",
            parameters,
        ).fetchall()
        return [task_dict(row) for row in rows]


def set_tarea_estado(db_path: Path, tarea_id: int, completada: bool) -> dict | None:
    with connection(db_path) as database:
        cursor = database.execute(
            "UPDATE tareas SET completada = ? WHERE id = ?",
            (int(completada), tarea_id),
        )
        if cursor.rowcount == 0:
            return None
        row = database.execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,)).fetchone()
        return task_dict(row)
