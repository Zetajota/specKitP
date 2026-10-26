"""Reglas de entrada compartidas por las rutas."""

from dataclasses import dataclass
from datetime import date
import re

LIMITE_MATERIA = 80
LIMITE_TITULO = 120
LIMITE_DESCRIPCION = 1000
COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class InputError(Exception):
    message: str
    status_code: int = 422


def clean_text(value: object, field: str, maximum: int, required: bool = True) -> str | None:
    if value is None and not required:
        return None
    if not isinstance(value, str):
        raise InputError(f"{field}: debe ser texto.")
    result = value.strip()
    if required and not result:
        raise InputError(f"{field}: es obligatorio.")
    if len(result) > maximum:
        raise InputError(f"{field}: máximo {maximum} caracteres.")
    return result or None


def validate_materia(payload: dict) -> dict:
    nombre = clean_text(payload.get("nombre"), "Nombre de la materia", LIMITE_MATERIA)
    color = payload.get("color")
    if not isinstance(color, str) or not COLOR_PATTERN.fullmatch(color):
        raise InputError("Color de la materia: usa el formato #RRGGBB.")
    return {"nombre": nombre, "color": color.upper()}


def positive_id(value: object, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise InputError(f"{field}: debe ser un entero positivo.")
    return value


def validate_tarea(payload: dict) -> dict:
    materia_id = positive_id(payload.get("materia_id"), "Materia")
    titulo = clean_text(payload.get("titulo"), "Título de la tarea", LIMITE_TITULO)
    descripcion = clean_text(
        payload.get("descripcion"), "Descripción", LIMITE_DESCRIPCION, required=False
    )
    fecha = payload.get("fecha_entrega")
    if not isinstance(fecha, str) or not DATE_PATTERN.fullmatch(fecha):
        raise InputError("Fecha de entrega: usa una fecha real en formato AAAA-MM-DD.")
    try:
        date.fromisoformat(fecha)
    except ValueError as error:
        raise InputError("Fecha de entrega: introduce una fecha real.") from error
    return {
        "materia_id": materia_id,
        "titulo": titulo,
        "descripcion": descripcion,
        "fecha_entrega": fecha,
    }
