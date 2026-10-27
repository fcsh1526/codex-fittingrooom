# Mira Daily Image Job

- carousel_id: `2026-W36-001`
- look_id: `2026-W36-001-L02`
- look_name: 奶油白薄風衣＋霧藍背心洋裝
- model_profile_id: `M05`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_full.png`
- attach_reference_images: `required`
- trend: 輕薄機能疊穿
- clothing_item: 奶油白可收納連帽薄風衣；霧藍細肩帶方領棉質中長洋裝；炭灰薄底芭蕾平底鞋；橄欖綠小型托特包
- occasion: 週末採買／空調商場
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W36\generated_images\2026-W36-001\looks\2026-W36-001-L02\reel\codex_generation_handoff.md
```