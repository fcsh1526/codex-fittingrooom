# Mira Daily Image Job

- carousel_id: `2026-W45-002`
- look_id: `2026-W45-002-L02`
- look_name: 白T＋苔綠開襟衫，棕褲延用
- model_profile_id: `M02`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_full.png`
- attach_reference_images: `required`
- trend: 苔綠配棕，看到你就笑著走近
- clothing_item: 奶油白棉圓領短袖T、苔綠薄棉針織V領開襟衫敞開、同款可可棕直筒長褲、同款米白低筒鞋、深棕小肩包、細金色耳針
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W45\generated_images\2026-W45-002\looks\2026-W45-002-L02\carousel\codex_generation_handoff.md
```