# Canva Connector Workflow

Purpose: make Canva assembly semi-automatic while keeping the carousel image-led and low-text.

## What Canva Connector Can Automate

Codex can use the Canva connector to:

1. Open or duplicate a Canva brand template.
2. Replace the single text placeholder.
3. Replace or insert image fills.
4. Resize or reposition image crops.
5. Generate page thumbnails for review.
6. Commit changes only after user approval.

## Current Best Workflow

```text
weekly_content_packet.csv
-> Codex-generated images
-> image inventory + review scores
-> canva_asset_plan.md
-> canva_placeholder_map.json
-> Canva connector edits the 3-slide template
-> user reviews thumbnails
-> commit Canva changes
-> export / publish
```

## Canva Template Requirement

Use a 3-slide panorama master canvas:

```text
3240 x 1350 px
slice guides: x = 1080, 2160
export: 3 images, each 1080 x 1350 px
```

Text placeholders:

```text
{{slide2_line}}
```

Image placeholders:

```text
cover_image
motion_crop
detail_image
```

Slide roles:

1. Image-led hook. No required text.
2. One short transition sentence only.
3. Image-led ending. No CTA wall.

Keep AI disclosure in the Instagram caption, not on the image.

## Important Limitation

Canva edits are transactional. Codex can draft the edit and show thumbnails, but final save should happen only after the user confirms the preview is correct.

Photo uploads through `image_to_design` may be split by Magic Layers into background, person cutout, and object layers. For the registered Mira templates, that path is prohibited for final fills. Replace whole flat images into the named frames (`cover_image`, `motion_crop`, `detail_image`) instead of assembling separate background/person/object layers.

Daily production must duplicate one registered master template before replacing assets. Never overwrite the master templates directly.

## Hard Gate: Flat Image Assets Only

Canva autofill must use complete flat PNG/JPG images. The source for each image slot must be one of:

1. A complete flat PNG/JPG already uploaded to Canva and known to render the full person plus background as one image asset.
2. A complete flat PNG/JPG image item found in Canva folders with `list_folder_items`, using its Canva image asset id.
3. A complete flat PNG/JPG uploaded through a Canva connector path that returns a single image asset id. `upload_asset_from_url` is one such path, but public URL is not required when the asset already exists in Canva.

Do not use these sources for final fills:

- `image_to_design` output.
- Magic Layers / Background Remover output.
- Canva asset ids copied from old filled designs unless the asset is verified as a complete flat image.
- Background-only, person-cutout-only, or object-only assets.

If Codex only has local PNG paths and no safe Canva image asset id, stop and resolve the image asset first. Do not improvise with old Canva design asset ids. Do not use `image_to_design(image_file=...)` for final fills, because it creates an editable Magic Layers design instead of a guaranteed single flat image asset.

## Human Review Checklist

- Outfit is readable within one second.
- Mira identity is consistent.
- The image feels like a believable daily moment, not a posed ad.
- Slide 2 has only one short sentence.
- No comment-bait or shopping-list copy appears on the carousel.
- No logos, brand marks, or fake endorsements appear.
