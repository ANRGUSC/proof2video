"""Local Kokoro speech with content-addressed caching and sample-derived timing."""
from pathlib import Path
import math,importlib.metadata
import numpy as np
import soundfile as sf
from .core import *

def build(root,models_dir=None):
 root=Path(root).resolve();p=validate(root);cache=root/'audio/cache';cache.mkdir(parents=True,exist_ok=True)
 voice=dict(name='af_heart',speed=.9,language='en-us');voice.update(p['voice'])
 model_meta=root/'audio/model_provenance.json'
 if models_dir:
  models_dir=Path(models_dir).resolve();model=models_dir/'kokoro-v1.0.onnx';voices=models_dir/'voices-v1.0.bin'
  models={'model_sha256':digest(model),'voices_sha256':digest(voices),'kokoro_onnx_version':importlib.metadata.version('kokoro-onnx')}
  write(model_meta,models)
 elif model_meta.exists():models=read(model_meta)
 else:raise ValueError('First audio build needs --models DIR with Kokoro model and voices files')
 synth=None;cursor=0;cues=[];blocks=[];old_ch=None;created=0;reused=0
 for c in p['cues']:
  lead=.55 if c['chapter']!=old_ch else .24;old_ch=c['chapter'];parts=[np.zeros(round(lead*SR),dtype=np.float32)];local=len(parts[0]);sentences=[]
  for i,s in enumerate(c['sentences']):
   key=speech_key(s,voice,models);wav=cache/(key+'.wav');meta=cache/(key+'.json')
   valid=wav.exists() and meta.exists() and read(meta).get('sha256')==digest(wav)
   if not valid:
    if models_dir is None:raise ValueError('Missing or changed speech: rerun with --models DIR')
    if synth is None:
     from kokoro_onnx import Kokoro
     import onnxruntime as ort
     opts=ort.SessionOptions();opts.intra_op_num_threads=4;opts.inter_op_num_threads=1
     synth=Kokoro.from_session(ort.InferenceSession(str(model),sess_options=opts,providers=['CPUExecutionProvider']),str(voices))
    samples,rate=synth.create(s['say'],voice=voice['name'],speed=voice['speed'],lang=voice['language'])
    if rate!=SR:raise ValueError(f'Unexpected sample rate {rate}')
    sf.write(wav,samples,SR,subtype='PCM_16');write(meta,dict(sha256=digest(wav),key=key));created+=1
   else:reused+=1
   samples,rate=sf.read(wav,dtype='float32')
   if rate!=SR or samples.ndim!=1 or len(samples)==0 or not np.isfinite(samples).all() or float(np.max(np.abs(samples)))<1e-5:raise ValueError(f'Invalid speech clip: {wav.name}')
   start=(cursor+local)/SR;parts.append(samples);local+=len(samples)
   sentences.append(dict(s,audio_start=start,audio_end=(cursor+local)/SR,audio_file=str(wav.relative_to(root))))
   if i<len(c['sentences'])-1:gap=np.zeros(round(.1*SR),dtype=np.float32);parts.append(gap);local+=len(gap)
  frames=math.ceil((local/SR+c.get('hold',3))*FPS);total=frames*(SR//FPS);parts.append(np.zeros(total-local,dtype=np.float32))
  for i,s in enumerate(sentences):s['caption_end']=sentences[i+1]['audio_start'] if i+1<len(sentences) else (cursor+total)/SR
  cues.append(dict(c,start=cursor/SR,end=(cursor+total)/SR,frames=frames,sentences=sentences));blocks.append(np.concatenate(parts));cursor+=total
 audio=np.concatenate(blocks);peak=float(np.max(np.abs(audio)))
 if peak>.9:audio*=.9/peak
 sf.write(root/'audio/narration.wav',audio,SR,subtype='PCM_16')
 chapters=[]
 for ch in p['chapters']:
  cc=[c for c in cues if c['chapter']==ch['id']];chapters.append(dict(ch,start=cc[0]['start'],end=cc[-1]['end']))
 t=dict(schema_version=1,project_sha256=fingerprint(p),duration=cursor/SR,fps=FPS,sample_rate=SR,chapters=chapters,cues=cues,voice=voice,models=models,audio_sha256=digest(root/'audio/narration.wav'))
 write(root/'timeline.json',t)
 out=root/'exports';out.mkdir(exist_ok=True);ss=[s for c in cues for s in c['sentences']]
 (out/'subtitles.srt').write_text('\n'.join(f"{i+1}\n{stamp(s['audio_start'])} --> {stamp(s['caption_end'])}\n{s.get('caption',s['say'])}\n" for i,s in enumerate(ss)),encoding='utf-8')
 (out/'subtitles.vtt').write_text('WEBVTT\n\n'+'\n'.join(f"{stamp(s['audio_start'],'.')} --> {stamp(s['caption_end'],'.')}\n{s.get('caption',s['say'])}\n" for s in ss),encoding='utf-8')
 (out/'transcript.txt').write_text('\n\n'.join(c['title']+'\n'+' '.join(s['say'] for s in c['sentences']) for c in cues),encoding='utf-8')
 (out/'chapters.txt').write_text('\n'.join(stamp(ch['start'],'.').split('.')[0]+' '+ch['title'] for ch in chapters)+'\n',encoding='utf-8')
 write(out/'audio_build.json',dict(created=created,reused=reused,duration=t['duration'],audio_sha256=t['audio_sha256']))
 print(f"Speech: {created} synthesized, {reused} cached; duration {stamp(t['duration'],'.')}",flush=True)
 return t
