# F04 local inspection and append tools

Prepared 2026-10-20. These tools do not generate media, use a browser, upload, publish or grant visual approval. Source inspection and four-shot composition have **not** been executed at preparation time.

## Exact inputs and protections

- Future motion input: `F04_source.mp4`; its exact lowercase SHA256 is a mandatory argument for both commands.
- Accepted picture input: `../F03/phase_match_review_v1/F01_F02_F03_phase_plus1_native_soft_review_v1.mp4`, SHA256 `f36b079261d6ba43bc1bf17f9504b4a1424efc393c24e5d53d9f4075165eaa33`, 331 frames,720×1280,24fps,13.791667s,silent.
- Approved starting and corrected ending stills are verified by their known SHA256 before and after each command. They are never modified.
- The accepted prefix is used as decoded media input. Earlier source films and earlier join/phase mathematics are **not recomposed**. The new output is re-encoded, so compressed bytes/pixels are not guaranteed identical.

## Procedure

1. Root operator downloads one actual F04 source into this folder and records its actual hash.
2. Run `inspect_F04_source.py --f04-sha <EXACT_SHA>`. This exclusively creates `source_inspection_v1/` containing a complete technical decode, stream inventory,25 full-frame checkpoints,5 fixed head windows, first1.5s foot/ground windows every0.125s, and early/middle/late full-frame gait/turn samples. Head/foot crops are inspection-only.
3. Inspect source/site/gait and normal-speed playback separately. The extractor does not declare a visual pass. If source is usable, run `build_four_shot_review.py --f04-sha <SAME_EXACT_SHA>`.
4. This exclusively creates `four_shot_review_v1/`, a silent four-shot candidate, detailed receipt and per-frame input mapping, full25 checkpoints, and J34's complete18 transition frames plus8 frames on either side.
5. Check source, new join and whole film; request exact user video feedback. Stills approval and technical decode are not video approval. F05 is not automatically authorized by technical success.

Both scripts require native unrotated720×1280,24fps and reject existing output directories. Use a deliberate `--version v2` only for a genuinely new reviewed need; preserve partial failures and history.

## Composition

`prefix[0,313)` → 18-frame linear dissolve of `prefix[313,331)` with `F04[0,18)` → `F04[18,N)`.

The outgoing segment corresponds to original F03 `[127,145)`. J34 output is frames `[313,331)` /13.041667–13.791667s. Incoming alpha is `(overlap_index+1)/18`,index0..17. No other frame/order/phase changes are introduced. Native full raster, original speed,0.75s join,no text/audio/retime/crop/freeze/reverse/replay/interpolation.

For a145-frame F04, result is `331+145−18=458` frames /19.083333s. Actual count is measured, not assumed. No files in Drive or earlier deliveries are changed.
