"""Extractor stub: solo texto. No lee gold ni llama a la red."""
from __future__ import annotations

PLANTED = "cita plantada del stub de extraccion sintetica"

def extract(texto: str) -> list[dict]:
    """Devuelve la cita plantada solo si aparece en el texto."""
    if not isinstance(texto, str):
        raise TypeError("extract acepta solo str")
    if PLANTED in texto:
        return [{"disposicion_id": None, "cita_texto": PLANTED}]
    return []
