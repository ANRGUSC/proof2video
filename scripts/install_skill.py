"""Install only the self-contained skill; never overwrite an existing one."""
from pathlib import Path
import argparse,os,shutil
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--skills-dir',type=Path);a=p.parse_args()
base=a.skills_dir or Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'skills'
src=Path(__file__).resolve().parents[1]/'plugins/proof-to-video/skills/proof-to-video';target=base/'proof-to-video'
if target.exists():raise SystemExit(f'Already exists: {target}. Preserve or remove that installation deliberately before reinstalling.')
shutil.copytree(src,target,ignore=shutil.ignore_patterns('__pycache__','*.pyc'));print(target.resolve())
