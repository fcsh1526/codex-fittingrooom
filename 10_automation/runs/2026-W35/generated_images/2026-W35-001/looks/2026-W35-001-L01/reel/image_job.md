# Mira Daily Image Job

- carousel_id: `2026-W35-001`
- look_id: `2026-W35-001-L01`
- look_name: 石墨黑高領薄夾克＋米灰直筒褲
- model_profile_id: `M05`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_full.png`
- attach_reference_images: `required`
- trend: 輕量高領外套
- clothing_item: 石墨黑無鋪棉短版高領薄夾克；奶油白合身棉質短袖上衣；米灰高腰窄直筒褲；黑色方頭樂福鞋；深灰小型肩背包
- occasion: 通勤／空調辦公室
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W35\generated_images\2026-W35-001\looks\2026-W35-001-L01\reel\codex_generation_handoff.md
```