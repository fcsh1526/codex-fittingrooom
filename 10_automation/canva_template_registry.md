# Canva Template Registry

Last updated: 2026-07-14

Purpose: source of truth for Mira Canva master templates and automation slot names.

Active version: `v3` (committed in Canva). The original v2 designs remain archived and are no longer selected by automation.

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
| A | Mira Template Master v3 - A Cross-Boundary Contact Sheet | https://www.canva.com/d/c-IyIaIsCawzyCI | Standard daily editorial. General weekday outfit posts and most daily trends. |
| B | Mira Template Master v3 - B Cross-Boundary Symmetric | https://www.canva.com/d/UoVSnPEpgguD3be | Formal balanced magazine spread. Quiet, calm, symmetric posts. |
| C | Mira Template Master v3 - C Cross-Boundary Noir | https://www.canva.com/d/C9QGHZ6OH7HtYux | Dark evening / autumn-winter editorial. Night, black, evening, or low-light moods. |
| D | Mira Template Master v3 - D Cross-Boundary Full-Bleed | https://www.canva.com/d/Kh_uu5y-twQzbF- | Strongest image-led impact. Use when photos are strong and should dominate. |
| E | Mira Template Master v3 - E Cross-Boundary Weekend Air | https://www.canva.com/d/djICquyAb4kcGwW | Quiet weekend / Kinfolk-like. Linen, cafe, soft daylight, airy negative space. |

## Selection Rule

Default to `A Contact Sheet` unless the daily outfit clearly matches another mood:

- Use `C Noir Evening` for dark, night, autumn-winter, or evening styling.
- Use `E Weekend Air` for light weekend, linen, cafe, or soft daylight styling.
- Use `D Full-Bleed` when the selected images are visually strong enough to carry the post.
- Use `B Symmetric` for formal calm balance when the story benefits from restraint.
