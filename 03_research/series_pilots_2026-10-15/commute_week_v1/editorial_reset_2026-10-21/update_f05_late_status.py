from pathlib import Path
import json
base = Path(__file__).resolve().parent
project = next(p for p in base.parents if (p/'CURRENT_STATUS.md').exists())
d = base/'F05_full_late_01'
p = d/'generation_receipt.json'
r=json.loads(p.read_text(encoding='utf-8'))
r['root_review']['viewed'].append('first_late_comparison.jpg')
r['independent_image_review']={'agent':'/root/paper_to_source_audit_oct21','scope':'Native still and first_late_comparison.jpg only; no motion review','findings':['No obvious blocking wardrobe or anatomy error; complete skirt, bag and both shoes readable','Person a little taller, head higher; far arm swings out and rear foot angle changes','Hem opens farther backwards; cobalt bag and white-shirt/black-skirt designs broadly continue','Large tree moves left behind woman; planter segments and glass grid reprojected, unvalidated angle','No new doorway/canopy/crosswalk visible'],'motion_or_spatial_pass':False}
p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
canonical=project/'10_automation/CANONICAL_WORKFLOW.md'
s=canonical.read_text(encoding='utf-8-sig')
start=s.index('- Latest F05 full-start gate,2026-10-21:')
end=s.index('\n\n',start)
new='- Latest F05 late-still gate,2026-10-21: user「可以，沿用這張」approved exact full-start SHA `ac588ec1674df43923140e17f46c4734706cf834f2b7f5599aeeec60376f9c82`; receipt `editorial_reset_2026-10-21/F05_full_start_01/user_still_approval.json`. Exact prior385f/16.0417s four-look preview remains accepted. One built-in edit from approvedfirst + M03v3 face/full generated full-late SHA `e04a1f4267a02738a83a2851878133e627f4457d78d74ce0b5309fc716418cdd`,941x1672,2,351,932bytes,27.896s,no correction in `F05_full_late_01/`, awaiting exact new-still visual approval. Complete white shirt/black calf-A-line skirt/cobalt bag/plainblackheels remain readable. Root and independent still review find no blocking defect; person slightlylarger, farhand/hem/feet change, tree/planter/glass reprojected: disclose unvalidated angle, not exact route continuity. No newdoor/canopy/road; outdoor facade closing, not company entry. Proposed4.0s late guide within102f selection, not6s lastframe/literalpin. No newF05 Grokupload or motion; exactlate approval precedes one bounded trial. Planned385+102−18=469f/19.5417s still budget, no motion/final/publish pass. All originals/Drive retained; formalweeklycontract unchanged. This supersedes pendingfirst and olderpendingfourlook feedback below.'
s=s[:start]+new+s[end:]
canonical.write_text(s,encoding='utf-8')
status=project/'CURRENT_STATUS.md'
s=status.read_text(encoding='utf-8-sig')
start=s.index('## 前四套已接受，第五套全身首圖待視覺核准')
end=s.index('\n## ', start+3)
new='''## 第五套首圖已核准，收束候選待視覺核准 — 2026-10-21

使用者已對第五套精確全身首圖回「可以，沿用這張」；SHA `ac588ec1674df43923140e17f46c4734706cf834f2b7f5599aeeec60376f9c82`。精確問題、答覆、範圍在 `03_research/series_pilots_2026-10-15/commute_week_v1/editorial_reset_2026-10-21/F05_full_start_01/user_still_approval.json`。它沿用新 F04 實際 f90 作換裝對位（交疊 f90–107），披露的裙面細紋與鞋位／背景差異已接受；不是新動態或整片核准。此前385幀／16.0417秒四套試接也已由使用者接受，含披露的雙影與短階梯；下方待四套回饋為歷史。

本次一次內建 image_gen、27.896秒等待，無追加修正，生成 `editorial_reset_2026-10-21/F05_full_late_01/F05_M03_L04_full_late_candidate_A.png`，941×1672／2,351,932bytes，SHA `e04a1f4267a02738a83a2851878133e627f4457d78d74ce0b5309fc716418cdd`。以已核准首圖及M03 v3 face/full為參照；白短袖尖領襯衫、黑及小腿A字裙、鈷藍包、素黑低跟鞋與完整跨步可讀，保持右向行進，在玻璃外立面旁收束，不新增入口或過街，也不稱進公司。

root已看原尺寸與首／後段並排，獨立靜態檢查也未見阻擋送審缺陷。人物略大、頭稍高、遠手擺出、裙襬與鞋位改變；大樹移至左後，花台分段與玻璃格線重排，應披露為尚未動態驗證的新角度。靜態合理不代表背景視差、步態或裙襬已通過。候選、精確prompt／角色、耗時、目視及待答問題在 `F05_full_late_01/`。

**此收束新圖尚待精確使用者視覺核准，未上傳Grok或生成新F05動態。** 確認後才做一次有界影片測試；預計約4.0秒後段參照在102幀選段內，不把6秒末幀冒稱4.25秒終點。預算385+102−18＝469幀／19.5417秒，實際可用來源仍待驗證；維持原速、無字無音、0.75秒柔接。原片、舊版本及Drive發布包保留，無GitHub／Drive／IG異動；正式五人十套每週規則不變。
'''
s=s[:start]+new+s[end:]
status.write_text(s,encoding='utf-8')
print(json.dumps({'late_sha256':r['sha256'],'first_approval_recorded':True,'late_status':r['status'],'independent_still_review_saved':True,'status_docs_updated':True,'F05_motion_generated':r['F05_motion_generated']},ensure_ascii=False))

