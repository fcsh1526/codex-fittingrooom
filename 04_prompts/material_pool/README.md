# 跨週素材池的使用方式

這裡是衍生索引，不取代原始週報、完整搭配計畫或精確核准收據。Perplexity仍只供趨勢研究；系列及情境搭配在本專案編輯。

## 新週對話先讀什麼

依AGENTS既有讀取順序，再讀 `10_automation/MIRA_EDITORIAL_HANDOFF.md` 及這裡的 `CURRENT_POOL.md`。只按目前內容問題展開相關來源，無須重讀整段歷史對話。

| 檔案 | 用途 | 維護方式 |
|---|---|---|
| CURRENT_POOL.md | 近期週報覆蓋、候選系列、歷史試片回饋與下一步 | 重建產生 |
| current_pool.json | 指定日期／近2–3週的候選 material_id，缺週與天氣狀態 | 重建產生 |
| material_index.json | 原始列、主庫對應、歷史版本、來源快照、對照群組、搭配計畫入口 | 重建產生 |
| series_registry.json | 系列構想與實際使用／回饋／發布紀錄，weather_checks留查證收據 | 人工維護；重建不覆寫 |

## 每週更新

1. 將完整原始CSV另存為 `10_automation/runs/{ISO週}/source_perplexity.csv`，維持原欄位。取得方式、日期、原報／CSV網址、SHA256、列數及證據限制存同週 `source_receipt.json`。週目錄項目不等於已匯入。
2. 在本專案執行以下指令；日期換為實際台灣規劃日。若 `python` 不在路徑，使用專案已配置的Python執行環境。

```powershell
python 10_automation/build_material_pool.py --as-of 2026-10-15 --window-weeks 3
```

3. 檢查 `CURRENT_POOL.md` 的缺週、收據問題及候選數。未取得的週次明示缺少，不複製前週冒充新研究。較早素材仍保留，重審用途及季節後可再用。
4. 企劃系列時，在人工registry填入選中的 `source_material_ids`；完整搭配仍存獨立look計畫，不能把單品列當完整造型。跨主題組合是編輯提案，不是來源的直接結論。
5. 每次試作／發布新增一筆use：分開來源週、製作週／日、確切模特兒與look、成片及回饋收據、發布日期／網址、成效。未知值填 `null`；同片視覺核准不代表系列採納或受眾成效。新實驗不得替換歷史發布包。
6. 規劃／發布前查實際台灣地區與日期的天氣、交通和場合要求，在 `weather_checks` 記來源及查詢時間。重建索引本身沒有查天氣，不會把歷史weather_checks當成本次有效預報。

## 資料判讀

- `saved_weekly_source`：有本機精確原始CSV；相同週與id的主庫副本合為一筆，保留各來源。這不代表已獨立查證外部報導或商品主張。
- `legacy_source_unverified`：主庫有正式ISO週資料，原始CSV未找到。使用前補來源，不能算已確認近期研究。
- `editorial_expansion`：編輯擴寫；即使原列status為editorial_approved，也不是圖片／影片核准。
- 非ISO週／測試資料隔離，原主庫不動。相同週與id若內容衝突，兩份皆保留並排除近期候選，直到人工核對原檔修正。單一CSV內衝突重複id會直接停止重建。
- 收據缺檔為 `missing`：可看到保存的CSV，但取得鏈不完整。收據SHA／列數／週不符或內容為空，標 `mismatch`，排除近期候選。JSON無法解析會停止重建，保留原有索引。
- 對照群組只用單品／顏色／材質／版型／搭法五欄的NFKC與空白／大小寫正規化。不自動翻譯或合併近義詞，不丟棄不同場合、週別與來源；群組數不是已驗證趨勢數。
- 穩定material_id由來源週＋原列id形成，與列排序無關。內容或來源關係變動留revision；來源檔／收據變動留source_history；原列移出輸入後保留歷史並標記缺席。若來源id本身改變，視為新資料，不自動猜測同一筆。
- 重建只寫三個衍生檔，不修改主庫、週CSV、搭配、圖片、影片、核准或registry；不自動同步Drive／GitHub、不排程或發文。需要在新資料取得／新週規劃時執行，沒有背景自動更新。
- 產量、每片套數及媒體授權以最新canonical與交接頁為準；索引不啟動舊固定配額。當前仍為內容企劃階段。

## 檢查

```powershell
python -m unittest discover -s 10_automation -p test_build_material_pool.py
```

測試使用獨立暫存資料，不改原始研究。衍生輸出逐檔原子替換；中斷時重建即可，正式選材先確認三個檔案的as-of日期一致。持久索引不允許倒填較早日期，歷史分析請在獨立副本進行。
