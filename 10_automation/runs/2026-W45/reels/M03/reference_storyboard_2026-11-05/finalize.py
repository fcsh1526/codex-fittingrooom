from pathlib import Path
import json, hashlib, subprocess, sys, os
from PIL import Image

P=Path(__file__).resolve().parent; ROOT=P.parents[5]; W=ROOT/'10_automation/runs/2026-W45'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()

env=dict(os.environ);env['PYTHONIOENCODING']='utf-8'
r=subprocess.run([sys.executable,str(ROOT/'11_skills/mira-reel-director/scripts/plan.py'),'validate',str(P/'production_plan.json'),'--project-root',str(ROOT)],capture_output=True,text=True,encoding='utf-8',env=env)
validation=json.loads(r.stdout);assert not validation['errors'],validation
put(P/'planning_validation.json',validation)
with Image.open(P/'timing_animatic.gif') as im:
    durations=[]
    for i in range(im.n_frames):im.seek(i);durations.append(im.info['duration'])
assert sum(durations)==9000, sum(durations)
qa=read(P/'layout_preflight.json');qa['status']='static_layout_and_storyboard_visually_reviewed_not_motion_approved'
qa['assistant_review']={'viewed':['storyboard.png','approved_stills_layout.png','key_03.png','key_06.png'],
 'finding':'Initial photo layout shows complete heads/shoes and hands/bags. Sketch visibly changes pose/foot placement and scale; end lower legs intentionally outside picture. Narrow-panel margins need actual source verification.',
 'not_certified':['realistic acting','gait or contact','exact perspective','generator ability','continuous native-speed footage','user acceptance']}
put(P/'layout_preflight.json',qa)
snapshots=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts']
for item in snapshots:assert sha(ROOT/item['snapshot_path'])==item['sha256'],item['snapshot_path']
protected={
 'reels/M01/paired_review_v1/M01_W45_two_looks_review_v1.mp4':'aa1a657e88480a966226bdbf72ea3e5c46346290df154408d376ebcc2b27a2fb',
 'reels/M02/trial_03/M02_W45_trial03_silent_review.mp4':'bf1828d34ce61ac76e82d1573a49e85d8403d5a5ae9be9bb8be46c16fa114b67',
 'reels/M03/natural_parallel_2026-11-05/paired_review_v1/M03_W45_natural_parallel_review_v1.mp4':'13cd4260052fb452e396d2293874e0fa7496b0dfee868c8702e4c004621d072c'}
for path,digest in protected.items():assert sha(W/path)==digest,path

old='新線稿與必要預檢尚待完成，未新增生成。'
new='使用者後續ok接續後，9秒新連接線稿、構圖節奏示意及核准首圖雙欄預檢已完成，見 `10_automation/runs/2026-W45/reels/M03/reference_storyboard_2026-11-05/REVIEW.md`。新稿以完整輪廓→短步／角度→靠近收尾，末段提出輕抬鏡保留頭頂；仍待新稿視覺回饋及單側實測，沒有新增生成。'
for name in ['CURRENT_STATUS.md','10_automation/CANONICAL_WORKFLOW.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W45/publishing_structure.md']:
    path=ROOT/name;text=path.read_text(encoding='utf-8-sig');assert text.count(old)==1,name;text=text.replace(old,new)
    if name.endswith('publishing_structure.md'):
        text=text.replace('| M03 | 同件柔肩西外，工作直褲與休閒淺裙兩種拆搭 | 2 | 2 | 10.5秒 | [M03](planning/M03/SHOT_CARDS.md) |','| M03 | 同件柔肩西外：完整輪廓→短步／角度→靠近看層次 | 2 | 2 | 新稿9秒 | [新連接分鏡](reels/M03/reference_storyboard_2026-11-05/REVIEW.md) |')
        text=text.replace('依[參考落實檢討](reels/M03/reference_execution_audit_2026-11-05/REVIEW.md)重做連接分鏡。','[新9秒分鏡與預檢](reels/M03/reference_storyboard_2026-11-05/REVIEW.md)已完成，先看具體內容發展及靠近取景，再做單側測試。')
    if name.endswith('MIRA_EDITORIAL_HANDOFF.md'):
        text=text.replace('目前下一步：依M03參考落實檢討，完成參考機制對照的連接線稿與實際並排尺度預檢；不再重貼6.04秒片待審，不直接追加生成。','目前下一步：M03新9秒線稿／構圖節奏示意已完成，檢視具體內容發展與末段靠近／輕抬鏡後，先單側測試；不重貼舊6.04秒片待審。')
    path.write_text(text,encoding='utf-8')
q=read(W/'production_queue.json')
q.update(status='M03_reference_storyboard9s_preflight_completed_pending_visual_review',
 active_reviews=[rel(P/'storyboard.png'),rel(P/'timing_animatic.gif')],
 active_trial=None, latest_editorial_proposal=rel(P/'production_plan.json'),
 next={'model':'M03','action':'Review concrete9s connected storyboard, actual layout and approach/re-aim framing. Then one L01 motion test using approved still, not both looks automatically.'})
put(W/'production_queue.json',q)
rp=ROOT/'04_prompts/material_pool/series_registry.json';reg=read(rp)
s=next(x for x in reg['series'] if x['series_id']=='SERIES_W45_M03')
s.update(status='reference_storyboard9s_preflight_completed_pending_visual_review',current_reassessment=rel(P/'REVIEW.md'),latest_editorial_proposal=rel(P/'production_plan.json'))
if rel(P/'production_plan.json') not in s['proposal_paths']:s['proposal_paths'].append(rel(P/'production_plan.json'))
put(rp,reg)
put(P/'verification.json',{'date':'2026-11-05','storyboard_sha256':sha(P/'storyboard.png'),'animatic_sha256':sha(P/'timing_animatic.gif'),
 'animatic_frames':len(durations),'animatic_duration_ms':sum(durations),'structure_errors':validation['errors'],
 'ready_for_generation':validation['ready_for_generation'],'immutable_snapshots_verified':len(snapshots),
 'accepted_M01_M02_unchanged':True,'old_M03_unchanged':True,'new_AI_stills':0,'new_Grok_jobs':0,
 'user_visual_acceptance':None,'publication_approval':None,'no_IG_browser_operations':True})
print(json.dumps({'board_completed':True,'animatic_seconds':sum(durations)/1000,'snapshots_unchanged':len(snapshots),'new_generation':0}))
