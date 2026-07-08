# Canva Fill Guide - 2026-W26

Select and duplicate one registered Mira Canva master template:

```text
10_automation/canva_template_registry.md
```

Automation labels saved in Canva:

```text
cover_image
motion_crop
detail_image
slide2_line
```

## Template Contract

- Canvas: `3240 x 1350 px`
- Export: `3 slides x 1080 x 1350 px`
- Slice guides: `x = 1080, 2160`
- Slide 1: image-led hook.
- Slide 2: one short transition line and one editorial motion crop.
- Slide 3: image-led closing frame.
- Keep disclosure in the caption, not on the image.

## 2026-W26-002 / W26-P002

Status: use this item for the first Canva v2 test-fill.

### Text Replacement

| Placeholder | Value |
|---|---|
| `{{slide2_line}}` | 黑白波點，留一點午後的輕盈。 |

### Asset Slots

| Slot | Use File | Path |
|---|---|---|
| `cover_image` | `2026-W26-002_M02_candidate_A_v2.png` | `10_automation/runs/2026-W26/generated_images/2026-W26-002/2026-W26-002_M02_candidate_A_v2.png` |
| `motion_crop` | `2026-W26-002_M02_candidate_B_v2.png` | `10_automation/runs/2026-W26/generated_images/2026-W26-002/2026-W26-002_M02_candidate_B_v2.png` |
| `detail_image` | `2026-W26-002_M02_candidate_C_v2.png` | `10_automation/runs/2026-W26/generated_images/2026-W26-002/2026-W26-002_M02_candidate_C_v2.png` |

### Image QA Notes

- `A_v2`: selected cover; full outfit readable, stable face, no ghosting.
- `B_v2`: selected motion crop; intentional half-body crop, stable face and hands.
- `C_v2`: selected closing frame; clear dress, shoes, and bag; feet are close to bottom but not cropped.

### Instagram Caption Draft

```text
黑白波點洋裝，適合週末午後或輕鬆約會。

相似單品整理在個人頁連結。
AI 生成虛擬造型影像。

#週末穿搭 #洋裝穿搭 #波點洋裝 #AI穿搭 #虛擬造型 #Mira
```

### Before Saving Canva

- No head crop on Slide 1 or Slide 3.
- Motion crop on Slide 2 looks intentional, not like a broken cut.
- `{{slide2_line}}` has been replaced.
- Final image has no product list, CTA wall, comment bait, or AI disclosure on the image.
- The carousel still reads as one editorial spread after slicing.
