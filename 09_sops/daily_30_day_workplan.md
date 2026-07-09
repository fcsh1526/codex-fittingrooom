# Daily Cockpit Operating Plan

This replaces the old Day X companionship plan.

Current strategy:

```text
Production-first:
Perplexity weekly trend rows -> Codex image generation with M01-M05 anchors -> Canva master template -> Instagram carousel -> metrics
```

## Daily Start

Run:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action cockpit -TodayDate 2026-07-09
```

Open:

```text
10_automation/DAILY_COCKPIT.html
10_automation/PUBLISH_QUEUE.md
10_automation/TODAY.md
```

Use `PUBLISH_QUEUE.md` as the concrete source of truth when files disagree.

## If Top Item Is `needs_image_asset_selection`

1. Open the carousel folder under `generated_images/{carousel_id}/`.
2. Use `codex_generation_handoff.md` and `candidate_prompts.md`.
3. Generate 2-3 Codex image candidates with the assigned model reference anchors.
4. Save candidates in the carousel folder.
5. Score `review_sheet.csv` or `image_review_template.csv`.
6. Run `select_codex_assets.py`.
7. Validate with `-RequireAssets`.

## If Top Item Is `ready_for_canva_and_publish`

1. Open `canva_fill_guide.md`.
2. Open `canva_asset_plan.md`.
3. Duplicate one registered Mira Canva master template.
4. Replace only complete flat PNG/JPG image assets.
5. User manually crops/exports and posts to Instagram.

## If Top Item Is Metrics

1. Record reach, likes, saves, comments, shares, profile visits, follows, and CTA comments.
2. Zero reach does not stop the next carousel.
3. Keep production moving unless the user explicitly pauses.

## User Inputs Codex May Need

Only ask for the smallest missing input:

- Perplexity weekly URL or CSV, when no weekly run exists.
- Visual approval or rejection notes, when candidates are generated.
- Canva preview approval, when a duplicate template is filled.
- Instagram post URL and publish time, after publishing.
