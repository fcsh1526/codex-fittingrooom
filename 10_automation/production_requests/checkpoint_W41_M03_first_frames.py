import csv, hashlib, json
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[2]
base=root/'10_automation/runs/2026-W41'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
target=base/'reels/M03_full_pair_static_review_2026-10-08.json'
if target.exists(): raise SystemExit('Preserve existing review.')
records=[]
for look,filename,source,prompt in [
 ('2026-W41-004-L01','2026-W41-004-L01_M03_reel_candidate_A_v2.png','exec-6fad12f7-1b4a-4fea-af3b-c262d82adf6f.png','hero_edit_prompt_v2.txt'),
 ('2026-W41-004-L02','2026-W41-004-L02_M03_reel_candidate_A.png','exec-2026bacf-1be0-4355-bc7f-d8b259d7722d.png','hero_production_prompt_v1.txt')]:
    folder=base/f'generated_images/2026-W41-004/looks/{look}/reel'
    p=folder/filename
    with Image.open(p) as im: size=list(im.size)
    assert abs(size[0]/size[1]-9/16)<.002
    rec=dict(look_id=look,file=p.relative_to(root).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),native_pixels=size,
      tool='built-in image_gen',original_generated_name=source,prompt=(folder/prompt).relative_to(root).as_posix(),
      identity_anchors=['02_brand/reference_models/M03_start_v3_face.png','02_brand/reference_models/M03_start_v3_full.png'],
      framing_transform='none',assistant_review='Hair and both shoes visible with generous margin; ordinary body proportions; open lapels, crewneck tee, one cuff fold, plain straight trousers, shoes and image-right shoulder bag readable. Recognizable anchor face/hair in static inspection. Shared left daylight and grounded shadows; full-person scale and walkway layout broadly matched. Dynamic contact and identity/background stability not established.',
      status='assistant_static_pass_user_visual_approval_pending',user_approval=None)
    records.append(rec);save(folder/('generation_receipt_v2.json' if look.endswith('L01') else 'generation_receipt_v1.json'),rec)
    rp=folder/'review_sheet.csv'
    with rp.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f); fields=reader.fieldnames; rows=list(reader)
    for row in rows:
        if row['candidate_file'].endswith('candidate_A.png'):
            row['candidate_file']=filename
            for key in ['model_consistency','body_proportion_consistency','reader_relatability','outfit_clarity','ai_realism','scene_lighting_integration','outfit_continuity','expression_liveliness','pose_variation','canva_frame_fit','commerce_value']: row[key]='4'
            row.update(publishable='pending',status=rec['status'],notes=rec['assistant_review'])
    with rp.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
save(target,dict(week='2026-W41',model='M03',selected_sources=records,generation_calls=3,targeted_edits=1,
    first_attempt=dict(file='10_automation/runs/2026-W41/generated_images/2026-W41-004/looks/2026-W41-004-L01/reel/2026-W41-004-L01_M03_reel_candidate_A.png',status='preserved_superseded_framing',reason='Hair-top margin about5percent; selected v2 widens framing. No animation.'),
    observed_generation_wait_seconds=[43.8,29.1,62.3],active_minutes=None,
    user_approval=None,video_generation='not_started',proof_and_carousel='incomplete'))
p=base/'reels/production_manifest.json';manifest=read(p)
entry=next(x for x in manifest['reels'] if x['model_profile_id']=='M03')
for rec in records:
    view=next(x for x in entry['views'] if x['look_id']==rec['look_id'] and x['role']=='full')
    view.update(source_path=rec['file'],source_type='native_reel_candidate_still',framing_review='assistant_static_pass_user_pending',clarity_review='assistant_static_pass_user_pending',approval=None)
entry['status']='two_full_first_frames_candidate_pending_user_visual_approval'
save(p,manifest)
p=root/'10_automation/production_requests/2026-10-08_next_five_reels.json';req=read(p)
slot=next(x for x in req['slots'] if x['model']=='M03')
slot.update(status=entry['status'],first_frame_candidates=[x['file'] for x in records]);save(p,req)
p=base/'publishing_structure.md';text=p.read_text(encoding='utf-8')
text=text.replace('M03–M04已準備独立Reel/Carousel工作單，尚未生成新素材。','M03兩套輕薄西外全身候選已生成（第一套v2留白修正、第二套v1），待使用者逐張視覺核准後才送Grok；M04已準備獨立Reel/Carousel工作單，尚未生成新素材。')
p.write_text(text,encoding='utf-8')
p=root/'CURRENT_STATUS.md';text=p.read_text(encoding='utf-8');heading='# Current Status - Mira AI Fashion Creator\n\n'
new='## W41 M03 full-person pair prepared; continue current batch before further research — 2026-10-08\n\nUser says `先這樣，繼續做，之後再精進`, keeping current batch production moving. User also interprets reference short walking as approaching a front-mounted camera and slightly bending to start phone recording. This is saved as user observation in `03_research/ig_saved_ootd_study_2026-10-06/self_recording_context_user_observation_2026-10-08.md`; equipment/action not reverified, and this full self-recording sequence is not attributed to approved M02 or imposed on current batch.\n\nM03 two full-person stills now prepared from approved v3 face/full anchors: ivory blazer/white tee/navy straight trousers, then navy blazer/light-grey tee/cream straight trousers. Each blazer open with once-folded cuffs, bag image-right. L01 v1 hair margin was short; one targeted framing edit produced selected v2. L02 uses own wardrobe/anchors and L01v2 only for camera/scene continuity. Three built-in calls total; native portrait files unchanged, no crop/resize. Static face/outfit/framing/contact/light and paired-scale checks completed; exact paths/hashes saved in `reels/M03_full_pair_static_review_2026-10-08.json` under W41. Both selected sources await user visual approval before Grok; no new video, proof or Carousel completion claimed. Planned cuff adjustment requires actual fingers/cloth contact and response per M01 feedback. M01/M02 pictures accepted; M05 film/proof pending, M04 stills pending. Existing W37/Drive files unchanged.\n\n'
assert text.startswith(heading);p.write_text(heading+new+text[len(heading):],encoding='utf-8')
print(json.dumps(dict(status=entry['status'],sources=records),ensure_ascii=False))
