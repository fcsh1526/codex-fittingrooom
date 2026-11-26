# 《窗框去哪了》B1 首圖候選

使用者選 B，依[既有分鏡](../../../../../workflow_audits/2026-11-26_Df6_nBeA1eq/CINEMATIC.md)先做一張窗框、黑紗與褲管同框的首圖，逐圖確認後再做動態。服裝沿用 W47 M05 v1 L02。此鏡是腰下至鞋的剪接用首圖。

| 版本 | 影像結果與決定 |
|---|---|
| v1 | ImageGen 使用 M05 核准正臉及全身參照。霧面亮窗和黑紗能讀清，窗框與褲管相距太遠，缺少第三種遮擋。 |
| v2 | 以 v1 局部修正窗框與褲管的重疊位置，窗框在亮窗前可見，到炭灰褲管處被遮住，在較低的薄紗右側重新出現。側邊留有橫移空間，雙鞋與地面接觸清楚。窗框靠近紗邊處的線略斜，後續動態需檢查它是否在同一機位保持穩定。鏡頭沒拍到臉，身份以既有參照續接。 |

待使用者逐圖確認 v2。工作區 PNG 為 `M05_B1_window_candidate_v2.png`，941×1672，SHA-256 `c201f6bf179c7f1077773d2ba922606140e8e43fbcbea7ed32e18e8e0ce9da7b`。本輪一張基礎靜態及一次局部修正，尚無動態。

## 造型來源複核 · 暫停試片

使用者看完 v2 後暫停，提出薄紗罩在西裝感直褲外是否有實例。W47 原 CSV 的 P017／P018 記載「透膚罩裙疊在不透直筒褲上」，來源欄只記概括的國際秋冬系列與時尚編輯整理，兩列沒有可追到同一套造型的連結。v2 的炭灰西裝感直褲、奶油白針織與完整黑紗罩裙是 Mira 的具體搭配。

- CHANEL 2025/26 秋冬成衣確有黑薄紗上衣與裙罩在米白褲裝外，屬秀場案例。[FHCM 系列資料](https://www.fhcm.paris/en/news/chanel-fall-winter-202526-ready-to-wear-collection)
- Kendall Jenner 在巴黎時裝週穿 St. Agni 半透明橄欖色裙外搭於黑色寬褲。裙的垂墜、褲管的寬鬆比例與 M05 v2 有別。[現場穿搭照片](https://www.harpersbazaar.com/celebrity/latest/a68119181/kendall-jenner-sheer-skirt-over-pants-paris-fashion-week-2025/)

兩例支持這種疊法確有實穿或成衣先例。M05 v2 仍是待確認的編輯造型，常見程度與日常可穿性另待判斷。生成狀態維持暫停，等使用者決定是否保留造型。

## 垂墜裙與鬆身褲候選

使用者回覆「ok」。按前一則提出的造型方向，先做一張首圖供逐圖確認。保留 B1 的腰下取景、霧面窗框與奶油白上衣，將黑紗改成平腰頭、貼順垂墜的過膝薄裙，深色褲改為放鬆褲管與自然垂褶，搭黑低跟鞋。沿用 M05 已核准的臉部與全身參照。此版是 B 案的造型調整。

新圖裙腰較平整、沒有明顯的皮帶環，兩隻鞋都入鏡。靠右的窗框在亮窗前與裙的透明側邊都能讀到。這張的窗框大致在褲管外緣，褲管遮住窗框的效果留到人物小幅橫移後檢驗。新圖造型待使用者確認，尚未進入動態。

工作區檔案 `M05_B1_window_soft_layers_v1.png`，941×1672，SHA-256 `05de46495825c5102b9234bab2cbeaf67bb4b288a033b8a17b00da4d49111977`。

## 2026-11-26｜兩版實穿造型複審

使用者要求重新檢視實際服裝。回查 [W47 原始研究](../../../source_perplexity.csv) 的 P018，材質欄明列「細網紗、棉丹寧」。週搭配表保留黑罩裙和炭灰直筒褲，省略了丹寧材質。v2 的褲耳和俐落褲腳顯出西裝感；soft_layers_v1 放平腰頭、放長褲管後，褲腳在鞋面堆褶，仍少了能辨識丹寧的紋理。黑紗在大腿前與炭灰底色融在一起，透感主要靠右側亮窗襯出。窗框可保留作為材質特寫，現圖作為日常穿搭示範的說服力有限。

日本 PARIGOT 冬季型錄印刷頁 02 有 Chika Kisada 黑紗裙搭 RED CARD TOKYO 牛仔褲的全身造型，可對照兩種面料在自然站姿下如何區分。[品牌型錄](https://www.parigot.co.jp/uploads/2024/09/WOMEN-24-WNTER.pdf#page=2)

編輯建議為黑色薄紗過膝裙配洗灰直筒牛仔褲，保留奶油白上衣與黑低跟鞋。若續作，先以全身比例確認裙襬、褲管和鞋面，再選窗框位置。建議限本套；本次只複審，兩版均未取得使用者定裝確認。

## 洗灰丹寧全身定裝候選 v1

使用者同意先看全身比例。ImageGen 以 M05 v1 已核准的正臉及全身圖為身份與比例參照，完成一張素背景定裝照。黑紗下可辨識五袋褲的袋口、金屬鈕與大腿洗色；過膝紗襬下方露出一段較亮的灰色褲管。雙鞋完整入鏡，褲腳停在腳踝附近，露出腳背，較原訂剛碰鞋面的長度稍短。本圖待使用者確認，窗框分鏡與動態尚待接續。

本機圖檔 `M05_L02_washed_denim_full_v1.png`，941 × 1672，SHA-256 `0fba2b82738919875732fb0c533b7660c52a5541da5f67c75446d48ae997674b`。

<details><summary>定裝照生成提示</summary>

One photoreal vertical 9:16 full-length Mira fashion fitting photograph. Ref 1 gives the identity and hair of adult M05, ref 2 her body proportions. Dress her afresh: a slim cream crewneck fine-knit long-sleeved top tucked into medium washed charcoal grey straight-leg five-pocket cotton JEANS with visible twill, subtle faded thighs, curved pocket stitching and a stitched fly. Over the jeans she wears a separate, single layer of very sheer black fine mesh, a softly draping slightly A-line midi overskirt with a narrow flat waistband and fine hem just below knees to upper calf. The grey denim's subtle wash, seam, and pocket should remain distinguishable through the sheer black front. No lining, embellishment, ruffles or stiff flaring tulle. Jeans hems just brush the uppers of her black low-heeled leather shoes with no pooling. Small black handheld bag resting beside her thigh, small silver hoops. Standing naturally with one foot a little forward, both shoes separated, no fabric held up. Plain warm light grey wall, soft side daylight, level front view with full head and shoes, comfortable frame margins, natural skin and textile texture. One unlettered editorial wardrobe proof, no windows, graphics or logos.

</details>
