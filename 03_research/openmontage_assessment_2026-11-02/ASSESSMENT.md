# OpenMontage 對 Mira 的適用性評估

評估日：2026-11-02。以本機 openmontage commit `08e2151fa02de28a5d6a312b3d575692bf147ad7` 為依據。GitHub網頁讀取失敗，未宣稱與遠端最新版本一致。本次只有文件／程式碼閱讀及能力查詢，沒有採用新製作管線、生成媒體、下載模型、修改依賴、變更已核准影片或執行付費生成。

## Mira 的現況與優先順序

- M02重做11秒版已由使用者核准可發布，特別肯定第二鏡細緻活潑的動作；舊柱面M02仍廢棄。
- M01活潑v1在預覽第2秒左右因轉身手部飄移被否決；v2錯開轉肩與手勢，仍待使用者觀看，不能寫成通過。
- M01／M02曾出現人物尺度不一致；M05遮鏡停留太長，已按使用者意見縮短。這些需要前置構圖和動態審查，不能只靠提示詞補負面要求。
- 因此優先為：人物表演拆解與原速動態QA，其次接點連續性，再其次企劃執行紀錄與生成提示詞。一般剪裁／拼接已可做，換剪輯引擎不是當前最大瓶頸。
- 本輪讀到的CURRENT_STATUS與跨週入口部分仍為歷史狀態；M01_TRIAL已有v2，但跨週入口仍有尚未生成描述。適合借用結構化版本／狀態紀錄，但看板必須讀到正確來源才有用。
- 今日為W45，W45 publishing_structure.md不存在。本輪評估延續W44現有素材，不另建W45生產或誤稱W44是本週新企劃。

## 值得借用的方法與實作依據

| 問題 | 文件／實作 | 對Mira的用途 | 證據層級 |
|---|---|---|---|
| 表演提示過長而動作時序不清 | `skills/creative/video-gen-prompting.md`、`skills/pipelines/cinematic/scene-director.md`、`asset-director.md` | 五面向：人物、人物動作、場景、空間構圖、相機；寫清動作先後，再做草稿→批評→修訂並記錄。M01應明確分開轉肩和抬手 | 已讀文件；對Mira生成改善尚未實測 |
| 參考片僅看氣氛，難以複製有效機制 | `skills/meta/video-reference-analyst.md`、`tools/analysis/video_analyzer.py`、`frame_sampler.py` | 分開記錄內容、節奏、結構、動作、構圖與鏡頭；把M02已接受第二鏡當表演參考，保留動機而非複製全部姿勢 | 文件及程式碼已讀；分析流程未對Mira執行 |
| 靜態檢查誤作動態通過 | `tools/analysis/visual_qa.py`、`skills/meta/reviewer.md` | 用probe確認格式，密集抽手部／接點，再由助理或人觀看原速全片；缺陷必附影格、時間、修正方案 | 可用性查詢通過；無新增影片QA實測 |
| 版本／核准／退件資訊互相覆蓋 | `lib/checkpoint.py`、`schemas/artifacts/source_media_review.schema.json`、`asset_manifest.schema.json`、`edit_decisions.schema.json`、`AGENT_GUIDE.md` decision_log規則、`backlot/state.py` | 保存歷史checkpoint、精確來源區間、有效版／退件版；決策採追加紀錄；看板作觀察介面 | 已檢查實作；未建立Mira看板專案 |
| 遮擋過長、節奏平淡 | `skills/pipelines/cinematic/edit-director.md`、`tools/video/video_trimmer.py`、`video_stitch.py` | 按衣服清楚可讀與情緒節點剪裁，保護M02有效表演，M05遮鏡按實際時段縮短 | 剪輯工具狀態可用；未使用它重剪 |
| 重試與生成成本不可追蹤 | `tools/cost_tracker.py`、`AGENT_GUIDE.md` | estimate→reserve→reconcile；每支記生成次數、傳輸等待、可用秒數、費用及失敗原因 | 有實作；不代表過去Grok網頁費用可自動回填，未知值須保留未知 |

## 不能直接照搬的地方

1. `reviewer.md` 第87行：兩輪仍有critical時PASS_WITH_WARNINGS。Mira的手部飄移、換臉、混衣等實質缺陷不能因此升為可發布；兩次失敗後改設計或轉研究，使用者的精確核准仍有效。
2. `visual_qa.py` 的實際operations只有review／probe／audio_levels。雖模組說明提到遮擋和轉場，實作未提供手腕、腳掌、身份或時序連續性自動判斷。`validation_passed`只是期望格式的比對；`success=True`也不代表畫面可用。
3. `visual_qa.py` 第168–169行以時間四捨五入至一位小數命名抽幀，24fps密集時間可能同名覆寫。最小測試應用`frame_sampler`的timestamps策略（序號檔名）與獨立輸出目錄，核對張數，不能直接用visual_qa做逐幀採樣。
4. `video_analyzer.py` 以少數光流樣本判斷motion_clip／animated_still／static_image，是啟發式，不會識別AI來源或證明步態合理。`_suggest_pipeline`會把Instagram等短片直接推薦animation；Mira仍應依真人時裝素材與目的選擇。
5. `video_understand.py` quality模式只是模糊、亮度、對比；describe／qa會載入CLIP／BLIP2／LLaVA等權重。模型套件或可下載不等於能可靠偵測手部漂移，亦不可把抽幀分析寫成已完整看過影片。
6. `face_tracker`是臉框／裁切輔助，沒有完整身體尺度、手部或步態檢測。自動追臉裁切可能裁掉鞋和裙襬，須保留Mira全身閱讀需求。
7. `character_animation.py`和`.agents/skills/character-animation-qa`針對可編輯SVG／rig／動作時間線；可借概念做示意預演，不能當作修理已生成寫真人物手部的方法。Three.js／GSAP曲線也不會自動成為Grok可執行的攝影軌道。
8. `grok_video.py`走xAI API而非已登入的Grok網頁，另需API憑證與計費；它的image/reference輸入不等於原畫布代理所有first／last／keyframe控制都相同。其他模型的提示長度與能力不可直接套用。
9. Cinematic預設多輪research／三方案／配樂等較重；可借source-led、五面向及審核方法。若日後真正採管線，須依Mira授權及無字、原速、身份、讀衣規則明確適配，不能讓模板自動加入字幕、配音、特效或素材庫路人。

