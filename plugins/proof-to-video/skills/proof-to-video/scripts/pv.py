#!/usr/bin/env python3
"""Proof to Video command-line entry point. Run --help for the workflow."""
import argparse,sys,shutil,importlib.util,subprocess
from pathlib import Path
from proof_video.core import validate,read,write,digest

def main():
 ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='cmd',required=True)
 init=sub.add_parser('init');init.add_argument('project',type=Path)
 doc=sub.add_parser('doctor');doc.add_argument('--tts-python')
 for name in ['validate','audio','render','verify','review','package']:
  p=sub.add_parser(name);p.add_argument('project',type=Path)
  if name=='audio':p.add_argument('--models',type=Path);p.add_argument('--tts-python')
  if name in ['render','verify']:p.add_argument('--preview',action='store_true')
  if name=='review':p.add_argument('--notes',required=True);p.add_argument('--component',choices=['both','visual','audio'],default='both')
 args=ap.parse_args()
 if args.cmd=='init':
  src=Path(__file__).resolve().parent.parent/'assets/example'
  if args.project.exists():raise ValueError('Choose a new project directory; init never overwrites a project')
  shutil.copytree(src,args.project);p=read(args.project/'project.json');p['proof_review']['proof_sha256']=digest(args.project/p['proof_file']);write(args.project/'project.json',p);validate(args.project);print(args.project.resolve());return
 if args.cmd=='doctor':
  missing=[]
  for n in ['ffmpeg','ffprobe','pdflatex']:
   found=shutil.which(n);print(n,found or 'MISSING');missing += [] if found else [n]
  for n in ['manim','PIL','numpy']:
   found=importlib.util.find_spec(n) is not None;print(n,'available' if found else 'MISSING');missing+=[] if found else [n]
  if not (shutil.which('dvisvgm') or shutil.which('pdftocairo')):missing.append('dvisvgm or pdftocairo')
  tts=args.tts_python or sys.executable
  check=subprocess.run([tts,'-c','import kokoro_onnx,onnxruntime,soundfile'],capture_output=True)
  print('TTS dependencies','available' if check.returncode==0 else 'MISSING');missing+=[] if check.returncode==0 else ['TTS dependencies']
  if missing:raise ValueError('Missing: '+', '.join(missing))
  return
 if args.cmd=='validate':validate(args.project);print('Project structure passed; this does not verify the proof.');return
 if args.cmd=='audio':
  if args.tts_python:
   command=[args.tts_python,str(Path(__file__).resolve()),'audio',str(args.project.resolve())]
   if args.models:command+=['--models',str(args.models.resolve())]
   subprocess.run(command,check=True);return
  from proof_video.audio import build
  build(args.project,args.models);return
 from proof_video import media
 if args.cmd=='render':media.render(args.project,args.preview)
 elif args.cmd=='verify':media.verify(args.project,args.preview)
 elif args.cmd=='review':media.mark_review(args.project,args.notes,args.component)
 elif args.cmd=='package':media.package(args.project)
if __name__=='__main__':
 try:main()
 except (ValueError,AssertionError,FileNotFoundError,subprocess.CalledProcessError) as e:print('ERROR:',e,file=sys.stderr);sys.exit(1)
