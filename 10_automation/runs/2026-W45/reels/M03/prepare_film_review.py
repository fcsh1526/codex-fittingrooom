"""Create isolated M03 review utilities without rendering/submitting media."""
from pathlib import Path
HERE=Path(__file__).resolve().parent
base=HERE.parent/'M01/paired_review_v1'
dest=HERE/'paired_review_v1';dest.mkdir(exist_ok=True)
s=(base/'build_review.py').read_text(encoding='utf-8')
s=s.replace("A=HERE.parent/'L01_trial_01/source.mp4'","A=HERE.parent/'L01_trial_02/source.mp4'")
s=s.replace('M01_W45_two_looks_review_v1','M03_W45_two_looks_review_v1')
s=s.replace('start_frame=12:end_frame=144','start_frame=0:end_frame=96').replace('start_frame=0:end_frame=132','start_frame=0:end_frame=174').replace('offset=4.75','offset=3.25')
s=s.replace('==246','==252').replace('-10.25','-10.5').replace("'total_frames':246,'duration_seconds':10.25","'total_frames':252,'duration_seconds':10.5")
s=s.replace('[12,144]','[0,96]').replace('[.5,6.0]','[0.0,4.0]').replace('[0,132]','[0,174]').replace('[0,5.5]','[0,7.25]').replace("'output_start_frame':114","'output_start_frame':78").replace('[114,132]','[78,96]').replace('[4.75,5.5]','[3.25,4.0]')
s=s.replace('whole=[i*.5 for i in range(21)]','whole=[i*.5 for i in range(21)]+[251/24]').replace('join=[4.5]+[i/24 for i in range(114,132,2)]+[5.5,5.75]','join=[3.0]+[i/24 for i in range(78,96,2)]+[4.0,4.25]')
s=s.replace("'-ss',4.25","'-ss',2.75")
s=s.replace("sheet(join,'join_contact',4)","sheet(join,'join_contact',4)\nsheet([i*.25 for i in range(22,37)],'full_to_medium_contact',5)")
(dest/'build_review.py').write_text(s,encoding='utf-8')
s=(base/'verify_source_mapping.py').read_text(encoding='utf-8')
s=s.replace('L01_trial_01','L01_trial_02').replace('M01_W45','M03_W45').replace('len(v)==246','len(v)==252')
s=s.replace('v[:114]-a[12:126]','v[:78]-a[0:78]').replace('v[132:]-b[18:132]','v[96:]-b[18:174]')
s=s.replace("'unblended_output_frames_checked':228","'unblended_output_frames_checked':234").replace('output[0,114)=A[12,126)','output[0,78)=A[0,78)').replace('output[132,246)=B[18,132)','output[96,252)=B[18,174)')
(dest/'verify_source_mapping.py').write_text(s,encoding='utf-8')
print(dest)
