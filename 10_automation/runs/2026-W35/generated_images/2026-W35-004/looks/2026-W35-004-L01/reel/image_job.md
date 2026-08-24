# Mira Daily Image Job

- carousel_id: `2026-W35-004`
- look_id: `2026-W35-004-L01`
- look_name: 白襯衫＋黑白窄領巾＋深藍直筒褲
- model_profile_id: `M02`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_full.png`
- attach_reference_images: `required`
- trend: 窄領巾與蝴蝶結細節
- clothing_item: 白色自然合身純棉襯衫；黑白細窄絲巾在鎖骨下方打小蝴蝶結；深海軍藍高腰直筒西裝褲；黑色尖頭平底鞋；黑色小型肩背包
- occasion: 辦公室／會議
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W35\generated_images\2026-W35-004\looks\2026-W35-004-L01\reel\codex_generation_handoff.md
```