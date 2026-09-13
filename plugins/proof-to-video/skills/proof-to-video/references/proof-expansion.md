# Expanding a paper proof into an explanation

The goal is enough supporting detail for a senior undergraduate or first-year
graduate student with the stated prerequisites to reconstruct each step. It is
not a target page count, runtime, or a demand to reprove all undergraduate math.

## Source inventory

Record the exact statement and proof locations, notation definitions, version,
authors, and paper status. Look for detailed companion guides, expanded proof
reports, appendices, and prior approved explanations. Read their relevant
sections in full. Cite both the paper and the expanded sources; distinguish an
existing derivation from new explanatory material. Pin Git revisions or hash
local files. Keep the paper's intended scope when a broader guide contains other
versions or extensions.

## Expansion depth

For each proof step, give its input assumptions, calculation, rule used, and
conclusion. Expand compressed phrases such as “standard calculations,” “by
conditioning,” “it follows,” and “similarly” where they hide the central work.
Show intermediate algebra, dimensions, summation limits, signs, denominators,
measurability/integrability conditions, and the justification for limits or
interchanging operations. Define conditional expectations, projections,
quadratic forms, or other prerequisites before using them if needed by the
intended audience. Explain why a proposed test function or perturbation is
admissible. Separate necessity, sufficiency, existence, and uniqueness: a proof
of one is not a proof of the others.

Keep a compact mapping such as:

| Step | Claim | Source | Supporting calculation | Status |
|---|---|---|---|---|
| P1 | Intermediate identity | Appendix A, Eq. 3 | Fully written in proof.md | Reviewed |

Use statuses that reflect the evidence: supported, newly derived and reviewed,
open, or contradicted. Record accepted background explicitly. If external proof
checkers are used, report their actual output and exact verified scope. Do not
present numerical checks or an LLM verdict as machine-checked mathematics.

## Concrete examples

Choose small values that preserve the interesting structure. First calculate the
example analytically, then compare with a deterministic implementation. Label
special-case pictures clearly and explain what changes in the general case.
Check degenerate/boundary cases, equality conditions, units, and limiting
behavior. Do not let a nice plot replace a missing argument.

## From proof to narration

The script should explain what the viewer should notice before or as it appears.
Give intuition before a dense derivation, work through one step at a time, and
return to the exact theorem at the end. State when a quantity is a random
variable, vector, scalar, function, realization, or expectation if confusion is
plausible. Retain qualifications such as almost surely, positive, nonzero,
finite, independent, or conditioned on. End with what was proved and where its
assumptions matter. Avoid irrelevant generalizations or promotional claims.
