import csv
import hashlib
import json
from pathlib import Path
from PIL import Image

BASE=Path(__file__).resolve().parent
ROOT=next(p for p in BASE.parents if (p/'10_automation').is_dir())
JOB=ROOT/'10_automation/runs/2026-W37/generated_images/2026-W37-001/looks/2026-W37-001-L02/reel/body_distance_matched_start_v2'
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,data):
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

selected=JOB/'2026-W37-001-L02_M02_body_distance_matched_start_candidate_v3.png'
prior=JOB/'2026-W37-001-L02_M02_body_distance_matched_start_candidate_v2.png'
with Image.open(selected) as im:
    im.load()
    size=list(im.size)
old_path=JOB/'generation_receipt_v2.json'
old=json.loads(old_path.read_text(encoding='utf-8'))
old.update(status='retained_superseded_wardrobe_strap_failed_before_user_review',independent_review_status='v2_failed_dark_blue_strap',superseded_by=selected.name,publishable=False)
save(old_path,old)
new=dict(old)
new.pop('superseded_by',None)
new.update(status='pending_user_visual_approval',selected_asset=selected.relative_to(ROOT).as_posix(),selected_sha256=sha(selected),actual_size=size,generation_count=3,base_generation_count=1,targeted_edit_count=2,targeted_edit=['person_distance','tote_strap_wardrobe_regression'],
           prompt_files=['matched_B_start_v2_prompt.txt','matched_B_start_v2_distance_edit_prompt.txt','matched_B_start_v3_strap_edit_prompt.txt'],
           independent_review='03_research/ig_saved_ootd_study_2026-10-06/backward_step_trial/qa/matched_B_start_v2/independent_review_v3.md',independent_review_status='pending_at_recording',user_approval=None,uploaded_to_Grok=False,video_generated_from_selected_still=False,publishable=False)
new['additional_targeted_edit_exception']={'reason':'Independent QA found a concrete inherited L01 dark-blue strap on the L02 grey tote. Corrected that wardrobe regression before requesting user approval, while preserving selected geometry.','count_honesty':'One base plus two targeted edits; exceeds the normal skill one-edit guideline. No competing Hero or global rule change. All variants retained.','further_edits_planned':False}
new['last_edit_input']={'path':prior.relative_to(ROOT).as_posix(),'sha256':sha(prior),'role':'person-position/outfit edit target except erroneous strap'}
new['root_static_review']['tote_strap']='Visible grey canvas strap matching grey tote restored; body/head/feet and main scene geometry visually retained from v2.'
save(JOB/'generation_receipt_v3.json',new)
with (JOB/'PROMPTS.md').open('a',encoding='utf-8') as f:
    f.write('\n\n## Additional wardrobe regression correction\n\nThe independent v2 check found an inherited dark-blue strap. This is one extra targeted strap correction beyond the normal one-edit guideline; one base plus two edits are recorded, all variants preserved, no further edit planned. Selected v3 remains pending individual user approval.\n\n'+(BASE/'matched_B_start_v3_strap_edit_prompt.txt').read_text(encoding='utf-8'))
with (JOB/'review_sheet.csv').open('r',encoding='utf-8-sig',newline='') as f:
    reader=csv.DictReader(f)
    columns=reader.fieldnames
    rows=list(reader)
for r in rows:
    r.update(status='superseded_failed_tote_strap_before_user_approval',publishable='no')
rows.append({'filename':selected.name,'publishable':'no','status':'candidate_pending_user_visual_approval','notes':'One additional strap-only correction restores grey canvas shoulder strap. Head alignment closer to A actualf96; remaining shoes/proportions difference preserved. Static independence/user approval/dynamic success separate.'})
with (JOB/'review_sheet.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)

mp=BASE/'trial_manifest.json'
m=json.loads(mp.read_text(encoding='utf-8'))
m.update(status='near_A1_and_B1_sampled_pass_native_join_failed_matched_B_v3_pending_user_approval',new_stills_generated=5)
m['matched_second_start'].update(path=selected.relative_to(ROOT).as_posix(),sha256=sha(selected),status='pending_user_visual_approval',generation_receipt=(JOB/'generation_receipt_v3.json').relative_to(ROOT).as_posix(),targeted_edit_count=2,additional_strap_correction=True)
m['matched_second_start'].pop('single_targeted_edit',None)
save(mp,m)
for name in ('README.md','revised_storyboard_v3.md'):
    with (BASE/name).open('a',encoding='utf-8') as f:
        f.write('\n\n### Selected static candidate v3\n\nIndependent v2 QA found the L01 dark-blue strap inherited into the L02 grey tote. A strap-only correction produced selectedv3, SHA `'+sha(selected)+'`, actual941×1672. Onebase+two targetededits are retained and honestly recorded as one additional wardrobe-regression correction beyond the normal one-edit guideline. Root visible review sees greystrap restored and v2 person/scene geometry retained; independentv3 QA and user still approval remain separate. No new B generation or upload from this still. Prompt/receipt in L02 `reel/body_distance_matched_start_v2/`.\n')

sp=ROOT/'CURRENT_STATUS.md'
s=sp.read_text(encoding='utf-8')
head='''## Matched B candidate v3: grey tote strap corrected; new still approval pending — 2026-10-06

Independent matched-start v2 QA found inherited L01 dark-blue strap on the L02 grey tote, so v2 is not submitted for user approval. One additional strap-only correction produced selected941×1672 v3, SHA `f8098adfefc9be66ffcfea9bc3bad424e3f5e34a30a343d50dc4478f10af16e6`, under L02 `reel/body_distance_matched_start_v2/`. Actual count is onebase+two targetededits (distance then wardrobe regression), an explicitly logged exception to the normal one-edit guideline; no third edit planned. Root visible review sees greystrap restored and v2 person/head/feet/main-room geometry retained; independent v3/static user approval remains pending. New still has not been uploaded to Grok or dynamically tested. A/B sources and rejected8.25s diagnostic retained, first-wave five/old research protected hashes verified at composition. No cloud write, publication, speed change, text/audio or global template. Prior v2/pending-generation notes below historical.

'''
s=s.replace('# Current Status - Mira AI Fashion Creator\n\n','# Current Status - Mira AI Fashion Creator\n\n'+head,1)
sp.write_text(s,encoding='utf-8')
pp=ROOT/'10_automation/runs/2026-W37/publishing_structure.md'
p=pp.read_text(encoding='utf-8-sig')
note='**M02固定鏡位距離研究（2026-10-06）：** 近起點A退遠及原B走近抽查可用；原生8.25秒試剪的0.75秒疊加仍有明顯雙臉，接點未通過，診斷檔保留。新B起點按實際A f96／4秒重設人物距離與圖書館幾何；selectedv3已修回灰托特肩帶，仍待逐張視覺核准，未送Grok或動態驗收。完整分鏡／來源／提示／失敗與核准狀態見 `03_research/ig_saved_ootd_study_2026-10-06/backward_step_trial/`。第一波五支與Drive維持；研究不代表發布成效或通用模板。\n\n'
p=p.replace('# W37 Publishing Structure\n\n','# W37 Publishing Structure\n\n'+note,1)
pp.write_text(p,encoding='utf-8')
print(json.dumps({'selected':str(selected),'sha256':sha(selected),'status':m['status'],'base_plus_edits':[1,2]},ensure_ascii=False))
