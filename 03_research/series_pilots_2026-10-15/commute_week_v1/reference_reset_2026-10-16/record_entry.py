import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
root=Path.cwd(); base=root/'03_research/series_pilots_2026-10-15/commute_week_v1/reference_reset_2026-10-16'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
rel='03_research/series_pilots_2026-10-15/commute_week_v1/urban_commute_v3/U01_user_still_approval_2026-10-15.json'
approval=json.loads((root/rel).read_text(encoding='utf-8-sig'))
image=root/approval['file']
assert sha(image)==approval['sha256']
refs=[('02_brand/reference_models/M03_start_v3_face.png','6236309c-2343-41e6-985c-994239ff744a','face identity'),('02_brand/reference_models/M03_start_v3_full.png','ac9ede4e-1715-4518-95b4-bda341a62061','body proportions only')]
entry={'recorded_date':'2026-10-16','created_at_utc':datetime.now(timezone.utc).isoformat(),'shot_id':'R01','model_id':'M03','look_id':'ED-W42-COMMUTE-V1-L01','status':'submitted_generation_pending','generation_count_requested':1,'still_approval':{'receipt':rel,'receipt_sha256':sha(root/rel),'file':approval['file'],'sha256':sha(image),'pixels':Image.open(image).size,'user_quote':approval['user_quote'],'asset_id':'34793323-1f6a-4db7-ab21-5c2c9d5fd44b','input_role':'first frame and wardrobe/scene'},'identity_references':[{'path':p,'sha256':sha(root/p),'asset_id':u,'role':role} for p,u,role in refs],'prompt':{'path':str((base/'R01_motion_prompt.txt').relative_to(root)).replace(chr(92),'/'),'sha256':sha(base/'R01_motion_prompt.txt')},'requested_settings':{'seconds':6,'resolution':'720p','aspect_ratio':'9:16','last_frame':None,'audio':'off if exposed; otherwise preserve and locally strip'},'actual_selected_settings':None,'source_motion_approval':None,'single_shot_preview_only':True,'whole_five_look_approval':None,'new_stills_generated':0,'publishing_files_replaced':[]}
with (base/'entry_receipt.json').open('x',encoding='utf8') as f: json.dump(entry,f,ensure_ascii=False,indent=2)
print(json.dumps({'entry_saved':True,'still_hash_verified':True,'references_present':len(refs)},ensure_ascii=False))

