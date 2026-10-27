import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[5]
run = root / '10_automation/runs/2026-W37'
reels = run / 'reels'
source = reels / 'videos/M01_A_L01_fixed_full_v1_01.mp4'
scan = json.loads((reels / 'qa/M01_A_L01_fixed_full_v1_01/decode_scan.json').read_text(encoding='utf-8'))
record = dict(reel_id='2026-W37-M01-reel',look_id='2026-W37-004-L01',trial_id='M01_A_L01_fixed_full_v1_01',date='2026-10-01',
              status='decoded_sampled_review_complete_continuous_qa_pending',
              source_post_url='https://grok.com/imagine/post/6ff969d3-1fb5-4c34-b459-852b355c6eb0?conversation=3b3e5491-81b8-4cb3-8337-019b36c8a6ce',
              input_still='10_automation/runs/2026-W37/generated_images/2026-W37-004/looks/2026-W37-004-L01/reel/2026-W37-004-L01_M01_S01_full_start_candidate_v1.png',
              still_user_approval='可以，沿用這張',input_role='Single First frame, Add last frame control visible; no Last frame.',
              identity_reference='No separate saved character reference attached. Approved near-frontal outfit still is identity input.',
              prompt_path='10_automation/runs/2026-W37/reels/prompts/M01_A_L01_motion_v1.md',
              ui_settings=dict(resolution='720p',duration='6s',audio='off (checkbox0 confirmed)',model='unnamed in visible UI'),
              video=dict(output_path=str(source.relative_to(root)).replace('\\','/'),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),resolution=[720,1264],fps=24,duration_seconds=145/24),
              qa=dict(decode_scan=scan,sample_sheet='reels/qa/M01_A_L01_fixed_full_v1_01/checkpoints.jpg',
                      sampled_review='Nine timepoints inspected. Near-frontal face, gray ankle-clear trousers and burgundy T intersections remain readable; complete shoes remain in frame. Slight scale increase with the short approach; no obvious sampled background morph. Initial waiting may be trimmed. Full playback, foot/strap motion and eventual two-look cut still pending.',
                      provisional_selection_seconds=[.75,4.5],usable_seconds=None,continuous_watch_done=False,user_visual_approval=None),
              time=dict(active_minutes=None,generation_wait_minutes=None),
              upload=dict(status='assistant_upload_success',method='waitForEvent(filechooser) then tab.click(actual AX Upload media button) then chooser.setFiles; verify exact filename checkbox selected and First-frame attachment.',prior_failure_cause='Unresolved; do not conclude permanent unavailable capability.'))
(reels / 'M01_A_L01_fixed_full_v1_01.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest_path = reels / 'production_manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
item = next(r for r in manifest['reels'] if r['model_profile_id']=='M01')
trial = dict(trial_id=record['trial_id'],output_path=record['video']['output_path'],source_url=record['source_post_url'],record_path='10_automation/runs/2026-W37/reels/M01_A_L01_fixed_full_v1_01.json',qa=record['status'],motion_result=None)
item['generation']['trials']=[t for t in item['generation']['trials'] if t.get('trial_id')!=record['trial_id']]+[trial]
item['generation'].update(settings='Single First frame, no saved character;720p,6s,audiooff;actual720x1264/24fps/145frames.',prompt_version='M01_A_L01_motion_v1')
item['storyboard'][0].update(source_video=record['video']['output_path'],dynamic_status=record['status'])
item['storyboard'][1]['plan']='Matched full-person scale, eye/shoe positions and left daylight; natural weight shift and one very short planting step, avoiding forward approach that might crop shoes.'
item['status']='A_motion_sampled_review_complete_B_full_still_generating'
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('M01 A motion and successful delegated upload recorded.')
