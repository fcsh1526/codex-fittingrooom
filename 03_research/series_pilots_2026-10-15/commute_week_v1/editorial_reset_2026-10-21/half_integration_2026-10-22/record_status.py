from pathlib import Path
import json, hashlib
base=Path(__file__).resolve().parent
project=next(p for p in base.parents if (p/'CURRENT_STATUS.md').exists())
q='建議保留已接受的前四套，第五套先完整展示裙裝約3秒，再於同一鏡推近白襯衫與藍包，以半身收尾；整片預計約21.3秒。是否照這份線稿分鏡準備新的半身收束圖？這尚未改動影片，原全身收束圖仍保留待審。'
r={'date':'2026-10-22','status':'proposed_storyboard_pending_user_editorial_choice','artifact':'half_shot_board.png','sha256':hashlib.sha256((base/'half_shot_board.png').read_bytes()).hexdigest(),'plan':'SHOT_PLAN.md','source_audit':'SOURCE_AUDIT.md','question':q,'options':['採用第五套全身推近半身','維持原全身收束','半身改放其他位置'],'answer':None,'new_photographs_generated':0,'new_videos_generated':0,'four_look_accepted_preview_modified':False,'prior_F05_late_still_approval':False,'noteworthy_budget':'proposed511f at24fps ~21.2917s vs prior469f~19.5417s; no source feasibility pass','independent_audit':'/root/half_shot_reuse_audit_oct22: read-only receipts and QA images, no continuous playback','user_continue_scope':'Source audit and concrete storyboard preparation; not exact prior-late photo approval or automatic selection of new edit'}
(base/'user_storyboard_review_request.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=project/'CURRENT_STATUS.md'
t=p.read_text(encoding='utf-8-sig')
heading='## 半身位置已補成分鏡提案，待選定再補照片 — 2026-10-22'
body='''

使用者問半身方案是否廢棄，root說明為當前五套修正版暫時移出、方法與來源保留；使用者「繼續」。本次完成來源核對及具體線稿，沒有把此句當作原待審第五套全身收束圖的核准。

建議唯一最少重工方向：保留已接受385幀／16.0417秒前四套，第五套沿用核准全身首圖，先約3秒純全身展示裙裝，再在同一鏡內約1.5秒靠近、約0.75秒半身收尾，突出白襯衫領口／腰線與藍包。含18幀柔接，第五鏡暫144幀／6秒，整片預算511幀／21.2917秒，比原全身草案多1.75秒。這只是新分鏡提案，不是已選定改案或已存在動態；先選位置再補照片，不強塞原102幀。

資料在 `03_research/series_pilots_2026-10-15/commute_week_v1/editorial_reset_2026-10-21/half_integration_2026-10-22/`：`half_shot_board.png`、`SHOT_PLAN.md`、`SOURCE_AUDIT.md` 與精確待答問題。舊11.333秒全身推近→格紋近景局部曾接受，但其原F03 f127接點與新版[1,109)及新F04f90全身邊界不同，不能直接搬回；舊29.6667秒整片未接受，舊F05拉開沒有獨立動態核准。root／獨立查核為收據與QA圖，不宣稱完整原速播放。

未生成新照片或影片、未使用Grok、未修改已接受片／發布包或Drive。原第五套全身收束候選SHA`e04a1f4267a02738a83a2851878133e627f4457d78d74ce0b5309fc716418cdd`仍待精確視覺核准，保留分支。若選此半身提案，才補一張相容半身後段照片、先核准再一次有界動態測試。正式每週規則不變。

'''
if heading not in t:
    pos=t.index('\n## ')
    t=t[:pos]+'\n'+heading+body+t[pos:]
p.write_text(t,encoding='utf-8')
p=project/'10_automation/CANONICAL_WORKFLOW.md'
t=p.read_text(encoding='utf-8-sig')
t=t.replace('Updated: 2026-10-21','Updated: 2026-10-22',1)
bullet='- Latest half-shot clarification,2026-10-22: user asks whether half-shot abandoned then「繼續」permits audit/concrete planning, NOT exact pendingF05full-late approval or automatic editorial switch. New explicit proposal in `editorial_reset_2026-10-21/half_integration_2026-10-22/`: keep accepted385f fourlooks; F05 approvedfullfirst →~3spurewholeoutfit →1.5scontinuouspushin →.75shalf close on whitecollar/waist/cobaltbag. Planned144f6s, total511f/21.2917s (prior469f+1.75s), not source guarantee; no newphoto/motion. Sourceaudit confirms accepted11.333s oldpushin→close local only, not24.375scontext/29.667sfilm. OldF03f127 and new[1,109)/F04f90 boundaries unaligned; do not insert oldclose as compatible. Storyboard selection must precede one newhalf-late candidate and exactstill gate. Priorfull-lateSHAe04a1f… remainspending/preserved, all acceptedfilms/Drive untouched. Formalweeklycontract unchanged.\n\n'
if '- Latest half-shot clarification,2026-10-22:' not in t:
    t=t.replace('Active rules:\n\n','Active rules:\n\n'+bullet,1)
p.write_text(t,encoding='utf-8')
print(json.dumps({'board_sha256':r['sha256'],'status':r['status'],'photos_generated':0,'videos_generated':0,'old_photo_still_pending':True},ensure_ascii=False))

