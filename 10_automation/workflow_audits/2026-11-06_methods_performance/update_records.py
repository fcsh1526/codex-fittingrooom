from pathlib import Path
import json

root=Path.cwd()
note='2026-11-06使用者確認：六種剪輯方法為依序穿搭展示、左右並排比較、日常片段敘事、前景遮鏡揭裝、連續行進換裝、單鏡頭互動表演；另兩種待研究為主次雙畫面／子母畫面、俯拍扇葉換裝。動作豐富左右比較仍屬第二種。當前優化重點為各方法內的人物動作、表情、情緒等細節，詳 `09_sops/mira_reel_method_catalog.md` 與導演技能 `references/performance-and-reference.md`；不新增生成前必須對照已接受片段的門檻。左右比較暫停及既有圖／片核准範圍保持。'
for name in ['10_automation/CANONICAL_WORKFLOW.md','CURRENT_STATUS.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','09_sops/mira_reel_production_sop.md','10_automation/runs/2026-W45/publishing_structure.md']:
    p=root/name
    text=p.read_text(encoding='utf-8-sig')
    if note not in text:
        title,body=text.split('\n',1)
        text=title+'\n\n'+note+'\n'+body
    text=text.replace('three layout families, five editorial production recipes with scoped accepted examples, plus one unresolved primary/detail experiment. These layers are not additive counts.', 'six editing methods and two research candidates, as confirmed by the user on 2026-11-06. Layout descriptions do not add to that count; performance is optimized within each method.')
    text=text.replace('目前下一步：11/6使用者澄清要先盤點現有剪輯方法；撤回助理新增的「生成前必須與已接受片段具體對照」要求，不加入skill。按看點選用方法再重做M04連接分鏡及素材需求；', '目前下一步：六種剪輯方法與兩種待研究方法已確認；在選定方法內優化人物動作、表情與情緒，落實於M04連接分鏡與選段。不設強制已接受片段對照門檻；')
    p.write_text(text,encoding='utf-8')

p=root/'10_automation/runs/2026-W45/production_queue.json'
q=json.loads(p.read_text(encoding='utf-8-sig'))
q['next']['action']='Six editing methods plus two research candidates confirmed. Optimize actions, gaze, expressions and emotional development within the selected method, starting with M04 storyboard and performance. Rich split-screen acting remains parallel comparison; parallel editing stays paused. No mandatory accepted-footage comparison gate.'
q['latest_workflow_clarification']='10_automation/workflow_audits/2026-11-06_methods_performance/user_clarification.json'
p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

receipt={'date':'2026-11-06','actor':'user','quote':'5種加上單鏡頭應該有六種。待研究方向中的動作豐富左右比較，其實應該屬於(2)左右並排比較。因此這6種剪輯方法大致上是正確，再加上待研究的主次雙畫面／子母畫面、俯拍扇葉換裝。上述都是剪輯方法。但是實際上的差異是，裡面的人物動作、表情、情緒等細節的優化。','scope':'Method taxonomy and performance optimization; no new media acceptance or unpause of parallel editing.','established_methods':6,'research_methods':2,'mandatory_accepted_footage_comparison':False}
(Path(__file__).parent/'user_clarification.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=root/'10_automation/runs/2026-W45/reels/M04/editorial_reset_2026-11-06/REVIEW.md'
text=p.read_text(encoding='utf-8-sig')
marker='## 下一輪的具體工作\n'
text=text.replace(marker,marker+'\n最新澄清：六種方法與兩種研究方法已確認。這次要改善的是選定方法內的人物動作、表情、情緒細節；M04不因退件就必須換方法，依實際看點決定。完整原話見 `10_automation/workflow_audits/2026-11-06_methods_performance/user_clarification.json`。\n',1)
p.write_text(text,encoding='utf-8')
print('Updated method/performance clarification in current workflow records; no media changed.')
