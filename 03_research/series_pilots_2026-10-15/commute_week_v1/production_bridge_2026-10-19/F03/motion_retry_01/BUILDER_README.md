# F03 same-input motion retry tools

Prepared 2026-10-20. No video generation or media processing was run while preparing these tools.

Place the downloaded retry at `F03_source.mp4` in this folder, compute its exact SHA256, then run `inspect_retry_source.py --f03-sha <exact_sha>`. The script verifies the hash and creates exclusive `QA_source/` and `technical_scan.json` outputs. Full/native samples, dense first-1.5-second foot windows and early/mid/late windows are for visual inspection only; they do not grant a gait or normal-speed playback pass.

After inspecting the exact retry source, run `build_review_after_retry.py --f03-sha <exact_sha>`. It imports `../build_three_shot_review.py` and overrides only `HERE` and `F03`. Original F01, accepted corrected F02, protected accepted pair, hashes and source ranges remain unchanged. No source crop, retiming, freezes, text or audio is introduced. Both joins retain 18 frames / 0.75 seconds at native 24fps. If F03 has 145 frames, output has 332 frames / 13.8333 seconds.

The default output is exclusive `three_shot_review_v1/` in this retry folder. Existing or partial output causes failure; use a new `--version v2` only if another reviewed build is justified. The underlying builder re-encodes the native sources; it does not claim encoded pixels match the accepted pair. Its receipt records the established builder's own path/hash. No historical source, preview, approval or delivery is overwritten.

Run both scripts using the bundled Python runtime. The exact `--f03-sha` is mandatory for each command. The build remains a research candidate until separate source/join review and user feedback.
