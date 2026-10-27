"""Build five two-look production records without overwriting editorial work."""
import argparse
import csv
import json
from pathlib import Path


def rows(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def build(root, run):
    root, run = Path(root).resolve(), Path(run).resolve()
    looks = rows(run / "weekly_look_plan.csv")
    packet = rows(run / "weekly_content_packet.csv")
    groups = {}
    for look in looks:
        groups.setdefault(look["carousel_id"], []).append(look)
    if len(looks) != 10 or len(groups) != 5 or len({x['look_id'] for x in looks}) != 10:
        raise ValueError("Exactly five themes and ten unique looks are required")
    if set(groups) != {p['carousel_id'] for p in packet}:
        raise ValueError("Look themes must match the weekly packet")
    models = []
    for theme, pair in groups.items():
        if len(pair) != 2 or len({p['model_profile_id'] for p in pair}) != 1:
            raise ValueError(f"{theme}: requires two looks of one model")
        if {str(p['look_order']) for p in pair} != {'1', '2'}:
            raise ValueError(f"{theme}: look orders must be 1 and 2")
        if any(p['week_id'] != run.name for p in pair):
            raise ValueError("Week differs from run directory")
        model = pair[0]['model_profile_id']
        if any(p['model_profile_id'] != model for p in packet if p['carousel_id'] == theme):
            raise ValueError("Packet and look model assignments differ")
        models.append(model)
    if sorted(models) != ['M01', 'M02', 'M03', 'M04', 'M05']:
        raise ValueError("M01–M05 must each appear in exactly one theme")
    refs = {r['model_profile_id']: r for r in rows(root / '02_brand/mira_reference_images.csv')}
    target = run / 'reels/production_manifest.json'
    old = json.loads(target.read_text(encoding='utf-8')) if target.exists() else {}
    prior = {r['reel_id']: r for r in old.get('reels', [])}
    expected = {f'{run.name}-{m}-reel' for m in models}
    if set(prior) - expected:
        raise ValueError("Existing records do not match current models; reconcile manually")
    records = []
    for theme, pair in sorted(groups.items()):
        pair.sort(key=lambda p: int(p['look_order']))
        model = pair[0]['model_profile_id']
        ref = refs[model]
        if ref['status'] != 'approved' or any(not (root / ref[k]).is_file() for k in ['reference_face_path', 'reference_full_path']):
            raise ValueError(f'{model}: approved identity files are missing')
        rid = f'{run.name}-{model}-reel'
        ids = [p['look_id'] for p in pair]
        if rid in prior:
            if prior[rid]['look_ids'] != ids or prior[rid]['theme_id'] != theme:
                raise ValueError(f'{rid}: existing look lock changed; reconcile manually')
            records.append(prior[rid])
            continue
        slots = []
        for look in pair:
            for role in ['full', 'proof']:
                slots.append(dict(slot_id=f"{look['look_id']}_{role}", look_id=look['look_id'],
                    role=role, source_path=None, source_type=None, approval=None,
                    framing_review=None, clarity_review=None, evidence=look['visual_proof'] if role == 'proof' else look['clothing_item']))
        records.append(dict(reel_id=rid, week_id=run.name, theme_id=theme, model_profile_id=model,
            look_ids=ids, theme=pair[0]['theme_name'], audience_problem=None,
            editorial_candidates=[p['dressing_decision'] for p in pair], format_variant=None,
            identity=dict(face=ref['reference_face_path'], full=ref['reference_full_path'], saved_reference_name=None),
            views=slots, visual_theme=None, storyboard=[],
            delivered_video_text='none', instagram_editor_text_note=None,
            generation=dict(settings=None, prompt_version=None, trials=[]),
            output_path=None, qa=dict(status='pending', continuous_watch_done=False, user_approval=None),
            time=dict(active_minutes=None, generation_wait_minutes=None, upload_wait_minutes=None),
            music=dict(source=None, license_evidence=None, clean_master=None),
            commerce=dict(kind='similar_style_inspiration', products=[], tracked_links=[]),
            publication=dict(url=None, published_at=None, metrics_checkpoints=['24h','72h','7d']),
            status='planning'))
    manifest = dict(old)
    manifest['editing_defaults'] = dict(transition='cross_dissolve', duration_seconds=0.75,
        character_action='unchanged', source_speed='unchanged', decision_date='2026-10-02',
        applies_to='subsequent_edits', historical_exports='preserved',
        evidence='User: 之後所有的切換都要柔和一點，約0.75秒疊加')
    manifest.update(schema_version=1, week_id=run.name, mass_production_gate=old.get('mass_production_gate', 'M02_pilot_pending'), reels=records)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for record in records:
        brief = target.parent / f"{record['reel_id']}_brief.md"
        if not brief.exists():
            brief.write_text(f"# {record['reel_id']}\n\n主題：{record['theme']}\n\n兩套：{' / '.join(record['look_ids'])}\n\n製作資料唯一來源：`production_manifest.json` 中相同 reel_id。\n\n先填觀眾問題、A/B 形式與四個畫面來源，定整支視覺主題後再逐鏡寫分鏡、提示詞版本與實際生成設定。交付影片不烙字；若畫面文字確有必要，另給使用者 Instagram 編輯器手動加字提醒。QA、耗時、成片和發布網址分別記錄；空白不表示通過。\n", encoding='utf-8')
    schedule = target.parent / 'four_week_trial.csv'
    if not schedule.exists():
        with schedule.open('w', encoding='utf-8-sig', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=['trial_week','weekday','model_profile_id','format_variant','planned_date','local_publish_time','reel_id','post_url','status'])
            writer.writeheader()
            for week in range(1,5):
                for day in range(1,6):
                    writer.writerow(dict(trial_week=week, weekday=day, model_profile_id=f'M0{day}',
                        format_variant='A' if (week+day)%2 == 0 else 'B', status='after_pilot_gate'))
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--run-dir', type=Path, required=True)
    args = parser.parse_args()
    print(build(args.project_root, args.run_dir))
