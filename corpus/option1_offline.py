"""Medidor offline de la opción 1, contrato 4ea52b6.

Precisiones de la adopción: inicio < fin; una predicción que falla L es
falso positivo con diagnóstico prediccion_invalida; dos gold con el mismo
(inicio, fin) se rechazan. No es el juez de T2 ni una corrida con modelo.
"""
from __future__ import annotations

from corpus.verify_citations import _normalize

_CIERRES = frozenset(".?!;")
_ABREV = frozenset({
    "4o", "art", "núm", "num", "inc", "fracc",
    "sr", "sra", "dr", "dra", "etc", "op",
})
_NEG = (
    "documento sin citas",
    "artículo inventado",
    "no debe inventar",
)
_POS = (
    "tiene derecho",
    "definirá",
    "reglamenta",
    "es de aplicación",
    "orden público",
)
_QUITAR = frozenset(".,;:!?¿¡«»\"'()[]-")


def N(texto: str) -> str:
    if not isinstance(texto, str):
        raise TypeError("texto")
    return _normalize(texto)


def segmentar(texto: str) -> list[dict]:
    if not isinstance(texto, str):
        raise TypeError("texto")
    n = len(texto)
    salida: list[dict] = []
    inicio = 0
    i = 0
    while i < n:
        caracter = texto[i]
        if caracter in _CIERRES and not (caracter == "." and _es_abreviatura(texto, i)):
            fin = i + 1
            if fin > inicio:
                salida.append(_segmento(texto, inicio, fin, "cerrado"))
            j = fin
            while j < n and texto[j].isspace():
                j += 1
            inicio = j
            i = j
            continue
        i += 1
    if inicio < n:
        salida.append(_segmento(texto, inicio, n, "cierre_ausente"))
    return salida


def baseline(texto: str) -> list[dict]:
    return [
        {"cita_texto": segmento["cita_texto"], "inicio": segmento["inicio"], "fin": segmento["fin"]}
        for segmento in segmentar(texto)
        if segmento["clase"] == "benchmark_positivo"
    ]


def literal(texto: str, inicio: object, fin: object, cita: object) -> bool:
    return _motivo_literal(texto, inicio, fin, cita) is None


def diagnosticos(prediccion: str, gold: str) -> dict:
    pn = N(prediccion)
    gn = N(gold)
    sin_pred = "".join(c for c in pn if c not in _QUITAR)
    sin_gold = "".join(c for c in gn if c not in _QUITAR)
    return {
        "cobertura": gn in pn,
        "sobreextension": pn not in gn,
        "puntuacion": sin_pred == sin_gold and pn != gn,
    }


def evaluar(texto: str, gold: list, predicciones: list) -> dict:
    if not isinstance(texto, str):
        raise TypeError("texto")
    if not isinstance(gold, list) or not isinstance(predicciones, list):
        raise TypeError("listas")
    for indice, registro in enumerate(gold):
        motivo = _motivo_registro(texto, registro)
        if motivo is not None:
            return _rechazo(motivo, indice)
    vistos: dict[tuple[int, int], int] = {}
    for indice, registro in enumerate(gold):
        clave = (registro["inicio"], registro["fin"])
        if clave in vistos:
            return _rechazo("ocurrencia_duplicada", indice)
        vistos[clave] = indice

    papeles: list[dict] = []
    por_ocurrencia: dict[tuple[int, int], list[int]] = {}
    for indice, registro in enumerate(predicciones):
        motivo = _motivo_registro(texto, registro)
        if motivo is not None:
            papeles.append({
                "indice": indice,
                "papel": "fp",
                "valida": False,
                "diagnostico": "prediccion_invalida",
                "razon": motivo,
            })
            continue
        clave = (registro["inicio"], registro["fin"])
        papeles.append({
            "indice": indice,
            "papel": "fp",
            "valida": True,
            "diagnostico": None,
            "razon": None,
        })
        por_ocurrencia.setdefault(clave, []).append(indice)

    tp = 0
    for clave in vistos:
        indices = por_ocurrencia.get(clave, [])
        if not indices:
            continue
        papeles[indices[0]]["papel"] = "tp"
        tp += 1
    fp = len(predicciones) - tp
    fn = len(gold) - tp
    if predicciones:
        precision: float | None = tp / len(predicciones)
        razon_precision = None
    else:
        precision = None
        razon_precision = "denominador_cero"
    if gold:
        recall: float | None = tp / len(gold)
        razon_recall = None
    else:
        recall = None
        razon_recall = "denominador_cero"
    return {
        "estado": "ok",
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "razon_precision": razon_precision,
        "razon_recall": razon_recall,
        "predicciones": papeles,
    }


def _segmento(texto: str, inicio: int, fin: int, cierre: str) -> dict:
    if not inicio < fin:
        raise ValueError("segmento vacio")
    cita = texto[inicio:fin]
    return {
        "inicio": inicio,
        "fin": fin,
        "cita_texto": cita,
        "clase": _clase(cita),
        "cierre": cierre,
    }


def _clase(cita: str) -> str:
    bajo = cita.lower()
    if any(senal in bajo for senal in _NEG):
        return "benchmark_negativo"
    if any(senal in bajo for senal in _POS):
        return "benchmark_positivo"
    return "fuera_de_benchmark"


def _es_abreviatura(texto: str, indice: int) -> bool:
    j = indice
    while j > 0 and texto[j - 1].isalnum():
        j -= 1
    return texto[j:indice].casefold() in _ABREV


def _motivo_registro(texto: str, registro: object) -> str | None:
    if not isinstance(registro, dict):
        return "ausente"
    if "inicio" not in registro or "fin" not in registro or "cita_texto" not in registro:
        return "ausente"
    return _motivo_literal(texto, registro["inicio"], registro["fin"], registro["cita_texto"])


def _motivo_literal(texto: str, inicio: object, fin: object, cita: object) -> str | None:
    if not isinstance(cita, str):
        return "ausente"
    if not _entero_real(inicio) or not _entero_real(fin):
        return "tipo"
    inicio_i = int(inicio)
    fin_i = int(fin)
    n = len(texto)
    if inicio_i == fin_i and 0 <= inicio_i <= n:
        return "vacio"
    if not (0 <= inicio_i < fin_i <= n):
        return "rango"
    if texto[inicio_i:fin_i] != cita:
        return "cita"
    return None


def _entero_real(valor: object) -> bool:
    return isinstance(valor, int) and not isinstance(valor, bool)


def _rechazo(detalle: str, indice_gold: int) -> dict:
    return {
        "estado": "rechazo",
        "razon": "gold_invalido",
        "detalle": detalle,
        "indice_gold": indice_gold,
    }
