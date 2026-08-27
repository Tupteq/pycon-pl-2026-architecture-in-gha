# Test/coverage reporting belongs behind a hook, not baked into core

The real `tox-dev/workflow` (`reference/reusable-tox-annotated.md`) has
unconditional core steps for JUnit-to-summary (`test-summary/action`),
Cobertura-to-summary (`irongut/CodeCoverageSummary`), and two Codecov
uploads (`codecov/codecov-action`, one per report type). Every caller pays
for these steps whether or not they use Codecov, and adding/opting out
requires editing the core workflow's inputs (`codecov-token`,
`require-successful-codecov-uploads`) rather than an extension point.

**This is arguably inconsistent with Pattern 4's own philosophy** — even
the reference implementation doesn't perfectly follow "extend without
modifying core" for this particular concern. That's a genuinely useful
thing to notice, not a criticism to soften: real designs accumulate
exceptions to their own principles, and recognizing where is itself a
skill.

## What real callers actually do instead (mixed evidence, cited precisely)

- `ansible/awx-plugins`, `ansible/awx_plugins.interfaces`, and
  `aio-libs/propcache` each have a **real `post-tox-job` hook**, gated on
  `toxenv == 'pre-commit'`, that uploads MyPy's coverage data to
  **Coveralls** (`coverallsapp/github-action@v2`, `format: cobertura`) —
  proof that hooks *can* carry this kind of behavior. But it's narrow: only
  MyPy coverage, only one specific external service, not a general
  test/coverage-reporting pattern applied consistently.
- `aio-libs/propcache` also has the cleanest possible one-liner for
  rendering coverage as a job-summary table:
  ```bash
  python -Im coverage report --format=markdown >> "${GITHUB_STEP_SUMMARY}"
  ```
  **Important correction, verified directly (not just cited secondhand):**
  this line lives in propcache's `test:` job, which runs plain `pytest`
  directly and does **not** call `reusable-tox.yml` at all. It is real,
  production code — but nobody has wired this technique into a
  `reusable-tox.yml` hook in any repo surveyed. Don't repeat the claim that
  "propcache does this via a hook" — it doesn't, yet.
- Every repo that *does* call `reusable-tox.yml` for testing and wants a
  markdown coverage summary instead embeds a much more complex pattern
  directly in `tox.ini`'s `commands_post` — inline Python constructing a
  `coverage.Coverage()` object and calling `.report(output_format=
  "markdown")` inside a shell `-c` string (confirmed verbatim in
  `tox-dev/tox-pre-commit`, `tox-sphinx`, `tox-build`, `tox-towncrier`,
  `sphinx-contrib/towncrier`, `cherrypy/magicbus`, `cherrypy/cheroot`,
  `aio-libs/aiosignal`, and both `ansible/awx*` repos). This is exactly the
  kind of thing that's hard to read at a glance — a worse teaching example
  than the plain CLI one-liner above, even though it's the more common
  real-world pattern.

## The workshop's synthesis: the real one-liner, in the right place

`workshop-template`'s `answer-key` branch has a working `post-tox-run` hook
(`.github/reusables/tox-dev/workflow/reusable-tox/hooks/post-tox-run/
action.yml`) that combines the pieces above correctly:

```yaml
runs:
  using: composite
  steps:
  - name: Append coverage results to the job summary
    if: '!cancelled()'
    run: >-
      tox exec --skip-pkg-install --quiet -- coverage report --format=markdown
      >> "${GITHUB_STEP_SUMMARY}"
    shell: bash
```

- **`tox exec`** runs the command inside the already-provisioned tox env
  from Stage 2 (no reinstalling anything, no separate coverage-tool setup)
  — `coverage` is already present transitively via `pytest-cov`.
- **`coverage report --format=markdown`** is coverage.py's own native
  markdown output (added in coverage.py 7.x, confirmed working with a
  plain `pip install coverage`, no extras) — the same real command
  propcache uses, just invoked through `tox exec` instead of a bare
  `python -Im coverage` call, so it works regardless of which Python/venv
  the job happens to be using.
- **It's a hook**, not a core step — a caller who doesn't want this simply
  doesn't add the file, exactly like the `jq`-install hook you built by
  hand in Phase C. No core-workflow input, no required secret, no external
  account.

This was tested end-to-end against this repo's own package and produces a
real markdown table in the job summary. It's shown as a reveal in Phase C,
not something you build hands-on — but it's real, working code you can
copy into your own project's hooks directory afterward.
