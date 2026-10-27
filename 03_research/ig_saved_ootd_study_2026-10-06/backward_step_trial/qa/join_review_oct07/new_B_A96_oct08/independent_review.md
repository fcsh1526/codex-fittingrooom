# Independent native join inspection — A96 + matched B

Date: 2026-10-08. This is a QA-only A/B linear-blend inspection, not a rendered film or a normal-speed full watch. No source/status/approved film was modified.

## Decision

**Reject this A96 join as the next review candidate.** Matching the new B starting still reduced the prior gross vertical head-placement difference, but the actual 18-frame overlap still produces visible double eyes/mouth, double hands and two sets of legs/shoes. It is insufficient to present this join as resolved or passed. The new B remains separately usable for a better actual native-frame selection, subject to its recorded source-review limits.

## Exact tested mapping

- A: retained near-start retreat, SHA256 `be49906fa1ec7397bb456acc1ce7947325e71b4ce5a0692d7235d878ad6017ea`.
- B: new matched-start approach attempt01, SHA256 `ee829f278e30de0a0e0db1d8aa8bc11d258c50a8475044d5320e1cdae07673c8`.
- Each source hash checked before and after reading; both native 720×1280 / 24fps.
- A selection budget `[0,96)`, B would start at0. Tested18 native pairs A78–95 with B0–17, alpha `(k+1)/18`, equivalent to output78–95. The helper generated inspection PNGs/boards only; no MP4.

## Evidence viewed

- All18 paired head/shoulder rows in `paired_head_01_06.jpg`, `paired_head_07_12.jpg`, `paired_head_13_18.jpg`.
- All18 paired full-image rows in `paired_full_01_06.jpg`, `paired_full_07_12.jpg`, `paired_full_13_18.jpg`.
- All18 paired lower-body rows in `paired_lower_01_06.jpg`, `paired_lower_07_12.jpg`, `paired_lower_13_18.jpg`.
- Native full blend `transition_native_full/output_000086_A86_B8.png` at original720×1280 detail: exact50/50 composition.
- `qa_receipt.json` mapping/hash receipt. There was no continuous playback or encode/decode inspection of a film, because this review intentionally did not make one.

## Findings

The centre of the transition, particularly output84–90, shows vertically displaced face details. At86 the eyes/mouth do not register into one face; instead they form a soft duplicated face. Head-top closeness alone did not align the eyes, chin and shoulders as A continues stepping backward.

The lower-body mismatch is larger. At the50/50 native blend, A's moving front lace-up shoe and lower calf extend well below B's stationary early cream slip-ons. Two differently placed leg/shoe sets are clearly visible through the two dress hems. The bag-holding hand and free arm also leave separate displaced outlines. These are expected consequences of blending differently scaled poses; their cause does not make the resulting join visually passed.

The major room geometry is much closer than the person. Window, bench, table and right bookshelf do not show a comparable large gross shift in the inspected pairs/native middle blend. Fine floor/book/leaf details are not pixel-registered, and slight generative-detail differences remain possible. This is not a finding of perfect background retention; the clear rejection here is driven by the duplicated person.

New B remains nearly still through its first0.75 seconds, whereas A continues retreating through the tested window. A f96 was used to design B but lies outside the current A `[0,96)` selection; much of the actual blend sees earlier, larger A positions. Thus the static approval and original A-f96 matching did not certify the moving window. A later real A tail is a reasonable next diagnostic to compare; no result for A102/A90 or another selection is inferred here.

No changes to character speed/action, crop, alpha duration, text, audio, original five first-wave videos, Drive or publication were made.
