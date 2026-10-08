# Mira Daily Image Job

- carousel_id: `2026-W41-003`
- look_id: `2026-W41-003-L01`
- look_name: 奶油白棉T配可可棕丹寧
- model_profile_id: `M02`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_full.png`
- attach_reference_images: `required`
- trend: 可可棕直筒丹寧
- clothing_item: 奶油白圓領棉短袖，整齊紮入；可可棕高腰直筒丹寧褲，無刷破、褲腳停在鞋面；米白薄短外套敞開；黑色低跟便鞋；黑色小方肩包；黑色窄皮帶
- occasion: 通勤
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W41\generated_images\2026-W41-003\looks\2026-W41-003-L01\reel\codex_generation_handoff.md
```