# Adoption census: `reusable-tox.yml`

Sourced verbatim from `~/src/experiments/gh-lookup-ep-2026/adoption.md`
(census date 2026-07-03, via `gh search code` + per-repo `gh api`
verification). Raw data alongside this file as `adoption.csv`. Cross-checked
against `VERIFIED-SOURCE.md` §3 (independently confirmed live 2026-08-26 that
`cherrypy/cheroot` and `ansible/awx-plugins` both still pin
`1bb961580e20073f66ccb9024f248357f8c8fecb`, matching row data below) — no
discrepancies found between the two independently-produced sources.

## Canonical workflow

`tox-dev/workflow` → `.github/workflows/reusable-tox.yml` (default branch
`unstable/v1`, repo self-describes as "[DO NOT USE] THIS REPOSITORY IS
UNSTABLE AND HIGHLY EXPERIMENTAL!" — adopted anyway, see below). Latest
commit touching the file as of the census: `1bb961580e20` (2026-06-08).

## Headline numbers

- **20 unique repos** reference the workflow on their default branch — all
  20 are non-forks (0 forks found; GitHub code search only indexes default
  branches and skips most forks, so fork-side copies are invisible to this
  census by construction).
- **17 are genuine callers** (a `uses: …reusable-tox.yml@…` line in an
  active workflow). The other 3 host copies: `tox-dev/workflow` (canonical),
  `cobycloud/actions` (own copy + docs), `CCChz233/FeatureLiftBench`
  (vendored yarl clone in a benchmark corpus).
- **16 of 17 callers call the canonical `tox-dev/workflow` path; every
  single one pins a full commit SHA** — no branch/tag refs at all.
  `antonbabenko/pre-commit-terraform` calls its own vendored copy instead.
- Combined reach of the 17 caller repos: **≈ 17,400 stars**.

### Pinned-ref distribution (canonical callers)

| Pinned SHA | Callers |
|---|---|
| `1bb96158` (latest, 2026-06-08) | jazzband/pip-tools, cherrypy/cheroot, ansible/awx-plugins, ansible/awx_plugins.interfaces, tox-dev/tox-pre-commit, tox-dev/tox-towncrier |
| `208490c7` | cherrypy/cherrypy, cherrypy/magicbus, aio-libs/aiosignal, sphinx-contrib/sphinxcontrib-towncrier |
| `34958348` | aio-libs/yarl, aio-libs/propcache |
| `89de3c6b` | ansible/ansible-runner, ansible/ansible-builder |
| `cf231470` | msabramo/requests-unixsocket |
| `617ca35c` | re-actors/alls-green |

**Teaching point for the 0:18–0:28 "duplication problem" block:** this
spread of pinned SHAs is the honest cost of Pattern-1/2 reuse against an
explicitly unstable upstream — real projects lag behind HEAD by design,
each catching up on their own schedule via periodic bump commits (see
`before-after/before-after-notes.md` for cheroot's own bump history).

## Method notes (for "how many people use this" questions)

- Primary search: `gh search code 'reusable-tox.yml path:.github/workflows'`
  → 17 caller files.
- The exact-`uses:`-line search returned 0 hits — GitHub's code-search API
  tokenizes on punctuation, so slashed paths can't be phrase-matched.
  Instead, every caller file was fetched raw and its actual `uses:` line
  extracted.
- Fork/star/archived status verified per repo via `gh api repos/…`; none
  are forks, none archived.
- **State this plainly if asked:** adoption is chiefly within ecosystems
  the author maintains, unified deliberately to trial the approach — don't
  inflate the number.
