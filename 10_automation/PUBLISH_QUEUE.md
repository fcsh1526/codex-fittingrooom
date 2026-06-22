# Publish Queue

Runs directory: `10_automation\runs`
Queue items: `3`

## Top Next Item

- Type: `visibility_test`
- ID: `2026-W21-test-002-visibility-01`
- Stage: `ready_to_publish_visibility_test`
- Asset: `IMG_1455.JPG`
- Package: `10_automation\runs\2026-W21-test\visibility_test_package.md`
- Next action: Publish the single-image visibility test, share once to Story, then record 6h / 24h metrics.

## Queue

| Type | ID | Stage | Asset | Reach | Next Action |
|---|---|---|---|---:|---|
| `visibility_test` | `2026-W21-test-002-visibility-01` | `ready_to_publish_visibility_test` | `IMG_1455.JPG` | `` | Publish the single-image visibility test, share once to Story, then record 6h / 24h metrics. |
| `carousel` | `2026-W21-test-002` | `visibility_recovery` | `IMG_1455.JPG` | `0` | Publish or record the generated single-image visibility test before making another carousel. |
| `carousel` | `2026-W21-test-001` | `ready_for_canva_and_publish` | `IMG_1453.JPG` | `` | Use Canva handoff files to finish the carousel and publish it. |
