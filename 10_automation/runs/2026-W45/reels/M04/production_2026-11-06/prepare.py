from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[5];W=ROOT/'10_automation/runs/2026-W45';P.mkdir(exist_ok=True)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
hero=ROOT/'10_automation/runs/2026-W45/generated_images/2026-W45-004/looks/2026-W45-004-L01/reel/2026-W45-004-L01_M04_reel_candidate_A_face_v2.png';assert h(hero)=='5e6c7a2a00997c2774d0f7a6a1dfa27075cb1304afeb9a81c66cf3133e01957c'
put(W/'approvals/M04_L01_face_v2_still_approval_2026-11-06.json',{'actor':'user','decision':'approved','quote':'ok','recorded_at':'2026-11-06','timezone':'Asia/Taipei','scope':'exact displayed M04 L01 face-v2 starting still; continue its film','asset_path':hero.relative_to(ROOT).as_posix(),'target_sha256':h(hero),'limits':'Still acceptance, including visible clothing/accessories/framing; not unseen motion, full film or publication approval.'})
prompt='''Continue from the supplied first image. She is browsing a bookstore window with the person filming, and is ready to leave with them. Still smiling softly, she turns her head and shoulders partway toward the books, then pivots comfortably back to the person behind the camera and takes one small sideways step toward the open walkway. Her arms respond naturally to the turn and settle freely by her body; her expression brightens in response to the photographer, then softens. Her eyes, shoulders and weight move together, with no repeated rocking, dance routine, exaggerated fixed grin or long frozen pose. She stays at the same camera distance; do not walk toward the lens.

One continuous ten-second real-time full-person shot, locked level chest-height 50mm camera. Keep her complete head, hands and shoes visible. Preserve the exact woman from the corrected first frame and approved identity anchors: tied-back black hair, normal head/body proportions and natural facial texture. Preserve exactly the dark berry-red and cream floral blouse including its motif size and positions, plain black straight trousers, dark-brown loafers, dark-brown shoulder bag, small silver earrings and the existing fine necklace. Keep the bookstore window, arcade wall and paving coherent, with the original daylight. No cut, zoom, slow motion, outfit change or text.'''
(P/'S01_prompt.txt').write_text(prompt,encoding='utf-8')
req='''W45 M04 單畫面正式企劃第一段來源。使用者已於11/6對剛展示的M04臉修正版回覆ok。只使用本次上傳三張素材：檔名含reel_candidate_A_face_v2的是唯一First；M04_start_v3_face與M04_start_v3_full是身份參照。First不是原始漂臉候選，也不是身份棚拍。先實際查看三張並回報對應UUID，不可憑文字代替圖。

只生成一支10秒、720p、9:16原片；不設last／keyframes，不生成新照片，不重試、不加購／升級／換服務。若三張未到齊、圖不符、額度不足或需額外費用，停止回報。若有真實音訊開關則關，無則如實記錄。不要自動做細節鏡或剪輯。

以下英文逐字作prompt，標記不傳入：
PROMPT_BEGIN
'''+prompt+'''
PROMPT_END

完成回報first與身份UUID、實際接受設定、影片UUID／時長／像素／音軌。參數回報、可見畫面與品質通過分開。不宣稱已通過真人感或整片驗收。'''
(P/'S01_request.txt').write_text(req,encoding='utf-8')
put(P/'execution_plan.json',{'date':'2026-11-06','purpose':'Full outfit → floral detail → full outfit; one M04, one look.','approved_weekly_plan':'10_automation/runs/2026-W45/approvals/user_planning_approval_2026-11-03.json','still_approval':'10_automation/runs/2026-W45/approvals/M04_L01_face_v2_still_approval_2026-11-06.json','first_path':hero.relative_to(ROOT).as_posix(),'first_sha256':h(hero),'first_source_request':'one10s full-person source; evaluate distinct early/late sections for S01/S03, no repeating footage','detail_strategy':'derive a traceable same-outfit crop/frame after source review; evaluate clarity before further source generation','join_baseline_frames':18,'fps':24,'editorial_seconds':10,'camera':'fixed; no shared-space route model needed','prompt_sha256':h(P/'S01_prompt.txt'),'max_current_jobs':1,'quota':'unknown','new_stills':0,'publication':None})
print('Exact still approval and one-source request prepared')
