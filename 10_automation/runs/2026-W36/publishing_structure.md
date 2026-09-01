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

The ten accepted Reel A sources may become either:

1. One 10-look Reel in look-plan order.
2. Two 5-look Reels:
   - Reel 1: `L01` from each of the five themes.
   - Reel 2: `L02` from each of the five themes.

Each look contributes one full-person shot. The final edit does not create ten separate Reels by default.

## Carousel completion gate

For each look, accept Carousel A as the identity, outfit, styling, proportion and photographic lock before producing B/C. Normalize accepted A/B/C to the registered template pixels without stretching and with no more than 15% center crop, then keep the set at `needs_canva_frame_review` until the connected Canva preview is approved by the user.

## Caption policy

All W36 Instagram copy follows `09_sops/mira_instagram_caption_sop.md`: one concise editorial conclusion followed by one image-verifiable styling reason, normally 35–75 Traditional Chinese characters. Do not add hashtags, forced questions, keyword-comment CTAs, internal trend labels, model ids, or repeated account-level AI disclosure.

## Manual boundary

The user performs final Canva design decisions, Reel assembly, export and Instagram publishing. Codex records accepted assets and production status, and pauses for user visual approval at the required preview gates.
