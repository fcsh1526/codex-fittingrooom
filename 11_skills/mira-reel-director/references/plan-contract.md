# Production-plan contract v1

This is an inspectable planning record, not a media engine. The starter is deliberately incomplete and `draft`: it does not create approval, a weekly quota, a scene, or a five-look film. Fill it from the approved editorial plan. Do not fill missing historical facts with guesses.

## Commands

From the project root, using an available Python 3.10+ interpreter:

```text
python 11_skills/mira-reel-director/scripts/plan.py init tmp/my-film/production_plan.json --recipe continuous_route
python 11_skills/mira-reel-director/scripts/plan.py validate tmp/my-film/production_plan.json
python 11_skills/mira-reel-director/scripts/plan.py validate tmp/my-film/production_plan.json --for-generation
```

`init` refuses to overwrite a file. `validate` reports `invalid`, `incomplete`, or `complete_evidence`. Exit 2 means invalid data/files; exit 3 means `--for-generation` is blocked by missing evidence; a valid but incomplete draft returns 0 in ordinary planning mode. An exit code of 0 alone is **not** a generation green light: read `ready_for_generation`. Even `complete_evidence` only means machine-checkable fields and exact artifact receipts are present; it does not mean an image or film has passed visual QA.

`path_base: "plan"` resolves every asset and approval-receipt path from the plan's folder. `"project"` requires `--project-root PATH` and resolves all paths there. Use forward-slash relative paths; no absolute paths, backslashes, traversal, or symlink escape. All image/video/scene references must identify local files; remote URLs belong in source documents, not path fields. Large media may remain outside Git but must exist in the chosen local project when checked.

## Fields and evidence

2026-10-29 extension: `presentation.recipe_id` also accepts `custom_experiment`. Supply nonempty `recipe_name`, `viewer_mechanism`, and `evidence_status` (for example, proposed or trial). This opens the method library without granting visual approval. One, two or multiple looks follow the editorial purpose; weekly inventory is managed separately. Shared-world and generation evidence checks still apply.

- `weeks.source`: source ISO weeks; `weeks.content`: editorial content week; `weeks.delivery`: nullable delivery week. They may differ. Missing current planning-week records remain missing.
- `editorial`: audience, takeaway, visual_theme and selection_rationale. State what clothing information a viewer will see, then select the form.
- `presentation.layout_id`: `single_sequential`, `parallel_comparison`, `primary_detail`.
- `presentation.recipe_id`: six methods `sequential_lookbook`, `parallel_comparison`, `everyday_sequence`, `foreground_reveal`, `continuous_route`, `single_shot_performance`; two research methods `primary_detail_experiment`, `overhead_fan_transition_experiment`; or `custom_experiment` with the fields above. A valid ID does not certify this recipe as accepted or production-ready. Performance development is described in the shot choreography, not counted as another recipe.
- `models`: `{id, identity_asset_ids:[...]}`. `looks`: `{id, model_id, wardrobe_summary, source_asset_ids:[...]}`. No fixed look count is imposed by this per-film contract; the applicable production contract and series approval still govern it.
- `assets`: `{id, kind, path, sha256}`. Kinds used by the gate: `identity`, `still`, `frame_extract`, `source_clip`, `storyboard`, `previs`, `overhead`, `scene`, `space_plan`; source documents can use `source`. Existing file bytes are hashed. Missing files/hashes are incomplete; mismatches are errors.
- `approvals`: `{asset_id, scope, decision:"approved", target_sha256, receipt_path}`. Still/design scopes are `identity`, `still`, `storyboard`, `previs` or `overhead`; approved source clips retain their original scoped approval, e.g. `gait_and_join`. A receipt must be JSON with `{actor:"user", decision:"approved", scope, target_sha256, quote, recorded_at}`. Exact user words and genuine evidence must be recorded by the operator; the checker cannot authenticate them. Normalize genuine existing receipts to these fields with their original record link/quote; never ask again only because a format changed, or broaden approval scope.
- A genuinely new AI still requires its own `still` approval. A `frame_extract` instead records `lineage:{source_asset_id, source_sha256, frame_index, extracted_sha256}`; the source asset is `source_clip` with its known `frame_count`. Add `reuse_authority:{source_approval_scope, evidence_path, purpose}` pointing to the genuine instruction/decision authorizing the specific reuse. The checker verifies frame bounds, image/source hashes, the source's original user-approval receipt and reuse-evidence presence. **Do not fabricate a new extracted-still approval.** Exact extraction, scope applicability and actual evidence still need operator review; the checker does not decode the source video.
- `missing_assets`: human-readable unresolved needs; nonempty entries block the evidence gate. Deleting entries is not a substitute for resolving corresponding shot dependencies.

## Timing contract

`film.fps` is positive; `frame_count` is the final number of frames. Optional `duration_seconds` must equal `frame_count / fps` within 0.00001s. `native_speed:true` and `baked_text:false` remain explicit. Times use integer **global half-open frame intervals** `[start,end)`, so `[0,120)` contains 120 frames. Timed route boundary samples may include `end` as a geometric endpoint; this does not add a rendered frame.

Each shot needs:

