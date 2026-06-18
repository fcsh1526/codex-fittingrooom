# 2026-W25 Work Order

Created: 2026-06-18

Purpose: restart the project with a more automated weekly carousel workflow.

## Current Priority

Produce a steady stream of polished Instagram carousel posts before monetization.

Do not prioritize affiliate links until reach is non-zero.

## Required Inputs From User

Paste these when ready:

```text
Perplexity weekly URL:
Google Drive folder for Grok images:
Canva panorama design URL:
Instagram account visibility status:
```

## If Perplexity URL Is Available

Codex should:

1. Extract 5 trends.
2. Pick 1-2 carousel candidates.
3. Fill `weekly_content_packet_template.csv`.
4. Generate Grok prompts from `04_prompts/grok_weekly_carousel_prompt.md`.
5. Generate Canva placeholder values from `canva_placeholder_values_template.csv`.

## If Grok Images Are Available

Codex should:

1. List the Drive folder.
2. Build an image inventory.
3. Review image quality.
4. Pick the cover and detail assets.
5. Update the weekly content packet.

## If Canva Design Is Available

Codex should:

1. Read placeholder fields.
2. Replace placeholder text.
3. Show preview.
4. Ask user before saving.
5. Record the final Canva URL.

## If Instagram Still Has Zero Reach

Publish a simpler second test before doing product links.

Use:

```text
05_content/second_test_zero_reach_post.md
```

## Done Criteria For This Week

Minimum:

```text
1 polished carousel or simple second-test post published
metrics recorded after 24 hours
reach status known
```

Better:

```text
2 posts published
at least one post reaches 20+ people
one repeatable Canva template validated
```

