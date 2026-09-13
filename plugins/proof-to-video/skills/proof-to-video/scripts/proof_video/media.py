"""Manim/FFmpeg orchestration, export verification, and shareable packages."""
from pathlib import Path
import os,sys,subprocess,json,tempfile,struct,zipfile,importlib.util,shutil
from .core import *

def run(args,**kwargs):return subprocess.run([str(a) for a in args],check=True,**kwargs)
def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_chapters','-show_format','-of','json',str(path)]))
def ffescape(s):return str(s).replace('\\','\\\\').replace('\n',' ').replace('=','\\=').replace(';','\\;').replace('#','\\#')

def render(root,preview=False):
 root=Path(root).resolve();p,t=current_timeline(root)
 review=p.get('proof_review',{})
 if review.get('status')!='ready' or review.get('open_issues') or review.get('proof_sha256')!=digest(inside(root,p['proof_file'])):raise ValueError('Complete the mathematical review and bind proof_review.proof_sha256 to the reviewed proof before rendering')
 if digest(root/'audio/narration.wav')!=t['audio_sha256']:raise ValueError('Narration changed since the timeline was built')
 build=root/'build';build.mkdir(exist_ok=True);media=Path(tempfile.mkdtemp(prefix='proof_video_'));log=media/'render.log'
 env=os.environ.copy();env['PROOF_VIDEO_PROJECT']=str(root);scripts=Path(__file__).resolve().parent.parent;env['PYTHONPATH']=str(scripts)+os.pathsep+env.get('PYTHONPATH','')
 try:
  with log.open('w') as f:run([sys.executable,'-m','manim','-qm' if preview else '-qh','--fps','30','--disable_caching','--media_dir',media,Path(__file__).with_name('scene.py'),'ProofVideo'],env=env,cwd=root,stdout=f,stderr=subprocess.STDOUT)
 finally:
  shutil.copy2(log,root/'build/render.log')
 raw=media/'videos/scene'/('720p30' if preview else '1080p30')/'ProofVideo.mp4'
 expected_frames=round(t['duration']*FPS);v=next(s for s in probe(raw)['streams'] if s['codec_type']=='video')
 if int(v['nb_frames'])!=expected_frames:raise ValueError('Renderer frame count does not match the speech timeline')
 meta=root/'build/chapters.ffmetadata';lines=[';FFMETADATA1','title='+ffescape(p['title']),'comment='+ffescape('Synthetic narration. '+p['source']['title']+'; '+p['source']['status'])]
 for ch in t['chapters']:lines+=['[CHAPTER]','TIMEBASE=1/1000',f"START={round(ch['start']*1000)}",f"END={round(ch['end']*1000)}",'title='+ffescape(ch['title'])]
 meta.write_text('\n'.join(lines)+'\n',encoding='utf-8')
 # Audio encoding is keyed by the WAV digest and reused across visual-only edits.
 audio=root/'audio/narration.m4a';audio_meta=root/'audio/encoded.json'
 if not audio.exists() or not audio_meta.exists() or read(audio_meta).get('wav_sha256')!=t['audio_sha256'] or read(audio_meta).get('encoded_sha256')!=digest(audio):
  run(['ffmpeg','-v','error','-y','-i',root/'audio/narration.wav','-c:a','aac','-b:a','160k','-ar','48000','-ac','2',audio]);write(audio_meta,dict(wav_sha256=t['audio_sha256'],encoded_sha256=digest(audio)))
 target=root/'exports'/('preview.mp4' if preview else 'video.mp4');tmp=media/'export.mp4'
 run(['ffmpeg','-v','error','-y','-i',raw,'-i',audio,'-i',meta,'-map','0:v:0','-map','1:a:0','-map_metadata','2','-map_chapters','2','-c:v','copy','-c:a','copy','-movflags','+faststart',tmp]);shutil.copy2(tmp,target)
 write(root/'build/render_manifest.json',dict(plugin_version=VERSION,project_sha256=fingerprint(p),video_sha256=digest(target),video_file=target.name,proof_sha256=digest(inside(root,p['proof_file'])),preview=preview))
 print(str(target),flush=True);return target

def faststart(path):
 boxes=[]
 with Path(path).open('rb') as f:
  while b:=f.read(8):
   if len(b)!=8:raise ValueError('Invalid MP4 box')
   n,k=struct.unpack('>I4s',b);head=8
   if n==1:n=struct.unpack('>Q',f.read(8))[0];head=16
   boxes.append(k)
   if n==0:break
   if n<head:raise ValueError('Invalid MP4 box size')
   f.seek(n-head,1)
 return b'moov' in boxes and b'mdat' in boxes and boxes.index(b'moov')<boxes.index(b'mdat')

