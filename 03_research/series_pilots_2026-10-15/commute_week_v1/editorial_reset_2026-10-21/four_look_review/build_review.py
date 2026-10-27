"""Research preview: trim accepted prefix to295frames, append reviewed first108ofnewF04."""
from pathlib import Path
import argparse, importlib.util, json, sys

HERE=Path(__file__).resolve().parent
RESET=HERE.parent
COMMUTE=RESET.parent
BRIDGE=COMMUTE/'production_bridge_2026-10-19'
HELPER=BRIDGE/'F04/close_tracking_proposal_2026-10-20/close_join_review_2026-10-21/build_close_study.py'
spec=importlib.util.spec_from_file_location('mira_close_review_helper',HELPER)
close=importlib.util.module_from_spec(spec)
spec.loader.exec_module(close)
native=close.native

ap=argparse.ArgumentParser()
ap.add_argument('--source-sha',required=True)
ap.add_argument('--review-eligible',action='store_true')
a=ap.parse_args()
assert a.review_eligible,'Root must inspect exact source before research-viewing render'
SRC=RESET/'F04_motion_01/F04_source.mp4'
PREFIX=BRIDGE/'F03/phase_match_review_v1/F01_F02_F03_phase_plus1_native_soft_review_v1.mp4'
OLD=BRIDGE/'F05/five_look_review_2026-10-21/v1/review.mp4'
PAIR=BRIDGE/'F02/motion_retry_01/F01_F02_gait_fix_review_v1.mp4'
hashes={SRC:a.source_sha,PREFIX:'f36b079261d6ba43bc1bf17f9504b4a1424efc393c24e5d53d9f4075165eaa33',OLD:'be262d6771141eeda11d2671cc5c1a87b7a03d869aacf60c117e5d5bc8b38b03',PAIR:'54da666276fd89fc93461fc25bbe2aa805e565beff8f708bf071b78118a462dd'}
for p,sha in hashes.items():native.verified_source(p,sha)
outdir=HERE/'v1'
assert not outdir.exists(),'Preserve partial or existing output; use a separate version'
outdir.mkdir()
sources=[('accepted_prefix_first295',PREFIX,295),('new_F04_full_first108',SRC,108)]
output=outdir/'review.mp4'
native.encode_new(output,close.make_sequence(sources))
decode=native.full_decode(output)
assert decode['decoded_frames']==385
streams=native.stream_inventory(output)
assert not streams['audio_stream_present']
fidelity=close.fidelity_check(output,sources,385)
qadir=outdir/'QA';qadir.mkdir()
full=native.uniform_indices(385)
join=list(range(269,303))
keep=set(full+join)
frames={}
with native.native_reader(output) as rd:
    for i,b in enumerate(rd):
        if i in keep:frames[i]=native.Image.frombytes('RGB',native.SIZE,b)
native.contact_sheet([(i,frames[i]) for i in full],qadir/'full25.png','Four-look work in progress; source and new join need user review')
native.contact_sheet([(i,frames[i]) for i in join],qadir/'join.png','NewJ34 .75s; visible double edges may remain')
for i in (277,285,294,302):native.image_new(qadir/f'f{i}.png',frames[i])
for p,sha in hashes.items():native.verified_source(p,sha)
receipt={
 'date':'2026-10-21','status':'four_look_research_work_in_progress_not_whole_five_look_film',
 'source_sha256':a.source_sha,'protected_hashes_unchanged':{str(p):sha for p,sha in hashes.items()},
 'sources':[{'role':role,'path':str(p),'selected_prefix_frames':n} for role,p,n in sources],
 'prefix_cut_detail':'First295ofexisting331 corresponds originalF01[0,78), correctedF02[0,145), originalF03[1,109), earlier two .75s joins retained',
 'output':{'path':str(output),'sha256':native.sha256(output),'bytes':output.stat().st_size,'frames':385,'fps':24,'duration_seconds':385/24,'size':[720,1280],'audio':False,'text':False,'retime':False,'crop':False},
 'new_dissolve':{'output_frames_half_open':[277,295],'seconds_half_open':[277/24,295/24],'duration_seconds':.75,'outgoing_original_F03_frames_half_open':[91,109],'incoming_new_F04_frames_half_open':[0,18]},
 'full_decode':decode,'streams':streams,'fidelity':fidelity,
 'limits':['Source contains previously unseen short stairs revealed from right edge; site membership unvalidated','Source and blend gait not measured slide-free; new dissolve may show phase mismatch','No user normal-speed or whole-film approval','Fifth look not included; no publishing pass'],
 'next':'Root densejoin inspection, then user research viewing before deciding ambiguous stairs/join acceptability; no automatic source retry',
}
native.json_new(outdir/'edit_receipt.json',receipt)
print(json.dumps(receipt,ensure_ascii=False,indent=2))
