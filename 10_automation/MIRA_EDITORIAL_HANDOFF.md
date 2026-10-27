# Mira 跨週編輯交接頁

流程核對：2026-10-27（台灣時間，W44）。最新已核准的創作／交付決策：2026-10-22。

主規則見 [CANONICAL_WORKFLOW.md](CANONICAL_WORKFLOW.md)，目前成果見 [CURRENT_STATUS.md](../CURRENT_STATUS.md)。本頁是新對話的短交接入口；完整舊交接內容保存於 [歷史快照](history/MIRA_EDITORIAL_HANDOFF_before_2026-10-27.md)。10/16的暫停、待審及W42規劃週只屬當時紀錄，不能當成目前狀態。

## 現在進行到哪裡

- 狀態：`approved_for_publication_drive_delivered_refinement_pending`。
- 「同一路線・連續行進換裝」21.29秒五套通勤初版已獲使用者核准可發布，並登錄為單畫面依序展示下的子型。
- 精確核准片：[context_review_v2/review.mp4](../03_research/series_pilots_2026-10-15/commute_week_v1/editorial_reset_2026-10-21/pace_rebuild_2026-10-22/context_review_v2/review.mp4)，SHA256 `e5e8a90878b00bab29ecf4da32a6fe5472e1376f1b835b999beaa9a812e225c2`。
- 最新核准包含保留這版並可發布；仍需更快步、人物與攝影機各自的曲線運動，以及減少不舒服的疊影閃爍。發布核准不表示這些改善已達成。
- 10/22已交付 [W43 Drive](https://drive.google.com/drive/folders/1eZsL7PjRcf3FtvRq-DwiI3J5nCedWFBB) 的影片及原生Google文案文件。本任務未代發IG；使用者／bot後續是否發布、發布網址及成效尚待回填，本次未查詢IG。
- 下一個研究交付物：同一場地的**人物曲線＋攝影機曲線俯瞰圖，以及同時間軸的相機視角預演**。先看實際畫框中的尺度、相對角度、步伐與背景視差，再產生最少必要的新照片／影片。

## 從每週資料到發布的流程

1. **來源資料**：Perplexity收集有來源的每週流行資訊；本專案負責穿搭情境、組合與內容系列，不要求上游虛構系列候選卡。
2. **跨週素材池**：優先檢視近期約2–3週的資料，保留較早可重用的單品；原始來源、編輯搭配與AI視覺素材分開追溯。這是編輯窗口，不是流行效期保證。
3. **先定觀眾問題與系列**：例如五日通勤、商務／現場出差、一件多搭、一天不同場合，再決定完整搭配、人物、套數及每鏡要展示的衣服資訊。
4. **先規劃整支，再生成圖**：整支視覺主題→連貫線稿分鏡→必要時的空間／人物與相機路徑預演→首／中／尾與接點需求。每個場景都服務衣服與情境。
5. **人物與照片核准**：使用已核准face/full身份；新AI照片逐張視覺核准後才做動態。既有影片實幀再用須記來源、畫格與雜湊，不偽造新照片核准。
6. **逐鏡動態與整片驗收**：分別檢查身份、衣服、手包、腳步、背景，再驗兩側接點及整片觀看。來源步頻／位移不合，先修來源；不以後製加速或更長疊化遮掩。
7. **保留原速無字無音母版**：約0.75秒柔接仍是現有比較基準；此通勤版疊影不適尚未解決。若真需畫面文字，另通知使用者在IG編輯器添加。
8. **Drive交付**：`800.Codex IG/{編輯內容ISO週}/`保存影片與手機可讀的原生Google文案／交接文件；來源素材週、編輯交付週及實際發布日分開記。研究版另存，既有發布包不覆蓋。
9. **發布與成效回填**：發布後記網址，並在24小時、72小時、第7天比較觸及、觀看、收藏、分享與追蹤；沒有的數據留空，不能補0。

## 正式週產規格與已核准系列例外

既有正式週產契約仍為五個主題、M01–M05各一次、每位兩套、十套、五支Reel；每套的full/proof與獨立Carousel A/B/C需求維持。

M03五套通勤是使用者明確核准的單支系列例外，按其專屬look清單與分鏡執行。不能把它硬改回兩套，也不能推成所有新片一律五套或新週配額；新的系列目的、人物與套數須有相應企劃／核准紀錄。

## 目前資料的時效與同步

- [CURRENT_POOL.md](../04_prompts/material_pool/CURRENT_POOL.md)是2026-10-16／W42的生成快照，不是10/27／W44的新資料。開始新的週企劃前，按實際規劃日刷新索引並檢查缺少的原始週資料；本次沒有重建素材池或抓取新週報。
- 台灣地區天氣應於實際規劃／發布時查核，不沿用幾週前預報。本次為工作流核對，未查新天氣。
- W43是最近已交付的系列批次，來源服裝來自W41；W44目前沒有新週企劃或發布結構，不能從日期自動產生新量產任務。
- 最新工作流、程式、素材索引與核准／交付metadata納入2026-10-27的Git同步檢查點，詳見 [GitHub同步範圍](GITHUB_SYNC_SCOPE.md)，實際提交版本以Git歷史與遠端main為準。大量圖片、原始影片、QA圖及本機工具資料保留在本機／既有Drive；僅有最終成片在Drive不等於五段原始片已備份，新checkout重剪需另備來源媒體。

## 新對話接手時必讀

先依AGENTS順序讀主流程、CURRENT_STATUS、相應週的publishing_structure；本頁作跨週短入口，再按任務讀素材池與所選系列的專屬核准紀錄。當前規劃週缺檔時明示缺檔，勿把舊週配額或舊暫停狀態當成新決策。

- [W43交付結構](runs/2026-W43/publishing_structure.md)：一支已核准系列試作，非完整新週五支產出。
- [影像類型分類](../03_research/reel_presentation_study_2026-10-12/PRESENTATION_TYPES.md)。
- [通勤初版製作紀錄](../03_research/series_pilots_2026-10-15/commute_week_v1/editorial_reset_2026-10-21/pace_rebuild_2026-10-22/ACCEPTED_RECIPE.md)。
- [下一版規格](../03_research/series_pilots_2026-10-15/commute_week_v1/editorial_reset_2026-10-21/pace_rebuild_2026-10-22/TYPE_AND_NEXT_VERSION.md)。
- [最新發布核准](../03_research/series_pilots_2026-10-15/commute_week_v1/editorial_reset_2026-10-21/pace_rebuild_2026-10-22/context_review_v2/user_publication_approval_2026-10-22.json)。
- [W43 Drive交付收據](runs/2026-W43/reels/series_delivery_2026-10-22/google_drive_delivery_2026-10-22.json)。

不同對話接手須實際讀取同份專案檔案；不要假定會自動取得其他對話的完整內容。
