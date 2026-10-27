# Mira 全雲端可行性查核

## 後續準備進度

使用者 `ok` 後已完成隔離的M02雲端試作包，核准素材/參照、四個全身與重點畫面、A原片、提示詞及相對路徑剪輯工具另存至Drive研究資料夾，並提供手機可讀的Google文件。36份必要輸入及ZIP逐檔驗證，本機完整解碼145幀/24幀讀寫測試通過。這些只證明本機準備；新雲端工作、Grok新B來源、雲端剪輯與端到端路徑仍未執行。收據 `cloud_trial_2026-10-07/drive_delivery.json`；在具體試作包完成後已詢問是否建立新的ChatGPT Work雲端工作。下文是先前可行性查核紀錄。

2026-10-07；只做官方文件及本機唯讀盤點，未建立雲端工作或遷移。使用者自述為個人 Plus/Pro，並表示 Grok 已恢復、不用安裝 TinyFish。帳號實際功能開放、雲端介面、登入及生產路徑均尚未實測。

## 官方功能與限制

- [Codex Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)：雲端任務可執行程式及指令，但目前限制明列不支援電腦與瀏覽器操作。本機個人技能不自動同步；repository 內的技能可供雲端任務使用。因此現行 Grok 網頁路徑不能直接照搬進 Codex Cloud。
- [ChatGPT Work](https://learn.chatgpt.com/docs/get-started-with-work)：可結合檔案、工具及外掛執行多步工作。只用雲端協調加本機工具，仍需本機在線；真正不依賴本機需使用雲端執行與雲端可讀素材。既有任務不會自動轉換執行環境。
- [官方雲端瀏覽器](https://learn.chatgpt.com/docs/browser)：Plus/Pro 在網頁及手機的可用範圍包含網站登入，但仍依 rollout。雲端有獨立登入狀態，不繼承本機 cookies/分頁；部分網站會擋自動瀏覽器或出現 CAPTCHA。未證明本帳號能登入 Grok、選保存人物參照、上傳 First frame 或下載新影片。
- [雲端協調與本機執行](https://learn.chatgpt.com/docs/enterprise/cloud-local-access)：協調移到雲端並不會把工具或檔案全部移走。此頁主要說明企業本機存取配置，不能用它推定個人帳號已開放特定功能。

## 本機盤點

| 環節 | 已確認 | 移轉需要 |
| --- | --- | --- |
| 週次資料、分鏡、核准與成效 | CSV/JSON/Markdown/Python | 帶入準確週次檔案，保留狀態與核准範圍 |
| 入口與依賴 | PowerShell/Windows 路徑；已有 Python 核心 | 相對路徑；雲端版本的 Python、Pillow、NumPy、imageio_ffmpeg |
| 技能與人物參照 | repository 的 Mira skill 與 M01–M05 approved anchors 有 Git 追蹤 | 在目標雲端讀回檔案、版本及 hash；不依賴本機安裝副本 |
| 靜態生成 | 現行內建 imagegen 生產路徑 | 實測雲端影像工具與參照圖能力，不能假定等同本機 |
| Grok | 本機已保存角色參照、單張 First frame 生成、取回影片 | 雲端重新登入並確認實際參照、設定、上傳、生成及下載 |
| 最新影片/研究 | 最新 W37 reels/videos 與 backward_step_trial 無 Git 追蹤檔；.video_dependencies 被忽略 | GitHub clone 不能取得這批最新成果；先建立精確素材與核准同步包 |
| Drive/Canva/IG | 已有外部服務及人工核准/發布邊界 | 在目標工作確認連接器、帳號及操作能力；保留人工審看 |

未找到有效的既有全雲端遷移方案。7月的 COMPUTER_B_SYNC 文件是雙電腦同步，不能取代此查核。

## 建議與驗證標準（提案，未執行）

優先評估 ChatGPT Work 的真正雲端工作台，保留 GitHub 版控與 Drive 媒體保存。必要剪輯指令在雲端執行；是否在同一工作具備全部工具，仍須實測。

先用 M02 的一人兩套測一個完整流程：讀規格與核准參照 → 靜態生成/視覺核准 → Grok 上傳/選參照/生成 → 下載原片 → 原速剪輯及0.75秒交疊 → QA/使用者核准 → Drive另存與讀回驗證。先做既有影片解碼/剪輯以驗證環境，再進入新生成。

試搬包只含必要規格、技能、兩套 look、approved face/full、起始圖、核准/来源hash及需要的原片，不搬全部歷史或本機瀏覽器登入。原第一波五支保留。

只有在無本機檔案、工具或瀏覽器呼叫的情況下完成並保存這個流程，才能說通過單支全雲端試行；尚不能推定每週五支成功率或曝光結果。全雲端保留手機/網頁審看與必要登入，不代表取消人為核准。
