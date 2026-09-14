"""Portable packaging checks; does not verify a proof or render a video."""
from pathlib import Path
import json,sys,subprocess,ast
r=Path(__file__).resolve().parents[1];plugin=r/'plugins/proof-to-video';skill=plugin/'skills/proof-to-video';sys.path.insert(0,str(skill/'scripts'))
from proof_video.core import validate
m=json.loads((plugin/'.codex-plugin/plugin.json').read_text());assert m['name']==plugin.name and m['skills']=='./skills/' and m['version']=='0.1.0'
claude=json.loads((plugin/'.claude-plugin/plugin.json').read_text(encoding='utf-8'))
assert claude['name']==m['name'] and claude['version']==m['version'] and claude['license']==m['license']
assert (plugin/'skills'/claude['name']/'SKILL.md').is_file()
for name in ['LICENSE','README.md','THIRD_PARTY_NOTICES.md','environment.yml','CITATION.cff']:assert (r/name).is_file(),name
files=[r/name for name in subprocess.check_output(['git','ls-files','-z'],cwd=r).decode().split('\0') if name]
for p in files:
 if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
text=(skill/'SKILL.md').read_text();assert text.startswith('---\nname: proof-to-video\n') and '[TODO:' not in text
for name in ['proof-expansion.md','pipeline.md','custom-visuals.md','review-and-release.md']:assert (skill/'references'/name).is_file()
validate(skill/'assets/example')
assert not [p for p in files if p.suffix in {'.onnx','.wav','.mp4'}]
print('Repository checks passed.')
