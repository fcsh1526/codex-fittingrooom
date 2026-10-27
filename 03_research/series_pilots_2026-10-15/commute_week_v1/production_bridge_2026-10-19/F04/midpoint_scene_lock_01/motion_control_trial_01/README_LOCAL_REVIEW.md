# Midpoint-controlled F04 local tools

Tools only: no source inspection or composition performed at preparation time. Grok's requested image roles/settings still need separate evidence; these helpers do not prove generator controls were available or used.

Expected new source is this folder's `F04_source.mp4`. Both scripts require exact `--f04-sha` and reject both prior failed source hashes: `d83c6c18fa7d058c3eb3b374afad70db0a51cf0c561ba2c6bd4a255041d0bb50` and `25252192b6ce6052d88bd645fba47496246be59b23c953e5b3ad68f29ef11739`.

Before and after each operation, verify the accepted331-frame prefix SHA `f36b079261d6ba43bc1bf17f9504b4a1424efc393c24e5d53d9f4075165eaa33`, original start SHA `98687eb8365828d67850ddc03d57e48d9d28ad4628f9f62c727bcb166e002457`, approved midpoint SHA `25606eaac1e1bbd7f8e53873de07d2a2b99c87ace88924f1917cd94dae55175b`, and newly approved end SHA `c7ceec64741262645fd5a59339d5cece3162fe8d928f7a0e0dd7521ace1b0d14`.

1. Run `inspect_F04_source.py --f04-sha <NEW_SHA>` after a new source download. Exclusive `source_inspection_v1/` contains actual full decode/streams,25 full/5 fixed-head samples and dense early/middle/late gait/turn windows. Inspect crossing topology, background, feet, bag and face; samples do not replace normal-speed full playback.
2. Only after root source review, run `build_four_shot_review.py --f04-sha <SAME_NEW_SHA>`. Exclusive `four_shot_review_v1/` uses accepted prefix[0,313),18-frame linear dissolve of prefix[313,331)↔F04[0,18),thenF04[18,N). Earlier joins are not reconstructed. Native720×1280/24fps/full raster/original speed/no text/audio/crop/retime/freeze/reverse/replay/interpolation. Output is re-encoded, not byte/pixel identical to prefix.
3. For145-frame source expect458 frames/19.083333s; actual count is measured. Receipt, mapping, full25 and all J34 boundary frames±8 are saved. Technical checks never grant film approval or publishing authority.

Every wrapper saves `motion_control_execution.json` with exact source/protected inputs and wrapper/borrowed-helper hashes. Old files remain untouched. Existing/partial output directories abort; use a deliberate new `--version v2` only for a justified new operation.
