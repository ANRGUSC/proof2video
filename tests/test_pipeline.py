import unittest,tempfile,sys,shutil,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'plugins/proof-to-video/skills/proof-to-video'
sys.path.insert(0,str(SKILL/'scripts'))
from proof_video.core import *
from proof_video.rules import solidify_tex_rules

class ProjectTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'lesson';shutil.copytree(SKILL/'assets/example',self.root)
 def tearDown(self):self.tmp.cleanup()
 def test_example_valid_and_paths_confined(self):
  validate(self.root)
  with self.assertRaises(ValueError):inside(self.root,'../secret')
 def test_chapter_reentry_rejected(self):
  p=read(self.root/'project.json');p['cues'][-1]['chapter']='setup';write(self.root/'project.json',p)
  with self.assertRaisesRegex(ValueError,'contiguous'):validate(self.root)
 def test_invalid_voice_speed_rejected(self):
  p=read(self.root/'project.json');p['voice']['speed']=0;write(self.root/'project.json',p)
  with self.assertRaises(ValueError):validate(self.root)
 def test_caption_and_visual_edits_preserve_speech_identity(self):
  a={'say':'The average is three.'};b={'say':a['say'],'caption':'The average is 3.'}
  self.assertEqual(speech_key(a,{'speed':.9},{}),speech_key(b,{'speed':.9},{}))
  self.assertNotEqual(speech_key(a,{'speed':.9},{}),speech_key(a,{'speed':1},{}))
 def test_stale_timeline_rejected(self):
  p=read(self.root/'project.json');write(self.root/'timeline.json',{'project_sha256':fingerprint(p)})
  p['cues'][0]['title']='Different title';write(self.root/'project.json',p)
  with self.assertRaisesRegex(ValueError,'Project changed'):current_timeline(self.root)
 def test_open_proof_cannot_render(self):
  from proof_video.media import render
  p=read(self.root/'project.json');p['proof_review']['status']='open';write(self.root/'project.json',p);write(self.root/'timeline.json',{'project_sha256':fingerprint(p)})
  with self.assertRaisesRegex(ValueError,'mathematical review'):render(self.root)
 def test_rule_conversion_preserves_geometry_and_is_idempotent(self):
  import xml.etree.ElementTree as E
  p=self.root/'rule.svg';p.write_text('<svg xmlns="http://www.w3.org/2000/svg"><path fill="none" stroke="black" stroke-width="0.4" d="M 0 2 L 10 2"/><path fill="black" d="M 0 0 L 1 0 L 1 1 Z"/></svg>')
  self.assertEqual(solidify_tex_rules(p),1);nodes=list(E.parse(p).getroot());self.assertEqual(nodes[0].get('fill'),'black');self.assertTrue(nodes[0].get('d').endswith(' Z'));self.assertIsNone(nodes[0].get('stroke-width'));self.assertIn('2.200000000',nodes[0].get('d'));self.assertIn('1.800000000',nodes[0].get('d'));self.assertEqual(solidify_tex_rules(p),0)
 def test_unsupported_rule_fails_loudly(self):
  p=self.root/'rule.svg';p.write_text('<svg xmlns="http://www.w3.org/2000/svg"><path fill="none" stroke="black" stroke-width="0.4" d="M 0 0 C 1 0 1 1 2 2"/></svg>')
  with self.assertRaises(ValueError):solidify_tex_rules(p)
 def test_caption_timestamps_roll_over(self):self.assertEqual(stamp(59.9996),'00:01:00,000')
 def test_visual_review_does_not_claim_listening_or_allow_packaging(self):
  from proof_video.media import mark_review,package
  p=read(self.root/'project.json');write(self.root/'timeline.json',{'project_sha256':fingerprint(p)})
  v=self.root/'exports/video.mp4';v.parent.mkdir();v.write_bytes(b'review-fixture')
  from proof_video.media import render_inputs
  (self.root/'audio').mkdir();(self.root/'audio/narration.wav').write_bytes(b'audio-fixture')
  write(self.root/'build/render_manifest.json',{'project_sha256':fingerprint(p),'video_sha256':digest(v),'inputs':render_inputs(self.root,p)})
  write(self.root/'exports/verification.json',{'video_sha256':digest(v),'automated_media_checks':'passed','visual_review':'pending','audio_listening_review':'pending'})
  mark_review(self.root,'Inspected the exported frames for legibility and notation.',component='visual')
  r=read(self.root/'exports/verification.json');self.assertEqual(r['visual_review'],'passed');self.assertEqual(r['audio_listening_review'],'pending')
  with self.assertRaisesRegex(ValueError,'visual and audio review'):package(self.root)
  mark_review(self.root,'Fixture attestation for testing the packaging mechanism only.',component='audio')
  package(self.root)
  import zipfile
  with zipfile.ZipFile(self.root/'exports/video.zip') as z:
   self.assertIsNone(z.testzip());self.assertEqual(z.read('video.mp4'),b'review-fixture')
  with zipfile.ZipFile(self.root/'exports/project_source.zip') as z:
   self.assertIsNone(z.testzip());self.assertIn('proof.md',z.namelist());self.assertIn('exports/verification.json',z.namelist())
 def test_changed_render_inputs_block_review_and_package(self):
  from proof_video.media import render_inputs,mark_review,package
  p=read(self.root/'project.json');write(self.root/'timeline.json',{'project_sha256':fingerprint(p)})
  v=self.root/'exports/video.mp4';v.parent.mkdir();v.write_bytes(b'video-fixture')
  (self.root/'audio').mkdir();(self.root/'audio/narration.wav').write_bytes(b'audio-fixture')
  for name in ['proof.md','visuals.py','assets/plot.svg','audio/narration.wav','exports/subtitles.srt']:
   f=self.root/name;f.parent.mkdir(exist_ok=True);f.write_text('original')
  for name in ['proof.md','visuals.py','assets/plot.svg','audio/narration.wav','timeline.json','exports/subtitles.srt']:
   with self.subTest(name=name):
    write(self.root/'build/render_manifest.json',{'project_sha256':fingerprint(p),'video_sha256':digest(v),'inputs':render_inputs(self.root,p)})
    write(self.root/'exports/verification.json',{'video_sha256':digest(v),'automated_media_checks':'passed','visual_review':'passed','audio_listening_review':'passed'})
    f=self.root/name;original=f.read_bytes();f.write_bytes(original+b' ')
    with self.assertRaisesRegex(ValueError,'Stale render'):mark_review(self.root,'Inspected the final video and listened to all narration.')
    with self.assertRaisesRegex(ValueError,'Stale render'):package(self.root)
    f.write_bytes(original)
 def test_visual_only_revision_reuses_audio_and_all_times(self):
  import numpy as np,soundfile as sf
  from proof_video.audio import build
  p=read(self.root/'project.json');p['cues']=p['cues'][:1];p['chapters']=p['chapters'][:1];p['cues'][0]['sentences']=[{'say':'Cached test speech.'}];write(self.root/'project.json',p)
  models={'model_sha256':'test','voices_sha256':'test'};write(self.root/'audio/model_provenance.json',models)
  key=speech_key(p['cues'][0]['sentences'][0],p['voice'],models);wav=self.root/'audio/cache'/f'{key}.wav';wav.parent.mkdir();sf.write(wav,.1*np.sin(np.arange(24000)*.03),24000,subtype='PCM_16');write(wav.with_suffix('.json'),{'sha256':digest(wav),'key':key})
  a=build(self.root);wavhash=digest(self.root/'audio/narration.wav');p['cues'][0]['equations']=[r'\frac12'];write(self.root/'project.json',p);b=build(self.root)
  self.assertEqual(a['duration'],b['duration']);self.assertEqual(a['cues'][0]['sentences'],b['cues'][0]['sentences']);self.assertEqual(wavhash,digest(self.root/'audio/narration.wav'));self.assertEqual(read(self.root/'exports/audio_build.json')['created'],0)

if __name__=='__main__':unittest.main()
