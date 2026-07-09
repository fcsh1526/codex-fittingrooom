# Canva Template Registry

Last updated: 2026-07-08

Purpose: source of truth for Mira Canva master templates and automation slot names.

## Automation Contract

- Master canvas: `3240 x 1350 px`
- Export: `3 x 1080 x 1350 px`
- Slice guides: `x = 1080`, `x = 2160`
- Image slots: `cover_image`, `motion_crop`, `detail_image`
- Text slot: `slide2_line`

Daily-use rule:

```text
Duplicate a master template first. Replace assets only in the duplicate. Never write daily content directly into the master templates.
```

Replacement rule:

```text
Replace whole flat PNG/JPG images into the named Canva frames. Do not split uploads into background/person/object layers. Do not use image_to_design, Magic Layers, or old Canva design asset ids unless the asset is verified as a complete flat image.
```

## Master Templates

| Key | Canva master | URL | Use case |
| --- | --- | --- | --- |
| A | Mira Template Master - A Contact Sheet | https://www.canva.com/design/DAHOx6hb1Ug/A1sysuKRtad0lCYR8jqBQg/edit | Standard daily editorial. General weekday outfit posts and most daily trends. |
| B | Mira Template Master - B Symmetric | https://www.canva.com/design/DAHOxwp1cZ8/cIfSmcVa-DAJJrT-21PJoA/edit | Formal balanced magazine spread. Quiet, calm, symmetric posts. |
| C | Mira Template Master - C Noir Evening | https://www.canva.com/design/DAHOyEHkFvg/DBpyigPr05vQqxuuqV7wKA/edit | Dark evening / autumn-winter editorial. Night, black, evening, or low-light moods. |
| D | Mira Template Master - D Full-Bleed | https://www.canva.com/design/DAHOyNz_Dh4/SCdZqafV5zkpK5TVIB6kMw/edit | Strongest image-led impact. Use when photos are strong and should dominate. |
| E | Mira Template Master - E Weekend Air | https://www.canva.com/design/DAHOyEiLL24/yTWykrCQdrFjncOa46cq9g/edit | Quiet weekend / Kinfolk-like. Linen, cafe, soft daylight, airy negative space. |

## Selection Rule

Default to `A Contact Sheet` unless the daily outfit clearly matches another mood:

- Use `C Noir Evening` for dark, night, autumn-winter, or evening styling.
- Use `E Weekend Air` for light weekend, linen, cafe, or soft daylight styling.
- Use `D Full-Bleed` when the selected images are visually strong enough to carry the post.
- Use `B Symmetric` for formal calm balance when the story benefits from restraint.
