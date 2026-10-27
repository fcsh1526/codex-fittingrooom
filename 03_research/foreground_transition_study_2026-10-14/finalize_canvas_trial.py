from pathlib import Path
import json, sys, hashlib, subprocess

base = Path(__file__).resolve().parent
root = base.parents[1]
sys.path.insert(0, str(root / '10_automation/.video_dependencies'))
import imageio_ffmpeg

attempt = base / 'A_motion_attempt_01'
source = attempt / 'source.mp4'
preview = attempt / 'review_silent.mp4'
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-i', str(source),
                '-map', '0:v:0', '-c:v', 'copy', '-an', '-movflags', '+faststart',
                str(preview)], check=True, capture_output=True)
receipt = json.loads((attempt / 'technical_receipt.json').read_text(encoding='utf-8'))
receipt['source'] = source.relative_to(root).as_posix()
receipt['visual_review'] = {
    'status': 'sampled_single_shot_candidate_with_deviations',
    'reviewed': ['whole_25.jpg', 'face_5.jpg', 'all_00.jpg', 'all_01.jpg',
                 'all_02.jpg', 'all_03.jpg', 'frame_144.png'],
    'observations': [
        'Stable-looking face and wardrobe in inspected samples; final face sample is intentionally occluded.',
        'Foreground wall progressively covers subject from image-right toward image-left; final native frame is all wall.',
        'Subject steps toward camera from approximately 2.5 seconds despite standing-still prompt.',
        'Background remains visible at left in late thumbnails; requested final 0.5-second fully opaque handle is not demonstrated.',
        'No cut or graphic dissolve visible in sampled sequence. Physical pure lateral-camera compliance is not proven.'
    ],
    'continuous_playback_verified': False,
    'user_video_approval': None,
    'complete_two_look_join': False
}
receipt['silent_review'] = {
    'file': preview.relative_to(root).as_posix(),
    'sha256': hashlib.sha256(preview.read_bytes()).hexdigest(),
    'method': 'video stream copy; audio removed; original speed, dimensions and frame count retained'
}
(attempt / 'technical_receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
before = json.loads((attempt / 'canvas_pre_submit.json').read_text(encoding='utf-8'))
before.update(submission_count=1, completed=True, source_sha256=receipt['sha256'],
              downloaded_name='grok-6be40232-8d14-4f06-9471-e64a504daf32-720p.mp4',
              actual_output={'size':[720,1264], 'fps':24, 'frames':145, 'audio_codec':'aac'},
              original_still_sha256='a6ac27ac427cbe5d91f9d5751d6a4bc03ea98f771985ac6d70b520a7344dcff2',
              source_images_and_result_on_same_canvas=True,
              global_history_behavior_verified=False,
              historical_assets_deleted=False, publishing_files_replaced=False)
(attempt / 'canvas_generation_receipt.json').write_text(json.dumps(before,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'preview':str(preview),'frames':145,'submissions':1}))
