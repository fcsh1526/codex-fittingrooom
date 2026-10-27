import json
from pathlib import Path
root=Path(__file__).resolve().parents[5]
reels=root/'10_automation/runs/2026-W37/reels'
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=reels/'M03_L01_full_detail_review_v4_soft_075s_01.json';d=json.loads(p.read_text(encoding='utf-8-sig'))
d['status']='user_visual_accepted_for_L01_transition_only'
d['qa'].update(user_approval=dict(date='2026-10-01',reply='更舒服',scope='Preference/acceptance of displayed 0.75s L01 junction versus 0.5s. No approval of complete Reel, other tracks or publication.'),continuous_watch_done=True,continuous_watch_evidence='User comfort assessment after displayed full preview; no independent assistant continuous playback claim.')
save(p,d)
p=reels/'production_manifest.json';d=json.loads(p.read_text(encoding='utf-8-sig'));m=next(x for x in d['reels'] if x['model_profile_id']=='M03')
m['status']='L01_transition_075s_accepted_L02_full_preparing'
m['qa']['L01_transition_approval']=dict(record_path='10_automation/runs/2026-W37/reels/M03_L01_full_detail_review_v4_soft_075s_01.json',reply='更舒服',duration_seconds=.75,scope='L01 full-to-detail junction only')
m['edit_feedback_2026_10_01'].update(selected_transition_seconds=.75,adopted_globally=False)
save(p,d)
print('M03 L01 transition preference recorded; full two-look QA still pending.')
