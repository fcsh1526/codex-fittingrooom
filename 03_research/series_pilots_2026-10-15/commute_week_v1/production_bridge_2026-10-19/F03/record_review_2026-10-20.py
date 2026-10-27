from pathlib import Path
import hashlib, json

folder = Path(__file__).resolve().parent
edit_dir = folder / 'three_shot_review_v1'
edit = json.loads((edit_dir / 'edit_receipt.json').read_text(encoding='utf-8-sig'))
scan = json.loads((folder / 'technical_scan.json').read_text(encoding='utf-8-sig'))

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def checked(path, sha):
    if digest(path) != sha:
        raise ValueError(f'Hash mismatch: {path}')

def write_new(path, data):
    with path.open('x', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')

for entry in edit['sources']:
    checked(entry['path'], entry['sha256'])
checked(edit['accepted_pair_reference']['path'], edit['accepted_pair_reference']['sha256'])
checked(edit['output'], edit['output_sha256'])
checked(folder/'F03_M03_L03_start_candidate_A.png', 'a7b6e33248b5e90c9c63ba0cda1264f23b8ebe8a3dabcb5baeab017c0b30db9e')
checked(folder/'F03_M03_L03_end_candidate_A.png', 'e6442c7a17951eb536e88175285cad52dd8bc32c9732980741afee976d871c70')
if edit['frames'] != 332 or edit['output_stream_inventory']['audio_stream_present']:
    raise ValueError('Unexpected clean preview facts')

data = {
    'review_record_date_local': '2026-10-20',
    'date_authority': 'Asia/Taipei client date; original generation/build receipts retain their recorded date',
    'status': 'three_shot_candidate_ready_for_user_viewing_not_approved',
    'canvas': 'https://grok.com/imagine/agent/f040d332-48df-47c4-86d4-28e85c97d5b5?conversation=3f0241af-1184-4a74-9ced-b0b4715a1a95',
    'generation': {
        'new_asset_id': 'cdd9871e-3ebe-47b6-96d2-6bc5aa81be89',
        'submission_count': 1,
        'source_download': 'C:/Users/Brandon_ChangChien/Downloads/generated_video (51).mp4',
        'source': 'F03_source.mp4',
        'sha256': scan['source_sha256'], 'bytes': scan['bytes'],
        'actual_decoded_frames': 145, 'actual_fps': 24, 'actual_size': [720,1280],
        'actual_seconds_frame_count_over_fps': 145/24,
        'actual_audio': 'AAC; retained in source, removed only in clean local review',
        'requested_first': 'a7a33bb7-39ff-472d-b27d-53e50fe48c58',
        'requested_last': 'd3c047bd-a2e5-4def-adba-a4ffb7cdcaa4',
        'face_identity': '6236309c-2343-41e6-985c-994239ff744a',
        'full_proportions': 'ac9ede4e-1715-4518-95b4-bda341a62061',
        'input_role_confirmation': 'Grok agent reports content checked and simultaneous first/last/face/full assignment; internal controls not independently inspected',
        'grok_completion_record': 'grok_completion_dom.txt',
        'canvas_proof': 'grok_result_screenshot.png',
        'generation_wait_seconds_measured': None,
        'active_minutes_measured': None
    },
    'source_sample_review': {
        'method': 'assistant image inspection plus independent read-only agent of full25, head5 and early/mid/late0.125s foot windows',
        'observations': [
            'last square column shifts left and leaves the view around1.5s; no sampled new deep arched corridor',
            'near planter becomes prominent as camera follows; glass grid, trees and dappled paving remain readable',
            'outfit remains ivory short stand-collar jacket, white crew T, charcoal trousers and black bag/shoes in viewed samples',
            'early/mid/late step phases alternate; no obvious sampled end freeze',
            'no obvious face/outfit collapse in viewed samples'
        ],
        'limits': [
            'not full normal-speed visual playback',
            'shoe-on-tile sliding, pace match and exact topology not measured',
            'curb/crossing hints appear at the right late in source, but their same-site geometry is not validated',
            'generated endpoint has more prominent planter than starting view'
        ],
        'eligible_for_research_preview': True,
        'dynamic_qa_pass': None
    },
    'three_shot': {
        'file': 'three_shot_review_v1/F01_F02_F03_native_soft_review_v1.mp4',
        'sha256': edit['output_sha256'],
        'frames':332, 'fps':24, 'seconds':332/24, 'size':[720,1280],
        'source_intervals_half_open': {'F01':[0,78], 'F02_corrected':[0,145], 'F03':[0,145]},
        'joins_seconds_half_open': [[2.5,3.25],[187/24,205/24]],
        'join_frames':18, 'join_seconds':0.75,
        'native_speed':True, 'crop_resize_freeze_reverse':False,
        'text':'none', 'audio':'none',
        'sample_observations': [
            'large person scale, full shoes and rightward direction remain readable',
            'newJ23 at7.79-8.54s has visible face/arm/trouser/shoe and column/paving double edges, clearest around8.04s',
            'column-to-plaza progression is readable in samples, not exact measured site proof'
        ],
        'assistant_continuous_visual_playback':False,
        'user_normal_speed_playback_self_report':None,
        'user_video_approval':None,
        'full_five_look_film_approved':False,
        'publishable':False
    },
    'protected_media_hashes_rechecked':True,
    'accepted_pair_modified':False,
    'publishing_drive_github_changes':False,
    'next':'Exact13.83s three-shot user review of gait/cadence, new join and scene progression before F04 still planning'
}
write_new(folder/'motion_and_three_shot_review_receipt_2026-10-20.json', data)
readme = '''# 第三套動態與前兩鏡試接\n\n審查記錄：2026-10-20（台灣日期）。\n\n新預覽：`three_shot_review_v1/F01_F02_F03_native_soft_review_v1.mp4`，13.8333秒／332幀／24fps／720×1280。長西外→白襯衫棕丹寧→短外套灰褲；兩處0.75秒柔接，原速、完整畫面、無字無音。\n\nF03首尾均已逐張核准；原畫布一次生成原片，6.0417秒／145幀／AAC。未重生、未後製變速。角色選擇為Grok代理回報，實際檔案規格另經完整解碼確認。\n\n抽樣可供研究試看，尚非動態或成片核准。新接點7.79–8.54秒仍有人物、鞋及柱線雙影；約8.04秒較清楚。腳步自然度、是否忽然減速／滑動與整體舒服度，須播放精確影片確認。路緣／斑馬線位置不因材質相近就視為同場幾何通過。\n\n詳見`motion_and_three_shot_review_receipt_2026-10-20.json`與新版本`edit_receipt.json`／QA。舊兩鏡、來源、失敗版本及Drive發布包均保留。五套整片未完成，F04暫待本次三鏡回饋。\n'''
with (folder/'README.md').open('x',encoding='utf-8') as f:
    f.write(readme)
print(json.dumps({'status':data['status'],'film':data['three_shot']['file'],'sha256':edit['output_sha256'],'seconds':332/24,'protected_hashes':'verified'},ensure_ascii=False))
