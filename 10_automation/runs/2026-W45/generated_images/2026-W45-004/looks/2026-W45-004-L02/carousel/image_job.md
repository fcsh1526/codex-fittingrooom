# Mira Daily Image Job

- carousel_id: `2026-W45-004`
- look_id: `2026-W45-004-L02`
- look_name: 素色短袖＋深底花卉裙
- model_profile_id: `M04`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_full.png`
- attach_reference_images: `required`
- trend: 深底花卉，只讓一件當主角
- clothing_item: 奶油白薄棉短袖T、墨黑底莓紅花卉直筒小腿中段裙、深棕樂福鞋、同款深棕素色小肩包、銀色耳針
- occasion: 日常外出／赴約
- frame_plan: Reel: native 9:16 full A + reviewed styling-proof; Carousel: A full / B scene / C detail
- required_frames: Reel A+proof; Carousel A+B+C
- canva_template: `v3-A` / Mira Template Master v3 - A Cross-Boundary Contact Sheet
- canva_slot_targets: `canva_slot_targets.json`
- canva_crop_limit: `15%`

Generate Carousel A first. After acceptance, B Scene Application and C Accessory Detail are both required.
Do not reuse one surface's crop as the other surface's source.
Keep anatomy, identity, contact-shadow, crop-safety, and platform checks in review_sheet.csv rather than adding them to the generation prompt.

Codex handoff:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W45\generated_images\2026-W45-004\looks\2026-W45-004-L02\carousel\codex_generation_handoff.md
```