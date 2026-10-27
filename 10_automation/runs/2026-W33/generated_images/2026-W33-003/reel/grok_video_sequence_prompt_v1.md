# W33-003 Grok Imagine Video 1.5 Reel Package

## Production decision

- Final Reel: about 15 seconds, native 9:16.
- Generate three separate 6-second image-to-video clips and trim their strongest sections into one Reel.
- Each clip has one clear everyday action. Do not ask one generation to perform the whole story.
- Use Grok Imagine Video 1.5 / current Custom image-to-video mode.
- Generate one version of each clip. If a clip has a hard continuity or anatomy defect, rerun the same prompt once without changing the creative direction.
- Do not use any previously rejected generated video as an input.

This structure follows xAI's current guidance: provide a starting frame and describe the subject motion, camera movement, pacing, and sound; the model is also intended for shot sequences.

## Clip A — approach the magazine stall

Source image:

`2026-W33-003_M01_reel_candidate_A_refined_v2.png`

Grok settings:

- Duration: 6 seconds
- Aspect ratio: preserve source 9:16
- Resolution: highest available

Paste this prompt:

```text
她立刻從背心口袋取出深棕色皮夾，朝右側的刊物攤位自然走近一步，停下來看著桌上的刊物。胸口高度的輕微手持跟拍，裙襬、背心與髮絲隨步伐自然晃動，背景逛市集的人持續走動。保持原圖人物、身材比例、服裝、鞋子與場景，不看鏡頭，沒有對白。
```

Required result:

- Motion begins during the first half-second.
- The complete outfit remains visible from hairstyle to both sandals.
- The wallet comes fully out of the pocket and keeps the same size and color.
- Use only the first 4–5 clean seconds in the final edit.

## Clip B — browse one magazine

Source image:

`2026-W33-003_M01_reel_candidate_B.png`

Grok settings:

- Duration: 6 seconds
- Aspect ratio: preserve source 9:16
- Resolution: highest available

Paste this prompt:

```text
她用左手把架上的一本刊物輕輕抽出一點，低頭看封面，右手自然拿著深棕色皮夾。胸口高度的固定手持鏡頭，只有很輕的呼吸感，背景訪客自然走動。保持原圖人物、身材比例、服裝、鞋子、刊物攤位與夏日光線，不看鏡頭，沒有擺拍或對白。
```

Required result:

- One continuous hand action; no page flipping.
- The magazine slides only a few centimeters.
- Both hands stay anatomically stable and the wallet does not change shape.
- Use about 5 clean seconds in the final edit.

## Clip C — garment and pocket detail

Source image:

`2026-W33-003_M01_reel_candidate_C.png`

Grok settings:

- Duration: 6 seconds
- Aspect ratio: preserve source 9:16
- Resolution: highest available

Paste this prompt:

```text
她低頭看手上的薄刊物，幾秒後把刊物稍微放低，右手仍自然拿著深棕色皮夾。鏡頭非常緩慢地推近背心口袋、皮夾與刊物，保留她的臉和雙手；背心布料、髮絲與呼吸只有自然微動。保持原圖人物、服裝、物件和市集場景一致，沒有對白。
```

Required result:

- The slow push-in must not crop out her face or hands.
- The vest keeps four patch pockets, the same buttons, seams, color, and canvas texture.
- No finger duplication, magazine morphing, or wallet redesign.
- Use the strongest 5–6 seconds as the closing detail shot.

## Final 15-second edit

Use hard cuts, not dissolves or morph transitions.

| Final time | Source | Purpose |
| --- | --- | --- |
| 0.0–4.3 s | Clip A | Immediate movement and full outfit |
| 4.3–9.2 s | Clip B | Real-life interaction with the stall |
| 9.2–15.0 s | Clip C | Utility-vest construction and tactile detail |

Trim each source at the first stable moving frame. If an ending contains face, hand, garment, or background drift, cut before the drift rather than slowing or freezing the bad frame.

## On-screen title

Use only during approximately 0.0–1.8 seconds:

```text
機能背心，也能穿得很輕
```

Placement:

- Upper-left safe area, below the Instagram interface zone.
- Two short lines if needed.
- Small off-white editorial type with a restrained dark shadow.
- Do not cover her face, vest, hands, wallet, or the main outfit silhouette.

## Audio

- No generated dialogue.
- Keep one continuous low market-room ambience across the whole edit, or mute all three generated tracks and add one IG music track at low volume.
- Do not reuse three different generated ambience beds across the cuts.
- Do not automatically reuse `Good Morning`; choose the music separately at publishing time.

## Caption

```text
機能背心容易穿得太厚重，內搭換成黑色無袖長洋裝，保留層次，也更適合夏天。

你會搭洋裝，還是西裝褲？
```

## Cover

- Use Hero A, not the close detail frame.
- Keep the full outfit readable in the profile grid crop.
- Cover title: `機能背心的夏日穿法`

## Final rejection checks

Reject and regenerate only the defective clip when any of these occur:

- No meaningful motion in the first half-second.
- Face, hairstyle, apparent age, body build, outfit, sandals, wallet, or market scene changes.
- Fashion-elongated legs, sliding feet, broken balance, missing contact shadows, or camera-wide-angle distortion.
- Extra or merged fingers, hand size changes, wallet morphing, magazine bending unnaturally, or pocket construction changes.
- Runway posing, camera-facing performance, dramatic hair flip, large head turn, fast zoom, orbit, speed ramp, scene change, text, logo, or watermark.

