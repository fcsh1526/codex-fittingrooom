# W21-test Day 3 優先產圖 Prompt

來源：https://mika-lin-weekly.pplx.app/weeks/2026-W21-test.html  
CSV：https://mika-lin-weekly.pplx.app/data/2026-W21-test.csv

## 驗收狀態

W21-test 已符合新規格：
- 5 個 Trend Topics。
- 6-8 件代表性單品。
- 20 個 Item Prompt List。
- 7 則 Platform Content Plan。
- 20 筆 Machine-readable Export CSV。
- 首頁列表與 `data/index.json` 已包含 `2026-W21-test`。

## Day 3 先測 10 個 Prompt

優先順序依據：人物一致性容易保留、衣服輪廓明確、導購價值高、平台用途清楚。

| priority | prompt_id | reason | first_tool | target_platform |
| --- | --- | --- | --- | --- |
| 1 | W21-P001 | 奶油黃針織背心最適合做人物一致性基準，服裝結構簡單 | Grok | Instagram Carousel |
| 2 | W21-P002 | 通勤西裝套裝導購價值高，適合小紅書與 IG | Grok | 小紅書 |
| 3 | W21-P006 | 皺感襯衫洋裝視覺完整，適合 Pinterest 長尾 | Grok | Pinterest |
| 4 | W21-P007 | 沙色亞麻套裝可測靜奢與通勤客群 | Grok | Instagram Carousel |
| 5 | W21-P010 | Sacai 拼接西裝辨識度高，適合測高難度剪裁 | Grok | Instagram Reels |
| 6 | W21-P012 | 解構風衣洋裝視覺強，可測人物與複雜服裝穩定性 | Grok | Instagram Carousel |
| 7 | W21-P014 | Cobalt 緞面短洋裝色彩辨識強，適合短影音封面 | Grok | Instagram Reels |
| 8 | W21-P018 | 結構感肩背包導購價值高，尺寸容錯較好 | Grok | Instagram Carousel |
| 9 | W21-P019 | 手套鞋 / slingback 可測配件細節，但需注意腳部錯誤 | OpenAI 對照 | Pinterest |
| 10 | W21-P020 | 純白方包適合 quiet luxury 導購與品牌合作提案 | OpenAI 對照 | Instagram Reels |

## Day 3 操作建議

- Grok：先用 `W21-P001`、`W21-P002`、`W21-P006`、`W21-P007`、`W21-P010` 各產 3-4 張，建立第一批人物一致性評估。
- OpenAI imagegen：先用 `W21-P019`、`W21-P020` 各產 1 張做封面/配件細節對照。
- 評分填入 `07_metrics/image_ab_test_log.csv`：identity_consistency、outfit_clarity、body_integrity、platform_fit、shopping_value、publishable。
