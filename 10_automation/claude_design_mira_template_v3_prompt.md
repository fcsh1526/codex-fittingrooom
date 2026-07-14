# Claude Design Prompt - Mira Template v3 Cross-Boundary

Use this only when rebuilding a Mira master from scratch. For existing Canva masters, direct frame resizing in Canva is more reliable than asking Claude to reinterpret the layout.

```text
Create one editable 3240 x 1350 px panoramic Instagram carousel master for Mira. The export is still three 1080 x 1350 slides, cut at x=1080 and x=2160, but the composition must visibly continue across both cuts.

This is not three side-by-side cards. It is one fashion editorial spread viewed through three swipe windows.

Hard geometry requirements:
- cover_image must cross x=1080 by 120-200 px. Recommended bounds: x=60-130, width=1120-1240, height=1050-1350.
- motion_crop must cross x=2160 by 100-180 px, or begin 80-160 px before x=1080. Recommended bounds: x=1160-1450, width=980-1180.
- detail_image must begin 80-140 px before x=2160. Recommended bounds: x=2020-2080, width=1060-1220.
- Keep the final canvas exactly 3240 x 1350. Do not move the export cuts.
- At least two image frames must cross a cut line. A frame that merely touches a cut does not count.

Required editable layers:
- cover_image
- motion_crop
- detail_image
- slide2_line
- optional locked scene_backplate, boundary_insert, grain_overlay, brand_mark

Text safety:
- slide2_line is Traditional Chinese only and contains exactly two intentional lines.
- Reserve a calm text-safe zone in slide 2 that does not overlap a face.
- Text must stay at least 90 px away from x=1080 and x=2160.
- Do not rely on automatic wrapping. The supplied line break is part of the content.

Visual rules:
- Preserve full-body outfit readability on slide 1.
- Use overlap, crop rhythm, negative space, and scale to create swipe continuity.
- Avoid three equal columns, three isolated cards, visible gutters, rounded caption cards, labels such as FIG. 01, icons, arrows, and CTA blocks.
- Keep only slide2_line and a very small optional Mira mark.

Before returning the design, verify numerically:
1. Canvas is 3240 x 1350.
2. Cuts remain x=1080 and x=2160.
3. At least two image frames cross those cuts by 100 px or more.
4. slide2_line is in a face-free safe zone.
5. The three exported slices still work individually while clearly revealing shared imagery during a swipe.
```

Correction prompt if the result still looks separated:

```text
Reject this version. It is still three isolated slides. Show the exact x/width values for cover_image, motion_crop, and detail_image, then resize them so at least two frames cross x=1080 or x=2160 by 100-200 px. Keep the cut positions unchanged.
```
