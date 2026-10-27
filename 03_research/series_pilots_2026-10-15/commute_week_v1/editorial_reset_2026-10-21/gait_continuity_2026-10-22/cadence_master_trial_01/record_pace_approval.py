from pathlib import Path
import json
d=Path(__file__).resolve().parent
p=d/'user_pace_review_request.json';r=json.loads(p.read_text(encoding='utf-8'))
a={'date':'2026-10-22','question_item_id':'["request_user_input_async","call_6508e3c1e2d74d099ddfad85f1149af1",0]','artifact':r['artifact'],'sha256':r['sha256'],'question':r['question'],'answer':'右邊較合適，可作步態基準','status':'right_trial_selected_as_gait_pace_reference','reference_source':'cadence_source.mp4','reference_source_sha256':'9707b42d230466ef2c2088a926ec45745d546d717c0fa9756d1b8e52ac0ab21d','reference_asset_id':'192cccdc-1496-4803-95c2-99f6f38a64ac','scope':'Native right-side walking character/cadence is selected as reference for necessary shots. Not permission to drop accepted camera/half design; does not approve new scene/joins/finalfilm/publishing.','source_background_approved':False,'source_direct_insertion_approved':False,'complete_film_approved':False}
(d/'user_pace_approval.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
r.update(answer=a['answer'],status=a['status'],approval_receipt='user_pace_approval.json')
p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Selected native gait reference recorded; necessary source rework may proceed with boundary QA.')

