"""Verifica los bytes originales del inventario local, sin abrir servicios."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import stat


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INVENTORY = ROOT / 'docs/evidencia/ctim-source-register-2026-10-08.json'
SHA = re.compile(r'[0-9a-f]{64}\Z')


def verify(inventory_path=DEFAULT_INVENTORY):
    inventory = json.loads(Path(inventory_path).read_text(encoding='utf-8'))
    if inventory.get('schema') != 'expertogobernanza/source-inventory/v1':
        raise ValueError('inventory_schema')
    sources = inventory.get('sources')
    if not isinstance(sources, list) or not sources:
        raise ValueError('inventory_empty')
    seen = set()
    for source in sources:
        if set(source) != {'id', 'path', 'media_type', 'sha256', 'bytes', 'pages', 'url'}:
            raise ValueError('source_fields')
        name = source['id']
        relative = Path(source['path'])
        if not isinstance(name, str) or not name or name in seen:
            raise ValueError('source_id')
        seen.add(name)
        if (relative.is_absolute() or '..' in relative.parts
                or relative.parts[:3] != ('docs', 'fuentes', 'imss')):
            raise ValueError('source_path')
        if source['media_type'] not in ('application/pdf', 'text/html'):
            raise ValueError('source_media_type')
        if not isinstance(source['sha256'], str) or not SHA.fullmatch(source['sha256']):
            raise ValueError('source_sha256')
        if type(source['bytes']) is not int or source['bytes'] < 1:
            raise ValueError('source_bytes')
        if source['media_type'] == 'application/pdf':
            if type(source['pages']) is not int or source['pages'] < 1:
                raise ValueError('source_pages')
        elif source['pages'] is not None:
            raise ValueError('source_pages')
        path = ROOT / relative
        if not stat.S_ISREG(path.lstat().st_mode):
            raise ValueError('source_not_regular')
        raw = path.read_bytes()
        if len(raw) != source['bytes'] or hashlib.sha256(raw).hexdigest() != source['sha256']:
            raise ValueError('source_integrity:' + name)
    return {'status': 'ok', 'verified_sources': len(sources)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inventory', type=Path, default=DEFAULT_INVENTORY)
    args = parser.parse_args()
    print(json.dumps(verify(args.inventory), sort_keys=True))


if __name__ == '__main__':
    main()
