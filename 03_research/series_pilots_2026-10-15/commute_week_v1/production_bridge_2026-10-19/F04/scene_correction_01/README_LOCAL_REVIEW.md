# Scene-corrected F04 local tools

Prepared only; no new source inspection or video composition has run.

Future input is this folder's `F04_source.mp4`. Both commands require its exact new `--f04-sha`; the old `d83c6c18fa7d058c3eb3b374afad70db0a51cf0c561ba2c6bd4a255041d0bb50` source is explicitly rejected. Do not copy the old failed source into this folder.

Protected inputs are the exact accepted331-frame phase+1 three-shot prefix, original approved F04 start, and new approved background-corrected endpoint `F04_M03_L02_end_scene_correction_v3.png` SHA256 `fe97ba462401f7df3ef286a348853b65f54c51703980b402174c0a59ed605139`. Each command verifies these before and after its operation.

1. `inspect_F04_source.py --f04-sha <NEW_SOURCE_SHA>` exclusively creates `source_inspection_v1/`: full native decode/streams,25 full-frame/5 fixed-head checkpoints, dense first1.5s foot/ground and early/middle/late gait/turn windows. Review the actual background, crossing and gait before composition. These samples cannot approve normal-speed playback or site geometry.
2. After source review, `build_four_shot_review.py --f04-sha <SAME_NEW_SOURCE_SHA>` exclusively creates `four_shot_review_v1/`. It uses accepted prefix media unchanged through frame312, then prefix[313,331)↔newF04[0,18) for18 native frames/0.75s, then newF04[18,N). Earlier source joins are not rebuilt. Native720×1280/24fps, original speed, full raster, no text/audio/retime/crop/freeze/reverse/replay/interpolation. The output is re-encoded, not byte/pixel identical to the prefix.

For145-frame new source, the result is458 frames/19.083333s; actual count is measured. Receipt, frame mapping, full25 and all J34 transition frames±8 are saved. Borrowed algorithm and wrapper provenance are recorded separately in `scene_correction_execution.json`; no old code, source or delivery is overwritten. Existing/partial directories abort; choose a deliberate new `--version` only for a new justified operation. User visual approval of the new film remains pending after technical success.
