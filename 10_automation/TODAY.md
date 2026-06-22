# Mika Lin Daily Brief

Date: `2026-06-22`
Priority run: `2026-W21-test`
Stage: `visibility_recovery`

## Decision

Today is an Instagram visibility recovery day, not a carousel production day.

## Today Only

1. Check Instagram: public account, Account Status, profile grid visibility, and whether the post opens from another account.
2. Publish one simple single-image test with direct comment CTA, then share it once to Story.
3. Send the post to 3-5 trusted people and record 6h / 24h metrics.

## User Should Provide

- IG audit result
- Second-test post URL and publish time
- 6h and 24h metrics

## Codex Can Do Next

- Record the new post and metrics with record_post_metrics.py.
- Update the weekly dashboard and decide whether Instagram remains a growth channel.
- Prepare Threads / Pinterest fallback copy if the second test is still zero reach.

## Useful Files

- `10_automation/runs/2026-W21-test/visibility_test_package.md`
- `05_content/2026_06_18_reactivation_plan.md`
- `09_sops/instagram_zero_reach_recovery.md`

## Generated Files

- `10_automation\runs\2026-W21-test\visibility_test_package.md`
- `10_automation\runs\2026-W21-test\visibility_test_package.json`
- `10_automation\PUBLISH_QUEUE.md`
- `10_automation\PUBLISH_QUEUE.json`
- `10_automation\PUBLISH_QUEUE.csv`

## Publish Queue Top Item

- Type: `visibility_test`
- ID: `2026-W21-test-002-visibility-01`
- Stage: `ready_to_publish_visibility_test`
- Asset: `IMG_1455.JPG`
- Next action: Publish the single-image visibility test, share once to Story, then record 6h / 24h metrics.

## Current Next Action

Run Instagram zero-reach recovery, publish one simple single-image test, and mirror to one backup channel.

## Fixed Flow

```text
person identity -> weekly trend -> prompt packet -> Grok images -> Canva carousel -> publish -> metrics -> next decision
```

## Dashboard Summary

- Run count: `1`
- Stage counts: `{"visibility_recovery": 1}`
