# Current Status - Mira AI Fashion Creator

Last updated: 2026-06-25

## Project Goal

Build a repeatable AI virtual fashion creator workflow for the Traditional Chinese / Taiwan market.

Current priority:

```text
stable character -> weekly trend -> OpenAI / Grok image generation -> minimal Canva carousel -> Instagram post -> metrics
```

Monetization is intentionally delayed until there is non-zero reach.

Today's priority:

```text
use the best available AI image source -> keep 3-slide Canva carousel production moving -> record metrics when available
```

## Current Stage

Minimal image-led carousel transition.

The first Instagram carousel stayed at zero reach, so the project should not judge content quality yet. The user no longer wants to publish another similar carousel from the old Grok image batch. The next work is to produce more believable lifestyle outfit images and place them in a simpler 3-slide Canva format.

Production rule:

```text
Zero reach does not block the next carousel.
```

Current image source rule:

```text
Use OpenAI or Grok based on image quality and available credits.
```

## Key Links

- GitHub repo: https://github.com/fcsh1526/codex-fittingrooom
- Perplexity weekly site: https://mika-lin-weekly.pplx.app/
- W21 test page: https://mika-lin-weekly.pplx.app/weeks/2026-W21-test.html
- W21 CSV: https://mika-lin-weekly.pplx.app/data/2026-W21-test.csv
- Canva panorama carousel design: https://www.canva.com/d/jJOq1Yimawt9wfU
- Published IG carousel: https://www.instagram.com/p/DZCTbtWGuhx/?igsh=aG9kcjl3OWIybm01
- Published asset Drive folder: https://drive.google.com/drive/folders/1tRiBkj2JbAiuv6Ol88Jx6-FpF2a6nKml

## Completed

- Perplexity W21 test report was validated.
- 20 W21 prompt rows were imported into `04_prompts/item_prompt_database.csv`.
- Day 3 Grok prompt set was created.
- W21 Grok images were reviewed.
- Canva plugin was enabled in Codex.
- Old Canva panorama carousel template was tested at `5400 x 1350`.
- New Canva direction is `3240 x 1350`, exported as 3 image-led slides.
- First Instagram carousel was published.
- 24-hour and 10+ day zero-reach status were recorded.
- Instagram zero-reach recovery SOP was created.
- A second simple test post was drafted.
- Automation hub was created in `10_automation/`.
- Weekly packet builder was tested and generated `10_automation/runs/2026-W21-test/`.
- Weekly run folder now includes Grok prompts, Canva placeholders, platform post drafts, and publish checklist.
- Perplexity import automation now supports CSV files, direct CSV URLs, and markdown reports with fenced CSV blocks.
- One-command weekly pipeline was tested with `10_automation/examples/perplexity_export_example.md`.
- Weekly run quality validation now checks required files, required fields, AI disclosure, Grok safety terms, hashtag count, and Canva text length.
- Canva handoff automation now generates `canva_fill_guide.md`, `canva_placeholder_map.json`, and `canva_asset_slots.csv`.
- Grok asset selection automation now fills cover/detail/crop asset slots from visual review scores and Drive inventory.
- Publish and metrics automation now records post URLs, 6h/24h metrics, and next-action decisions.
- Weekly status automation now writes `weekly_status.md/json` and tells the next action for each run folder.
- Weekly dashboard automation now scans all run folders and writes `10_automation/runs/DASHBOARD.md/json`.
- Daily brief automation now writes `10_automation/TODAY.md/json` and translates dashboard status into today's 1-3 tasks.
- Daily cockpit automation now writes `10_automation/DAILY_COCKPIT.html/md` as the main daily-use artifact.
- Publish queue automation now writes `10_automation/PUBLISH_QUEUE.md/json/csv` and tracks each carousel / visibility test separately.
- Visibility test automation now writes `visibility_test_package.md/json` for single-image Instagram recovery tests.
- Main weekly pipeline now creates asset review/status files by default and can select Grok assets when score sheets are provided.
- Windows shortcut `10_automation/mika_weekly.ps1` now wraps pipeline, status, dashboard, queue, today, visibility-test, assets, metrics, and validate actions.
- Smoke test automation now verifies weekly pipeline, asset selection, metrics decisions, dashboard output, daily brief output, publish queue output, visibility test package output, and PowerShell entrypoint.
- Daily heartbeat was updated from old Day X companionship to queue-based automation status checking.
- Automation architecture brief was added to explain the current state machine and manual boundaries.
- Cross-computer handoff was added in `COMPUTER_B_SYNC.md` so Computer B can continue from GitHub without reading the old conversation.
- OpenAI image-generation automation was added as the new primary image source.
- Asset selection now supports provider labels such as OpenAI and Grok.
- Perplexity public index resolution was added, so Codex can use the saved weekly site instead of requiring a pasted CSV URL every time.
- Instagram creative direction changed to 3-slide, image-led, low-text carousel posts with simple captions and profile-link shopping direction.
- Canva connector workflow and template spec were simplified to one text placeholder: `{{slide2_line}}`.

