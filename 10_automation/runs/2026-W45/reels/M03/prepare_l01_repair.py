"""Prepare one bounded performance-blocking correction; never submit jobs here."""
import hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
old=HERE/'L01_trial_01'
new=HERE/'L01_trial_02';new.mkdir(exist_ok=True)
review={"date":"2026-11-04","result":"not_selected_for_planned_four_second_stationary_shot","evidence":"contact_sheet.png at 0.5 s intervals; exact URL/media/prompt matched","observations":["Subject advances with visible steps around 1–2.5 s, then retreats toward the original position by 4–5 s.","Requested fixed-camera stationary full-person performance was not obeyed; early approach crops shoes.","Late stationary tail alone does not provide the planned four-second source plus useful transition handles."],"cause":"Unknown. Forward-inclination and weight-shift wording may have encouraged translation; hypothesis only.","next":"One correction changes performance blocking only: both feet stay at the same paving marks, expression and small shoulder response carry the scene.","continuous_human_visual_review":False,"user_acceptance":None,"publication_approval":None}
(old/'visual_review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
s=json.loads((old/'submission.json').read_text(encoding='utf-8'));s['status']='not_selected_stationary_blocking_failed';(old/'submission.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
prompt='''She is already standing in a relaxed conversation with her friend directly behind the camera. Begin from the exact approved first image. Her gaze stays with that friend at the lens. A warm smile grows into a happy laugh, with a small easy shoulder release and natural breathing.

One continuous six-second real-time shot. Both feet stay planted on the same two paving marks for the entire shot. Her upright body remains at the same distance from the camera; her expression and gentle shoulder response carry the moment. Her hands hang comfortably low and visible, and her bag rests on her left shoulder. Keep the open blazer front, white neckline, waist and straight-trouser silhouette readable.

Preserve the exact M03 face, long wavy brown hair, deep-navy soft-shouldered lightweight blazer, white crewneck cotton tee, charcoal straight trousers, black low-heeled loafers, small black shoulder bag and fine silver necklace. Locked level chest-height 50mm camera with the original full-person framing, complete hair and both shoes visible. Keep the office windows, stone wall, bench, paving and shaded daylight coherent. Ordinary live-action tempo. No step, forward lean, walking, spin, large arm gesture, camera movement, cut, slow motion or text.
'''
(new/'video_prompt.txt').write_text(prompt,encoding='utf-8')
request=(old/'grok_request.txt').read_text(encoding='utf-8')
request=request.replace('本次只做W45 M03 L01，','本次只做W45 M03 L01 trial02一次修正。前次a5cdb89d自行前走再退，未選用；只改表演走位，其他首圖、身份、服裝、固定鏡頭與設定不變。不能沿用舊輸出冒充新片；不要再做L02。本次只做W45 M03 L01，',1)
request=re.sub(r'PROMPT_BEGIN\n.*?\nPROMPT_END','PROMPT_BEGIN\n'+prompt.rstrip()+'\nPROMPT_END',request,flags=re.S)
(new/'grok_request.txt').write_text(request,encoding='utf-8')
s={k:v for k,v in s.items() if k not in ['video_asset_id','download_path','local_source','generator_reported_parameters_accepted','actual_tool_call_directly_visible']}
s.update(status='prepared_not_submitted',trial=2,prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),repair_of='L01_trial_01',changed_variable='performance blocking only; planted feet instead of forward inclination/weight shift',failure_limit='If stationary mechanism fails again, stop this mechanism and redesign; no third same-mechanism request.')
(new/'submission.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(new/'inspect_clip.py').write_text((old/'inspect_clip.py').read_text(encoding='utf-8').replace('L01_trial01','L01_trial02'),encoding='utf-8')
print(new)