def verify(root,preview=False):
 from PIL import Image,ImageDraw
 root=Path(root).resolve();p,t=current_timeline(root);video=root/'exports'/('preview.mp4' if preview else 'video.mp4');info=probe(video);manifest=read(root/'build/render_manifest.json')
 if manifest['project_sha256']!=fingerprint(p) or manifest['video_sha256']!=digest(video):raise ValueError('Stale render: regenerate the video')
 v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio');size=(1280,720) if preview else (1920,1080)
 assert (v['width'],v['height'])==size and v['pix_fmt']=='yuv420p' and v['codec_name']=='h264' and v['avg_frame_rate']=='30/1'
 assert int(v['nb_frames'])==round(t['duration']*FPS)
 assert abs(float(a['duration'])-t['duration'])<.08 and a['codec_name']=='aac'
 assert faststart(video)
 assert len(info['chapters'])==len(t['chapters'])
 for actual,ch in zip(info['chapters'],t['chapters']):
  assert abs(float(actual['start_time'])-ch['start'])<.002 and abs(float(actual['end_time'])-ch['end'])<.002
 audit=read(root/'qa/timing.json');assert len(audit)==sum(len(c['sentences']) for c in t['cues'])
 error=max(abs(a['planned']-a['rendered']) for a in audit);assert error<=1/60+1e-6
 run(['ffmpeg','-v','error','-xerror','-i',video,'-f','null','-'],stdout=subprocess.DEVNULL)
 records=[]
 for c in t['cues']:
  # Last settled state plus early/middle samples catch reveal and transition errors.
  times=sorted(set([min(c['end']-.2,c['start']+2),(c['start']+c['end'])/2,c['end']-.2]))
  for i,sec in enumerate(times):
   target=root/'qa'/f"{c['id']}_{i}.png";run(['ffmpeg','-v','error','-y','-ss',str(sec),'-i',video,'-frames:v','1',target]);records.append(dict(cue=c['id'],time=sec,file=str(target.relative_to(root))))
 for start in range(0,len(records),6):
  subset=records[start:start+6];sheet=Image.new('RGB',(1600,480*((len(subset)+1)//2)),'#101824');draw=ImageDraw.Draw(sheet)
  for i,row in enumerate(subset):
   im=Image.open(root/row['file']).resize((800,450));x=i%2*800;y=i//2*480;sheet.paste(im,(x,y+30));draw.text((x+10,y+5),f"{row['cue']} at {row['time']:.2f}s",fill='white')
  sheet.save(root/'qa'/f'review_{start//6+1:02}.jpg')
 report=dict(video_sha256=digest(video),duration=t['duration'],frame_count=int(v['nb_frames']),decode='passed',max_sentence_onset_error=error,chapter_count=len(t['chapters']),automated_media_checks='passed',visual_review='pending',audio_listening_review='pending',proof_review='Model-assisted; not machine checked',snapshots=records)
 write(root/'exports/verification.json',report);print('Media checks passed. Inspect qa/review_*.jpg, full-resolution frames, and listen to narration; visual/audio review is still pending.',flush=True)
 return report

def mark_review(root,notes,component='both'):
 root=Path(root);p,t=current_timeline(root);r=read(root/'exports/verification.json');v=root/'exports/video.mp4'
 if not v.exists() or digest(v)!=r['video_sha256']:raise ValueError('Review must refer to the current full-quality video')
 if len(notes.strip())<30:raise ValueError('Record what was inspected and any remaining issues')
 if component not in {'both','visual','audio'}:raise ValueError('Unknown review component')
 if component in {'both','visual'}:r.update(visual_review='passed',visual_review_notes=notes)
 if component in {'both','audio'}:r.update(audio_listening_review='passed',audio_review_notes=notes)
 write(root/'exports/verification.json',r)

def package(root):
 root=Path(root).resolve();current_timeline(root);r=read(root/'exports/verification.json');v=root/'exports/video.mp4'
 if digest(v)!=r['video_sha256'] or r['visual_review']!='passed' or r['audio_listening_review']!='passed':raise ValueError('Complete final visual and audio review before packaging')
 out=root/'exports'
 with zipfile.ZipFile(out/'video.zip','w',zipfile.ZIP_STORED) as z:z.write(v,'video.mp4')
 p=read(root/'project.json');names=['provenance.json','build/render_manifest.json','project.json',p['proof_file'],'timeline.json','visuals.py','simulation.py','audio/model_provenance.json','audio/narration.wav','audio/narration.m4a','audio/encoded.json']
 for d in ['audio/cache','assets','simulation_results']:
  names += [str(f.relative_to(root)) for f in (root/d).rglob('*') if f.is_file()] if (root/d).exists() else []
 names+=['exports/'+n for n in ['subtitles.srt','subtitles.vtt','transcript.txt','chapters.txt','verification.json','upload_metadata.md']]
 with zipfile.ZipFile(out/'project_source.zip','w',zipfile.ZIP_DEFLATED) as z:
  for name in sorted(set(names)):
   f=inside(root,name)
   if f.is_file():z.write(f,name)
 print(str(out/'video.zip'));print(str(out/'project_source.zip'))
