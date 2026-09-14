# Release procedure

Run the tests, repository checker, plugin/skill validators when available, and an
end-to-end example. Inspect the actual exported video and record what was tested.
Use `python scripts/package_release.py --output /path/to/release` to produce source and installable-plugin
archives from tracked Git files. Commit all intended source changes first.

The public repository already exists at https://github.com/ANRGUSC/proof2video.
Review and merge intended changes there, wait for CI on the release commit, and
package from a clean checkout. Publishing commits, tags, or assets requires the
repository owner's authorization. Never put tokens in source or command text.

After source publication and review, tag `v0.1.0` and attach release archives and
the reviewed example video ZIP to the release. Do not include model weights,
research-paper PDFs, speech caches, or video binaries in ordinary Git history.
Update CITATION.cff and plugin manifests together for later versions.
