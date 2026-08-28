# ci-patterns-demo — workshop companion repo

Companion repo for **"Software Architecture Meets CI/CD: Building Reusable
GitHub Actions Workflows for Python"** (PyCon PL 2026). A tiny Python
package exists here only to give tox and CI something real to run — the
point of the workshop is the `.github/workflows/reusable-tox.yml` you'll
build, not the package.

## Prerequisites (do this before the workshop, not during)

- A **personal** GitHub account (not a managed/SSO/org-provisioned one —
  confirm you can create public repos and enable Actions on them).
- Git and a code editor installed locally.
- Python 3.9+ and `tox` installed locally (`pip install tox`) — this is
  your offline fallback if the room's wifi or GitHub Actions queues are
  slow: everything in Phase B can be explored locally with plain `tox`
  commands before it ever needs to run in CI.
- A laptop with a charger.

## How this repo is organized

- **`main`** — the starting point. `.github/workflows/*.yml` are stubs with
  comments describing what you'll build.
- **`checkpoint/phase-a-skeleton`**, **`checkpoint/phase-b-three-stage`**,
  **`checkpoint/phase-c-hooks`**, **`checkpoint/phase-d-caller`** — the
  finished end-state of each workshop phase. Fell behind? Check one out and
  keep going from there — see that branch's own "what you missed" note in
  its README for the concept, not just the code.
- **`reference/reusable-tox-annotated.md`** — the full, real, 22-input
  production `reusable-tox.yml` (from `tox-dev/workflow`), annotated. What
  you build here is a deliberately smaller teaching version of that file —
  read this handout when you want to see the "real world" version.

## Further reading

- GitHub Actions: [Reuse workflows](https://docs.github.com/en/actions/sharing-automations/reusing-workflows)
- GitHub Actions: [Creating a composite action](https://docs.github.com/en/actions/sharing-automations/creating-actions/creating-a-composite-action)
- GitHub Actions: [Evaluate expressions in workflows and actions](https://docs.github.com/en/actions/reference/evaluate-expressions-in-workflows-and-actions)
- [tox documentation](https://tox.wiki/en/stable/)

## Local fallback

Everything in Phase B can be run without any GitHub Actions dependency:

```console
$ pip install tox
$ tox --notest                                  # Stage 1: provision
$ tox --skip-pkg-install --quiet                # Stage 2: main run
$ tox --skip-pkg-install -- --lf -vvvvv          # Stage 3: debug rerun style
```

To trigger the deliberate failure used in the "break something on purpose"
demo, flip `BREAK_ME_ON_PURPOSE = True` in `tests/test_basic.py`, run tox,
then flip it back.
