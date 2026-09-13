"""Project validation, safe paths, timing utilities, and asset fingerprints."""
from pathlib import Path
import hashlib,json,math,re
VERSION='0.1.0'
ID=re.compile(r'^[a-z][a-z0-9_-]*$')
FPS=30
SR=24000

def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def digest(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def fingerprint(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def inside(root,name):
 root=Path(root).resolve();p=(root/name).resolve()
 if not p.is_relative_to(root):raise ValueError(f'Path escapes project: {name}')
 return p

def stamp(t,sep=','):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
 return f'{h:02}:{m:02}:{s:02}{sep}{ms:03}'

def validate(root):
 root=Path(root);p=read(root/'project.json')
 for key in ['title','result','source','chapters','cues','voice','proof_file']:
  if key not in p:raise ValueError(f'Missing project field: {key}')
 if p.get('schema_version')!=1:raise ValueError('Expected schema_version=1')
 for key in ['title','result']:
  if not isinstance(p[key],str) or not p[key].strip():raise ValueError(f'Empty {key}')
 for key in ['title','locator','status']:
  if not p['source'].get(key):raise ValueError(f'Missing source.{key}')
 if not inside(root,p['proof_file']).is_file():raise ValueError('Expanded proof file is missing')
 if not p['chapters'] or not p['cues']:raise ValueError('Empty chapters/cues')
 chapters=[c['id'] for c in p['chapters']]
 if len(set(chapters))!=len(chapters) or any(not ID.fullmatch(x) for x in chapters):raise ValueError('Invalid or duplicate chapter IDs')
 ids=[];seen=[];last=None
 for c in p['cues']:
  if not ID.fullmatch(c['id']) or c['id'] in ids:raise ValueError('Invalid or duplicate cue ID')
  ids.append(c['id'])
  if c['chapter'] not in chapters:raise ValueError('Unknown chapter')
  if c['chapter']!=last:
   if c['chapter'] in seen:raise ValueError('Chapter cues must be contiguous')
   seen.append(c['chapter']);last=c['chapter']
  if not c.get('proof_step'):raise ValueError('Each cue needs a proof_step/source mapping')
  sentences=c.get('sentences',[])
  if not sentences or any(not isinstance(s,dict) or not s.get('say','').strip() for s in sentences):raise ValueError('Provide explicit sentence objects with say text')
  hold=c.get('hold',3)
  if not isinstance(hold,(int,float)) or not math.isfinite(hold) or hold<0:raise ValueError('hold must be nonnegative and finite')
  visual=c.get('visual','equations')
  if visual not in ['equations','number_line','curve','custom']:raise ValueError(f'Unknown visual {visual}')
  if visual=='custom' and not inside(root,'visuals.py').is_file():raise ValueError('custom visuals require project visuals.py')
  if len(c.get('equations',[]))>4:raise ValueError('At most four equations per cue; split dense derivations')
  for e in c.get('equations',[]):
   latex=e if isinstance(e,str) else e['latex']
   if re.search(r'\\(?:input|include|write|openout|read|catcode|usepackage|documentclass)\b',latex):raise ValueError('Use mathematical LaTeX fragments only')
 if seen!=chapters:raise ValueError('Chapters must follow declared order and each have a cue')
 speed=p['voice'].get('speed',.9)
 if not isinstance(speed,(int,float)) or not .5<=speed<=2:raise ValueError('voice.speed must be between .5 and 2')
 return p

def speech_key(sentence,voice,models):
 return fingerprint(dict(say=sentence['say'],voice=voice,models=models,engine='kokoro-onnx-0.6.1',sample_rate=SR))

def current_timeline(root):
 p=validate(root);t=read(Path(root)/'timeline.json')
 if t['project_sha256']!=fingerprint(p):raise ValueError('Project changed: run audio again to refresh the timeline (cached speech is reused)')
 return p,t
