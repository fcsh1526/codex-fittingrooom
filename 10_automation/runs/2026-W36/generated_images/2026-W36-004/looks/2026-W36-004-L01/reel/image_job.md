# Mira Daily Image Job

- carousel_id: `2026-W36-004`
- look_id: `2026-W36-004-L01`
- look_name: 香檳緞面裹身裙＋黑色針織背心
- model_profile_id: `M04`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_full.png`
- attach_reference_images: `required`
- trend: 絲巾效果與緞面垂墜
- clothing_item: 黑色合身方領細針織背心；香檳色高腰裹身緞面中長裙；黑色尖頭平底鞋；黑色小型硬挺手提包；細版金色耳環
- occasion: 晚餐／約會
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W36\generated_images\2026-W36-004\looks\2026-W36-004-L01\reel\codex_generation_handoff.md
```