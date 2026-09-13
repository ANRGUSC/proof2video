# Final review and release

## Three distinct checks

1. Mathematical review: compare the expanded proof and narration to the exact
   statement and detailed sources. Check all hypotheses, calculations, signs,
   indices, equality cases, necessity/sufficiency, and declared conclusions.
2. Visual/audio review: inspect the encoded MP4, not just source TeX or static
   layout objects. Inspect fractions, long overlines, radical bars, accents,
   matrices, delimiters, labels, colors, captions, and animated states. Listen to
   narration for missing words, wrong pronunciations/negatives, rushed steps,
   synchronization, and comfortable reading holds.
3. Media checks: full-file decode, codec/resolution/frame count, durations,
   chapter positions, caption onsets, and fast-start structure. The supplied
   `verify` command performs these mechanical checks and extracts snapshots.

These checks have different meanings. A green media report does not certify the
proof or establish that every mathematical stroke is visible. `review` is an
attestation of inspections that actually occurred; it is not an automated
replacement for them. Record unresolved issues rather than setting passed by
convention. Use `review --component visual` or `review --component audio` to
record only the inspection actually completed; packaging requires both. Check a short export on a smaller screen when readability is uncertain.

## Metadata and packaging

Generate `exports/upload_metadata.md` with a clear title, paragraph explaining
what is proved, intended audience/prerequisites, chapter timestamps, paper and
expanded-guide links, authors, exact version/status, and synthetic-narration
credit. Use plain URLs in copy-ready platform description text. State submission
status accurately; do not imply acceptance. Keep authorship and AI assistance
clear without presenting a machine-generated explanation as an author-approved
artifact unless that approval exists.

`package` includes media and project source in separate ZIPs. Keep a pinned copy
of the plugin version used. Do not bundle model weights, credentials, unrelated
user files, or third-party papers unless redistribution is authorized. The
expanded proof and source ledger should identify where the user can obtain the
original material. Preserve required attribution/licenses for reused code.

Do not commit MP4s, speech caches, or model weights to ordinary Git history.
For an authorized public release, use repository text source plus release assets
for video/download packages, and links or embeds on a guide page. Uploading to a
video platform is a separate action from generating a file. Use available,
authorized platform capabilities; never claim an upload succeeded without a
returned URL or verification.

Platform constraints can change. Verify current official instructions before
advising on publishing. YouTube's current policy assigns a new URL to a new
video upload rather than replacing the original binary at its old URL:
https://support.google.com/youtube/answer/55770

## Visual-only correction checklist

Keep the original export and errata. Refresh visual metadata using the cached
speech, preserve WAV/AAC and timing hashes, render a notation sample, render the
full result, inspect all repaired scenes in the final MP4, and decode the file.
Use a distinct corrected filename and reuse the subtitle file only when timing
is demonstrably unchanged. Include a video ZIP because some clients fail to
download a raw MP4 reliably.
