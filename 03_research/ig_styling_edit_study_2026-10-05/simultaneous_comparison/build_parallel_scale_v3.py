"""Apply constant proportional size/position correction to separate research v3."""
import json
from pathlib import Path
from build_parallel_trial import ROOT, OUT, run, scan, checkpoints, sha, relative, save

CONFIG = {
    'A': {'x':132, 'width':488, 'pad_top':176, 'scaled_crop_y':0},
    'B': {'x':145, 'width':470, 'pad_top':176, 'scaled_crop_y':15},
}

def main():
    output = OUT / 'M02_parallel_compare_review_v4_size_matched.mp4'
    if output.exists():
        raise FileExistsError('Preserve existing variants; choose a new version.')
    prior = json.loads((OUT / 'M02_parallel_compare_review_v2.json').read_text(encoding='utf-8'))
    assert sha(ROOT / prior['output_path']) == prior['output_sha256']
    old_receipt = json.loads((ROOT / '10_automation/runs/2026-W37/reels/google_drive_update_2026-10-02.json').read_text(encoding='utf-8-sig'))
    protected = [(ROOT / row['source_video_path'], row['local_sha256']) for row in old_receipt['files']]
    assert all(sha(path)==expected for path,expected in protected)
    inputs, filters, source_records = [], [], []
    for index, letter in enumerate(('A','B')):
        source = OUT / f'grok_{letter}_attempt_01/source.mp4'
        assert sha(source) == prior['sources'][index]['source_sha256']
        config = CONFIG[letter]
        inputs += ['-i',str(source)]
        filters.append(f'[{index}:v]trim=start_frame=0:end_frame=144,setpts=PTS-STARTPTS,'
                       f'crop={config["width"]}:1280:{config["x"]}:0,'
                       'scale=352:-2:flags=lanczos,'
                       f'crop=352:924:0:{config["scaled_crop_y"]},'
                       f'pad=360:1280:4:{config["pad_top"]}:color=0xe8e2d9,'
                       f'setsar=1,settb=1/24[p{index}]')
        record = dict(prior['sources'][index])
        record.update(fixed_crop=[config['x'],0,config['width'],1280],
                      fixed_panel_position=[4,config['pad_top']],
                      proportional_scale=352/config['width'],
                      post_scale_background_crop=[0,config['scaled_crop_y'],352,924],
                      shared_visible_panel_bounds=[4,176,352,924],
                      temporal_selection_unchanged=True,
                      animated_crop_or_zoom=False)
        source_records.append(record)
    filters.append('[p0][p1]hstack=inputs=2,format=yuv420p[v]')
    run([*inputs,'-filter_complex',';'.join(filters),'-map','[v]','-an','-c:v','libx264',
         '-crf','18','-preset','medium','-r','24','-frames:v','144','-movflags','+faststart',str(output)])
    decoded = scan(output)
    assert decoded['decoded_frames']==144 and decoded['metadata']['size']==(720,1280)
    assert not decoded['black_candidate_frames'] and not decoded['near_identical_frame_pairs']
    board = checkpoints(output,'output_v4')
    receipt = dict(prior)
    receipt.update(status='research_size_revision_pending_user_full_film_review',
                   output_path=relative(output),output_sha256=sha(output),sources=source_records,
                   actual_seconds=decoded['decoded_seconds'],technical_scan=decoded,
                   checkpoint_board=board,
                   correction={'user_feedback':'左右人物大小有點不一致',
                               'relative_A_scale_to_B':470/488,
                               'A_reduction_percent':100*(1-470/488),
                               'method':'Constant proportional scaling via wider A source window. Common352x924 image panels at y176; B trims15px top/19px bottom of scaled ambient background, retaining the same subject position as B y161 without trim. No tracking, retime, pose edit or body deformation.',
                               'limitation':'Opening A is slightly smaller/lower after fixed correction because A moves forward; later sampled head/shoe positions match more closely. Not exact per-frame normalization.'},
                   assistant_sampled_visual_review='pending_v4',assistant_continuous_review=False,
                   user_video_approval=None,cloud_upload=False,publication=False,publishable=False)
    assert all(sha(path)==expected for path,expected in protected)
    assert sha(ROOT/prior['output_path'])==prior['output_sha256']
    save('M02_parallel_compare_review_v4_size_matched.json',receipt)
    print(json.dumps({'output':str(output),'sha256':receipt['output_sha256'],
                      'seconds':decoded['decoded_seconds'],'frames':144,
                      'A_reduction_percent':receipt['correction']['A_reduction_percent'],
                      'old_five_and_v2_unchanged':True},ensure_ascii=False))

if __name__=='__main__':
    main()
