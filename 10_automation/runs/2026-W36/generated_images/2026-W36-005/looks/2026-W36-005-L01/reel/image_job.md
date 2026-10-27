# Mira Daily Image Job

- carousel_id: `2026-W36-005`
- look_id: `2026-W36-005-L01`
- look_name: 炭灰針織上衣＋黑褲＋櫻桃紅小包
- model_profile_id: `M03`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_full.png`
- attach_reference_images: `required`
- trend: 深紅色小面積亮點
- clothing_item: 炭灰合身短袖細針織上衣；黑色高腰窄直筒長褲；櫻桃紅小型光滑皮革腋下包；黑色方頭樂福鞋；銀色細耳環
- occasion: 通勤／下班採買
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W36\generated_images\2026-W36-005\looks\2026-W36-005-L01\reel\codex_generation_handoff.md
```