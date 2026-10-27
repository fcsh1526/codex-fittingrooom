from pathlib import Path
import json, hashlib

d=Path(__file__).resolve().parent
base=d.parent
half=base/'F05_half_late_01'
review_path=half/'user_review_request.json'
r=json.loads(review_path.read_text(encoding='utf-8'))
p=half/r['asset']
assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
a={'date':'2026-10-22','question_item_id':'["request_user_input_async","call_50b27878807e4682b7139c2950cdfe1f",0]','asset':r['asset'],'sha256':r['sha256'],'question':r['question'],'answer':'可以，沿用這張半身圖','status':'user_visual_approved_exact_still','scope':'Exact new F05 half late still with disclosed arm/background differences; permits one six-second full-to-half trial after current controls checked. Does not establish motion path/gait/background/timing or final film approval.','F05_motion_approval':False,'complete_film_approval':False}
(half/'user_still_approval.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
r.update(answer=a['answer'],status=a['status'],approval_receipt='user_still_approval.json')
review_path.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=half/'generation_receipt.json';r=json.loads(p.read_text(encoding='utf-8'))
r.update(status=a['status'],approval_receipt='user_still_approval.json')
p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(d/'preflight.json').write_text(json.dumps({'date':'2026-10-22','status':'approved_inputs_waiting_upload_and_one_trial','first_sha256':'ac588ec1674df43923140e17f46c4734706cf834f2b7f5599aeeec60376f9c82','half_sha256':a['sha256'],'first_approval':'../F05_full_start_01/user_still_approval.json','half_approval':'../F05_half_late_01/user_still_approval.json','storyboard_approval':'../half_integration_2026-10-22/user_storyboard_approval.json','allowed_generations':1,'automatic_retry':False,'duration':'6','resolution_name':'720p','aspect_ratio':'9:16','intended_keyframe_timestamp_s':5.333333333333333,'actual_parameter_acceptance':None,'F05_motion_generated':False,'complete_film_approval':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Exact F05 half-still approval recorded; approved first/half ready for one bounded trial.')
