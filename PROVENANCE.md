# Provenance

Proof to Video was developed with AI assistance at Bhaskar Krishnamachari's
request. It generalizes a working workflow for expanded mathematical explanation,
Manim visuals, local Kokoro speech, sentence-level synchronization, captions,
chaptered MP4s, and reproducible review.

The standalone example is an original exposition of the standard least-squares
constant theorem. It requires no access to any research repository. Its source
mapping is entirely within the bundled proof.md. The numerical example is a
checked illustration, not a substitute for proof.

A prior rendering failure motivated a specific regression check: Poppler's
stroke-only fraction/radical/overline paths become invisible when imported with
Manim's zero stroke width. The converter now preserves their geometry as filled
paths. Both source-level tests and encoded-video visual review are used.

Reference implementations and documentation consulted:

- https://github.com/ManimCommunity/manim
- https://github.com/thewh1teagle/kokoro-onnx
- https://github.com/WWresearch/lamport-proof
- https://learn.chatgpt.com/docs/build-plugins

This is an initial implementation with the validation scope described in
`docs/VALIDATION.md`. It is not a claim that arbitrary paper-to-video tasks have
been exhaustively tested.
