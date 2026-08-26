# What you missed if you jumped straight here (Phase B)

**The idea, not just the code:** the reusable workflow now runs tox in
three deliberately separate stages: provision (`--notest`), the real run
(`id: tox-run`), and a conditional debug rerun on failure. This separation
means "the environment failed to build" and "a test failed" are never
ambiguous in the logs — you know which one happened before you even read a
line of pytest output.

**The single highest-value idea in the whole workshop, don't skip it:**
`steps.tox-run.outputs.*` isn't produced by this workflow at all. Open
`tox.ini` — the `commands_post` block writes to `$GITHUB_OUTPUT` directly,
gated on `GITHUB_ACTIONS == "true"` so it's a no-op on your laptop. The
workflow and `tox.ini` are **co-designed, not independent** — copy one
without the other and things silently stop working. (Also notice
`tox.ini`'s `passenv = GITHUB_ACTIONS GITHUB_OUTPUT` — without it, this
whole mechanism no-ops even inside a real CI run, because tox doesn't
forward host env vars into the testenv by default. That's not a bug we
hit by accident — it's the same category of "explicitness has a cost"
tradeoff Pattern 5 names later.)

The debug-rerun step ends with `&& exit 1` on purpose — even if the verbose
rerun happens to pass, the job stays red. A test that fails once and passes
on retry is *flaky*, not *fine*.

Next: `checkout checkpoint/phase-c-hooks` to see extension points added
around these three stages.
