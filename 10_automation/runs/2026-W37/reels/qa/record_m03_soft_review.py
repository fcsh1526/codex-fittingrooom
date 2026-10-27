import json
from pathlib import Path
root=Path(__file__).resolve().parents[5]
reels=root/'10_automation/runs/2026-W37/reels'
p=reels/'M03_L01_full_detail_review_v2_soft_01.json'
d=json.loads(p.read_text(encoding='utf-8-sig'))
d['sources'][1]['end_frame_exclusive']=55
d['qa']['visual_sample_review']='Start, ending and transition frames inspected. Full hair/shoes preserved in full shot; face excluded in detail. Brief double-scale overlap visible inside the dissolve. Continuous comfort remains pending.'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
updates={
root/'CURRENT_STATUS.md':('## M03 soft-transition experiment pending review — 2026-10-01\n\nUser reports slow-looking source motion across previous trials and uncomfortable hard cuts. Original edits did not retime the sources; that does not establish natural-looking tempo. New L01-only four-second `reels/videos/M03_L01_full_detail_review_v2_soft_01.mp4` tests a0.25s cross dissolve from2.0–2.25s. A1 frames18–71 and A2 frames6–54;96frames,720×1280,24fps, no text/audio, no zoom/blur/morph. Full decode and transition-frame inspection complete, no black/near-identical frames. Brief double-scale overlap remains visible; human continuous review pending. Do not apply to other approved tracks or adopt as weekly standard before review. Natural action pacing remains an upstream issue for the next motion test. L02 unstarted; all prior approvals preserved.\n\n'),
root/'10_automation/runs/2026-W37/publishing_structure.md':('**M03柔和接點試作（2026-10-01）：** 使用者反映所有試片人物有慢動作感，硬切與之不協調。原片未後製降速；新四秒 `reels/videos/M03_L01_full_detail_review_v2_soft_01.mp4` 試2.0–2.25秒的短交疊，維持來源速度、無字無音。96幀解碼與逐轉場幀抽查完成；交疊內短暫雙尺度重影仍須正常播放評估。待使用者視覺判定，未回改其他核准影片，第二套未開始。\n\n')}
for path,text in updates.items():
    s=path.read_text(encoding='utf-8-sig'); pos=s.find('\n\n')+2
    path.write_text(s[:pos]+text+s[pos:],encoding='utf-8')
print('Soft-transition review records updated; user acceptance remains pending.')
