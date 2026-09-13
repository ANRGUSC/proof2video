# Production pipeline

## Environment

The exercised baseline is Python 3.12, Manim Community 0.20.1, kokoro-onnx 0.6.1,
NumPy, Pillow, SoundFile, FFmpeg, and LaTeX. Use the repository `environment.yml`,
or an equivalent environment. Install TeX separately: pdflatex plus either
dvisvgm or Poppler's pdftocairo. On Debian/Ubuntu, useful packages include
`texlive-latex-extra texlive-fonts-recommended texlive-science dvisvgm poppler-utils`.
Run `doctor` to check the actual environment. Do not assume the host has a GPU,
API key, installed skill dependency, or network access.

Kokoro's model and voices are downloaded separately from the upstream
[kokoro-onnx model release](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.1).
Use `kokoro-v1.0.onnx` and `voices-v1.0.bin`. Model provenance is hashed into the
speech cache. Consult the upstream licenses before redistributing weights; this
plugin does not bundle them. The local speech backend requires no cloud account.

All helpers live under this skill's `scripts/`, so installation of the skill
alone also installs the pipeline. Let `PV` be the absolute path to `scripts/pv.py`.
In a single environment:

```bash
python "$PV" doctor
python "$PV" init my-lesson
# Edit my-lesson/proof.md and project.json; review the mathematics.
python "$PV" validate my-lesson
python "$PV" audio my-lesson --models /path/to/kokoro-models
python "$PV" render my-lesson
python "$PV" verify my-lesson
# Inspect final frames and listen to the speech before recording this review.
python "$PV" review my-lesson --notes "Describe the completed visual and audio checks and their outcome."
python "$PV" package my-lesson
```

To use separate rendering and speech environments, invoke `audio` with
`--tts-python /absolute/path/to/tts-env/bin/python`; `doctor` accepts the same
option. Run all other commands with the rendering Python. The model paths and
project path are passed as structured process arguments, not shell commands.

## Project format

`project.json` has `schema_version: 1`, `title`, `result`, `source`, `proof_file`,
`proof_review`, `voice`, ordered `chapters`, and ordered `cues`. See the fully
worked example under `assets/example/` for an executable specification.

- `source`: `title`, precise `locator`, `status`, and optional `authors`, `url`,
  `expanded_sources` list with URLs/paths, versions, and locations. For paper
  projects, supply hashes/pinned revisions in an additional `provenance.json`.
- `proof_review`: `status: "ready"`, `open_issues: []`, and `proof_sha256` matching
  the reviewed `proof_file` permit rendering. Record actual review in proof.md.
  Use `hashlib.sha256(Path(...).read_bytes()).hexdigest()` to bind the file.
- `voice`: `name`, `speed`, `language`; defaults af_heart, 0.90, en-us.
- Chapters: unique lower-case `id`, readable `title`. Every chapter has cues;
  chapters are contiguous and follow their declared order.
- Each cue: unique `id`, `chapter`, `title`, `proof_step`, `sentences`, optional
  `equations`, `note`, `hold` (seconds), `visual`, and `data`.
- Sentences are explicit objects: `say` is natural spoken text, optional
  `caption` is a plain-text subtitle, optional `highlight` is a zero-based
  equation index. Keep each sentence naturally sized. Never send raw LaTeX to TTS.
- Equations: strings or `{ "latex": "...", "color": "cyan" }`. Supported colors:
  white, cyan, gold, coral, green. Up to four rows; split dense cues further.
- Visuals: equations (default), number_line, curve, custom. See
  [custom-visuals.md](custom-visuals.md).

The schema is deliberately modest. Extend the renderer for genuinely different
visual needs rather than inventing unsupported JSON fields and expecting them
to animate. Project-local custom Python is part of the source and review scope.

## Timing and cache invariants

Every spoken sentence has one cached PCM WAV at 24 kHz. Cache identity includes
spoken text, voice/speed/language, engine version, and model/voices hashes.
Caption spelling and visual equation changes do not invalidate speech.

Cue lengths are rounded upward to whole 30-fps frames after speech, sentence
gaps, and reading holds. All chapter boundaries and captions derive from that
same sample timeline. The renderer rounds onset to the closest video frame;
maximum quantization error is half a frame. This is sentence-level synchronization,
not word-level forced alignment. Explicit animation overruns stop rendering.

After visual edits, `audio` without `--models` can reuse complete cached audio,
refreshing the timeline and captions. Missing/changed speech requires the model
directory. It should report zero synthesized clips for an equation-only edit.
Confirm the narration digest and times are unchanged. `render` rejects a stale
project/timeline and reuses a cached AAC track if the WAV is unchanged.

## Outputs

`exports/video.mp4` is 1080p H.264/yuv420p, AAC, fast-start, with chapters and
burned captions. `render --preview` produces a separate 720p preview; run
`verify --preview` to check it. Render and verify full quality before packaging.
The pipeline also writes SRT, VTT, transcript, chapters, verification JSON,
per-cue frames/contact sheets, a video-only ZIP, and a project-source ZIP.

Captions are burned into the video as well as exported for platform upload.
Viewers enabling platform captions may see two caption rows. If the user prefers
only switchable captions, omit the caption band in the project renderer while
retaining SRT/VTT and timing. Record that choice.

This release produces a chaptered master. Separate chapter MP4 exports, alternate
voices/backends, and word-level highlighting require explicit extensions; do not
claim those features are built in.
