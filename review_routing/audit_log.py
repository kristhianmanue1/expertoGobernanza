"""Bitácora tamper-evident de revisiones (plan router-harness §2, RH-T03).

Registro append-only (JSONL) encadenado por hashes: cada entrada lleva
`prev_hash` = `entry_hash` de la entrada anterior (genesis = sha256 + 64 ceros
para seq=1) y `entry_hash` = sha256(canonical_json(entrada sin entry_hash)),
con la misma canonicalización que el sello. Alterar cualquier campo, borrar o
reordenar entradas, o saltar `seq` → `verify_chain` = "BROKEN".

Ancla externa (F1) — LÍMITE DECLARADO: sin `anchor_hash`, `verify_chain` sólo
certifica consistencia interna; un atacante que trunque el log y lo reconstruya
desde genesis obtiene una cadena internamente consistente (no detectable sin
ancla). Con `anchor_hash` (último entry_hash conocido-good, commiteado a git =
sustrato firmado ADR-0002/0005), el reemplazo total se detecta: el último hash
de un log reconstruido difiere del ancla. `append` devuelve el `entry_hash`
para que el humano lo ancle periódicamente.
"""
import datetime as _dt
import json
import os
import pathlib

from .seal import _digest

GENESIS = "sha256:" + "0" * 64
REQUIRED = ("seq", "ts", "provider", "model", "seal_sha256", "bundle_sha256",
            "config_sha256", "response_sha256", "prev_hash", "entry_hash")


class AuditError(Exception):
    """Fallo fail-closed: no se extiende una bitácora previa inválida."""


def _parse(logpath):
    """Lee el log: (entradas, hallazgos). Una línea = una entrada JSON."""
    entries, findings = [], []
    text = pathlib.Path(logpath).read_text(encoding="utf-8")
    for i, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            findings.append(f"linea_no_json:{i}")
    return entries, findings


def _chain_findings(entries):
    """Recomputa hashes y enlaces. La posición i (1-based) exige seq == i."""
    findings = []
    prev = GENESIS
    for pos, e in enumerate(entries, 1):
        if not isinstance(e, dict) or any(k not in e for k in REQUIRED):
            findings.append(f"entrada_invalida:pos{pos}")
        else:
            if e["seq"] != pos:
                findings.append(f"seq_no_monotono:pos{pos}:seq={e['seq']}")
            if e["prev_hash"] != prev:
                findings.append(f"enlace_roto:pos{pos}")
            body = {k: v for k, v in e.items() if k != "entry_hash"}
            if not isinstance(e["entry_hash"], str) or _digest(body) != e["entry_hash"]:
                findings.append(f"entry_hash_no_recomputa:pos{pos}")
        eh = e.get("entry_hash") if isinstance(e, dict) else None
        prev = eh if isinstance(eh, str) else prev
    return findings


def append(seal, response_sha256, logpath):
    """Extiende la bitácora con una entrada por el sello dado.

    Fail-closed: si el log existente no verifica (lectura o cadena), lanza
    AuditError en vez de extender una bitácora corrupta. Devuelve el
    `entry_hash` de la nueva entrada (para anclar a git; F1).
    """
    logpath = pathlib.Path(logpath)
    entries = []
    if logpath.exists():
        entries, read_findings = _parse(logpath)
        broken = read_findings + _chain_findings(entries)
        if broken:
            raise AuditError("log_previo_invalido: " + "; ".join(broken[:3]))
    last = entries[-1] if entries else None
    entry = {
        "seq": (last["seq"] + 1) if last else 1,
        "ts": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "provider": seal["provider"],
        "model": seal["model"],
        "seal_sha256": seal["seal_sha256"],
        "bundle_sha256": seal["bundle_sha256"],
        "config_sha256": seal["config_sha256"],
        "response_sha256": response_sha256,
        "prev_hash": last["entry_hash"] if last else GENESIS,
    }
    entry["entry_hash"] = _digest(entry)  # excluido de su propio cómputo
    logpath.parent.mkdir(parents=True, exist_ok=True)
    with logpath.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())
    return entry["entry_hash"]


def verify_chain(logpath, anchor_hash=None):
    """Verifica la cadena completa. Devuelve ("OK"|"BROKEN", [hallazgos]).

    Sin `anchor_hash` certifica SÓLO consistencia interna (límite F1 declarado
    en el docstring del módulo). Con ancla: el último `entry_hash` debe
    igualarla (detecta truncado+reconstrucción).
    """
    logpath = pathlib.Path(logpath)
    if not logpath.exists():
        return "BROKEN", ["log_inexistente"]
    entries, findings = _parse(logpath)
    findings = list(findings) + _chain_findings(entries)
    if anchor_hash is not None:
        if not entries:
            findings.append("ancla_no_verificable:log_vacio")
        elif entries[-1].get("entry_hash") != anchor_hash:
            findings.append("ancla_no_coincide")
    if findings:
        return "BROKEN", findings
    return "OK", []
