from pathlib import Path
import json,hashlib,csv
from PIL import Image
root=Path(__file__).resolve().parents[2];base=Path(__file__).resolve().parent
p=base/'A_start_still_receipt.json';r=json.loads(p.read_text(encoding='utf-8'));asset=root/r['file']
r.update(sha256=hashlib.sha256(asset.read_bytes()).hexdigest(),native_pixels=list(Image.open(asset).size));p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=base/'reference_observation.json';d=json.loads(p.read_text(encoding='utf-8'));d['new_media']['still_calls']=1;d['new_media']['candidate']=r['file'];d['new_media']['static_user_approval']=None;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=asset.parent.parent/'review_sheet.csv'
with p.open(encoding='utf-8-sig',newline='') as f:
 reader=csv.DictReader(f);rows=list(reader);fields=reader.fieldnames
identifier='2026-W41-003-L01_foreground_start_v1'
if not any(row['prompt_id']==identifier for row in rows):
 rows.append(dict(carousel_id='2026-W41-003',look_id='2026-W41-003-L01',prompt_id=identifier,model_profile_id='M02',candidate_file='foreground_transition_2026-10-14/'+asset.name,tool='Codex built-in image_gen',publishable='not_assessed',status='candidate_pending_user_visual_approval',notes='New cafe-corner full-person source with real near foreground wall at image-right. Identity and plain wardrobe sampled native still review complete. User gate pending; no motion or architectural matching claim.'))
 with p.open('w',encoding='utf-8',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
print(json.dumps({'sha256':r['sha256'],'pixels':r['native_pixels'],'new_image_calls':1,'grok_submissions':0}))
