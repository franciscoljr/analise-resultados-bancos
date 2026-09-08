#!/usr/bin/env python3
"""Register project-owned specialist packages without overwriting other skills."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
profiles = json.loads((root / 'specialists/profiles.json').read_text())
target = Path.home() / '.agents/skills'
pairs = [(root / 'specialists/packages' / p['skill'], target / p['skill']) for p in profiles]
for source, destination in pairs:
    if not (source / 'SKILL.md').is_file():
        raise SystemExit(f'Missing package: {source}')
    if (destination.exists() or destination.is_symlink()) and destination.resolve() != source.resolve():
        raise SystemExit(f'Refusing to overwrite an existing skill: {destination}')
target.mkdir(parents=True, exist_ok=True)
for source, destination in pairs:
    if not destination.is_symlink() and not destination.exists():
        destination.symlink_to(source, target_is_directory=True)
    assert (destination / 'SKILL.md').is_file()
manifest = {'registration_directory': str(target), 'skills': [str(d) for _, d in pairs]}
(root / 'specialists/installation.json').write_text(json.dumps(manifest, indent=2))
print(json.dumps(manifest, indent=2))
