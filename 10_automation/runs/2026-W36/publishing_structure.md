# W36 Publishing Structure

W36 uses the active dual-surface production contract: five themes, one locked model per theme, two complete looks per model, and ten looks total. Every look requires a separately composed Reel source and a three-frame Carousel set.

## Theme and model locks

| Theme | Model | Looks |
| --- | --- | --- |
| 輕薄機能疊穿 | M05 | `2026-W36-001-L01`, `2026-W36-001-L02` |
| 短外套配長流動下身 | M02 | `2026-W36-002-L01`, `2026-W36-002-L02` |
| 麂皮質感小面積入秋 | M01 | `2026-W36-003-L01`, `2026-W36-003-L02` |
| 絲巾效果與緞面垂墜 | M04 | `2026-W36-004-L01`, `2026-W36-004-L02` |
| 深紅色小面積亮點 | M03 | `2026-W36-005-L01`, `2026-W36-005-L02` |

Model ids are private production identifiers and must never appear in published copy or images.

## Required assets per look

- Reel A: one native 9:16 full-person source composed directly for 1080x1920.
- Carousel A: one full-person Hero composed for the assigned Canva cover frame.
- Carousel B: one scene-application frame showing the exact outfit working in its intended occasion.
- Carousel C: one accessory-detail frame retaining enough garment context to prove the styling relationship.

Reel and Carousel compositions are separate jobs. Carousel B/C begin only after that look's Carousel A is visually accepted and locked.

W36 scene rule: do not use access-control turnstiles, ticket gates, badge-scanning actions, or visible access cards. Prefer open walkways and natural interaction with garments, bags, doors, books, menus, or other occasion-relevant objects.

## Reel compilation

User-approved revision, 2026-09-09: W36 is packaged as five Reels, one theme and one model per Reel. Each Reel combines both looks and all approved surface images in this fixed order:

1. L01 Reel A
2. L01 Carousel A
3. L01 Carousel B
4. L01 Carousel C
5. L02 Reel A
6. L02 Carousel A
7. L02 Carousel B
8. L02 Carousel C

Do not return to the superseded L01/L02 cross-model grouping unless the user explicitly requests a new experiment.

## Carousel completion gate

For each look, accept Carousel A as the identity, outfit, styling, proportion and photographic lock before producing B/C. Normalize accepted A/B/C to the registered template pixels without stretching and with no more than 15% center crop, then keep the set at `needs_canva_frame_review` until the connected Canva preview is approved by the user.

## Caption policy

All W36 Instagram copy follows `09_sops/mira_instagram_caption_sop.md`: one concise editorial conclusion followed by one image-verifiable styling reason, normally 35–75 Traditional Chinese characters. Do not add hashtags, forced questions, keyword-comment CTAs, internal trend labels, model ids, or repeated account-level AI disclosure.

## Manual boundary

The user performs final Canva design decisions, Reel assembly, export and Instagram publishing. Codex records accepted assets and production status, and pauses for user visual approval at the required preview gates.

## W36 batch-review authorization

On 2026-09-03, the user authorized continuous production of the remaining W36 image assets before reviewing them one look at a time. During this run, Codex may generate and internally review Reel A and Carousel A/B/C for successive looks without pausing after each image. Keep rejected candidates out of Canva and collect completed look sets into a review queue. User approval is still required before a look is marked final for Canva, and each Canva editing transaction must be previewed and explicitly approved before commit.
