"""Shared typography and robust vector equations for mathematical videos.

The portable converter supports pdflatex plus pdftocairo when dvisvgm is absent.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import textwrap
import re
import math as scalar_math
import xml.etree.ElementTree as ET
from pathlib import Path
from manim import *

ROOT = Path(__file__).resolve().parent
BG = "#101824"
WHITE = "#EDF2F5"
MUTED = "#A3B3C6"
GRID = "#344356"
CYAN = "#6DD9E5"
GOLD = "#FFD078"
CORAL = "#FFAC96"
GREEN = "#8AE3B3"
LAVENDER = "#C5B6FF"
FONT = "DejaVu Sans"

config.background_color = BG
config.frame_width = 14.2222222222
config.frame_height = 8
config.frame_rate = 30

from .rules import solidify_tex_rules

# A portable vector conversion path for environments without dvisvgm.
# Both routes compile the same LaTeX and produce SVG paths for Manim.
if not shutil.which("dvisvgm"):
    import manim.utils.tex_file_writing as tex_files
    config.tex_template = TexTemplate(tex_compiler="pdflatex", output_format=".pdf")

    def pdf_to_svg(path, extension=".pdf", page=1, **kwargs):
        path = Path(path)
        if extension != ".pdf" or page != 1:
            raise ValueError("The portable converter accepts single-page PDF formulas.")
        out = path.with_suffix(".svg")
        if not out.exists():
            subprocess.run(["pdftocairo", "-svg", str(path), str(out)], check=True,
                           stdout=subprocess.DEVNULL)
        solidify_tex_rules(out)
        return out

    tex_files.convert_to_svg = pdf_to_svg


def txt(s, size=26, color=WHITE, **kwargs):
    return Text(s, font=FONT, font_size=size, color=color, **kwargs)


def math(*parts, size=44, **kwargs):
    # Typeset the entire equation once so every term shares the true LaTeX
    # baseline. Partition its glyphs into animation groups using standalone
    # part counts, without relying on dvisvgm-specific SVG tags.
    color = kwargs.pop("color", WHITE)
    full = SingleStringMathTex(" ".join(parts), font_size=size, color=color, **kwargs)
    if len(parts) == 1:
        return VGroup(full)
    counts = [len(SingleStringMathTex(part, font_size=size, color=color, **kwargs).submobjects)
              for part in parts]
    if sum(counts) != len(full.submobjects):
        raise ValueError(f"Cannot partition equation glyphs reliably: {parts}")
    groups = []
    index = 0
    for part, count in zip(parts, counts):
        group = VGroup(*full.submobjects[index:index+count])
        group.tex_string = part
        groups.append(group)
        index += count
    return VGroup(*groups)