```json
{
  "id": "S01", "look_ids": ["L01"], "frames": [0,120],
  "clothing_purpose": "Full silhouette and trouser width remain visible during forward walking",
  "clear_read_intervals": [[0,102]],
  "storyboard_asset_id": "board01", "previs_asset_id": null,
  "input_asset_ids": ["start01"], "scene_reference_asset_ids": [],
  "space_mode": "independent"
}
```

The next shot `[102,222)` overlaps for 18 frames (0.75s at 24fps). Its clear interval can be `[120,222)`. Record the exact transition:

```json
{"from_shot":"S01", "to_shot":"S02", "frames":[102,120], "overlap_frames":18, "method":"cross_dissolve"}
```

The checker verifies contiguous film coverage, ordered shots, no three-way overlap, exact neighboring overlap endpoints, and `sum(shot lengths) - sum(overlaps) = frame_count`. Clear clothing intervals must be within their shot, mutually disjoint, and outside all transition mixes. They represent planned readable clothing time; visibility/comfort still needs visual review. A deliberate cut is `[n,n)` with zero overlap and its own approved method; the schema does not authorize changing Mira's current transition preference.

Parallel panels or picture-in-picture are **one composited shot** with multiple `look_ids`. Their simultaneous layers do not become overlapping editorial shots. Describe panel actions in additional `panels` metadata if useful. There is no compositor in this tool.

### Reusing existing footage

Shots default to `execution_mode:"generate"` and need approved image inputs. Use `execution_mode:"reuse_clip"` for editing existing footage; it does not require inventing a new still input. List `panel_ids` (`["full"]` for a single image, e.g. `["left","right"]` for parallel), and `clip_inputs`:

```json
{"asset_id":"accepted_raw_A", "panel_id":"left", "source_frames":[0,144], "output_frames":[0,144],
 "reuse_authority":{"evidence_path":"source_reuse_record.json", "purpose":"Use the interval already covered by the approved film and its EDL."}}
```

The `source_clip` asset records actual `fps` and `frame_count`. The checker verifies source bounds, equal source/output durations at matching fps, full uninterrupted coverage of each planned panel, and absence of repeated raw intervals within a panel. This contract does not implement mixed-fps conforming, retiming, freezes or loops. Two 6s panels do not make an 8s film. Match the planned duration to usable footage or explicitly leave a missing-source need.

Reuse evidence can cite an accepted final film plus its EDL covering this exact source interval; it must not invent separate user approval of an entire raw clip. Evidence existence and declared metadata can be checked; real decoding, lineage and approval applicability need operator review. `ready_for_generation` is the legacy field name for all listed production prerequisites, including reuse-only editing; it never orders generation.

Simple stationary or split-screen films can use the line storyboard alone. `previs_asset_id` and its user approval are required for `shared_world`, `continuous_route`, or an explicitly set `previs_required:true`; when an optional previs is supplied as part of the chosen plan its scoped approval is also checked. This does not impose a new universal approval stop between routine steps.

## Shared-world route contract

Only shots whose choreography requires it use `space_mode:"shared_world"`; they also name `overhead_asset_id`. `continuous_route` requires at least one such shot. The plan stores **one** `space` object:

```json
{
  "id":"office_block_v1", "units":"schematic", "unit_note":"Relative schematic units; physical scale has not been measured.", "axes":"x_right_y_up_z_forward",
  "geometry":[{"id":"column_01","vertices":[[0,0,0],[0,3,0]]}],
  "routes":[{
    "shot_id":"S01",
    "character_samples":[{"frame":0,"position":[1,0,0],"heading_degrees":0,"gait_phase":"left support"}],
    "camera_samples":[{"frame":0,"position":[1,1.5,4],"target":[1,1.1,0],"vertical_fov_degrees":40}],
    "projected_samples":[{"frame":0,"person_center_uv":[0.5,0.5],"person_height_fraction":0.75,"visible_landmark_ids":["column_01"],"visible_clothing":"full outfit"}]
  }]
}
```

This abbreviated example shows one sample only; a valid route has **at least start/middle/end** control samples. Character, camera and projected samples must use exactly the same increasing global frame times and match the shot boundaries. Camera position and target are independent from character position/heading. Coordinates use `space.units`: choose `schematic` with an explicit unmeasured-scale note for sketches, or `metres` only when the scale is actually established. `person_center_uv` uses the top-left of the projected image as `(0,0)`, bottom-right `(1,1)`; intentional out-of-frame centers are permitted. `person_height_fraction` is projected person height divided by frame height. These sampled values must actually be derived/reviewed using the common space; the checker does not calculate the projection.

Export the exact `space` object into a separate JSON asset of kind `space_plan`; put its ID in `shared_space_asset_id`. The checker compares this source JSON with the current plan's `space`. Produce the overhead and camera-view previs from **that same source**. Both view assets need:

```json
"derived_from": {"asset_id":"common_space_source", "sha256":"SHA256 of the exact exported space JSON"}
```

This allows an edit to geometry/timing to invalidate older views and approval hashes. Shared-world generation is blocked if either view, common source, matching provenance, trajectory data, or exact user view approval is absent. A source checksum records the stated dependency; it cannot prove a renderer really followed it. Stable geometry, camera projection, no collision, no axis crossing, camera smoothness, gait, actual garment readability and visual comfort require synchronized visual review. No claim of millimetre-accurate Grok camera control follows from this plan.
