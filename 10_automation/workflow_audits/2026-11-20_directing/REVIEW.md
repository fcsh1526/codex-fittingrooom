# W47 M01｜把同一個穿搭問題從分鏡帶到剪輯台

本次用既有成片回驗新版導演流程，另用原素材四格做了一次定時分鏡。W47 的製作版本仍以 11/19 的 v3 與後續使用者回饋為準。

## 成片回答了什麼

原企劃要講「她遇到冷風，所以把衣領拉高」。拉鍊操作曾因細節錯誤退回，後續以閉領首圖生成獨立片段。v1 的全身段被指出撞上玻璃；v2 的第二鏡又被指出縮放不佳。v3 剪去該段前 36 格。這三項意見分別涉及手與物件、人物與空間、觀眾注意力如何跨景別移動。[原企劃](../../runs/2026-W47/publishing_structure.md) · [拉鍊回饋](../../runs/2026-W47/reels/M01/S01_trial_01/REVIEW.md) · [v1 剪輯表](../../runs/2026-W47/reels/M01/full_edit_v1/REVIEW.md) · [版本紀錄](../../../CURRENT_STATUS.md)

| v3 成片格，24 fps | 畫面可見 | 導演判讀 |
|---|---|---|
| 0–33 | 一手在開領附近，內搭可見，視線移動 | 建立第一種領形，也容易引起「她要拉上嗎」的期待。 |
| 34–69 | 直接切到已閉領的全身，她抬手招呼再放下 | 雙鞋與全身比例可讀。動作最醒目之處在舉手，領口的變化發生在切點之外。 |
| 70–111 | 一左一右呈現敞開與立起的領口 | 兌現兩種輪廓的比較。若剪輯仍把核心寫成「看她如何拉上」，這個答案缺了一拍。 |

本次重新解碼 v3（本機素材 `../../runs/2026-W47/reels/M01/full_edit_v3/M01_W47_v3.mp4`），核到 720×1280、24 fps、112 格，並查看既有逐格圖。上述為影格觀察與剪輯判讀；v3 的整體觀感仍待使用者回饋。前 56 格（本機素材 `../../runs/2026-W47/reels/M01/full_edit_v3/qa_01.jpg`） · 後 56 格（本機素材 `../../runs/2026-W47/reels/M01/full_edit_v3/qa_02.jpg`）

W46 的正例提供了另一個判準。黑鞋版刪去重複鞋面及末段回望，讓出三秒給同雙黑鞋配褲與裙的比較；這個精確成片有使用者接受收據。W47 可以借的是「讓結尾回答這支片自己的問題」。兩片同樣使用並排，前面需要累積的期待各自不同。[W46 剪輯表](../../runs/2026-W46/reels/M01/comparison_ending_black_shoes_v3/REVIEW.md) · [W46 成片接受收據](../../runs/2026-W46/reels/M01/comparison_ending_black_shoes_v3/user_full_film_acceptance_2026-11-12.json)

## 一次可看的分鏡試排

這版先試「同件外套開領和立領，臉旁的線條差在哪裡？」。沿用 slow.and 用同件衣服比較穿法的思路；風吹時的小反應接到同景別的閉領，讓注意力留在下顎與領緣。syuan_ord 提供了另一種人物調度參考：視線先側移，再回到鏡頭。本片只取「先決定她在看哪裡」這個導演問題。[IG 觀察](../../../03_research/ig_reference_pair_2026-11-20/REVIEW.md)

| 預演格 起,迄) | 原片取樣 | 看點與切點 |
|---|---|---|
| [0,16) | wind 第 0 格 | 開領，內搭亮色三角清楚；手在門襟旁。 |
| [16,38) | wind 第 24 格 | 同一機位出現迎風側傾，肩線與門襟仍在同一畫面。此格有動態模糊，適合標記反應，動態是否保留須以原速選段。 |
| [38,70) | 閉領來源第 32 格 | 硬切到已閉合的穩定中景，讓視線有時間從臉移到立領。這一切是狀態比較，省略了閉合過程。 |
| [70,110) | v3 第 94 格 | 左右同看開領內搭與立領高度，直接收尾。 |

[播放 4.58 秒定時分鏡（本機素材 `collar_board.mp4`） · [可調整各拍長度的清單](board.json)。四格均取自現有素材；這輪只比較構圖、順序和閱讀時間。第二拍的髮絲、第三拍的手位跳變、並排在手機上的讀衣時間，要在動態粗剪核對。若主題改回實際扣合手法，分鏡與素材需求須重新計算。

## 如何重跑

在專案根目錄執行以下命令；輸出參數選一個新檔名。一般環境可使用 Python 3 及 PATH 上的 FFmpeg。本機的直式輸出完整解碼為 110 格、24 fps、360×640。

```powershell
& 'openmontage/.venv/Scripts/python.exe' '11_skills/mira-reel-director/scripts/animatic.py' '10_automation/workflow_audits/2026-11-20_directing/board.json' '10_automation/workflow_audits/2026-11-20_directing/collar_timing_alternative.mp4' --ffmpeg 'openmontage/.local/bin/ffmpeg.exe'
```

本機 OpenMontage 來源為 fcsh1526/openmontage 的 `08e2151fa02de28a5d6a312b3d575692bf147ad7`。本輪逐項讀了 cinematic 的 script、scene、asset 與 edit director，將節拍、關鍵畫面、可用來源與剪輯決定接入 Mira 的同一張工作表。先前實際採樣使用 FrameSampler，並已有多支剪輯腳本使用本機 FFmpeg；新版新增的是導演到剪輯的交接及可播放的分鏡。上游 Backlot 的階段簽核和 API 生成服務有各自的執行條件，本次沒有啟動。[先前評估](../../../03_research/openmontage_assessment_2026-11-02/ASSESSMENT.md) · [既有採樣腳本](../../../03_research/ig_reference_Db8AXqwpkef_2026-11-02/sample_reference.py) · [版本對應的導演文件](https://github.com/fcsh1526/openmontage/tree/08e2151fa02de28a5d6a312b3d575692bf147ad7/skills/pipelines/cinematic)
