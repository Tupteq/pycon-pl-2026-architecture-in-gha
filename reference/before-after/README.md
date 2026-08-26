# The real cheroot `tests:` job, before and after

`before-tests-job.yml` / `after-tests-job.yml` are the **`tests:` job only**
(not the whole `ci-cd.yml`), extracted verbatim from real
`cherrypy/cheroot` commits — sourced from
`~/src/experiments/gh-lookup-ep-2026/{before-monolithic.yml,after-caller.yml}`,
which are full-file `git show` dumps (1421 / 1293 lines respectively). This
is the fair, apples-to-apples comparison: same job, same repo, before vs.
after the `90ca482e` migration (author date 2025-04-09, merged/committed
2025-04-17).

**One clarification worth stating explicitly if asked:** the "5×
`actions/setup-python`, 7× `actions/checkout`" duplication figure (from
`before-after-notes.md`) is a **whole-file** count across `lint`, `build`,
and `tests` combined — the `tests:` job alone only has one of each. Don't
imply the whole 5×/7× duplication lived inside this one job; the point
still stands (near-identical ceremony repeated across sibling jobs), it's
just not visible from `before-tests-job.yml` in isolation.

- Before: 207 lines (with header comment), `runs-on: ${{ matrix.os }}-latest`
  feeding a job body with a dozen inline steps.
- After: 143 lines (with header comment), the same matrix now feeds
  `uses: tox-dev/workflow/.github/workflows/reusable-tox.yml@...` + `with:`.

Use these as the live-demo projection for `SCHEDULE.md`'s 0:08–0:18 block
instead of the full 1421/1293-line files — same real source, sized for a
projector.
