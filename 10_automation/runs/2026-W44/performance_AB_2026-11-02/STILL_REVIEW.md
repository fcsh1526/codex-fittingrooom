# A/B 共用起始圖與分鏡：v2已由使用者確認

後續更新2026-11-02：使用者「ok」已接受確切v2（user_start_still_approval.json），並已用同一圖各生成A/B一次。原待確認與未送影片描述是此前時間點，最新見EXECUTION_STATUS.md、RESULT_REVIEW.md；動態與發布未獲接受。

日期：2026-11-02。延續 W44 的表演研究，非 W45 週產量。W45 publishing_structure.md 不存在。使用者本輪「ok」承接準備共用過街起始構圖及對照試驗，不能倒寫為新圖已獲接受。

## 已完成的共同設計

- 一位 M02 v3、一套 2026-W44-001-L01 紫薄外搭／白T／灰褲造型，不換衣，不使用 IG 作者身份。
- 共用固定相機與場地：遠側人行道出現 → 路緣察看畫面右側來車方向 → 過街接近 → 視線相遇、微笑。
- shared_scene.json 為共同資料，build_previs.py 產生 shared_storyboard.png、overhead_route.png、start_composition_guide.png。0／2.2／5.5／10 秒為設計節點，不是影片生成的逐秒強制控制。
- 相機與人物投影來自同一示意場景；50mm／直式感光面僅設計模型，不是實測場地／照片校準。靜態關鍵視圖已檢視；未模擬連續步態、未生成影片。
- 原片末段的輕微重構圖在本對照先固定，以隔離原因句；不宣稱已復刻全部原片運鏡。

## 新圖與輸入

使用內建 image_gen，不設定外部生成 API 金鑰。一次新構圖生成＋一次取景修正，保留兩張，不重寫既有 Hero／核准影片。

已讀圖並確認存在的參照：02_brand/reference_models/M02_start_v3_face.png（身份）、M02_start_v3_full.png（比例）、M02_restart_2026-10-30/S01_start.png（服裝），以及本分支的示意構圖。首次與修正實際送出文字分別存 submitted_start_image_prompt.txt、submitted_framing_correction_prompt.txt；start_image_prompt.txt 是生成前草稿，不冒充實際送出版本。

| 檔案 | 實際像素／SHA256 | 狀態 |
|---|---|---|
| start_candidate_v1_framing_failed.png | 941×1672／495a4655037c8f50ba084246166c76ec0849db7f44b6ed8869bf2002e384f050 | 人物約68%畫高，較預定40–45%過大；不用作本次共同首圖 |
| start_candidate_v2.png | 941×1672／f8ed3b5606aca1af5ae56f9db07440d8de604214be58a1136deb246c0914547d | 取景修正版；待使用者精確視覺接受 |

來源檔仍保留於 .codex/generated_images/01a17c38-aa07-76f2-a857-3127abcc97fb/exec-dbd0fad8-8b80-44fc-95b3-50d22a46f04e.png 與 exec-e94a56ef-2588-4006-af36-972b3d4df9c0.png；專案內另存獨立副本。

## v2 可見結果及與分鏡的差異

- 人物完整頭鞋可見，紫外搭、白T、灰褲、白灰鞋、黑左肩包可辨；低髮髻與臉部視覺上接近輸入身份，未作量化身份檢測。
- 兩腳位於路緣後的人行道；前方有足夠可見道路，右側保留察看方向。無明顯車輛、額外人物或文字。
- **人物約33%畫高**：人工估框頭頂約 y456、鞋底約 y1005，占(1005−456)/1672≈32.8%；中心約畫面35%寬。這是人工估值，不是自動人物追蹤。
- 與設計40–45%、頭頂40%／鞋位82%不同：實際頭頂約27%、鞋位60%，前景道路更多。不能宣稱照片精確遵循投影；若使用者接受這張，後續分鏡須保留此實際起點差異再調整，不能倒改原計畫。
- 初始表情已帶笑、視線略偏畫面右方；尚非明顯大幅察看動作。後續應看其是否仍能作出清楚的道路察看與回到鏡頭的反應，不保證笑容一定逐步展開。
- 道路右側有白色標線殘段，非提示要求；不加斑馬線設計，不認證生成後標線／路緣穩定。
- 原始直式尺寸近9:16；未拉伸、未假稱1080×1920原生像素。品質檢視範圍限靜態，無動態／發布結論。

## 下一步

先由使用者確認 start_candidate_v2.png 是否沿用。適用 mira-reel-director/SKILL.md 的「Review new AI stills with the user before they enter motion generation」。本輪到此未送影片，也未查證 Grok 額度恢復。

接受後使用同一張圖與同一身份設定，核對當前 Grok 介面及額度，再各生成 A／B 一支；B 僅比 A 多一句 Her brief glance toward the lane is to check for approaching traffic before crossing. 保留完整送出文字、實際選項與結果；不在兩組之間偷偷改照片或動作。檢查原速全片與相同時間抽格，不以抽樣代替動態觀看。若使用者否決本張，先處理明確問題，不自動排更多圖片或付費替代服務。
