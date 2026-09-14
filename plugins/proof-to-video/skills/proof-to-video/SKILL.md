---
name: proof-to-video
description: Turn a theorem or lemma and its supporting proof material into a bottom-up narrated mathematical video with Manim animations, local TTS, subtitles, chapters, and reproducible source. Also revise existing proof videos while preserving approved narration and timing.
---

# Proof to Video

Create an explanation a senior undergraduate or first-year graduate student can
follow, then produce a synchronized video. The agent writes and reviews the
mathematics and chooses the visuals; bundled Python handles deterministic media
production. The scripts do not automatically understand or verify arbitrary PDFs.

## 1. Ground the result and expand the argument

Identify the exact paper version, theorem/lemma number, definitions, hypotheses,
notation, conclusion, and publication status. Inspect the actual source; do not
reconstruct a statement from a title or abstract. Prefer accompanying extended
explainers, appendices, lecture notes, and detailed or Lamport-style proof reports
for the intermediate calculations. Use the paper to anchor the result, and map
the expanded sources to it. Do not discard an existing detailed guide and start
from a compressed paper proof alone. Record file hashes or pinned revisions and
source locations. If sources conflict, resolve or explicitly report the conflict.

Write project `proof.md` before the narration: prerequisites, a notation table,
a proof roadmap, numbered derivations, justifications, equality cases, and
limits of the claim. Read [proof-expansion.md](references/proof-expansion.md) for
the expansion standard. Repairable source gaps may be filled with an explicitly
identified supporting argument; do not silently add assumptions or strengthen a
claim. An unresolved gap must not appear as a completed proof. Optional Lamport
or formal-proof tools can help if available; neither is required.

## 2. Plan a teachable sequence

Start with the needed preliminaries, give the main claim and proof idea, then
work through the details. Use as many chapters as the argument needs. Keep one
conceptual step per cue. Narrate symbols as mathematical English; keep display
LaTeX separate from the spoken text. Split sentences explicitly instead of using
an abbreviation-sensitive sentence splitter. Add reading holds after important
equations. Estimate duration from the script, then report the measured duration
after speech generation. Do not squeeze a derivation to fit an arbitrary runtime.

Initialize a working project with `python <skill>/scripts/pv.py init <new-dir>`.
This copies a fully worked example; replace its theorem, proof, narration,
chapters, numerical data, and attribution for the requested paper. Do not leave
example material in a new lesson. Read [pipeline.md](references/pipeline.md) for
the project format, commands, and environment. Populate `proof_review` after
checking the derivation, bind it to the proof file hash, and retain open issues.
This field records a review decision, not proof certification.

## 3. Build exact visuals and checked illustrations

Use Manim equations, geometric diagrams, and computed plots. Read
[custom-visuals.md](references/custom-visuals.md) when writing simulations or
custom animation code. Prefer a concrete low-dimensional worked example whose
numbers can be checked independently. Label simulation results as illustrations
and record seeds and parameters. No generated raster image should stand in for
an exact equation or scientific diagram. Show changing labels when quantities
change; preserve vector/scalar distinctions and nonzero side conditions.

## 4. Generate narration and derive the timing

Default to local Kokoro ONNX, `af_heart`, speed `0.90`, one WAV per explicit
sentence. User-selected voices or recorded narration take precedence; adapt the
backend while retaining sample-derived timing. The supplied backend needs no
speech API key. Read [pipeline.md](references/pipeline.md), run `doctor`, then
`audio`. Speech caching is keyed by spoken text, voice, speed, engine, and model
hashes. Equation-only edits should not resynthesize speech. Captions, holds,
chapter boundaries, and Manim events use the same timeline.

## 5. Render and inspect a sample, then the full video

Before an expensive render, make a small separate test project containing the
hardest notation and animation. Test fractions, radicals, long overlines,
subscripts/superscripts, matrix/delimiter sizes, and colored equations relevant to
the result. The portable converter preserves horizontal rules as filled paths;
do not remove it. After a successful sample, render the requested full project.
Run `verify` to decode the exported MP4 and extract initial, intermediate, and
final frames of every cue. Inspect the contact sheets and full-resolution frames.
A successful LaTeX compile, object bounds check, or codec test does not establish
that the mathematical notation is visible or correct.

Listen to the generated speech, especially mathematical terminology, negatives,
subscripts, and transition pacing. Use available audio playback/transcription
facilities where helpful, but automated ASR is not a substitute for checking the
meaning. Read [review-and-release.md](references/review-and-release.md). Only run
`review --notes ...` after those reviews actually occur. If the host cannot play
or inspect an artifact, state the remaining check rather than marking it passed.

## 6. Deliver and support revisions

Deliver MP4 plus a ZIP containing that MP4, SRT/VTT, transcript, chapter list,
source/provenance, and verification notes. Include upload metadata with paper and
expanded-guide links, source version/status, authors, and synthetic narration.
Keep binary video/model files out of ordinary Git history; use release assets
when publishing is requested. A publishing question alone is not authorization
to upload to a platform. Respect already-granted publishing authorization.

For visual-only revisions, keep the original export, modify equations/visuals,
rerun `audio` to refresh the project timeline using cached clips, and assert the
narration hash and all time boundaries are unchanged. Then render and review the
repaired scenes in the actual export. Cached encoded audio is reused. Update
errata and package a clearly named corrected version. Do not claim a revision is
complete just because source formulas are correct.
