from pathlib import Path
import json
import hashlib

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parent
JOB = ROOT / '10_automation/runs/2026-W41/generated_images/2026-W41-004/looks/2026-W41-004-L02/reel/lunch_outing_v1'
JOB.mkdir(parents=True, exist_ok=True)

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

edit = load(BASE / 'first_look_edit_receipt.json')
acceptance = {
    'date': '2026-10-13', 'user_quote': '這個方向可以',
    'context': 'Direct reply after showing5.5s same-outfit A1→A2 trial and asking whether it approaches an approachable everyday magazine.',
    'file': edit['file'], 'sha256': edit['sha256'],
    'scope': 'Editorial direction accepted; continue second look within existing storyboard. Not final full-Reel approval, account-wide template adoption, audience success or a self-report of uninterrupted playback.',
    'normal_speed_full_playback_user_self_report': None,
    'assistant_continuous_playback': False,
}
save(BASE / 'first_look_direction_acceptance_2026-10-13.json', acceptance)
edit['editorial_direction_acceptance'] = acceptance
edit['status'] = 'first_look_direction_accepted_continue_second_look'
save(BASE / 'first_look_edit_receipt.json', edit)
story = load(BASE / 'storyboard_candidate.json')
story['status'] = 'first_look_direction_accepted_B2_full_still_next'
story['first_look_direction_acceptance'] = acceptance
story['next_action'] = 'Generate and visually approve L02 full-person B2 departure-start candidate first as its new scene/wardrobe lock. Then derive B1 seated view matching A2 head/waist/bench focus. Every new still waits for user visual approval before Grok.'
story['second_look_image_order'] = ['B2 full-person session lock', 'B1 seated styling-proof view']
story['second_look_screen_order'] = ['B1 seated', 'B2 departure']
story['second_look_join_plan'] = {
    'A2_to_B1': 'Match seated framing, crossed-leg posture, face and waist position and left daylight. Navy blazer/gray tee/cream trousers/black bag remain the sole L02 wardrobe authority; no L01 clothing copied.',
    'B1_to_B2': 'Use same lunch-shop bench/window/warm-gray-wall scene. Full departure framing keeps readable face near viewing focus and leaves image-right walking space.0.75s independent-shot dissolve, not sit-to-stand keyframe morph.',
    'risks': 'Standing/seated scale change and reconstructing wider scene can still create visible overlap. Static candidates do not establish scene geometry matching or dynamic comfort.',
    'scene_reference': 'Approved clean A2v4 only for window, bench, light and photographic color; never its L01 wardrobe.',
}
save(BASE / 'storyboard_candidate.json', story)

prompt = '''Create one native vertical 9:16 daily-fashion editorial photograph for the departure shot of a lunch-break story. Show how a light blazer over a cotton tee keeps everyday straight trousers polished.

Image 1 anchors the same woman's face and brown wavy hair, mid 30s look, well-maintained; image 2 anchors ordinary body proportions only. Image 3 is the exact second-outfit authority. Image 4 provides only the lunch-shop window, chunky wooden bench, gray wall and soft left daylight; do not copy its clothes or seated pose.

She is already standing beside that bench, beginning one short diagonal step toward image-right, torso at a shallow three-quarter angle, face still clearly readable. Both arms hang naturally; her shoulder supports the bag. Leave room for one step while keeping her complete head and both shoes visible.

Preserve image 3's open navy single-breasted lightweight blazer with once-folded cuffs, plain light-gray tucked cotton crewneck tee, cream high-waisted straight trousers, black low-heel loafers, black shoulder bag on image-right and small silver studs. Solid fabrics with natural folds.

Photograph with a full-frame mirrorless camera, level chest-height 50mm view. Window left, bench behind-left, plain warm-gray wall right; natural skin, soft ambient spill and grounded shoe shadows. Approachable quiet expression. One person; no text, logos, patterns or exaggerated proportions.'''
(BASE / 'B2_prompt_v1.txt').write_text(prompt + '\n', encoding='utf-8')
(JOB / 'B2_prompt_v1.txt').write_text(prompt + '\n', encoding='utf-8')
refs = ['02_brand/reference_models/M03_start_v3_face.png', '02_brand/reference_models/M03_start_v3_full.png', '10_automation/runs/2026-W41/generated_images/2026-W41-004/looks/2026-W41-004-L02/reel/2026-W41-004-L02_M03_reel_candidate_A.png', '10_automation/runs/2026-W41/generated_images/2026-W41-004/looks/2026-W41-004-L01/reel/lunch_outing_v1/M03_L01_A2_seated_candidate_v4_clean.png']
save(BASE / 'B2_reference_plan.json', {'date': '2026-10-13', 'shot': 'B2', 'look_id': '2026-W41-004-L02', 'references': [{'path': p, 'sha256': hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} for p in refs], 'prompt': 'B2_prompt_v1.txt', 'status': 'planned', 'new_still_approved': False, 'grok_uploaded': False})
update = '''## M03午休小出走：方向已接受，續作第二套 — 2026-10-13

使用者看過第一套5.5秒試片後回覆「這個方向可以」。記錄為觀看方向接受與續作第二套，非整支正式Reel核准、帳號固定模板、流量或完整正常播放自述。第二套沿用深藍西外／淺灰棉T／奶油白直筒褲／黑肩包，仍在同一午休窗邊長椅場景。先製作並視覺核准B2全身離開起始圖以鎖定第二套，再製作B1坐姿圖；實際影片順序仍A1→A2→B1→B2。新圖未核准前不送Grok。無字、原速、約0.75秒疊化；研究與舊W41交付分開。核准範圍與第二套鏡頭計畫見`03_research/editorial_sequence_reset_2026-10-13/first_look_direction_acceptance_2026-10-13.json`及`storyboard_candidate.json`。下方為歷史進度。

'''
status = ROOT / 'CURRENT_STATUS.md'
heading, rest = status.read_text(encoding='utf-8-sig').split('\n', 1)
status.write_text(heading + '\n\n' + update + rest.lstrip('\n'), encoding='utf-8')
readme = BASE / 'README.md'
readme.write_text(update + readme.read_text(encoding='utf-8-sig'), encoding='utf-8')
print('Direction acceptance and L02 shot connections saved. B2 prompt words:', len(prompt.split()))
