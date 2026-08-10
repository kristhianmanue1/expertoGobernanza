#!/usr/bin/env python3
"""Gate de tamaño de archivos (tabla Duro, politica-agentes.md §3).

Camina un árbol, clasifica cada archivo y hace fallar (exit 1) si alguno
excede su límite "Duro". Exenta generados/lock/data, docs fuente y entornos.
"""
import argparse
import os
import subprocess
import sys

EXEMPT_DIRS = {
    ".git", ".venv", ".venv.broken-310", ".an-kla", ".archive",
    "__pycache__", "node_modules", ".mypy_cache", ".pytest_cache",
    ".ruff_cache", "site-packages", "dist", "build",
}
EXEMPT_FILES = {
    ".DS_Store", "LICENSE", "package-lock.json", "yarn.lock", "Pipfile.lock",
    "poetry.lock", ".gitignore", ".gitattributes", ".editorconfig",
}
SOURCE_EXT = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".go", ".rs", ".java",
    ".rb", ".kt", ".scala", ".c", ".h", ".cpp", ".hpp",
}
EXEMPT_EXT = {
    ".pyc", ".pyo", ".lock", ".min.js", ".min.css", ".map",
    ".json", ".toml", ".yaml", ".yml", ".ini", ".cfg", ".csv", ".log",
    ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".gz", ".tar",
}
VENDORED_GENERATED_PREFIXES = {
    os.path.join("interop", "akn", "schema"),
}

LIMITS = {
    "always_on": 300,
    "checkpoint": 250,
    "artifact": 800,
    "doc_ref": 1500,
    "source": 800,
}

LABEL = {
    "always_on": "always-on (AGENTS/CLAUDE)",
    "checkpoint": "checkpoint",
    "artifact": "artefacto agente",
    "doc_ref": "doc referencia",
    "source": "código fuente",
}


def is_exempt(rel, name):
    parts = rel.split(os.sep)
    if any(p in EXEMPT_DIRS for p in parts):
        return True
    if name in EXEMPT_FILES:
        return True
    if parts[0] == "docs" and len(parts) > 1 and parts[1] == "fuentes":
        return True
    if any(
        rel == prefix or rel.startswith(prefix + os.sep)
        for prefix in VENDORED_GENERATED_PREFIXES
    ):
        return True
    ext = os.path.splitext(name)[1].lower()
    if ext in EXEMPT_EXT:
        return True
    return False


def classify(rel):
    parts = rel.split(os.sep)
    name = parts[-1]
    if len(parts) == 1 and name in ("AGENTS.md", "CLAUDE.md"):
        return "always_on"
    if name.endswith(".md") and name.lower().startswith("checkpoint-"):
        return "checkpoint"
    if parts[0] == "docs" and name.endswith(".md"):
        lower = name.lower()
        if (name.lower().startswith("plan-") or "contrato" in lower
                or "reporte" in lower or "adversarial" in lower):
            return "artifact"
        return "doc_ref"
    if name.endswith(".md"):
        return "doc_ref"
    ext = os.path.splitext(name)[1].lower()
    if ext in SOURCE_EXT:
        return "source"
    return "doc_ref"


def count_lines(path):
    try:
        with open(path, "rb") as f:
            return f.read().count(b"\n")
    except OSError:
        return None


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXEMPT_DIRS]
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            yield rel, full


def tracked_files(root):
    try:
        r = subprocess.run(
            ["git", "-C", root, "ls-files", "--"],
            capture_output=True, text=True, timeout=15,
        )
    except Exception:
        return None
    if r.returncode != 0:
        return None
    out = []
    for line in r.stdout.splitlines():
        if not line:
            continue
        full = os.path.join(root, line)
        if os.path.isfile(full):
            out.append((line, full))
    return out or None


def main():
    ap = argparse.ArgumentParser(description="Gate de tamaño §3 (tabla Duro).")
    ap.add_argument("root", nargs="?", default=".", help="raíz a revisar (default: .)")
    args = ap.parse_args()

    files = tracked_files(args.root) or list(walk(args.root))

    rows = []
    violations = []
    for rel, full in files:
        name = os.path.basename(rel)
        if is_exempt(rel, name):
            continue
        cat = classify(rel)
        if cat is None:
            continue
        n = count_lines(full)
        if n is None:
            continue
        limit = LIMITS[cat]
        status = "OK" if n <= limit else "FAIL"
        rows.append((rel, cat, n, limit, status))
        if n > limit:
            violations.append((rel, cat, n, limit))

    rows.sort(key=lambda r: r[1])
    w = max((len(r[0]) for r in rows), default=12)
    print(f"{'archivo':<{w}}  {'categoría':<22} {'líneas':>7} {'límite':>7}  estado")
    print("-" * (w + 22 + 7 + 7 + 10))
    for rel, cat, n, limit, status in rows:
        print(f"{rel:<{w}}  {LABEL[cat]:<22} {n:>7} {limit:>7}  {status}")

    print("-" * (w + 22 + 7 + 7 + 10))
    if violations:
        print(f"FAIL: {len(violations)} archivo(s) exceden el límite Duro:")
        for rel, cat, n, limit in violations:
            print(f"  {rel} [{cat}] {n} > {limit}")
        return 1
    print(f"OK: {len(rows)} archivo(s) dentro de límites.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
