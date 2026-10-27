# Reel 成效紀錄

建立：2026-09-16。首批資料觀測日：2026-09-15。

## 檔案與用途

- `reel_publish_registry.csv`：每個 IG permalink 一列；已知時以 `reel_id`、`production_manifest` 連回正式製作清單。六支歷史影片的製作來源尚未核對，保留空白，不能從發佈日期猜 W35/W36 或模特兒。
- `reel_metric_snapshots.csv`：只追加的觀測及更正歷史。同一影片、檢查點、觀測時間、來源和統計範圍構成一次觀測。完全相同的輸入不重複寫入；更正會追加 `revision`。分析先取每個 `snapshot_id` 最大的 revision，不能把修訂列相加。
- `instagram_account_snapshot_2026-09-15.json`：帳號最近 30 天與當日個人檔案快照，與單片累計資料分開。
- 舊 `publish_registry.csv`、`metric_checkpoints.csv` 及其自動化維持原狀。新工具不把 Reel 填成舊 Carousel，不修改歷史，也不改變週製作狀態。

## 記錄原則

- 未知或看不到的數字為空白；`0` 只代表畫面明確顯示零。不可用舊工具的預設零補齊新 Reel 資料。
- 檢查點為 `24h`、`72h`、`7d`、`lifetime_snapshot`。早期影片現在才觀測，選最後一項，不能假冒 24 小時資料；實際觀測日期／時間仍須記錄。
- 只知道日期就記 `YYYY-MM-DD`；知道時間則記包含時區偏移的 ISO 時間。不要用資料輸入時間取代觀測時間。`recorded_at` 是工具實際寫入時間。
- `non_follower_views_percent` 的分母是觀看次數，不是觸及人數。百分比使用 0–100；skip rate 也如此。
- 平均觀看時間以 Insights 顯示為準；不以觀看次數反推平均觀看或完播率。缺少留存資料時不可聲稱觀眾在特定秒數流失。
- 讚、收藏、分享、傳送、追蹤各除以同一列 `reach`，存為 0–1 的比率值（事件可重複，並不限制最多 1）。分母未知或零時比率空白。分享與傳送是不同欄位，不互相代填。
- `scope` 分開保存 IG、IG/FB 合計、公開格狀頁讀值。先看事件數，再看比率；只比較相近發佈後時間、相同統計範圍。未確認付費／自然分布時，不宣稱純自然成效。
- 同一次觀測的部分更正保留未提供的原欄位；Python API 明確傳入 `None`，或 CLI 傳空字串，才清空該欄位。新的觀測日期不沿用先前數值。
- 單人依序寫入；CSV 不提供多程序同時寫入的鎖定機制。

## 操作

於專案根目錄，先登記已發佈影片；以下 POST_ID、REEL_ID 與時間皆須換成已查核的真實資料。

```powershell
python 10_automation/record_reel_metrics.py publish --post-url "https://www.instagram.com/reel/POST_ID/" --source manual_user_confirmation --observed-at 2026-09-16 --published-at "2026-09-16T18:00:00+08:00" --reel-id REEL_ID --production-manifest "10_automation/runs/2026-W37/reels/production_manifest.json" --format-variant A --production-minutes 45 --generation-attempts 3 --cost-amount 20 --cost-currency TWD
```

`production_manifest` 可選；提供時必須包含完全相同的 `reel_id`，位於頂層或 `reels`／`groups` 陣列。未知成本、製作時間或來源則省略相應參數。只記已發生的實際成本，不預設每次生成單價。

```powershell
python 10_automation/record_reel_metrics.py snapshot --post-url "https://www.instagram.com/reel/POST_ID/" --checkpoint 24h --observed-at "2026-09-17T18:00:00+08:00" --source instagram_mobile_insights --scope instagram --views 120 --reach 100 --saves 2 --shares 1 --follows 1
python 10_automation/record_reel_metrics.py latest --post-url "https://www.instagram.com/reel/POST_ID/"
```

上述數字僅示範命令，不能當作 Mira 實際成績。`latest` 讀出每一次觀測的最新修訂，不把 24h、72h、7d 合併成一筆。

## 四週試行

每週五支、每支同一模特兒兩套穿搭。以「同一需求兩種解法」與「兩個場合」兩種形式交错，每位模特兒四週各出現兩次 A、兩次 B；不要把形式固定綁定特定模特兒。每支保留開場、形式、片長、製作分鐘、生成次數及費用。

固定在 24h、72h、7d 留觀測。以 7d 觸及中位數、收藏／分享／追蹤的事件數及每次觸及比率作方向判讀；樣本小不設無來源的爆量或完播門檻。尚未提供觀看時間與跳過率時只記空白。單支突出只算複測候選，不能宣稱已證明有效。

每支製作預算 30–60 分鐘，五支約 2.5–5 小時。身份與服装 QA 仍是硬條件，不能用縮短工時交換失真的臉孔或商品細節。商品點擊與訂單歸因於未來有真實商品／合作時另行記錄，不由觀看數推估收入。
