import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'M03_L01_full_detail_review_v3_soft_05s_01.json'
d=json.loads(p.read_text(encoding='utf-8-sig'))
d['qa']['visual_sample_review']='Start, ending and all overlap-frame intervals inspected. Full shot retains hair and shoes; detail remains faceless. The longer dissolve visibly overlaps two scales briefly. No claim of continuous playback or user comfort acceptance.'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Sample review recorded; continuous user acceptance pending.')
