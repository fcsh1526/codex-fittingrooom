---
name: mira-reel-director
description: >-
  Plan and direct Mira fashion Reels from a viewer purpose into connected line storyboards,
  shared-scene character and camera routes, synchronized previs, source-image requirements,
  and shot/join/full-film review. Use for Mira Reel formats, storyboards, route design,
  production planning or continuity repair. Pair with mira-image-daily for actual still work.
---

# Mira Reel Director

For new films and re-edits, follow [從分鏡到剪輯台](references/directing-to-edit.md). Use the same directing sheet through the timed storyboard, camera blocking, footage selection and rough cut. If the pivotal action fails, revisit what the audience is waiting for before choosing coverage. Use the current film's existing approval scope.

2026-11-11 接續 Reel 前，先核對整片的多個鏡頭是否有不同看點、活潑人物反應及明快節拍，並逐項寫出「停下來、繼續看、記住我們」。六種既有剪輯方法都可按內容選用及組合，左右並排已恢復可選。交接需列整片時間軸、各鏡觀看功能、已具備與缺少素材、未兌現的期待及有效核准範圍。使用者對片段自然度的確認只記在該範圍，整片趣味另行檢查。

Turn a clothing story into a reviewable film design before spending on generated footage.
This skill coordinates production; it does not give a video engine deterministic camera control.

## Project entry

For a cloud checkout or a new production environment, begin with
`10_automation/CLOUD_HANDOFF.md`. It connects the six methods, motivated performance,
IG observations and camera-route experience to their project sources. Read the repo
skill directly when it is absent from the environment's installed-skill catalog.

Find the Mira project by `10_automation/CANONICAL_WORKFLOW.md`, starting from the active workspace.
Read that file, `CURRENT_STATUS.md`, the relevant content week's `publishing_structure.md`,
then `10_automation/MIRA_EDITORIAL_HANDOFF.md`. Read `09_sops/mira_reel_production_sop.md`
for current video rules. A missing current week is not permission to create a new batch.
Repository references below are relative to that project root, even when this skill is installed elsewhere.

For still planning/generation/review, also apply `mira-image-daily`; current user decisions and the
canonical workflow govern explicit series exceptions. Do not force the approved five-look pilot
back into two looks or generalize its count to every film. For copy, read the caption SOP.

## Choose the work

- **Editorial authority:** viewer purpose comes before look count, performance and camera design. A film may feature one, two or multiple looks; weekly outfit inventory is separate. The user confirmed six editing methods and two research candidates on 2026-11-06; use the current catalog, which remains open. Do not make continuous walking or complex camera curves a default.
- **Performance within the method (2026-11-06):** optimize actions, gaze, expressions and emotional development within the selected method. Richer split-screen acting remains parallel comparison. Method choice alone does not improve performance; purposeful larger actions are allowed, and natural does not mean tiny movement. Read the performance reference below for planning and selection criteria. Comparing every new film with accepted footage is not a mandatory gate.
- **Research alongside production:** read [research-and-production.md](references/research-and-production.md). Keep an executable film moving while inspecting a bounded set of IG references; do not wait for a complete method library. Record observations separately from hypotheses and tested Mira results.
- **Motivated performance and video references:** read [performance-and-reference.md](references/performance-and-reference.md) for natural expressions/actions, reference interpretation or prompt comparisons. Separate tool extraction, visible actions and inferred motives. Try concise context plus key reactions; allow coherent variants and distinguish one-pair preference from repeatability or publication approval. Reconcile the exact current version before resuming a historical pending item.

- **Inventory or format selection:** read `09_sops/mira_reel_method_catalog.md`. Keep layout,
  editorial recipe, camera movement and character action separate. New clothes or a reordered
  cut are not a new format. Exact accepted examples are evidence, not proof of repeatability or reach.
- **New film planning:** read [production-system.md](references/production-system.md), then
  [plan-contract.md](references/plan-contract.md). Use the template and validation helper described there.
