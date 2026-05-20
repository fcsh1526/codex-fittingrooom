# Grok + Codex/OpenAI 圖像工作流

目的：前 2 週不要預設哪個工具一定最好，而是用同一批 prompt 實測 Grok Imagine 與 Codex/OpenAI imagegen 的可用率。Grok 先作為主力，Codex/OpenAI 作為 prompt 驗證、封面變體與備用素材工具。

## 工具分工

| 工具 | 第一階段角色 | 適合任務 | 注意事項 |
| --- | --- | --- | --- |
| Grok Imagine | 主力產圖 | 固定虛擬人物、換衣、穿搭場景、短影音素材 | 需檢查一致性、合規與平台揭露 |
| Codex/OpenAI imagegen | 對照與補位 | 快速驗證 prompt、封面圖、Pinterest 2:3、風格變體 | 大量一致人物仍需實測，不當成唯一來源 |

## 2 週 A/B 測試設計

測試樣本：
- 從 Perplexity 每週報告挑 10 個 prompt。
- Grok：每個 prompt 產 3-5 張。
- Codex/OpenAI：挑其中 2-3 個 prompt 產對照圖或封面變體。

評分欄位：
- identity_consistency：是否像 Mika Lin，1-5 分。
- outfit_clarity：服裝版型、材質、顏色是否清楚，1-5 分。
- body_integrity：手、腳、臉、姿勢是否自然，1-5 分。
- platform_fit：是否適合 IG、小紅書、Pinterest，1-5 分。
- shopping_value：是否能幫助導購或收藏，1-5 分。
- publishable：yes/no。

決策規則：
- 若 Grok publishable rate 高於 60%，維持 Grok 主力。
- 若 OpenAI 在封面或 Pinterest 圖明顯更穩，固定用 OpenAI 補封面。
- 若某類 prompt 兩邊都失敗，改寫 prompt，不再硬產。

## Grok 主力 Prompt 組合

使用 `04_prompts/grok_imagine_prompt_template.md` 的人物一致性主提示詞，並把 Perplexity 產出的欄位填入：

- clothing_item
- color_palette
- fabric
- fit
- styling_rules
- pose
- background
- camera_style

每次產圖前都保留：
- same fictional AI virtual creator named Mika Lin
- no celebrity resemblance
- no real person reference
- no childlike appearance
- no visible brand logos

## Codex/OpenAI imagegen 對照 Prompt 格式

```text
Use case: photorealistic-natural
Asset type: social media fashion image for AI virtual outfit testing
Primary request: Create a realistic vertical fashion image of the same fictional AI virtual creator named Mika Lin wearing {clothing_item}.
Subject: Taiwanese woman in her late 20s, soft oval face, natural warm fair skin, deep brown collarbone-length layered hair with subtle wave, clean natural makeup, healthy slim body proportion, calm friendly city style.
Outfit: {clothing_item}, {color_palette}, {fabric}, {fit}.
Styling: {styling_rules}.
Scene/backdrop: {background}, Taiwan urban daily life.
Composition/framing: full outfit visible from head to shoes, vertical social media composition, clean background, no text.
Lighting/mood: realistic natural light, polished but everyday.
Constraints: fictional AI person only; keep identity consistent; clear clothing silhouette; no visible logo; no fake endorsement.
Avoid: celebrity resemblance, real person reference, childlike appearance, nudity, sexualized pose, distorted hands, extra fingers, unreadable text, watermark, luxury logo.
```

## 圖像檔案命名規則

```text
YYYYMMDD_tool_promptid_variant_platform_status.ext
```

範例：
- `20260520_grok_P001_v01_ig_candidate.png`
- `20260520_openai_P001_v01_pinterest_candidate.png`
- `20260520_grok_P002_v03_rejected_hands.png`

## 每批圖像回報格式

```text
批次日期：
使用 prompt id：
Grok 產圖數：
OpenAI 產圖數：
可發布張數：
主要失敗原因：
最適合平台：
下一步：
```

## 合規底線

- 不使用真人照片換衣。
- 不仿冒名人、網紅、素人。
- 不生成未成年、裸露、性化或暗示官方代言的圖。
- 不讓 AI 圖看起來像真實商品試穿照；文案需標註 AI 虛擬穿搭示意。