## 本機查核與未驗證範圍

安裝紀錄INSTALL_LOCAL.md聲稱Python依賴、看板健康、Remotion版本及一秒輸出測試通過；此為安裝時紀錄，不是本輪重新完整驗證。

本輪在專用venv及Activate-OpenMontage環境以registry查詢，沒有執行生成：

- available：frame_sampler、scene_detect、visual_qa、video_analyzer、video_trimmer、video_stitch、video_compose。
- unavailable：video_understand、face_tracker、ltx_video_local、grok_video、seedance_video、kling_video。
- video_compose.render_engines：ffmpeg=true、remotion=true、hyperframes=false。這是環境探測，不是長片渲染成功證據；HyperFrames探測還會查npm與CLI doctor，結果可能受網路／執行權限影響，不能只憑false宣布未安裝。
- 已取得HyperFrames具體診斷：node_major=24、ffmpeg_available=true、npx_available=true；npm_resolve_error為`timeout (5s) — offline or slow registry`，沒有進入CLI doctor探測。因此此輪false源自套件查詢逾時，與安裝時CLI啟動通過並不直接矛盾。
- 本輪讀取127.0.0.1:4750/api/health被目前執行權限拒絕；無法確認看板此刻是否運行，不是證明服務故障。沒有啟動或重啟服務。
- Repo有既有remotion-composer/package.json與package-lock.json修改；未改動它們，也未執行npm audit fix。安裝記載的安全公告另行維護，不為本輪評估做破壞性套件升級。

## 現有素材、補生成與費用

可直接做：整理有效／退件／待審版本、讀入現有原片、指定時間抽幀、比較接點尺度、原速小窗看片、調整可用區段長度、建立來源區間與技術報告。只增加本機運算；不需要新的雲端生成金鑰。

需補圖或重生：若M01手部漂移發生在要保留的主要動作內，剪輯引擎無法還原正確肢體；應重設表演／起始與導引圖，再重生必要片段。若只發生在可刪除的開頭或結尾，可另存裁切候選，清楚標示是取用可用段，非修好缺陷；若犧牲看點則不成立。M02已核准版可作正例，不因引入工具重生。

新的雲端影片生成或影片編輯需要選定服務、金鑰與支出上限；先說明再執行。Grok網頁額度與xAI API不能視為同一配額。LTX本機路徑目前不可用，需模型／依賴／硬體能力驗證；其程式宣告約12GB VRAM與16GB RAM只是資源profile，不是本機實測或成功保證。不得在本輪自動安裝或下載模型。

Remotion適合需要精確時間線與可重現版面比較的後續測試，代價是額外專案設定；HyperFrames適合HTML／GSAP動態版面或互動預演，對Mira無字寫真人物片的直接價值較少且完整渲染待驗。既有單純裁切與格式檢查可續用FFmpeg。這是方案比較，尚未鎖定新render_runtime。

## 建議的最小測試：本機雙樣本QA，不生成、不重剪

目的：驗證OpenMontage能否讓助理在交片前留下足夠的動態檢查證據，而非只做格式檢查。

輸入A：`10_automation/runs/2026-W44/lively_models_2026-10-30/M01_lively_review_v1.mp4`，已知負例，第2秒手部飄移。輸入B：`10_automation/runs/2026-W44/M02_restart_2026-10-30/M02_restart_review_v2_trim1s.mp4`，使用者已核准正例，尤其第二鏡表演。

方法：經registry取visual_qa執行probe；經frame_sampler的timestamps抽全片代表幀及M01 1.5–2.5秒逐幀／連續原速短窗，以唯一序號命名。助理對照五面向動作卡，觀看原速，記精確來源、時間／影格、觀察與修正建議。輸出單一review.json與檢查頁於獨立研究目錄；不建立production已通過checkpoint，不改主片／核准紀錄，不上傳外部媒體。

成功判斷：
- A即使格式通過仍被保留為visual-reject，缺陷位置可定位到已知約2秒區間並有具體證據；若偵測不出應誠實記不確定，不自動通過。
- B保留精確使用者核准，不因工具分數推翻；可分別指出第二鏡視線、停步、轉肩與笑容的實際可見時段。
- 抽幀數量／時間／檔名不漏失、不覆寫；技術通過與動態判斷分開。
- 沒有新增付費API呼叫、模型下載或媒體改動；費用只記本機操作，不能把助理平台用量寫成零成本。

若通過，再決定是否接入Backlot與正式checkpoint。這個測試尚未執行；本輪沒有採用或測產出新片。
