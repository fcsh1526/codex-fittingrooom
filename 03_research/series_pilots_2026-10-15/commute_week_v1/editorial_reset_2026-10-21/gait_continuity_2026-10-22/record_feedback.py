from pathlib import Path
import json
d=Path(__file__).resolve().parent
base=d.parent
project=next(p for p in d.parents if (p/'CURRENT_STATUS.md').exists())
five=base/'F05_half_motion_01/five_look_review_2026-10-22'
request_path=five/'user_review_request.json'
r=json.loads(request_path.read_text(encoding='utf-8'))
quote='運鏡及半身都可以，但是整體的走路步驟太慢，或這是各鏡的走路步驟不連續，忽快忽慢'
feedback={'date':'2026-10-22','question_item_id':'["request_user_input_async","call_5d3a3570c6aa4140bce9b917cc1962a4",0]','artifact':r['artifact'],'sha256':r['sha256'],'question':r['question'],'answer':quote,'status':'camera_and_half_direction_accepted_gait_revision_requested','camera_and_half_direction_accepted':True,'whole_film_accepted':False,'gait_or_transition_continuity_accepted':False,'background_acceptance_inferred':False,'normal_speed_full_playback_self_report':None,'scope':'Keep camera/half-shot direction. Diagnose source cadence versus step-phase mismatch and overlapping feet, then a single bounded source-paced walking sample; no automatic redoing five shots, retiming, or public delivery.'}
(five/'user_film_feedback.json').write_text(json.dumps(feedback,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
r.update(answer=quote,status=feedback['status'],feedback_receipt='user_film_feedback.json')
request_path.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(d/'user_feedback.json').write_text(json.dumps(feedback,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Exact gait feedback recorded. Camera/half direction retained; whole film not accepted.')

