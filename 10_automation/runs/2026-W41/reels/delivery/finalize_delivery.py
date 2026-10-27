from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[5]
DELIVERY = Path(__file__).parent
manifest_ref = '10_automation/runs/2026-W41/reels/delivery/google_drive_delivery_2026-10-08.json'
approval_ref = '10_automation/runs/2026-W41/reels/delivery/batch_film_user_approval_2026-10-08.json'
manifest = json.loads((ROOT / manifest_ref).read_text(encoding='utf-8'))
assert manifest['status'] == 'drive_delivery_verified_ready_for_grok_bot_handoff'
by_model = {r['model']: r for r in manifest['reels']}
for rel, collection, model_key in [
    ('10_automation/runs/2026-W41/reels/production_manifest.json', 'reels', 'model_profile_id'),
    ('10_automation/production_requests/2026-10-08_next_five_reels.json', 'slots', 'model'),
    ('10_automation/runs/2026-W41/reels/batch_storyboard.json', 'films', 'model'),
]:
    path = ROOT / rel
    doc = json.loads(path.read_text(encoding='utf-8-sig'))
    changed = 0
    for item in doc[collection]:
        model = item.get(model_key) or item.get('model_profile_id') or item.get('reel_id', '').split('-')[-2]
        if model not in by_model:
            continue
        r = by_model[model]
        item['output_status' if collection == 'films' else 'status'] = 'film_user_approved_drive_delivered_proof_and_carousel_incomplete'
        item['film_user_approval'] = approval_ref
        item['accepted_picture_file'] = r['source_path']
        item['drive_delivery_receipt'] = manifest_ref
        item['video_drive'] = r['video_drive']
        item['caption_doc'] = r['caption_doc']
        item['publication_status'] = 'not_published'
        if collection == 'films':
            item['user_video_approval'] = approval_ref
            item['output_path'] = r['source_path']
        if isinstance(item.get('qa'), dict):
            item['qa']['status'] = 'sampled_QA_complete_user_film_approved_continuous_playback_not_recorded'
            item['qa']['user_approval'] = approval_ref
            item['qa']['continuous_watch_done'] = False
        changed += 1
    assert changed == 5, (rel, changed)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

registry_path = ROOT / '10_automation/google_drive_archive_registry.json'
registry = json.loads(registry_path.read_text(encoding='utf-8-sig'))
registry['updated_date'] = '2026-10-08'
registry['weeks']['2026-W41'] = {
    'id': manifest['drive_folder']['id'], 'name': '2026-W41',
    'parent_id': registry['root']['id'], 'path': '800.Codex IG/2026-W41',
    'url': manifest['drive_folder']['url'],
    'first_wave': 'Five exact user-approved clean Reel masters, five native Google Docs captions and one native handoff Doc, verified by connector readback. No IG posting performed.',
    'handoff_document': manifest['handoff_doc'], 'delivery_receipt': manifest_ref,
}
registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

summary = (
    '## W41 five films approved and delivered to Drive — 2026-10-08\n\n'
    'User explicitly approves all five current films and requests videos/captions in Drive for later Grok bot posting. Exact hashes/bytes and bounded approval recorded in `' + approval_ref + '`. '
    'Accepted: M01 v2 9.5s, M02 v2 9s, M03 v1 11.25s, M04 parallel v1 6s, M05 v1 8s. All clean/audio-free; source motion unchanged, sequential dissolves0.75s; M04 has no internal cut. Approval does not imply a full-playback self-report or assistant continuous watch.\n\n'
    'Verified delivery: [800.Codex IG/2026-W41](' + manifest['drive_folder']['url'] + ') contains5 MP4s,5 native caption Docs and1 [Grok bot handoff Doc](' + manifest['handoff_doc']['url'] + '). Local receipt `' + manifest_ref + '` links exact source versions to cloud IDs. Source SHA256, remote sizes, folder containment, caption text/paired links, native Doc chips and inherited styles checked; remote checksum not exposed by connector. Previous W37 files/IDs unchanged.\n\n'
    'All five remain not_published; schedule and IG URLs empty. Handoff pairs files, copy-only caption sections, account mira.fitroom.ai, no baked text, optional IG music/cover review, duplicate prevention and24h/72h/7d metrics. No bot connection, IG publication or new public Git sync claimed. Styling-proof/Carousel gaps remain independently incomplete; this delivery closes the requested five-film handoff only.\n\n'
)
status_path = ROOT / 'CURRENT_STATUS.md'
status = status_path.read_text(encoding='utf-8-sig')
header, rest = status.split('\n', 1)
status_path.write_text(header + '\n\n' + summary + rest.lstrip('\n'), encoding='utf-8')

structure_path = ROOT / '10_automation/runs/2026-W41/publishing_structure.md'
structure = structure_path.read_text(encoding='utf-8-sig')
start = structure.index('當前狀態：')
end = structure.index('\n\n## 五支內容', start)
new_status = (
    '當前狀態（2026-10-08）：使用者已明確回覆「全部核准」，五支成片均已核准並交付 Google Drive。'
    '01 M01 格紋 v2（9.5秒）、02 M02 可可棕牛仔褲 v2（9秒）、03 M03 西裝外套 v1（11.25秒）、04 M04 藍色包左右版 v1（6秒）、05 M05 短外套 v1（8秒）。'
    '資料夾含五支 MP4、五份手機可讀的原生 Google 文案文件與一份 Grok bot 交接清單；影片大小、資料夾歸屬、文案內容與相互連結均已回讀確認。'
    '影片無字無音，依序換裝的四支使用0.75秒疊化，左右版無片內切鏡。使用者全批核准不推定其完整播放自述；助理完整原速播放紀錄仍未成立。'
    '五支目前未發布，發布日期與網址留空，後續交由 Grok bot 接續。proof／Carousel 資產仍未完成，不能由成片核准推定核准；原本失敗版本與 W37 檔案皆保留。'
    '\n\nDrive：[800.Codex IG／2026-W41](' + manifest['drive_folder']['url'] + ')；[Grok bot 發布交接清單](' + manifest['handoff_doc']['url'] + ')。'
    '\n\n交付與核准紀錄：`reels/delivery/google_drive_delivery_2026-10-08.json`、`reels/delivery/batch_film_user_approval_2026-10-08.json`。'
)
structure_path.write_text(structure[:start] + new_status + structure[end:], encoding='utf-8')
print(json.dumps({'film_records_updated': 15, 'drive_files': 11, 'week': '2026-W41', 'publication_status': 'not_published'}, ensure_ascii=False))
