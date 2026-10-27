import json, hashlib
from pathlib import Path

root = Path(__file__).resolve().parents[2]
work = root / '10_automation/runs/2026-W41/reels/M02'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

receipt_path = work/'B_attempt_01/browser_receipt.json'
if receipt_path.exists():
    raise FileExistsError('Preserve existing source receipt.')
receipt = read(work/'A_attempt_01/browser_receipt.json')
receipt.update(shot='B', first_frame='2026-W41-003-L02_M02_reel_candidate_A_v3.png',
    submitted_at='2026-10-08T08:11:51.775Z',
    submission_evidence='Timestamp captured immediately before fresh AX Send; form cleared. Result page displays exact prompt and M02 saved-reference chip.',
    result_url='https://grok.com/imagine/post/be4dc480-d7dd-4dc8-84dc-058505d94959?conversation=61863cf1-b489-42e6-ab5e-d0d9779acb21',
    sha256=hashlib.sha256((work/'B_attempt_01/source.mp4').read_bytes()).hexdigest(),
    sampled_review='25 full-frame and5 face checkpoints plus all145 consecutive lower-body windows inspected. Short approach, trailing-foot catch-up, followed by small stance opening; not exact single foot placement. No apparent gross shoe/pants collapse or foot teleport. Face, outfit and cafe broadly coherent in inspected samples; continuous normal-speed review pending.')
assert receipt['sha256']=='7924c288d65aacf9ce831d14787e95c349441a5e4ae5229510dff3155125e0c5'
save(receipt_path,receipt)
inspection = read(work/'QA_B01/inspection.json')
inspection['assistant_static_dynamic_review']=receipt['sampled_review']
save(work/'QA_B01/inspection.json',inspection)
lower=read(work/'QA_B01_lower/lower_body_inspection.json')
lower['lower_body_visual_result']='All145 consecutive native windows viewed. Forward-foot movement, trailing-foot catch-up and later small stance opening occur. No apparent gross deformation, missing shoe or foot teleport in inspected windows. Normal-speed comfort remains unestablished.'
save(work/'QA_B01_lower/lower_body_inspection.json',lower)
print('M02 B source and inspection evidence recorded.')
