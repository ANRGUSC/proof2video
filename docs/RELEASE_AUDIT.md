# Release audit — 13 September 2026

## Assessment

The supplied lesson and custom-animation pipeline work on this Windows machine
after installing dependencies. The source is suitable for a supervised early
release after reviewing these fixes. This is not evidence that arbitrary papers
can be converted reliably without expert authoring and review.

Before broader promotion, complete a listening review of the example, exercise
skill discovery and a new theorem in a fresh Codex session, and run CI on the
release commit. The new Linux/Windows/macOS CI matrix has been configured locally
but has not run on GitHub. No public release was published during this audit.

## Baseline and environment

Started from `2a2aad513db4cfc13dbd5f63128e675fdb91c98a` and tested the local
changes described below. Python 3.12, Manim 0.20.1, kokoro-onnx 0.6.1,
ONNX Runtime 1.30.0, NumPy 2.5.3, SoundFile 0.14.0, FFmpeg 8.0.1,
and existing MiKTeX/dvisvgm were used. Python packages were installed into a
fresh workspace virtual environment; this was not a clean conda installation.
The Windows font fallback selected Arial. MiKTeX needed access to its normal
configuration/cache directories outside the restricted workspace.

## Completed checks

| Check | Result |
|---|---|
| Unit/regression and CLI tests | 15 passed, including subprocess installation, paths with spaces, refusal to overwrite, missing-model diagnostics, cache preservation, stale-input rejection, and packaging fixture ZIP integrity |
| Repository checker and dependency consistency | Passed, including with ignored models/media/virtual environment present |
| Example mathematics | Expanded algebra and equality case reviewed; 100 deterministic numerical checks passed, maximum absolute error 1.78e-15 |
| Real local speech | 16 clips synthesized, 110.1-second timeline |
| Full example rendering | 1920×1080, H.264/yuv420p, AAC, 30 fps, 3,303 frames, 3 chapters |
| Media verification | Full decode, fast-start, frame count, audio duration, chapter positions, and all 16 sentence onsets passed; maximum onset error 1/60 second |
| Visual-only revision | 0 new clips, 16 cache hits; identical WAV, encoded AAC, and all sentence/cue timings after a note edit and rerender |
| Visual inspection | All 24 early/middle/final encoded-video snapshots reviewed, plus full-resolution split/cancellation frames |
| Notation regression | 1080p image inspected: simple/nested/colored fractions, radicals, overlines, sums, norms, matrices and delimiters |
| Custom visual hook | 14.333-second moving-dot fixture rendered and verified at 720p and 1080p |
| Preview isolation | Re-verifying preview after final verification left the final report byte-identical |
| Review gate | Visual review recorded for the actual example; packaging correctly rejected missing listening review |
| Release archives | Source and plugin ZIP integrity/content checks passed from an isolated temporary Git fixture; the extracted plugin CLI initialized and validated a lesson |

The final example's report is [windows-example-verification.json](windows-example-verification.json).
Its SHA-256 is `89be66024924d5f5b4ee17120c60486c2e54aadbc451ef9bae83716dfe880356`.
Generated files remain in ignored local `work/`: `mean example/exports/video.mp4`,
`mean example/qa/final/`, `custom-example/`, `notation/`, `cache-regression.json`,
and `test-environment.txt`.

## Fixes made

- Bind verification, review, and packaging to the rendered proof, timeline,
  narration, custom visual code, assets, simulation files, and subtitle/transcript
  sidecars. Previously, changes outside `project.json`, or rebuilding a timeline
  after a project edit, could leave an old video eligible for packaging.
- Separate preview/final manifests, timing audits, verification reports, and
  snapshots. Preview work previously overwrote records used for final delivery.
- Keep media validation active under optimized Python; explicit errors replace
  assertions that `python -O` would remove.
- Fall back to an installed font when DejaVu Sans is absent on Windows.
- Check tracked repository files instead of recursively treating ignored local
  environments and generated media as distribution contents.
- Expand CLI/regression tests and configure the unit CI matrix for three systems.
- Clarify README use cases, authoring responsibilities, prerequisites, shell
  syntax, installation locations, previews, outputs, and troubleshooting.

Old render manifests do not contain the new input hashes. Rerender and verify
existing projects after updating; do not manually bless an old manifest.

## Limits and next release checks

Listening was not performed: pronunciation, naturalness, and perceived audiovisual
synchronization remain pending. Automated speech checks and frame inspection do
not establish those properties. Only synthetic packaging fixtures received both
review attestations; the actual example was not falsely marked fully reviewed.

This audit did not exercise the current fixes on Linux/macOS, the conda solver,
the Poppler fallback on this Windows host, plugin marketplace UI installation,
or end-to-end authoring of a new research theorem. Existing Linux validation is
historical evidence in [VALIDATION.md](VALIDATION.md), not a rerun of this patch.
Custom code importing external files/modules is not fully covered by the project
input hashes. Keep dependencies pinned and inspect every new project's output.
