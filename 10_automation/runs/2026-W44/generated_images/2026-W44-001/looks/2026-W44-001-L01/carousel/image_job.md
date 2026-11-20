# Mira Daily Image Job

- carousel_id: `2026-W44-001`
- look_id: `2026-W44-001-L01`
- look_name: 皇家紫細針織V領薄開襟衫（敞開）、白圓領短袖T、炭灰高腰直筒褲、白灰低筒球鞋、黑小肩包、細銀耳環
- model_profile_id: `M02`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_full.png`
- attach_reference_images: `required`
- trend: 一件紫色薄針織，工作日到週末
- clothing_item: 皇家紫細針織V領薄開襟衫（敞開）、白圓領短袖T、炭灰高腰直筒褲、白灰低筒球鞋、黑小肩包、細銀耳環
- occasion: 台北，有遮簷的辦公街廓；週末造型同路段示意另一日，不冒稱同日現場變裝
- frame_plan: reel:full_9x16+vertical_styling_proof;carousel:hero_full+scene_application+accessory_detail
- required_frames: 5
- canva_template: `v3-B` / Mira Template Master v3 - B Cross-Boundary Symmetric
- canva_slot_targets: `canva_slot_targets.json`
- canva_crop_limit: `15%`

Generate Carousel A first. After acceptance, B Scene Application and C Accessory Detail are both required.
Do not reuse one surface's crop as the other surface's source.
Keep anatomy, identity, contact-shadow, crop-safety, and platform checks in review_sheet.csv rather than adding them to the generation prompt.

Codex handoff:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W44\generated_images\2026-W44-001\looks\2026-W44-001-L01\carousel\codex_generation_handoff.md
```