## Latest Published Post

- Instagram URL: https://www.instagram.com/p/DZCTbtWGuhx/?igsh=aG9kcjl3OWIybm01
- Confirmed publish time: 2026/06/01 16:08
- Format: Carousel
- Theme / prompt id: Sumer Looks!
- Product links: none
- CTA: 想看同風格清單？留言「沙色套裝」我整理平價 / 質感 / 替代款

## Current Metrics

First metrics check on 2026-06-02:

```text
reach = 0
likes = 0
saves = 0
comments = 0
shares = 0
profile_visits = 0
new_followers = 0
cta_comments = 0
```

10+ day visibility check on 2026-06-12:

```text
10+ days with no exposure / reach.
```

Interpretation:

```text
Treat this as an account visibility, distribution, or channel setup issue. Do not treat it as content failure.
```

## Automation Files

Start here:

```text
COMPUTER_B_SYNC.md
10_automation/AUTOMATION_ARCHITECTURE_BRIEF.md
10_automation/DAILY_COCKPIT.html
10_automation/README.md
10_automation/2026_W25_work_order.md
10_automation/weekly_carousel_pipeline.md
10_automation/weekly_handoff_checklist.md
10_automation/TODAY.md
10_automation/PUBLISH_QUEUE.md
10_automation/runs/DASHBOARD.md
10_automation/runs/2026-W21-test/visibility_test_package.md
```

Core templates:

```text
10_automation/weekly_content_packet_template.csv
10_automation/canva_placeholder_values_template.csv
02_brand/mika_lin_identity_block.md
04_prompts/grok_weekly_carousel_prompt.md
```

Recovery files:

```text
09_sops/instagram_zero_reach_recovery.md
05_content/second_test_zero_reach_post.md
```

## What The User Should Provide Next

For the next weekly carousel run:

```text
Perplexity weekly URL or use saved public index:
OpenAI API key available in environment: yes/no
Canva panorama design URL:
Instagram account visibility status:
```

If Instagram is still at zero reach:

```text
Use PUBLISH_QUEUE.md first. Use 05_content/2026_06_18_reactivation_plan.md only as a side visibility check.
```

1. Do not publish another old Grok-similar carousel.
2. Generate or dry-run OpenAI images for the next weekly run.
3. Use the 3-slide minimal Canva template automation or manual review to finish the next distinct carousel.
4. Record metrics after publishing.

## Next Codex Work

When the user provides the next Perplexity URL or Drive folder, Codex should:

1. Run `10_automation/daily_brief.py` first to create `TODAY.md`.
2. Open `10_automation/PUBLISH_QUEUE.md` to see the exact next content item.
3. If the top item is a visibility test, treat it as optional side evidence; do not let it block the next carousel.
4. Run `10_automation/weekly_dashboard.py` if the raw all-run table is needed.
5. Run `10_automation/check_weekly_status.py` if a specific run folder already exists.
6. Run `10_automation/run_weekly_pipeline.py --use-perplexity-index` if using the saved Perplexity public site, or pass `--perplexity-source` if a direct export is available.
7. Otherwise import weekly prompt rows into `04_prompts/item_prompt_database.csv`, then run `10_automation/build_weekly_packet.py`.
8. Confirm `quality_report.md` status is `pass`.
9. Use `10_automation/generate_openai_images.py --dry-run` to plan image generation.
10. Set `OPENAI_API_KEY` and rerun without `--dry-run` when ready to spend API credits.
11. Score `openai_asset_review_template.csv`.
12. Run `10_automation/select_grok_assets.py --provider OpenAI` after OpenAI images are scored.
13. Confirm `validate_weekly_run.py --require-assets` passes.
14. Use generated Canva handoff files or Canva connector edits to fill the 3-slide minimal carousel template.
15. Use generated IG / Threads / Pinterest drafts.
16. Run `10_automation/record_post_metrics.py` after publishing and at 6h/24h checkpoints.

On Windows, prefer the shortcut:

```text
10_automation/mika_weekly.ps1
```

First command after returning from a break:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action cockpit
```

Then open:

```text
COMPUTER_B_SYNC.md
10_automation/DAILY_COCKPIT.html
10_automation/TODAY.md
10_automation/PUBLISH_QUEUE.md
```

Only after reach becomes non-zero should Codex create affiliate/product links.
