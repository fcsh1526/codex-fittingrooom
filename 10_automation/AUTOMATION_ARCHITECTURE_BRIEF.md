# AI Virtual Fashion Creator Automation Brief

Updated: 2026-07-09

This is the current automation architecture for the Mira AI fashion creator workflow.

The purpose is not to keep adding disconnected scripts. The purpose is to run one fixed state machine:

```text
person identity -> weekly trend -> prompt packet -> Codex images -> Canva carousel -> publish -> metrics -> next decision
```

Monetization stays off until at least one channel gets non-zero reach.

---

## Slide 1 - Current Answer

The workflow is now organized around a queue, not a daily checklist.

Daily work should start with:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action cockpit -TodayDate 2026-06-22
```

Then open:

```text
10_automation/DAILY_COCKPIT.html
10_automation/TODAY.md
10_automation/PUBLISH_QUEUE.md
```

`DAILY_COCKPIT.html` is the daily-use artifact. It contains the top item, checklist, links, and reply template on one page.

Previous top item before the production-first correction was a visibility test. The production-first rule changes this:

```text
ready_for_canva_and_publish carousel items outrank visibility tests
```

This means: keep producing carousels continuously. Visibility tests and zero-reach metrics are side signals, not blockers.

---

## Slide 2 - System Layers

There are six layers.

```text
1. Brand layer
   Mira identity, visual rules, safety boundaries

2. Trend layer
   Perplexity weekly report / CSV / markdown export

3. Prompt layer
   item_prompt_database.csv -> weekly_content_packet.csv -> image_generation_briefs.md -> codex_generation_handoff.md

4. Asset layer
   Codex-generated images -> review sheet -> canva_asset_slots.csv

5. Publishing layer
   Canva handoff -> platform captions -> publish record -> metrics

6. Decision layer
   weekly_status -> dashboard -> publish queue -> today brief
```

The decision layer is now the control center.

---

## Slide 3 - Control Center Files

Use these three files in this order.

```text
10_automation/DAILY_COCKPIT.html
```

One-page daily operating page.

```text
10_automation/TODAY.md
```

What should happen today.

```text
10_automation/PUBLISH_QUEUE.md
```

Exact next content item across all carousels and visibility tests.

```text
10_automation/runs/DASHBOARD.md
```

Weekly run-level overview.

If these disagree, use `PUBLISH_QUEUE.md` for the concrete next publishing action.

---

## Slide 4 - State Machine

Each content item moves through stages:

```text
needs_weekly_input
needs_image_asset_selection
ready_for_canva_and_publish
published_waiting_for_metrics
visibility_recovery
ready_to_publish_visibility_test
wait_for_24h
weak_distribution
hook_or_save_gap
profile_interest
repeat_bucket
```

The queue ranks stages by urgency.

Current production-first rule:

```text
ready_for_canva_and_publish > needs_image_asset_selection > published_waiting_for_metrics > ready_to_publish_visibility_test > visibility_recovery
```

That is why the system should keep moving carousel production even if Instagram reach is still zero.

Weekly content cadence:

```text
5 Instagram carousel posts per week
1 carousel per day
M01-M05 each appear exactly once per week
Perplexity provides outfit topics; Codex assigns the internal model rotation
```

---

## Slide 5 - Weekly Automation Flow

When Perplexity export is ready:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action pipeline `
  -Week 2026-WXX `
  -PerplexitySource path_or_url_to_export `
  -Limit 2
```

This generates:

```text
weekly_content_packet.csv
image_generation_briefs.md
generated_images/{carousel_id}/codex_generation_handoff.md
canva_placeholder_values.csv
canva_fill_guide.md
canva_placeholder_map.json
canva_asset_slots.csv
post_drafts.md
publish_checklist.md
quality_report.md/json
weekly_status.md/json
```

If a scored Codex review sheet is available, the same pipeline can also select Canva assets.

---

## Slide 6 - Codex Image / Asset Automation

Current state:

```text
Codex image generation = primary workflow
Reference anchors = required before generation
Image scoring = CSV-driven
Asset selection = automated
Canva asset slots = automated
```

Command:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action assets `
  -Week 2026-WXX `
  -ScoreSheet path_to_scores.csv `
  -DriveInventory path_to_drive_inventory.csv
