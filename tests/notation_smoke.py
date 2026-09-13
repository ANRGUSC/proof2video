from manim import *
from proof_video.typography import math,txt,BG,WHITE,CYAN
class NotationSmoke(Scene):
 def construct(self):
  self.camera.background_color=BG
  self.add(txt('Notation regression: inspect every rule and delimiter',28).move_to([0,3.2,0]))
  rows=[r'\frac{1}{n}\quad\frac{\kappa}{n}\quad\frac{a^2}{a+b}\quad\frac{1}{1+\frac{1}{n}}',r'\sqrt{a+b}\quad\sqrt{\frac{1}{n}}\quad\overline{x_1+x_2+x_3}',r'\begin{pmatrix}1&\frac12\\\frac12&1\end{pmatrix}\quad\left[\frac{a}{b}\right]\quad\left\|x\right\|^2',r'\frac{\kappa}{n}\sum_{i=1}^{n}\left(u_i-\bar u\right)^2']
  for i,s in enumerate(rows):
   m=math(s,size=42).move_to([0,1.9-i*1.35,0])
   if i==3:m.set_color(CYAN)
   self.add(m)
  self.wait(1)
