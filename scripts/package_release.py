"""Package committed source and the installable plugin without local work files."""
from pathlib import Path
import subprocess,zipfile,argparse
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=Path(__file__).resolve().parents[1];out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
if subprocess.check_output(['git','status','--porcelain'],cwd=r).strip():raise SystemExit('Commit intended changes before packaging a release')
files=subprocess.check_output(['git','ls-files','-z'],cwd=r).decode().split('\0');prefix='plugins/proof-to-video/'
for name,plugin in [('proof-to-video-0.1.0-source.zip',False),('proof-to-video-0.1.0-plugin.zip',True)]:
 with zipfile.ZipFile(out/name,'w',zipfile.ZIP_DEFLATED) as z:
  for f in files:
   if not f or (plugin and not f.startswith(prefix)):continue
   z.write(r/f,f[len(prefix):] if plugin else 'proof-to-video/'+f)
 with zipfile.ZipFile(out/name) as z:assert z.testzip() is None
 print(out/name)
