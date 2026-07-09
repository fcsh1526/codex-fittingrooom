# Weekly Operating SOP

Purpose: keep the Mira AI fashion magazine workflow production-first and Codex-first.

## Monday - Trend Input

1. Use the Perplexity weekly public page or CSV.
2. Import or resolve the weekly prompt rows.
3. Generate the weekly run folder.

Primary command:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action pipeline -Week 2026-WXX -UsePerplexityIndex
```

## Tuesday - Daily Queue

1. Open `daily_queue.csv`.
2. Pick the top carousel from `PUBLISH_QUEUE.md`.
3. Confirm the assigned model is one of `M01` to `M05`.
4. Confirm its approved face/full reference images exist in `02_brand/mira_reference_images.csv`.

## Wednesday - Codex Image Generation

1. Prepare or open the image job folder under `generated_images/{carousel_id}/`.
2. Use `codex_generation_handoff.md` and `candidate_prompts.md`.
3. Generate 2-3 candidates in Codex.
4. Save files in the carousel job folder.
5. Score `review_sheet.csv` or `image_review_template.csv`.

Do not use Grok for the active workflow.

## Thursday - Asset Selection And Canva Handoff

1. Run `select_codex_assets.py` after the score sheet is filled.
2. Confirm `canva_asset_slots.csv` has selected `cover_image`, `motion_crop`, and `detail_image`.
3. Use one registered Mira Canva master template.
4. Duplicate the master before filling.

## Friday - Publish

1. User manually crops/exports from Canva.
2. User publishes or schedules the Instagram carousel.
3. Keep AI disclosure in the caption.
4. Send Codex the post URL and publish time.

## Weekend - Metrics

1. Record reach, likes, saves, comments, shares, profile visits, followers, and CTA comments.
2. Zero reach is a distribution signal, not a reason to stop carousel production.
3. Continue the next carousel even if the previous post has no visibility.
