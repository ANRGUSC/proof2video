# Proof to Video

By **Bhaskar Krishnamachari** · BSD-3-Clause

A Codex and Claude Code plugin for turning a theorem or lemma into a carefully expanded,
narrated mathematical video for advanced undergraduates and beginning graduate
students.

Give Codex the paper, the result to explain, and any detailed companion guide,
appendix, or proof report. The plugin guides it through the derivation and
storyboard, then supplies a working pipeline for Manim animations, local Kokoro
speech, synchronized subtitles, chaptered video, and final review.

This is a reusable production workflow, not an automatic proof verifier. Codex
still has to understand the sources, justify the steps, write appropriate visual
code, and inspect the result. No particular paper, mathematical model, or cloud
speech service is required.

## Use it

**Best for:** instructors preparing a proof walkthrough, researchers explaining a
specific result, and students who want the intermediate steps made explicit.
Identify the theorem or lemmas and provide their assumptions and source proofs.
Expect to review the mathematics and iterate on the visuals and pronunciation.

**Choose your starting point:**

- To explain your own result with Codex, [install the skill](#install-the-skill-from-a-checkout),
  set up the media environment below, then attach your sources and use this prompt.
- To try the renderer first, [run the supplied example](#run-the-supplied-example-without-codex).
  This route needs no Codex account or speech API key.

This is an early 0.1.0 workflow. It does not turn an arbitrary PDF into a finished
video in one command. Codex authors the proof, narration, and scene descriptions;
the Python CLI renders an already-authored lesson. Long research proofs and
specialized diagrams need additional authoring and review.

```text
$proof-to-video Explain Theorem 2 in this paper for a senior undergraduate or
first-year graduate student. Use the attached expanded proof report and guide
for the intermediate details. Start with the necessary preliminaries, then
build a chaptered video with narration, animations, and subtitles. Include the
expanded proof, reproducible source, and a ZIP of the final video.
```

For a later visual correction:

```text
$proof-to-video Fix these notation errors in the video. Preserve the existing
narration, subtitle timings, and chapter boundaries. Check the repaired scenes
in the final encoded MP4 before delivering a corrected video ZIP.
```

## Choose the length and number of videos

Tell the agent which results to cover, the intended audience, the desired depth,
and a target duration or range **per video**. For example, ask for an intuitive
overview, a complete proof walkthrough, or a detailed tutorial with prerequisites.
These choices determine the amount of narration, examples, and reading time.

There is no fixed output length and no CLI `--duration` option. Before speech is
generated, duration is an estimate based on the proposed script and pauses. After
`audio`, the pipeline reports the measured duration and writes it to
`timeline.json` (`duration`, in seconds), before video rendering starts. The
bundled example measures 110.1 seconds; other lessons can be substantially longer.
Video duration is separate from the time needed to generate/render it.

You can request a planning checkpoint and a second checkpoint after speech:

```text
$proof-to-video Explain Theorem 2 from this paper for senior undergraduates.
Aim for 8–10 minutes, including prerequisites and one example. First show me
the chapter outline, assumed background, and estimated duration. Wait for my
feedback before producing the media. After generating narration, tell me the
measured duration so we can adjust it before rendering.
```

A target is an authoring constraint, not an automatic exact-length guarantee.
If a complete explanation will exceed it, ask the agent to propose a narrower
scope, fewer examples, assumed prerequisites, or a split into several videos.
An overview that omits proof details should be labeled accordingly. Changing
speech speed affects duration too, but mathematical steps still need readable
pacing. Script edits require regenerating affected speech clips and timing.

For **two separate videos**, use two project directories, each with its own
proof, narration, timeline, MP4, and review. The agent runs the pipeline for each:

```text
$proof-to-video Use this paper to make two self-contained videos: one on
Theorem 1 and one on Theorem 3. Aim for 6–8 minutes each for beginning graduate
students. Include the prerequisites each needs, even if that repeats material.
First propose both outlines and duration estimates; wait for my feedback.
```

For **one combined video**, use one project with chapters for the shared
background and each theorem:

```text
$proof-to-video Make one 12–15 minute video covering Theorems 1 and 3 from this
paper. Explain shared prerequisites once, then give each theorem its own
chapters and explain their connection. First propose the outline and flag
whether complete proofs fit the target before generating media.
```

These are instructions to the authoring agent; the CLI does not select theorems
from a PDF or automatically split a master into separate theorem videos. You can
revise scope, audience, emphasis, and duration during planning, then revise the
script or preview. Make structural changes early to avoid unnecessary rerenders.
Multi-theorem authoring has not yet been validated end to end; see the release audit.

## What it produces

| Stage | Artifact |
|---|---|
| Grounding | Exact result/version, source locations, companion-proof inventory |
| Mathematics | Prerequisites, expanded proof, source mapping, review and open issues |
| Teaching | Explicit narration sentences and a chaptered storyboard |
| Illustrations | Checked numerical examples, plots, or custom Manim animation code |
| Speech and timing | Cached sentence WAVs, sample-derived timeline, SRT/VTT |
| Rendering | 1080p H.264/AAC MP4 with chapters and burned captions |
| Review | Full-file media checks and initial/middle/final cue snapshots |
| Delivery | Video ZIP, source ZIP, transcript, chapters, and upload metadata |

![Frame from the rendered example](docs/images/example-frame.png)

The bundled independent example proves that the arithmetic mean is the unique
constant minimizing average squared error. It includes the complete elementary
proof, a number-line animation, a loss curve, and deterministic numerical checks.

## Install the skill from a checkout

Clone the public repository, then install:

```bash
git clone https://github.com/ANRGUSC/proof2video.git
cd proof2video
```

From the checkout, run:

```bash
python scripts/install_skill.py
```

This copies the self-contained skill and its helpers into
`~/.codex/skills/proof-to-video` (or `$CODEX_HOME/skills/proof-to-video`). It does
not overwrite an existing installation. Start a new Codex session and invoke
`$proof-to-video`. To install in an isolated location, use
`python scripts/install_skill.py --skills-dir /path/to/skills`.

The installer copies files only: it does **not** install Python/media dependencies
or download speech weights. For clients using the current documented user skill
location, explicitly choose it: `python scripts/install_skill.py --skills-dir ~/.agents/skills`
(PowerShell: `python scripts/install_skill.py --skills-dir "$HOME/.agents/skills"`).
See [OpenAI's skill discovery documentation](https://learn.chatgpt.com/docs/build-skills).

The plugin manifest is at
`plugins/proof-to-video/.codex-plugin/plugin.json`; a repository-local marketplace
catalog is also included. Plugin-capable Codex clients can use this directory as
a plugin source. See [installation notes](docs/INSTALLATION.md) for the catalog
and the difference between a plugin installation and a standalone skill.

## Use locally with Claude Code

From this checkout, launch Claude Code with the plugin directory:

```bash
claude --plugin-dir ./plugins/proof-to-video
```

Then invoke its namespaced skill:

```text
/proof-to-video:proof-to-video Explain Theorem 2 in the attached paper.
First propose the outline and estimated duration before generating media.
```

This loads the plugin for that session without a marketplace. Pass `--plugin-dir`
on each launch; from another working directory, use the absolute plugin path.
The same skill, examples, Python pipeline, and media dependencies are shared with
Codex. Substitute `/proof-to-video:proof-to-video` for `$proof-to-video` in the
prompt examples above. The standalone `install_skill.py` installer is for Codex;
Claude Code uses the plugin directory directly.

Set up the media environment below before generating videos. Loading the plugin
does not install dependencies. See [Claude Code's local plugin documentation](https://code.claude.com/docs/en/plugins).

## Run the supplied example without Codex

You need Python 3.12, Manim 0.20.1, FFmpeg **and ffprobe**, LaTeX, and local Kokoro
speech dependencies and weights. A CPU is sufficient. Allow disk space for the
Python environment, roughly 340 MiB of speech weights, and temporary render files.
The first run downloads dependencies and synthesizes speech; later visual edits
reuse cached speech. Codex usage, if used for authoring, is separate.

The following commands use Bash (Linux/macOS):

```bash
conda env create -f environment.yml
conda activate proof-to-video
# Install LaTeX plus dvisvgm, or pdfLaTeX plus Poppler's pdftocairo.
# Download Kokoro model/voices separately as described below.
PV=plugins/proof-to-video/skills/proof-to-video/scripts/pv.py
python "$PV" doctor
python "$PV" init work/mean-example
python work/mean-example/simulation.py
python "$PV" audio work/mean-example --models /path/to/kokoro-models
python "$PV" render work/mean-example
python "$PV" verify work/mean-example
```

On Windows, use the same conda environment commands and set the script variable
with `$PV = "plugins/proof-to-video/skills/proof-to-video/scripts/pv.py"` in
PowerShell. The `python "$PV" ...` commands then work unchanged. Use a real model
directory, for example `--models "C:/models/kokoro"`. MiKTeX supplies LaTeX tools;
ensure required packages are installed before an unattended render.

If conda is unavailable, create a Python 3.12 virtual environment and install
`manim==0.20.1 kokoro-onnx==0.6.1 numpy pillow soundfile` with pip. Install FFmpeg
and LaTeX separately and add their executables to `PATH`. Manim may require
platform libraries when wheels are unavailable. Run `doctor` in the same Python
environment you will use for rendering; a successful check confirms dependency
discovery, while rendering the example tests that they actually work together.

Inspect `work/mean-example/qa/final/review_*.jpg`, open the full-resolution frames,
and listen to the video. Only after those checks:

```bash
python "$PV" review work/mean-example --notes "Describe what you inspected, heard, and verified."
python "$PV" package work/mean-example
```

To record only the review actually completed, use `review --component visual`
or `review --component audio`. Packaging requires both; never mark listening
complete based only on waveform or transcription checks.

The outputs are in `work/mean-example/exports/`. `init` copies a reviewed example;
when adapting it to another theorem, replace the proof review and its hash with
a review of the new mathematical argument.

Open `exports/video.mp4` for the final video. The same directory contains
`subtitles.srt`, `subtitles.vtt`, `transcript.txt`, `chapters.txt`, and
`verification.json`; after review and packaging it also contains `video.zip`
and `project_source.zip`. Upload metadata is authored separately by Codex or you;
see the [review and release guide](plugins/proof-to-video/skills/proof-to-video/references/review-and-release.md).

For a faster visual iteration, use `render ... --preview` and `verify ... --preview`
to produce/check `exports/preview.mp4` at 720p. Preview checks do not qualify a
final video for packaging. To adapt the example, edit `proof.md` and `project.json`
as described in the [project format](plugins/proof-to-video/skills/proof-to-video/references/pipeline.md).
Project-local `visuals.py` is executable Python; review supplied custom code before running it.

### Local speech

Use [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx) with the two files
from its [model release](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.1):

- `kokoro-v1.0.onnx`
- `voices-v1.0.bin`

No speech API key is needed. Weights are downloaded separately and their hashes
are recorded. Default voice: `af_heart`, speed `0.90`; it is configurable. Speech
is cached by text, voice settings, engine version, and model hashes. Visual-only
edits reuse existing speech and encoded audio.

If TTS and Manim are installed in separate Python environments, pass
`--tts-python /path/to/tts-python` to `audio` and `doctor`.

### Troubleshooting

| Symptom | Next step |
|---|---|
| `doctor` reports missing tools | Install them in the active environment or add their binary directory to `PATH`; both `ffmpeg` and `ffprobe` are needed. |
| First audio build fails | Check both model filenames and pass their containing directory with `--models`. |
| `Project changed` | Run `audio` again; unchanged speech is reused. Then render and verify again. |
| `Stale render` | A bound input changed. Render and verify the current project before recording a new review. |
| LaTeX or Manim render fails | Read `build/render.log`; install missing TeX packages or correct the reported formula/layout/timing issue. |
| Packaging asks for review | Inspect the final MP4 and listen, then record the completed components with `review`. |
| Skill is not visible | Check your client's discovery directory and restart Codex; see installation notes. |

## What the checks do and do not establish

The automated checks validate project structure, video decoding, codecs,
duration, frame count, chapters, and sentence timing. They do not prove a
mathematical theorem or replace visual/audio review. The renderer preserves
fraction bars, long overlines, and radical bars across the portable SVG pipeline;
the review still checks them in the actual MP4.

This release provides a chaptered master, built-in equation/number-line/polynomial
visuals, and project-local custom Manim hooks. Codex writes custom animations for
other mathematical structures. Word-level highlighting, alternative TTS backends,
and separate per-chapter MP4 export are extension points, not built-in promises.

## Develop and contribute

```bash
python -m unittest discover -s tests -v
python scripts/check_repository.py
```

Unit tests need NumPy and SoundFile (`python -m pip install numpy soundfile`).
Rendering needs the full environment. See
[validation notes](docs/VALIDATION.md), [contribution guide](CONTRIBUTING.md), and
[provenance](PROVENANCE.md). The initial release is version 0.1.0.
The [release audit](docs/RELEASE_AUDIT.md) records the Windows end-to-end checks,
fixes, and remaining listening/client-installation checks.

Public source belongs in Git; generated MP4s, audio caches, and model weights do
not. Use release assets for example videos and source bundles. The plugin does
not upload to YouTube or create repositories automatically.

BSD-3-Clause. See [LICENSE](LICENSE) and [third-party notices](THIRD_PARTY_NOTICES.md).
