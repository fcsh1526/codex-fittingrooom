# v3：按實際接段重建第二套起點

2026-10-06。保留已核准近起點、near_A1 原片及既有 B1 原片。v1 試剪是診斷輸出，不提交為可發布成片。

## 觀察而非假設

near_A1 確實退遠；B1 確實走近，單鏡抽查穩定。原生 v1 組片選 A[0,72) + B[0,144)，24fps，18幀疊加，共8.25秒。接段 f55–67 出現明顯雙臉，原因是人物頭位／尺度沒有對上；0.75秒交疊沒有消除。A 鞋完全可讀後在交疊外也僅約0.5秒。沒有加快動作、裁切或繼續延長轉場來掩飾。

## 新起點及預期鏡頭

- A 保留到約4秒；交疊預留約3.25–4.00秒，完全入鏡的鞋／全身比例在交疊外可讀約1.5秒。最後區間仍按新 B 真實來源重算。
- 新 B still 以 A 的原生 f96（名義4.00秒）作房間、人物距離、頭位、身形比例及站位基準，僅換成已核准 L02 全身圖的衣服、米白無鞋帶便鞋及灰托特，M02 v3 face/full 作身分與比例錨點。
- 這張 B 圖是新候選，先經獨立靜態構圖與服裝檢查、使用者逐張核准，再作 First frame。未核准前不上传 Grok。
- 新 B 仍以固定相機短距離正常走近，逐步看清方領／寬肩帶與敞開襯衫。不要把 B1 用倒放或人物圖層跟蹤改造為新機制。
- 新 B 來源生成後重檢首幀匹配、實際動作及固定背景，再按兩段真實頭／腰／鞋座標选接段。每次切換約0.75秒，原速，無字無音；動態舒適度仍需完整播放核准。

## 誠實邊界

此為針對已知接點問題的一次起點重設，不是素材已通過動態QA或固定產線。A f96 為 root／independent 抽查通過來源的版面基準，不是使用者已核准的新 still。新圖的衣服依已核准 L02 master；只有新候選核准後才用於 Grok。v1 診斷影片、B1 原片及全部歷史材料保留，第一波五支／Drive 不改。


### Selected static candidate v3

Independent v2 QA found the L01 dark-blue strap inherited into the L02 grey tote. A strap-only correction produced selectedv3, SHA `f8098adfefc9be66ffcfea9bc3bad424e3f5e34a30a343d50dc4478f10af16e6`, actual941×1672. Onebase+two targetededits are retained and honestly recorded as one additional wardrobe-regression correction beyond the normal one-edit guideline. Root visible review sees greystrap restored and v2 person/scene geometry retained; independentv3 QA and user still approval remain separate. No new B generation or upload from this still. Prompt/receipt in L02 `reel/body_distance_matched_start_v2/`.


### 2026-10-07：新 B v3 已核准

使用者 `OK` 核准精確 v3 起始圖（SHA `f8098adfefc9be66ffcfea9bc3bad424e3f5e34a30a343d50dc4478f10af16e6`）的臉、服裝與構圖。此核准只含靜態，尚無新 B 來源或成片核准。下一步固定鏡位走近，以實際 A/B 18 對交疊幀選接點，保留原速及 0.75 秒疊化。Grok 目前待安全驗證，尚未送生成；原五支發布檔與研究成片保留。
