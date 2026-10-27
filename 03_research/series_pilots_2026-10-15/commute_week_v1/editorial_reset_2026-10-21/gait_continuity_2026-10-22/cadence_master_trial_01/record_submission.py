from pathlib import Path
import hashlib,json
d=Path(__file__).resolve().parent
r={'date':'2026-10-22','status':'single_cadence_request_acknowledged_thinking','first_frame_asset_id':'b43b2900-fe9c-48f9-9193-fcd2e8d396f7','asset_ids':['6236309c-2343-41e6-985c-994239ff744a','ac9ede4e-1715-4518-95b4-bda341a62061'],'last_frame_asset_id':None,'keyframes':None,'duration':'6','resolution_name':'720p','aspect_ratio':'9:16','target_not_measured_result':'Brisk uniform alternating footfalls around0.5–0.6s, full person constant scale; no retiming','prompt':'grok_prompt.txt','prompt_sha256':hashlib.sha256((d/'grok_prompt.txt').read_bytes()).hexdigest(),'first_still_user_approval':'../../../F04_full_start_01/user_still_approval.json','allowed_generations':1,'submitted_requests':1,'automatic_retry':False,'actual_parameter_acceptance':None,'source':None,'full_film_modified':False,'UI_evidence':['submission_dom.txt','submission.png'],'next':'Download unique source, inspect native gait tempo/feet and source-only comparison, not append to final film before user pace feedback.'}
# Path from this folder to the existing F04 gate is two levels up within editorial reset.
r['first_still_user_approval']='../../F04_full_start_01/user_still_approval.json'
(d/'submission_receipt.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('One native-speed gait sample requested; no whole-film change.')

