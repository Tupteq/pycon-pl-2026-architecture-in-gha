# What you missed if you jumped straight here (Phase D)

**The idea, not just the code:** this is the final teaching-version state.
Two things landed in this phase:

1. **Pattern 5, Exhibit B** — the workflow-level `env:` block (color +
   encoding vars) and `TOX_TESTENV_PASSENV`. Notice this is a *different*
   mechanism than `tox.ini`'s own `passenv` line added back in Phase B —
   `TOX_TESTENV_PASSENV` widens every testenv's passenv list from outside
   `tox.ini` entirely. Explicitness has a cost: thirteen tools, thirteen
   different color env vars, one workflow forced to know all of them.
2. **A realistic caller matrix** (3 Python versions × 2 tox envs = 6 legs)
   in `ci-cd.yml` — the reusable workflow's own code did not change at all
   to support going from 2 legs (Phase A) to 6. That's the payoff of
   Pattern 1 + Pattern 2 together.

`reference/reusable-tox-annotated.md` has the full real 22-input production
version if you want to see what's cut here (wheel installs, Codecov,
sdist-checkout) — see `reference/bonus-wheel-and-codecov.md` for why those
were left conceptual-only.

This is the end of the guided build. From here: adapt this template to your
own project, or explore the full annotated reference.
