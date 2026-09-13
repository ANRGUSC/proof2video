# Installation and distribution

## Standalone skill (tested local installation route)

From a checkout, run `python scripts/install_skill.py`. This installs the full
self-contained skill directory, including its executable media helpers,
references, and worked example. It does not overwrite an existing skill.
Start a new Codex session and invoke `$proof-to-video`.

The copied skill requires a Python environment and media dependencies as
described in the README. The installer does not install dependencies, download
model weights, or copy credentials.

## Plugin-capable clients

The plugin directory is `plugins/proof-to-video`. It includes both a portable
root `plugin.json` and the Codex compatibility manifest at
`.codex-plugin/plugin.json`. Both identify the same version and skill. A client
should choose its supported manifest convention, not install them as two plugins.

A local test catalog is provided at `.agents/plugins/marketplace.json`; its
scaffolded marketplace name is `personal`, and it references the plugin under
`./plugins/proof-to-video`. This is a local test catalog, not an assertion that
the plugin is listed in a public store or installed in the user's client.

Use your client's supported local-plugin or marketplace installation interface.
The [official builder guide](https://learn.chatgpt.com/docs/build-plugins)
describes the portable and compatibility layouts. Client UI installation was
not exercised in the development environment; manifest and skill validators
were run, and the standalone skill installer was tested separately.

## Public repository

The complete source is intended for its own public GitHub repository. Once
published, users can clone it or download a tagged release and use the installer.
Keep the plugin identifier `proof-to-video` stable. Publish versioned plugin ZIPs
with the plugin directory contents at the ZIP root, and keep video/demo archives
as separate release assets.

A public GitHub repository and a universal plugin-directory listing are separate
publication steps. This project does not claim public-store approval. Directory
submission can follow after broader user testing.
