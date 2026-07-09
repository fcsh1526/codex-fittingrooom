# Canva Automation Trial Log - 2026-W26

## 2026-07-08 Trial 1

- Template duplicated: `Mira Template Master - A Contact Sheet`
- Trial design id: `DAHOyDPZHeQ`
- Trial design URL: `https://www.canva.com/d/q9ytQ_Tl2yFqcPx`
- Intended item: `2026-W26-002` / `M02` / polka dot outfit
- Intended local images:
  - `10_automation/runs/2026-W26/generated_images/2026-W26-002/2026-W26-002_M02_candidate_A_v2.png`
  - `10_automation/runs/2026-W26/generated_images/2026-W26-002/2026-W26-002_M02_candidate_B_v2.png`
  - `10_automation/runs/2026-W26/generated_images/2026-W26-002/2026-W26-002_M02_candidate_C_v2.png`

Result: failed. The saved design reused Canva asset ids from an older filled design instead of uploading the complete flat PNGs. Those asset ids represented split / Magic Layers content, so the Canva result had missing person layers and blurred background-only street images.

Repair attempt: cancelled before saving after the user confirmed the same split-layer failure mode.

Current status: do not export or publish `DAHOyDPZHeQ`. Rerun only after the three selected PNGs are resolved to verified Canva image asset ids. Public HTTPS URLs are only one optional upload route; they are not required when the complete image already exists as a Canva image item.

Verified Canva image assets found on 2026-07-08:

- `cover_image` candidate A: `MAHOCYb2mPI` / `Mira W26-002 Candidate A cover` / `type=image` / `import_status=success`
- `motion_crop` candidate B: `MAHOCUFmjRs` / `Mira W26-002 Candidate B detail` / `type=image` / `import_status=success`
- `detail_image` candidate C: `MAHON_SkSjs` / `2026-W26-002_M02_candidate_C_v2.png` / `type=image` / `import_status=success`

Hard gate: no future Canva autofill may use `image_to_design`, Magic Layers output, background/person cutout layers, or unverified old Canva design asset ids.

## 2026-07-09 Trial 2

- Template duplicated: `Mira Template Master - A Contact Sheet`
- Trial design id: `DAHO2rHNkZs`
- Trial edit URL: `https://www.canva.com/d/BADXM4PGvSs2Rlh`
- Source template id: `DAHOx6hb1Ug`
- Intended item: `2026-W26-002` / `M02` / polka dot outfit

Result: invalidated on 2026-07-09 after user review. The copy uses complete flat image assets, but those assets were generated before the approved M02 v3 reference anchors were created, so the model identity is old.

Do not export or publish `DAHO2rHNkZs`.

Invalidated assets:

- `cover_image`: `MAHOCYb2mPI` / `2026-W26-002_M02_candidate_A_v2.png`
- `motion_crop`: `MAHOCUFmjRs` / `2026-W26-002_M02_candidate_B_v2.png`
- `detail_image`: `MAHON_SkSjs` / `2026-W26-002_M02_candidate_C_v2.png`

Next action: regenerate W26-002 using `M02_start_v3_face.png` and `M02_start_v3_full.png`, score new candidates, then duplicate Canva again only after user-approved asset selection.
