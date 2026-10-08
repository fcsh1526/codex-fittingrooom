# Mira Daily Image Job

- carousel_id: `2026-W41-001`
- look_id: `2026-W41-001-L02`
- look_name: 炭灰短外套配淺灰直筒褲
- model_profile_id: `M05`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_full.png`
- attach_reference_images: `required`
- trend: 短領口薄外套與俐落短比例
- clothing_item: 炭灰短版無鋪棉立領外套，敞開；奶油白圓領棉短袖；淺灰高腰直筒斜紋長褲；黑色低跟樂福鞋；黑色小方肩包；窄黑皮帶
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W41\generated_images\2026-W41-001\looks\2026-W41-001-L02\reel\codex_generation_handoff.md
```