```

Current external boundary:

```text
Canva final crop/export and Instagram posting remain manual.
The local repo prepares prompts, image handoffs, score sheets, asset slots, captions, queues, and metrics commands.
```

---

## Slide 7 - Canva / Carousel Automation

Current state:

```text
Canva text placeholders = automated
Canva fill guide = automated
Canva asset slots = automated
Caption / hashtags / checklist = automated
Final Canva editing / export = still manual unless we later implement Canva API/plugin replacement
```

Primary files:

```text
canva_fill_guide.md
canva_placeholder_map.json
canva_asset_slots.csv
canva_asset_plan.md
post_drafts.md
publish_checklist.md
```

This is enough to repeatedly create polished Instagram carousels, but the final Canva design action is still semi-manual.

---

## Slide 8 - Publishing / Metrics Automation

After publishing, record the post:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action metrics `
  -Week 2026-WXX `
  -CarouselId 2026-WXX-001 `
  -PostUrl "https://www.instagram.com/p/POST_ID/" `
  -PublishedAt "YYYY/MM/DD HH:mm"
```

At 6h / 24h, record metrics:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action metrics `
  -Week 2026-WXX `
  -CarouselId 2026-WXX-001 `
  -PostUrl "https://www.instagram.com/p/POST_ID/" `
  -PublishedAt "YYYY/MM/DD HH:mm" `
  -RecordMetrics `
  -MeasuredAt YYYY-MM-DD `
  -HoursAfterPublish 24 `
  -Reach 0 `
  -Likes 0 `
  -Saves 0 `
  -Comments 0 `
  -Shares 0
```

The decision engine then routes the next step.

---

## Slide 9 - Visibility Signal

The first IG carousel had:

```text
reach = 0
likes = 0
saves = 0
comments = 0
shares = 0
```

The system interprets that as:

```text
visibility_recovery
```

Not as:

```text
bad content
```

Therefore, the queue generated:

```text
visibility_test_package.md
```

The next action is not to stop carousel production. The visibility test is optional side evidence while the queue keeps preparing the next polished carousel.

---

## Slide 10 - What Is Fully Automated Now

Automated locally:

```text
Perplexity CSV / markdown import
prompt database upsert
weekly packet generation
Codex image brief generation
Canva placeholder generation
Canva handoff generation
asset slot generation
quality validation
Codex asset selection from score sheet
publish / metrics recording
decision classification
weekly dashboard
daily brief
publish queue
single-image visibility test package
smoke test
```

Not automated yet:

```text
Perplexity scheduled webpage scraping without user URL or export
Canva final export
Google Drive image inventory through connector in this exact pipeline
Canva final design replacement / export
Instagram publishing and insight retrieval
```

These are external-tool boundaries, not missing local state-machine logic.

---

## Slide 11 - Recommended Next Automation Milestones

Milestone 1: keep the carousel production loop running.

```text
Use PUBLISH_QUEUE.md
Finish the next ready_for_canva_and_publish carousel
Record post URLs and metrics when available
```

Milestone 2: automate Drive inventory from Google Drive connector.

```text
Input: Drive folder URL
Output: drive_image_inventory.csv
```

Milestone 3: automate Canva placeholder replacement.

```text
Input: Canva design URL + canva_placeholder_map.json
Output: updated Canva design or filled export checklist
```

Milestone 4: automate weekly Perplexity pull.

```text
Input: fixed Perplexity CSV URL
Output: weekly run folder without manual download
```

Milestone 5: add cross-platform queue.

```text
Instagram
Threads
Pinterest
Xiaohongshu
```

---

## Slide 12 - Operating Rule From Now On

Do not ask:

```text
What Day X are we on?
```

Do ask:

```text
What is the top item in PUBLISH_QUEUE.md?
What external input is missing for that item?
```

Current external input needed:

```text
For the top carousel item, provide Canva progress / final Canva URL / post URL when published.
Visibility test URL and metrics are useful, but they do not block the next carousel.
```

After that, the automation can decide whether to:

```text
continue Instagram
move first growth test to Threads / Pinterest / Xiaohongshu
return to carousel production
```
