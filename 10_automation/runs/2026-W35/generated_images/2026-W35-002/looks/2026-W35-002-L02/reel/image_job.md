# Mira Daily Image Job

- carousel_id: `2026-W35-002`
- look_id: `2026-W35-002-L02`
- look_name: 奶油白洋裝＋深棕麂皮低跟鞋
- model_profile_id: `M01`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png`
- attach_reference_images: `required`
- trend: 深棕麂皮觸感
- clothing_item: 奶油白無袖薄棉直身中長洋裝；巧克力棕方頭麂皮低跟鞋；黑色小型光滑皮革肩背包；細版銀色耳環
- occasion: 週末逛街／午餐
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W35\generated_images\2026-W35-002\looks\2026-W35-002-L02\reel\codex_generation_handoff.md
```