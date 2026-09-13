# Release procedure

Run the tests, repository checker, plugin/skill validators when available, and an
end-to-end example. Inspect the actual exported video and record what was tested.
Use `python scripts/package_release.py --output /path/to/release` to produce source and installable-plugin
archives from tracked Git files. Commit all intended source changes first.

For a new GitHub repository, an authenticated owner can run from this checkout:

```bash
gh repo create ANRGUSC/proof2video --public --source=. --remote=origin --push
```

Alternatively, create an empty public repository in the GitHub interface, add its
URL as `origin`, and push `main`. These are publishing actions; run them only
when the repository owner has authorized that publication. Never put tokens in
source or command text.

After source publication and review, tag `v0.1.0` and attach release archives and
the reviewed example video ZIP to the release. Do not include model weights,
research-paper PDFs, speech caches, or video binaries in ordinary Git history.
Update CITATION.cff and plugin manifests together for later versions.
