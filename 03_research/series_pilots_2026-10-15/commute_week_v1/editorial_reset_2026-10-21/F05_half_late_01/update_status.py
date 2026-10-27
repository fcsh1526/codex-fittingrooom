from pathlib import Path
import json
d=Path(__file__).resolve().parent
project=next(p for p in d.parents if (p/'CURRENT_STATUS.md').exists())
r=json.loads((d/'generation_receipt.json').read_text(encoding='utf-8'))
r['root_review']['viewed'].append('first_half_comparison.jpg')
(d/'generation_receipt.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
old=d.parent/'F05_full_late_01/user_review_request.json'
o=json.loads(old.read_text(encoding='utf-8'))
o['status']='deferred_unapproved_branch_after_user_selected_full_to_half_storyboard'
o['deferred_by']='../half_integration_2026-10-22/user_storyboard_approval.json'
o['answer']=None
old.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
heading='## 全身推近半身分鏡已核准，半身新圖待視覺核准 — 2026-10-22'
body='''

使用者已明確選「採用第五套全身推近半身」，精確線稿SHA`32901080f8ffcf66e40a940921d9cc5addffdc8057df68f6903375d8a69dad58`，完整問題／答覆及範圍見`editorial_reset_2026-10-21/half_integration_2026-10-22/user_storyboard_approval.json`（通勤五套研究根目錄下）。前四套已接受385幀／16.0417秒保留，第五套使用核准全身首圖：先讀整套黑裙、再同鏡靠近白襯衫領口／腰線與藍包、半身收束。144幀新鏡減18幀重疊的整片預算511幀／21.2917秒，實際節奏仍待動態驗證。

本次一次內建image_gen、48.322秒等待，無追加修正，產生`F05_half_late_01/F05_M03_L04_half_late_candidate_A.png`，941×1672／2,148,124bytes，SHA`114300736fbcf321316d20ce992f968bcb39d9dcea0e85542f0491ee97539ab7`。以核准全身首圖及approved M03v3 face/full為鎖；完整頭、襯衫領口／短袖／黑裙高腰與完整鈷藍包在框內。root看原尺寸及首／半身並排，近手保持腰旁、遠側手改為自然擺前，裙面保留原細紋；背景樹、花台與玻璃重新取景，未建立精確視差。靜態候選不是連續推近或步態通過。

**此精確半身候選尚待使用者視覺核准，未上傳Grok或生成新F05動態。** 確認後才核對現行控制並做一次6秒有界單鏡試作；驗證先全身閱讀、再推近，不能由首末照片推定時序達成。保持原速、無字無音、跨套約0.75秒柔接，套內不另剪。原全身末段候選仍未核准，改為暫存分支，不再要求本輪回答該舊問題；原片／已接受版本／Drive發布包均保留，無外部異動。精確prompt、來源、耗時、目視及待答問題在`F05_half_late_01/`。

'''
p=project/'CURRENT_STATUS.md';t=p.read_text(encoding='utf-8-sig')
if heading not in t:
 pos=t.index('\n## ');t=t[:pos]+'\n'+heading+body+t[pos:]
p.write_text(t,encoding='utf-8')
p=project/'10_automation/CANONICAL_WORKFLOW.md';t=p.read_text(encoding='utf-8-sig')
bullet='- Latest approved half-shot storyboard,2026-10-22: user explicitly selected「採用第五套全身推近半身」for exactboardSHA32901080f8ffcf66e40a940921d9cc5addffdc8057df68f6903375d8a69dad58; receipt `half_integration_2026-10-22/user_storyboard_approval.json`. Keep accepted385f prefix, F05 approvedfullfirst then continuouspushin/half close, planned144f6s,total511f21.2917s not outcome. One built-in imagegen48.322s,no correction created `F05_half_late_01/F05_M03_L04_half_late_candidate_A.png` SHA114300736fbcf321316d20ce992f968bcb39d9dcea0e85542f0491ee97539ab7,941x1672,2148124bytes from approvedfirst/M03v3facefull. Head/collar/waist/completecobaltbag readable; fararmchanges, skirttexture remains, tree/planter/glass reprojected unvalidatedparallax. Rootnative/paired review, no motionpass. Exactnewstillvisualapproval pending before Grokupload and one6s boundedtrial. Oldfull-lateSHAe04a1f… deferred unapproved preservedbranch, no oldquestion answer needed this branch. No newF05motion/film/publish approval, protectedsources/Drive unchanged; formalweeklycontract unchanged. This supersedes pendingstoryboard-selection status below.\n\n'
if '- Latest approved half-shot storyboard,2026-10-22:' not in t:
 t=t.replace('Active rules:\n\n','Active rules:\n\n'+bullet,1)
p.write_text(t,encoding='utf-8')
print(json.dumps({'new_half_still_sha256':r['sha256'],'storyboard_approved':True,'new_still_pending':True,'old_full_late_deferred_unapproved':True,'new_F05_motion':False},ensure_ascii=False))

