# Geometry-reset F04 source inspection

Prepared 2026-10-20. The tools have not generated, decoded or combined any new media during preparation.

Save the single new Grok result as `F04_source.mp4` in this folder. Compute its exact lowercase SHA256, then run this folder's `inspect_F04_source.py --f04-sha <exact_sha>` using the bundled Python runtime. `--version v1` is the default and allocates a new exclusive `source_inspection_v1/`; existing or partial inspection output is never overwritten.

The wrapper reuses the established F04 inspector for metadata, stream inventory, full native decode,25 whole-source samples,5 fixed head windows and dense early/middle/late gait windows. It adds native full-frame and QA-only foot/road windows every2 frames through2.5–3.5 seconds and4–5 seconds. These crops never enter footage. `dense_road_gait_windows.json` records exact native indices; `technical_scan.json` and `motion_control_execution.json` preserve source/protected-input hashes, settings limits and pending visual QA.

Protected inputs, verified before and after inspection:

- Accepted331-frame three-shot prefix: `F03/phase_match_review_v1/F01_F02_F03_phase_plus1_native_soft_review_v1.mp4`, SHA`f36b079261d6ba43bc1bf17f9504b4a1424efc393c24e5d53d9f4075165eaa33`.
- Original F04 approved start: `F04/F04_M03_L02_start_candidate_A.png`, SHA`98687eb8365828d67850ddc03d57e48d9d28ad4628f9f62c727bcb166e002457`.
- New approved midpoint v3: `photographic_midpoint_01/F04_M03_L02_mid_camera_no_planter_v3.png`, SHA`0a4fe3eb96bf2473cb441844e770ec1ed391718eceb997bcf38b50a886b5b22f`.
- New approved endpoint v2: `photographic_endpoint_01/F04_M03_L02_end_camera_correction_v2.png`, SHA`e3117eef0d3854bb279d2070a08378b9eefacbabeae0889c057cbcf75e52e8e9`.

The three prior failed source hashes beginning`d83c6c18`, `25252192`, `619053fe` are explicitly rejected. This context deliberately provides no composite-build function. No four-shot film, source edits, generation, automatic gait/scene pass, normal-speed playback claim, publishing or Drive changes are performed.
