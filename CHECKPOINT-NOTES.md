# What you missed if you jumped straight here (Phase C)

**The idea, not just the code:** four hook points now exist —
`post-src-checkout` → `prepare-for-tox-run` → `post-tox-run` →
`post-tox-job` — each gated by `hashFiles('.../action.yml') != ''` used as
a poor man's `file.exists()`. Only one is actually implemented here
(`post-src-checkout`); the other three are real extension points that
currently do nothing because their `action.yml` files don't exist yet in
this repo. Delete `.github/reusables/.../post-src-checkout/action.yml` and
push — the hook cleanly no-ops, no error. That's the whole point: adding a
hook never requires touching the reusable workflow's own code.

**Look at the hook itself**
(`.github/reusables/tox-dev/workflow/reusable-tox/hooks/post-src-checkout/action.yml`):
it doesn't just check "does this repo want a hook," it also branches on
*which tox environment* triggered it
(`fromJSON(inputs.calling-job-context).toxenv == 'needs-jq'`). Every hook
gets the calling job's entire input set as one JSON blob, not individual
named parameters — new inputs on the core workflow never require touching
the hook interface. Real production hooks (see
`reference/reusable-tox-annotated.md` and the facilitator's live reveal) use
this exact same `fromJSON(...).toxenv == '...'` idiom, just for narrower,
release-automation-specific purposes.

Next: `checkout checkpoint/phase-d-caller` for the realistic matrix and
Pattern 5's explicit-env-var block.
