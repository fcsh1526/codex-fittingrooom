import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent
manifest_path = BASE / 'trial_manifest.json'
m = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
m['status'] = 'near_start_A1_sampled_gate_passed_B1_submitted'
m['editorial_limit'] = 'New near A start already shows dress hem; the retreat adds shoes and complete proportion. A source is trimmed by actual join geometry, not assumed to match B full master at six seconds.'
m['dynamic_qa'].update(stage='near_A1_sampled_gate_passed', near_start_source='retrieved_reviewed', source_mechanism='near_start_A1_retreat_observed_old_full_start_A1_A2_failed', review_method='25_full_checkpoints_5_head_windows_145_consecutive_native_lower_body_windows', new_composite=None, assistant_continuous_full_watch=False)
m['near_start_attempts'][0].update(mechanism_pass=True, quality_gate='sampled_identity_wardrobe_background_and_continuous_lower_body_sequence_pass', actual_motion='multiple backward steps over most of six seconds, no long final settled hold', information_gain='shoes and complete proportion')
m['near_start_candidate']['purpose'] = 'Closer woman in the same library framing; approved near start already shows hem, retreat reveals shoes and complete proportion.'
m['B_started'] = True
m['B_source_plan'] = 'B_source_plan.md'
m['B_attempts'] = [{'folder':'grok_B_attempt_01','send_clicks':1,'source_retrieved':False,'mechanism_pass':None,'input_receipt':'grok_B_attempt_01/input_receipt.json'}]
manifest_path.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

status_path = ROOT / 'CURRENT_STATUS.md'
s = status_path.read_text(encoding='utf-8-sig')
head = """## M02 near-start approved; real retreat sampled pass; second look generating — 2026-10-06

User `ok` individually approved near-start v2 SHA `e85778d9d38b7541cc5cf96fb73ea047c26da22c8179fe10b8c30f5c38356cb7`; approval receipt stored beside that still. One new A submission completed and downloaded: `near_start_A_attempt_01/source.mp4`, SHA `be49906fa1ec7397bb456acc1ce7947325e71b4ce5a0692d7235d878ad6017ea`, actual720×1280/24fps/145frames/6.041667s. Root and independent 25 full checkpoints, 5 head windows and all145 consecutive native lower-body windows show whole-person retreat, shoes entering and room landmarks staying broadly fixed; sampled face/wardrobe/background gate passes. Actual motion is multiple backward steps rather than two short steps then a hold. A ending is smaller than approved L02 full; choose actual join geometry instead of using the whole source automatically. B plan saved, one submitted L02 fixed-camera approach from its individually approved full master with M02 v3; source/review pending. No two-look composite or user video approval yet. UI recovery required one fresh tab, exact cause unknown; no generation in failed configuration. No speed change, synchronization, text/audio addition, first-wave replacement, cloud write, publication or global format adoption. Prior notes below are historical.

"""
s = s.replace('# Current Status - Mira AI Fashion Creator\n\n','# Current Status - Mira AI Fashion Creator\n\n'+head,1)
status_path.write_text(s,encoding='utf-8')
print(json.dumps({'manifest':m['status'],'B_started':True,'CURRENT_STATUS':'prepended'},ensure_ascii=False))
