from pathlib import Path
import json, hashlib

d=Path(__file__).resolve().parent
p=d/'user_storyboard_review_request.json'
r=json.loads(p.read_text(encoding='utf-8'))
assert hashlib.sha256((d/'half_shot_board.png').read_bytes()).hexdigest() == r['sha256']
receipt={'date':'2026-10-22','question_item_id':'["request_user_input_async","call_d75b83345de049bdbeaf7b81e72d6e5e",0]','artifact':r['artifact'],'sha256':r['sha256'],'question':r['question'],'answer':'採用第五套全身推近半身','status':'user_selected_exact_storyboard_direction','scope':'Keep accepted four-look preview; prepare one compatible F05 head-to-mid-thigh late candidate after approved full-person first; exact still visual approval still required before new video. Budget~21.3s not generated outcome.','new_half_still_approved':False,'F05_motion_approved':False,'complete_film_approved':False,'prior_full_late_still_approved':False}
(d/'user_storyboard_approval.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
r.update(answer=receipt['answer'],status=receipt['status'],approval_receipt='user_storyboard_approval.json')
p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Exact half-shot storyboard direction recorded; new photograph approval still pending.')
