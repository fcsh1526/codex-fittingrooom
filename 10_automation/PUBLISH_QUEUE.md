# Publish Queue

Runs directory: `10_automation\runs`
Queue items: `3`

## Top Next Item

- Type: `carousel`
- ID: `2026-W21-test-001`
- Stage: `ready_for_canva_and_publish`
- Asset: `IMG_1453.JPG`
- Package: `n/a`
- Next action: Use Canva handoff files to finish the carousel and publish it.

## Queue

| Type | ID | Stage | Asset | Reach | Next Action |
|---|---|---|---|---:|---|
| `carousel` | `2026-W21-test-001` | `ready_for_canva_and_publish` | `IMG_1453.JPG` | `` | Use Canva handoff files to finish the carousel and publish it. |
| `visibility_test` | `2026-W21-test-002-visibility-01` | `ready_to_publish_visibility_test` | `IMG_1455.JPG` | `` | Optional side test: publish the single-image visibility test, share once to Story, then record 6h / 24h metrics. |
| `carousel` | `2026-W21-test-002` | `visibility_recovery` | `IMG_1455.JPG` | `0` | Keep carousel production moving; optionally publish or record the generated single-image visibility test in parallel. |
