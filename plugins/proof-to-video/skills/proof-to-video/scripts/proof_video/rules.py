"""Normalize mathematical SVG rules without importing Manim."""
from pathlib import Path
import re
import math as scalar_math
import xml.etree.ElementTree as ET

def solidify_tex_rules(path):
    """Preserve Poppler's straight rule strokes as closed, filled SVG paths.

    SingleStringMathTex sets stroke_width=0, which hides open fraction,
    radical and overline paths. Filled outlines retain the original geometry
    and scale with the glyphs without globally thickening the lettering.
    """
    path = Path(path)
    tree = ET.parse(path)
    changed = 0
    number = r"[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?"
    line = re.compile(rf"\s*M\s*({number})[ ,]+({number})\s*L\s*({number})[ ,]+({number})\s*")
    for node in tree.getroot().iter():
        if not node.tag.endswith('}path') or node.get('fill') != 'none':
            continue
        width = float(node.get('stroke-width', '0'))
        if width <= 0:
            continue
        match = line.fullmatch(node.get('d', ''))
        if match is None:
            raise ValueError(f'Unrecognized stroked TeX rule in {path}')
        x1, y1, x2, y2 = map(float, match.groups())
        length = scalar_math.hypot(x2-x1, y2-y1)
        if not length:
            raise ValueError(f'Zero-length TeX rule in {path}')
        dx, dy = -(y2-y1)*width/(2*length), (x2-x1)*width/(2*length)
        points = [(x1+dx,y1+dy),(x2+dx,y2+dy),(x2-dx,y2-dy),(x1-dx,y1-dy)]
        node.set('d', 'M '+' L '.join(f'{x:.9f} {y:.9f}' for x,y in points)+' Z')
        node.set('fill', node.get('stroke', 'black'))
        node.set('fill-opacity', node.get('stroke-opacity', '1'))
        for key in list(node.attrib):
            if key == 'stroke' or key.startswith('stroke-'):
                del node.attrib[key]
        changed += 1
    if changed:
        ET.register_namespace('', 'http://www.w3.org/2000/svg')
        ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
        tree.write(path, encoding='utf-8', xml_declaration=True)
    return changed
