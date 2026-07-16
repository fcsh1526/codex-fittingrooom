# Canva Template Registry

Last updated: 2026-07-16

Purpose: source of truth for Mira Canva master templates and automation slot names.

Active version: `v3` (committed in Canva). The original v2 designs remain archived and are no longer selected by automation.

## Automation Contract

- Master canvas: `3240 x 1350 px`
- Export: `3 x 1080 x 1350 px`
- Slice guides: `x = 1080`, `x = 2160`
- Image slots: `cover_image`, `motion_crop`, `detail_image`
- Text slot: `slide2_line`

Crop-fit contract:

```text
Selected images must remain publishable under the assigned frame's untouched fill. Compose A/B/C for the exact ratios in this registry, preserve the full hairstyle with at least 8% top clearance whenever the head appears, and keep face/outfit focus inside the central 70%. A design is not ready to publish when manual focal-point adjustment is still required.
```

Generation order:

```text
choose one master -> read its A/B/C slot geometry -> generate each composition for that exact ratio -> normalize without stretching -> visual frame-fit review -> Canva fill
```

Do not generate all five template variants. Each carousel uses one selected master and therefore still produces only three final Canva-ready images.

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

## Audited Slot Geometry

Coordinates and dimensions are Canva canvas pixels. The complete machine-readable record, including Canva element ids, is in `canva_template_registry.json`.

| Master | A / `cover_image` | B / `motion_crop` | C / `detail_image` |
| --- | --- | --- | --- |
| v3-A | `1160 x 1190` (0.9748:1) | `980 x 430` (2.2791:1) | `1080 x 1080` (1:1) |
| v3-B | `1240 x 1350` (0.9185:1) | `1140 x 560` (2.0357:1) | `1180 x 1350` (0.8741:1) |
| v3-C | `1230 x 1350` (0.9111:1) | `1000 x 460` (2.1739:1) | `1180 x 1350` (0.8741:1) |
| v3-D | `1240 x 1350` (0.9185:1) | `1140 x 1350` (0.8444:1) | `1180 x 1350` (0.8741:1) |
| v3-E | `1120 x 1050` (1.0667:1) | `1120 x 410` (2.7317:1) | `1060 x 1010` (1.0495:1) |

Template E correction saved on 2026-07-16: the bottom-right `MIRA` text box was moved left to a 40px right-safe margin in the master and in W29-002 / W29-005.

## Selection Rule

Default to `A Contact Sheet` unless the daily outfit clearly matches another mood:

- Use `C Noir Evening` for dark, night, autumn-winter, or evening styling.
- Use `E Weekend Air` for light weekend, linen, cafe, or soft daylight styling.
- Use `D Full-Bleed` when the selected images are visually strong enough to carry the post.
- Use `B Symmetric` for formal calm balance when the story benefits from restraint.
