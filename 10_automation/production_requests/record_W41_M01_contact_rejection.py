import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
run=root/'10_automation/runs/2026-W41'
work=run/'reels/M01'
receipt_path=work/'review_v1/composition_receipt.json'
receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
film=root/receipt['output_path']
assert hashlib.sha256(film.read_bytes()).hexdigest()==receipt['sha256']
feedback=dict(date='2026-10-08',model='M01',file=receipt['output_path'],sha256=receipt['sha256'],user_quote='第二鏡頭的袖口動作是虛的，手跟衣服沒有互動',decision='rejected_hand_cloth_contact',scope='second shot; no acceptance of first shot inferred',source='10_automation/runs/2026-W41/reels/M01/B_attempt_01/source.mp4',source_sha256=hashlib.sha256((work/'B_attempt_01/source.mp4').read_bytes()).hexdigest(),response='Keep A original bytes and approved B first frame. One B retry with visible thumb/index contact at actual folded cuff edge on forearm, cloth response and release; inspect consecutive contact frames. Original film retained as failed version.')
(work/'review_v1/user_feedback_2026-10-08.json').write_text(json.dumps(feedback,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
receipt.update(status='user_rejected_B_hand_cloth_contact',user_approval=None,user_feedback='user_feedback_2026-10-08.json')
receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest_path=run/'reels/production_manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
record=next(r for r in manifest['reels'] if r['model_profile_id']=='M01')
record.update(status='B_contact_rejected_retry_in_progress')
record['qa'].update(status='user_rejected_B_hand_cloth_contact',user_approval=None,feedback=feedback)
record.setdefault('revision_history',[]).append(dict(file=receipt['output_path'],sha256=receipt['sha256'],status=receipt['status'],feedback=feedback['user_quote']))
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Rejected M01 B contact recorded; source and failed cut preserved.')
