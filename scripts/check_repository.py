"""Portable packaging checks; does not verify a proof or render a video."""
from pathlib import Path
import json,sys,subprocess,ast
r=Path(__file__).resolve().parents[1];plugin=r/'plugins/proof-to-video';skill=plugin/'skills/proof-to-video';sys.path.insert(0,str(skill/'scripts'))
from proof_video.core import validate
m=json.loads((plugin/'.codex-plugin/plugin.json').read_text());assert m['name']==plugin.name and m['skills']=='./skills/' and m['version']=='0.1.0'
for name in ['LICENSE','README.md','THIRD_PARTY_NOTICES.md','environment.yml','CITATION.cff']:assert (r/name).is_file(),name
for p in r.rglob('*.py'):
 if '__pycache__' not in str(p):ast.parse(p.read_text(),filename=str(p))
text=(skill/'SKILL.md').read_text();assert text.startswith('---\nname: proof-to-video\n') and '[TODO:' not in text
for name in ['proof-expansion.md','pipeline.md','custom-visuals.md','review-and-release.md']:assert (skill/'references'/name).is_file()
validate(skill/'assets/example')
assert not list(r.rglob('*.onnx')) and not list(r.rglob('*.wav')) and not list(r.rglob('*.mp4'))
print('Repository checks passed.')
