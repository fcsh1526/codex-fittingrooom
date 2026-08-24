# Mira Daily Image Job

- carousel_id: `2026-W35-003`
- look_id: `2026-W35-003-L01`
- look_name: 海軍藍運動薄外套＋深灰直筒裙
- model_profile_id: `M03`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_full.png`
- attach_reference_images: `required`
- trend: 運動外層配裙裝
- clothing_item: 深海軍藍短版立領薄尼龍運動外套；灰白合身棉質短袖；深灰高腰直筒中長裙；白色低調平底球鞋；黑色小型肩背包
- occasion: 上班／午間外出
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W35\generated_images\2026-W35-003\looks\2026-W35-003-L01\reel\codex_generation_handoff.md
```