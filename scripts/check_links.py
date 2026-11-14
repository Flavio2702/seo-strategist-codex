"""Verifica offline dei collegamenti relativi nei documenti del repository."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

root = Path(__file__).resolve().parents[1]
errors = []
checked = 0
for path in [root / 'README.md', root / 'AGENTS.md', *sorted((root / 'docs').glob('*.md'))]:
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
        if urlsplit(target).scheme or target.startswith('#'):
            continue
        resolved = (path.parent / unquote(target.split('#')[0])).resolve()
        checked += 1
        if not resolved.is_relative_to(root) or not resolved.exists():
            errors.append(f'{path.name}: {target}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'{checked} collegamenti locali verificati; fonti esterne nel registro SOURCES.md')
