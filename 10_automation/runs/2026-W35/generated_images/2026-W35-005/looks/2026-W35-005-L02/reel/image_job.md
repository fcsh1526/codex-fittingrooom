# Mira Daily Image Job

- carousel_id: `2026-W35-005`
- look_id: `2026-W35-005-L02`
- look_name: 淡紫灰垂墜上衣＋深藍直筒丹寧
- model_profile_id: `M04`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_full.png`
- attach_reference_images: `required`
- trend: 深色直筒丹寧與柔和上衣
- clothing_item: 淡紫灰短袖嫘縈垂墜上衣；深藍中高腰直筒薄丹寧褲；奶油白尖頭平底鞋；酒紅小型結構手提包
- occasion: 週末午餐／展覽
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- required_frames: 3
- direct_reel_frame: `1080x1920` / `9:16`
- reel_frame_targets: `reel_frame_targets.json`
- canva_crop_limit_applies: `no`

Generate and review the native 9:16 full-person Reel A; it is the only still required for this surface.
Do not reuse one surface's crop as the other surface's source.
Keep anatomy, identity, contact-shadow, crop-safety, and platform checks in review_sheet.csv rather than adding them to the generation prompt.

Codex handoff:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W35\generated_images\2026-W35-005\looks\2026-W35-005-L02\reel\codex_generation_handoff.md
```