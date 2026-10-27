import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[5]
run = root / '10_automation/runs/2026-W37'
reels = run / 'reels'
sys.path.insert(0, str(root / '10_automation'))
from prepare_reel_production import build

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

manifest_path = reels / 'production_manifest.json'
before = load(manifest_path)
build(root, run)
manifest = load(manifest_path)
assert manifest['reels'] == before['reels'], 'Weekly rebuild must preserve all existing production and approvals'
assert manifest['editing_defaults']['duration_seconds'] == 0.75

record_path = reels / 'M01_two_looks_soft_review_v2_01.json'
record = load(record_path)
record['qa']['sampled_review'] = 'Twelve timepoints inspected including start/end and overlap. Full hair and shoes retained; no obvious sampled wardrobe or background drift outside intentional dissolve. During overlap two offset faces, shoes and window edges are briefly visible. Source speed unchanged. Continuous comfort review pending with user.'
save(record_path, record)
entry = next(r for r in manifest['reels'] if r['model_profile_id'] == 'M01')
entry['prior_output_path'] = entry['output_path']
entry['output_path'] = record['output_path']
entry['output_record_path'] = record_path.relative_to(root).as_posix()
entry['status'] = 'soft_transition_review_pending_user_approval'
entry['qa'].update(status='technical_sampled_complete_soft_cut_full_review_pending',
    continuous_watch_done=False, user_approval=None)
entry['edit'] = dict(transition='cross_dissolve', duration_seconds=0.75, start_seconds=2.75,
    end_seconds=3.5, actual_duration_seconds=record['duration_seconds'],
    source_speed='unchanged', character_action='unchanged', decision_date='2026-10-02')
save(manifest_path, manifest)

for path, heading, note in [
    (root / 'CURRENT_STATUS.md', '# Current Status - Mira AI Fashion Creator',
     '\n\n## Global soft-transition rule; M01 revised — 2026-10-02\n\nUser explicitly requests all subsequent switches use approximately0.75-second overlaps. Canonical workflow, Reel SOP and future manifest preparation now carry this rule, superseding direct-cut advice and earlier non-global transition limits. Keep character actions/source speed unchanged. M01 revised to `reels/videos/M01_two_looks_soft_review_v2_01.mp4`: actual6.7083s,720×1280,24fps,161frames, overlap2.75–3.5s; original source selections/framing retained. Whole decode and12 sampled timepoints inspected; normal-speed user comfort approval pending. M03 remains accepted. Previously accepted M02/M04/M05 exports preserved; no publication.\n'),
    (run / 'publishing_structure.md', '# W37 Publishing Structure',
     '\n\n**現行通用轉場（2026-10-02）：** 使用者明確要求之後所有切換約0.75秒柔和交疊；人物動作與速度不改。已同步總工作流、Reel SOP及未來製作單預設。M01改版 `reels/videos/M01_two_looks_soft_review_v2_01.mp4`，約6.71秒、2.75–3.5秒交疊、無字無音，161幀解碼及12個時間點抽查完成，整片仍待使用者確認。M03已核准；其他歷史核准影片保留。下方「不採通用轉場」是較早紀錄，已由本次明確決定取代。\n'),
    (reels / 'M01_storyboard_v1.md', '# W37 M01｜先讓鞋面看清楚，再比較兩套',
     '\n\n**現行柔和轉場版（2026-10-02）：** 依使用者所有後續切換約0.75秒交疊的新規則，保留原來源選片、構圖與速度。A全身0–3.5秒、B全身2.75秒起；交疊2.75–3.5秒。實際161幀、6.7083秒（編碼交疊尾端少一影格，不補停格）。新檔 `videos/M01_two_looks_soft_review_v2_01.mp4`，全身與鞋面保留；重疊期間短暫雙臉／雙鞋及背景重影，完整舒適度待使用者確認。下方「不溶接」為被取代的原始規劃。\n')
]:
    text = path.read_text(encoding='utf-8-sig')
    assert text.startswith(heading)
    path.write_text(text.replace(heading, heading+note, 1), encoding='utf-8')

caption_path = reels / 'M01_instagram_caption_draft.md'
text = caption_path.read_text(encoding='utf-8-sig').replace('videos/M01_two_looks_review_v1_01.mp4', 'videos/M01_two_looks_soft_review_v2_01.mp4')
caption_path.write_text(text, encoding='utf-8')
gate_path = reels / 'REEL_RELEASE_GATE_2026-09-30.md'
text = gate_path.read_text(encoding='utf-8-sig').replace('`videos/M01_two_looks_review_v1_01.mp4`，7.5秒', '`videos/M01_two_looks_soft_review_v2_01.mp4`，約6.71秒、0.75秒交疊')
text = text.replace('全180幀解碼與切點抽查通過', '全161幀解碼與12個時間點抽查完成')
text = text.replace('本次0.75秒交疊不自動套用其他影片。', '2026-10-02使用者已明確將約0.75秒交疊定為所有後續切換預設；歷史版本保留。')
gate_path.write_text(text, encoding='utf-8')
print('Global transition default saved; rebuild preserves all five existing records. M01 soft candidate linked; full user review pending.')