- **Continuous travel, orbiting or shared locations:** also read [route-previs.md](references/route-previs.md).
  Both paths and the camera view must use one scene and clock. Simple stationary/split-screen films
  can use ordinary line boards without a spatial route model.
- **Repair:** first locate the exact rejected shot/join and feedback. Preserve the accepted film,
  change the necessary source or design only, and review both adjacent joins in full context.

## Directing sequence

For new production and continuity repair, apply [production-checkpoints.md](references/production-checkpoints.md): viewer hook and motivated performance, actual-layout scale checks, join-first trials, bounded retries, timed occlusion, honest review states and complete handoff. Current explicit user authorization governs approval scope; do not repeatedly request already-waived routine approvals.

1. Write what the viewer can see and take away. Connect it to the actual outfit relationships and
   occasion. “Magazine-like” is an aesthetic; it is not the viewer takeaway. Select a recipe for that
   purpose, not to consume available images. Separate sourced trend facts from editorial combinations.
2. Establish the film-wide visual theme and a connected line board. Each shot needs a clothing
   information goal, action start/end, framing, clear reading interval and neighboring join.
   Mark proposed choices as proposals. Reuse already accepted decisions without asking again.
3. For shared-space movement, validate geometry and synchronized projected views before deriving
   images. If the preview does not show the written camera move, repair the preview; do not count
   the accompanying text as visual verification. Keep the shot clock independent of generation lengths.
4. Derive only the missing first/middle/end views and identity/outfit references. Review new AI stills
   with the user before they enter motion generation. Existing video-frame reuse needs source/frame
   lineage, not invented new-still approval. A still's approval does not approve a new camera path or motion.
   When existing footage already serves the shot, use `execution_mode: reuse_clip` with exact source
   intervals and panel coverage. Do not create new stills or stretch a six-second source to meet an
   eight-second plan; expose the footage shortage or propose the shorter valid edit.
5. Check actual tool controls at execution time. Record requested, UI-available, submitted and observed
   settings separately. Use the existing Mira Grok canvas when operating Grok; one bounded shot request
   with approved inputs. If a planned movement is unsupported, simplify the plan or test a short bridge;
   do not send invisible route/video parameters or claim references were selected without evidence.
6. Compare actual output to the planned key views, then review single-shot stability, the full overlap
   of adjacent shots, and the full film at native speed. Schema or frame-difference checks cannot certify
   appeal, comfort, physical foot contact or identity. Record what was actually watched versus sampled.
7. Save the approved recipe with exact source intervals, settings, limitations and scoped feedback.
   Link delivery and actual posting/metrics separately; follow existing delivery authority and SOP.

## Current Mira defaults and failure handling

- No baked text in the video or cover. Keep a native-speed clean master. Optional IG text is delivered
  separately for the user to add. Do not add text to rescue an unclear film purpose.
- Around 0.75 s dissolve remains the comparison baseline for changes. The latest commute film is
  approved for publication **with unresolved uncomfortable ghosting/flicker**. First fix scale, phase,
  pose, motion and light mismatch. A longer dissolve is not a generic repair; propose and visually
  compare any changed transition approach instead of silently replacing the user's preference.
- A planned close-up/soft background can be legitimate; cropping feet or blurring a failed source
  afterward does not prove that its geometry/gait was fixed. No retiming/freezes/duplicate frames to
  disguise bad motion. The faster gait request belongs to the commute film, not all series.
- If a bounded trial fails, classify whether editorial intent, spatial design, source image, engine
  adherence or edit timing caused the failure. Follow the SOP's retry bound. Repeatedly adding negative
  prompts without changing the failed constraint is not a production strategy.
- Keep the film plan as the current record and the actual EDL/QA as observed evidence. On source or
  timing changes, invalidate dependent neighboring joins and derived views; preserve historical approvals.
  Update the compact handoff with the next actionable step, not every transient browser state.

The skill package is versioned in `11_skills/mira-reel-director/`. A locally installed copy should match
it; installing or loading a skill does not publish media or synchronize new files to GitHub.
