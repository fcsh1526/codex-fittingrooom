# Mira Daily Image Job

- carousel_id: `2026-W36-002`
- look_id: `2026-W36-002-L02`
- look_name: 淺灰短版西裝外套＋深藍長寬褲
- model_profile_id: `M02`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_full.png`
- attach_reference_images: `required`
- trend: 短外套配長流動下身
- clothing_item: 淺灰無內裡短版單釦西裝外套；奶油白合身無袖針織上衣；深海軍藍高腰長寬褲；深棕尖頭低跟鞋；深棕窄版手提包
- occasion: 通勤／簡報
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W36\generated_images\2026-W36-002\looks\2026-W36-002-L02\reel\codex_generation_handoff.md
```