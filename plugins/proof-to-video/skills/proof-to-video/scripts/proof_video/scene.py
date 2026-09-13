"""Generic narrated lesson renderer; project visuals.py supplies custom animations."""
from pathlib import Path
import os,json,textwrap,importlib.util
import numpy as np
from manim import *
from proof_video.typography import math,txt,solidify_tex_rules,BG,WHITE,MUTED,GRID,CYAN,GOLD,CORAL,GREEN
from proof_video.core import read,write,inside

COLORS={'white':WHITE,'cyan':CYAN,'gold':GOLD,'coral':CORAL,'green':GREEN}
def fit(m,width=12.2,height=None):
 if m.width>width:m.scale_to_fit_width(width)
 if height and m.height>height:m.scale_to_fit_height(height)
 return m

def eq(spec):
 if isinstance(spec,str):spec={'latex':spec}
 return fit(math(spec['latex'],size=43).set_color(COLORS.get(spec.get('color','white'),WHITE)))

class ProofVideo(Scene):
 def setup(self):
  self.root=Path(os.environ['PROOF_VIDEO_PROJECT']).resolve();self.project=read(self.root/'project.json');self.timeline=read(self.root/'timeline.json');self.caption=VGroup();self.audit=[];self.layouts=[];self.custom=None
  config.text_dir=str(Path(config.media_dir)/'texts');Path(config.text_dir).mkdir(parents=True,exist_ok=True)
  if any(c.get('visual')=='custom' for c in self.timeline['cues']):
   path=inside(self.root,'visuals.py');spec=importlib.util.spec_from_file_location('project_visuals',path);self.custom=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.custom)
 def heading(self,s):return fit(txt(s,29),12.2).move_to([0,2.12,0])
 def frame(self):
  title=fit(txt(self.project['title'],30),11.8).move_to([-6.2,3.4,0],aligned_edge=LEFT)
  rule=Line([-6.2,2.72,0],[6.2,2.72,0],color=GRID,stroke_width=1)
  foot=fit(txt(self.project['result']+' · '+self.project['source']['status'],14,MUTED),12.2).move_to([-6.2,-2.7,0],aligned_edge=LEFT)
  band=Rectangle(width=14.23,height=1.03,fill_color='#0B111B',fill_opacity=1,stroke_width=0).move_to([0,-3.485,0]);self.add(title,rule,foot,band);self.chrome=set(self.mobjects)
 def caption_text(self,words):
  self.remove(self.caption);self.caption=fit(txt(textwrap.fill(words,width=100),20,line_spacing=.75),12.7,.8).move_to([0,-3.48,0]);self.add(self.caption)
 def wait_to(self,t):
  frames=round(t*30)-round(float(self.renderer.time)*30)
  if frames<0:raise RuntimeError(f'Visual event exceeded sentence timing by {-frames/30:.3f}s. Shorten the event or extend that cue; do not silently speed up speech.')
  if frames:self.wait(frames/30,frozen_frame=True)
 def equations(self,c):
  eqs=VGroup(*(eq(e) for e in c.get('equations',[]))).arrange(DOWN,buff=.4);fit(eqs,12.1,2.9).move_to([0,.15,0])
  g=VGroup(self.heading(c['title']),eqs);events={}
  if c.get('note'):g.add(fit(txt(textwrap.fill(c['note'],width=93),22,MUTED),12.2,.58).move_to([0,-2.1,0]))
  for i,s in enumerate(c['sentences']):
   if 'highlight' in s:
    index=s['highlight']
    if not isinstance(index,int) or not 0<=index<len(eqs):raise ValueError('Invalid equation highlight index')
    events[i]=lambda index=index:self.play(Indicate(eqs[index],color=CYAN,scale_factor=1.02),run_time=.6)
  return g,events
 def number_line(self,c):
  data=c['data'];values=data['values'];mean=float(np.mean(values));lo=min(values)-1;hi=max(values)+1
  line=NumberLine(x_range=[lo,hi,1],length=10,include_numbers=True,color=MUTED).move_to([0,.35,0]);g=VGroup(self.heading(c['title']),line)
  for v in values:g.add(Dot(line.n2p(v),color=CYAN,radius=.08))
  marker=ValueTracker(data.get('start',mean));arrow=always_redraw(lambda:Arrow(line.n2p(marker.get_value())+UP*1.1,line.n2p(marker.get_value())+UP*.14,color=GOLD,buff=.03))
  label=math(r'\bar x='+f'{mean:g}',size=38).set_color(GOLD).move_to([0,-1.1,0]);g.add(arrow,label)
  if c.get('note'):g.add(fit(txt(c['note'],23,MUTED),12.2).move_to([0,-2.1,0]))
  def move():self.play(marker.animate.set_value(mean),run_time=1.2)
  return g,{data.get('event_sentence',0):move}
 def curve(self,c):
  data=c['data'];coeff=data['coefficients'];xr=data.get('x_range',[-3,3,1]);yr=data.get('y_range',[0,12,2]);axes=Axes(x_range=xr,y_range=yr,x_length=9,y_length=2.8,axis_config={'color':GRID,'include_tip':False,'include_numbers':True,'font_size':20}).move_to([0,-.1,0])
  graph=axes.plot(lambda x:float(np.polyval(coeff,x)),x_range=xr[:2],color=CYAN)
  labels=VGroup(math(data.get('x_label','a'),size=26).next_to(axes.x_axis,RIGHT),math(data.get('y_label','F(a)'),size=26).next_to(axes.y_axis,LEFT,buff=.25).align_to(axes.y_axis,UP))
  g=VGroup(self.heading(c['title']),axes,graph,labels);events={}
  if 'start' in data and 'target' in data:
   marker=ValueTracker(data['start']);dot=always_redraw(lambda:Dot(axes.c2p(marker.get_value(),float(np.polyval(coeff,marker.get_value()))),color=GOLD));g.add(dot)
   def move():self.play(marker.animate.set_value(data['target']),run_time=1.2)
   events[data.get('event_sentence',0)]=move
  if c.get('note'):g.add(fit(txt(c['note'],22,MUTED),12.2).move_to([0,-2.2,0]))
  return g,events
 def visual(self,c):
  kind=c.get('visual','equations')
  if kind=='custom':return self.custom.make_visual(self,c)
  return getattr(self,kind)(c)
 def construct(self):
  self.frame()
  for c in self.timeline['cues']:
   self.wait_to(c['start']);group,events=self.visual(c)
   if any(not isinstance(k,int) or not 0<=k<len(c['sentences']) for k in events):raise ValueError('Visual event must reference a sentence index')
   for i,s in enumerate(c['sentences']):
    self.wait_to(s['audio_start']);self.caption_text(s.get('caption',s['say']));self.audit.append(dict(cue=c['id'],sentence=i,planned=s['audio_start'],rendered=float(self.renderer.time)))
    if i==0:
     old=[m for m in self.mobjects if m not in self.chrome and m is not self.caption];self.play(*(FadeOut(m) for m in old),FadeIn(group),run_time=.6);self.remove(*old)
    if i in events:events[i]()
    self.wait_to(s['audio_end'])
   self.wait_to(c['end']);b=dict(left=float(group.get_left()[0]),right=float(group.get_right()[0]),top=float(group.get_top()[1]),bottom=float(group.get_bottom()[1]));self.layouts.append(dict(cue=c['id'],**b))
   if b['left']< -6.48 or b['right']>6.48 or b['top']>2.57 or b['bottom']< -2.49:raise RuntimeError(f'Content outside safe area: {c["id"]} {b}')
  self.wait_to(self.timeline['duration']);write(self.root/'qa/timing.json',self.audit);write(self.root/'qa/layouts.json',self.layouts)
