"""Isolated native-speed first-pair research edit; preserves sources and publishing files."""
import hashlib
import importlib.util
import json
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = next(path for path in HERE.parents if (path / '10_automation').is_dir())
HELPER = ROOT / '03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py'
spec = importlib.util.spec_from_file_location('native_pair_primitives', HELPER)
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    a = HERE / 'motion_attempt_01/S01_source.mp4'
    b = HERE / 'motion_attempt_01/S02_source.mp4'
    expected = ['499fa888e084649a4988ede3f0469619e2313456f4bd5035338f4d57bb9f3d04',
                'a8f9fc6e9019c23433c855e3d108d97d3236c05f76fa30b02b6b0fcdc97c6ec0']
    assert [sha(a), sha(b)] == expected, 'Actual source hash changed'
    output = HERE / 'first_pair_review_v1'
    assert output.resolve().parent == HERE and not output.exists(), 'Preserve existing edit'
    output.mkdir()
    video = output / 'M03_commute_first_pair_review_v1.mp4'
    stream_a = native.selected_frames(a, 0, 156)
    stream_b = native.selected_frames(b, 60, 216)
    mapping = []

    def frames():
        for index in range(138):
            mapping.append(dict(output_frame=len(mapping), S01_frame=index, S02_frame=None, S02_alpha=0))
            yield next(stream_a)
        for index in range(18):
            alpha = (index + 1) / 18
            mapping.append(dict(output_frame=len(mapping), S01_frame=138 + index,
                                S02_frame=60 + index, S02_alpha=alpha))
            yield Image.blend(next(stream_a), next(stream_b), alpha)
        for index in range(18, 156):
            mapping.append(dict(output_frame=len(mapping), S01_frame=None,
                                S02_frame=60 + index, S02_alpha=1))
            yield next(stream_b)

    images = frames()
    try:
        native.encode_new(video, images)
    finally:
        images.close()
        stream_a.close()
        stream_b.close()
    decoded = native.full_decode(video)
    assert decoded['decoded_frames'] == len(mapping) == 294
    assert decoded['metadata'].get('audio_codec') is None
    assert [sha(a), sha(b)] == expected
    qa = output / 'QA'
    qa.mkdir()
    native.extract_boards(video, qa, 0, 294, range(130, 164))
    (qa / 'frame_mapping.json').write_text(json.dumps(mapping, indent=2) + '\n', encoding='utf-8')
    (qa / 'full_decode.json').write_text(json.dumps(decoded, indent=2) + '\n', encoding='utf-8')
    receipt = dict(date='2026-10-15', output=video.relative_to(ROOT).as_posix(), sha256=sha(video),
                   native_size=[720, 1280], native_fps=24, decoded_frames=294, seconds=12.25,
                   sources=[dict(shot='S01', path=a.relative_to(ROOT).as_posix(), sha256=expected[0],
                                 selected_frames_half_open=[0, 156], seconds_half_open=[0, 6.5]),
                            dict(shot='S02', path=b.relative_to(ROOT).as_posix(), sha256=expected[1],
                                 selected_frames_half_open=[60, 216], seconds_half_open=[2.5, 9])],
                   transition=dict(type='linear_cross_dissolve', frames=18, seconds=0.75,
                                   output_frames_half_open=[138, 156],
                                   output_seconds_half_open=[5.75, 6.5], B_alpha='(index+1)/18'),
                   clear_outfit_seconds_each=5.75, audio=False, baked_text=False,
                   retiming=False, crop=False, scaling=False,
                   image_operation='PIL blend of18 corresponding native RGB frames only',
                   encoding='native RGB frame sequence encoded h264 CRF18, no audio',
                   source_hashes_preserved=True, combined_sampled_visual_review='pending',
                   assistant_continuous_playback=False, user_film_approval=None,
                   publishing_files_replaced=[],
                   helper_note='Reused native read/encode/QA primitives only; did not execute prior study main or approval gates.')
    (output / 'edit_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(output=str(video), frames=294, seconds=12.25, audio=False)))


if __name__ == '__main__':
    build()
