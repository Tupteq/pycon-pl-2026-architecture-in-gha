# Bonus (conceptual only — not built live): testing a pre-built wheel

Wheel-install is real-world plumbing, not a new architectural idea, so the
workshop schedule shows it as a slide rather than live-building it (frees
~10–15 min for the Phase B "aha moment" instead — see `SCHEDULE.md`).

**Looking for Codecov?** It's deliberately not covered here as a "just cut
for time" bonus anymore — see `reference/coverage-reporting-hook.md`
instead. Baking a specific external reporting service into shared CI infra
is a design choice worth teaching *against*, not a feature worth a bonus
slide.

## Testing a pre-built wheel instead of source

```yaml
built-wheel-names:
  description: >-
    A glob for the built distributions in the artifact to test (is
    installed into tox env if passed)
  required: false
  type: string
```

Used in the provision stage:

```yaml
${{
  inputs.built-wheel-names != ''
  && format('--installpkg dist/{0}', inputs.built-wheel-names)
  || ''
}}
```

The idea: test the *actual artifact* you're about to publish, not a fresh
`pip install -e .` of the source tree — catches packaging bugs a source
install never would.

### Real example: the `build:` → `tests:` job pair

Eight real callers of `reusable-tox.yml` (`tox-dev/tox-pre-commit`,
`tox-sphinx`, `tox-build`, `tox-towncrier`, `sphinx-contrib/towncrier`,
`msabramo/requests-unixsocket`, `cherrypy/magicbus`, `cherrypy/cheroot`)
share the same clean two-job pattern — exemplar:
`tox-dev/tox-pre-commit`'s `ci-cd.yml`:

```yaml
build:
  needs: [pre-setup]
  uses: tox-dev/workflow/.github/workflows/reusable-tox.yml@<sha>
  with:
    toxenv: build-dists
    job-dependencies-context: ${{ toJSON(needs) }}
    # ...

tests:
  needs: [build, pre-setup]
  uses: tox-dev/workflow/.github/workflows/reusable-tox.yml@<sha>
  with:
    built-wheel-names: ${{ needs.pre-setup.outputs.wheel-artifact-name }}
    dists-artifact-name: ${{ needs.pre-setup.outputs.dists-artifact-name }}
    source-tarball-name: ${{ needs.pre-setup.outputs.sdist-artifact-name }}
    toxenv: py
```

Notice how little of this is visible to the caller: `build:` runs
`toxenv: build-dists` (its `post-tox-run` hook uploads the artifact via
`actions/upload-artifact`), and `tests:` just names the artifact to
download and install — all the `download-artifact`/`--installpkg`
mechanics live inside `reusable-tox.yml` itself, not duplicated per caller.
`aio-libs/propcache` does something similar but adds a separate
`cibuildwheel`-based cross-arch build job on top — more moving parts than
needed for a first example; the 8-repo pattern above is the cleaner one to
point at.

## Why this is cut from the live build, not just shortened

It requires an upstream build step that doesn't exist in this teaching
repo (a real sdist/wheel build job) and doesn't teach a new **pattern**,
only a new integration. If your own project needs it, the production
annotated reference (`reference/reusable-tox-annotated.md`) shows the
exact real code, and the citation above shows a real caller-side example.
