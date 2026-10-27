"""Save assistant sampled/crop review. User continuous approval remains pending."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[5]
run = root / '10_automation/runs/2026-W37'
reels = run / 'reels'
def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest_path = reels / 'production_manifest.json'
manifest = read(manifest_path)
item = next(r for r in manifest['reels'] if r['model_profile_id']=='M01')
for index in [1,2]:
    look = f'2026-W37-004-L0{index}'
    p = run / f'generated_images/2026-W37-004/looks/{look}/reel/shoe_proof_crop_review_v1.json'
    proof = read(p)
    proof.update(status='approved_source_reuse_framing_and_clarity_reviewed', framing_review='450x800 exact9:16 crop; entire paired shoes, contact shadows and hem-to-instep space retained. No stretching or resampling.', clarity_review=('Burgundy T intersections on both shoes clearly visible; trouser hems above instep.' if index==1 else 'Cream T intersections on both shoes clearly visible; black midi hem and lower-leg gap retained.'), limitations='450x800 independent proof asset at original crop resolution, not a newly generated full-HD detail shot. Not inserted in the video; no face-reveal motion.', assistant_review_date='2026-10-01')
    write(p,proof)
    view = next(v for v in item['views'] if v['look_id']==look and v['role']=='proof')
    view.update(approval='reused_from_user_approved_source_after_vertical_clarity_review', framing_review=proof['framing_review'], clarity_review=proof['clarity_review'], review_record_path=p.relative_to(root).as_posix())
item['caption_path'] = (reels / 'M01_instagram_caption_draft.md').relative_to(root).as_posix()
item['cover_candidate_path'] = next(v['source_path'] for v in item['views'] if v['role']=='full')
item['generation']['prompt_version'] = 'M01_A_L01_motion_v1 + M01_B_L02_motion_v1'
write(manifest_path,manifest)

status = root / 'CURRENT_STATUS.md'
text = status.read_text(encoding='utf-8-sig')
entry = '''## M01 two-look candidate ready; user continuous review pending — 2026-10-01

Both M01 native full stills received explicit approval 「可以，沿用這張」. Assistant delegated both uploads successfully. Two single-First-frame clips generated at720p/6s/audiooff, with no saved character or Last frame; actual720×1264/24fps/145frames each. B nine-point sample review shows intact cream T-straps, mid-calf skirt and no obvious sampled window/door/paving morph. No continuous assistant playback is claimed.

`reels/videos/M01_two_looks_review_v1_01.mp4` is a **7.5-second pending candidate**, using A frames18–101 and B frames18–113 at unchanged speed. One direct outfit cut at3.5s. A uniform cover-scale, B fixed642×1140 crop at39,20 to720×1280; no animated zoom, stretch, text, music or transition effects. All180frames decode, no black candidates or near-identical pairs; sampled start/cut/final views retain full hair and both shoes. User full-playback approval question has been sent; do not mark accepted until reply.

Four usable views now link to two approved full stills plus exact450×800 vertical shoe-proof crops. Assistant review confirms T intersections and hem-to-instep space; crops are source reuse without upscale, independent proof assets, not two added video cuts. Caption and cover candidate linked. Exact output/selection/QA at `reels/M01_two_looks_review_v1_01.json`, B trial at `reels/M01_B_L02_fixed_full_v1_01.json`. Three accepted picture tracks remain M02/M05/M04; M01 pending, M03 unstarted. Music and publication remain open. Reel-first priority continues.

'''
marker='## M01 first motion saved; delegated upload succeeded'
text=text.replace(marker,entry+marker,1)
status.write_text(text,encoding='utf-8')

structure=run/'publishing_structure.md'
text=structure.read_text(encoding='utf-8-sig')
text=text.replace('# W37 Publishing Structure\n','# W37 Publishing Structure\n\n**M01雙套候選（2026-10-01）：** 兩套全身起始圖皆核准，助手已代傳完成動態。7.5秒無字無音預覽 `reels/videos/M01_two_looks_review_v1_01.mp4` 採兩個全身鏡、一次3.5秒換裝直接切鏡、正常速度；B固定裁切對齊人物尺度。全180幀解碼、無黑畫面／近乎重複影格，抽查完整頭髮／雙鞋及切點。使用者完整播放核准待回覆，尚未接受或發布。兩套鞋面proof為已核准全身圖的450×800直式原像素裁切，已檢查鞋帶／下襬關係，不硬插入影片。\n',1)
structure.write_text(text,encoding='utf-8')

gate=reels/'REEL_RELEASE_GATE_2026-09-30.md'
text=gate.read_text(encoding='utf-8-sig')
old='| M01／復古 T 字帶鞋日常化 | 無雙套成片；`M01_storyboard_v1.md`就緒，先兩個固定全身鏡，保留鞋面；第一套941×1672全身候選已生成 | 第一套原生全身圖待使用者靜態核准；未動態核准 | 每套全身＋鞋面證據、兩套動態及完整验收 |'
new='| M01／復古 T 字帶鞋日常化 | `videos/M01_two_looks_review_v1_01.mp4`，7.5秒、720×1280、無字無音；兩套全身＋獨立鞋面proof齊備 | 兩套起始圖已核准；全180幀解碼與切點抽查通過，完整正常速度使用者核准待回覆 | 使用者動態核准、音樂與使用範圍、IG最後組裝與發布；內文已準備 |'
if old not in text:
    raise ValueError('Release gate M01 row changed; inspect before replacing')
gate.write_text(text.replace(old,new),encoding='utf-8')

story=reels/'M01_storyboard_v1.md'
text=story.read_text(encoding='utf-8-sig')
text=text.replace('# W37 M01｜先讓鞋面看清楚，再比較兩套\n','# W37 M01｜先讓鞋面看清楚，再比較兩套\n\n**候選剪接（2026-10-01）：** 兩套全身靜態已核准，兩個單一First-frame來源均完成。實際使用A來源0.75–4.25秒、B來源0.75–4.75秒，共7.5秒，3.5秒處一次直接換裝切鏡。B以固定642×1140裁切（x39,y20）對齊A末段尺度，保留完整頭髮及雙鞋；不動畫縮放、不加速。兩套各有原核准圖450×800鞋面proof裁切，直式與清晰度已審查；獨立保存不加兩次切鏡。全片技術／抽查完成，使用者完整播放核准仍待回覆。以下初期狀態為歷史規劃。\n',1)
story.write_text(text,encoding='utf-8')
print('M01 reviewed crops/caption/candidate handoff saved. Three accepted picture tracks; M01 user full playback pending.')
