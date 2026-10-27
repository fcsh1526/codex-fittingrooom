from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[5]
DELIVERY = Path(__file__).parent
manifest_path = DELIVERY / 'google_drive_delivery_2026-10-08.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
for reel in manifest['reels']:
    src = ROOT / reel['source_path']
    data = src.read_bytes()
    assert hashlib.sha256(data).hexdigest() == reel['sha256'], reel['model']
    reel['size_bytes'] = len(data)
    reel['md5'] = hashlib.md5(data).hexdigest()
    reel['caption_local_path'] = str((DELIVERY / (reel['number'] + '_' + reel['title'] + '_貼文文字.txt')).relative_to(ROOT)).replace('\\', '/')
    (ROOT / reel['caption_local_path']).write_text(reel['caption'] + '\n', encoding='utf-8')
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
approval = {k: manifest[k] for k in ['approved_on','user_approval_quote','approval_scope','continuous_watch_done']}
approval['films'] = [{k: r[k] for k in ['model','source_path','sha256','size_bytes']} for r in manifest['reels']]
approval_path = DELIVERY / 'batch_film_user_approval_2026-10-08.json'
approval_path.write_text(json.dumps(approval, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
approval_ref = str(approval_path.relative_to(ROOT)).replace('\\', '/')
by_model = {r['model']: r for r in manifest['reels']}
for path, collection, model_key in [
    (ROOT / '10_automation/runs/2026-W41/reels/production_manifest.json', 'reels', 'model_profile_id'),
    (ROOT / '10_automation/production_requests/2026-10-08_next_five_reels.json', 'slots', 'model'),
    (ROOT / '10_automation/runs/2026-W41/reels/batch_storyboard.json', 'films', 'model'),
]:
    doc = json.loads(path.read_text(encoding='utf-8-sig'))
    for item in doc[collection]:
        model = item.get(model_key) or item.get('model_profile_id')
        if model not in by_model:
            continue
        reel = by_model[model]
        key = 'output_status' if collection == 'films' else 'status'
        item[key] = 'film_user_approved_drive_delivery_preparing_proof_and_carousel_incomplete'
        item['film_user_approval'] = approval_ref
        item['accepted_picture_file'] = reel['source_path']
        if collection == 'films':
            item['user_video_approval'] = approval_ref
        if isinstance(item.get('qa'), dict):
            item['qa']['user_approval'] = approval_ref
            item['qa']['continuous_watch_done'] = False
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'verified_films': len(manifest['reels']), 'bytes': sum(r['size_bytes'] for r in manifest['reels']), 'captions': [len(r['caption'].replace('\n','')) for r in manifest['reels']]}, ensure_ascii=False))
