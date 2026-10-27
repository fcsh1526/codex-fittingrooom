"""Record user's M04 parallel choice before deriving new first frames."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
week=ROOT/'10_automation/runs/2026-W41'
work=week/'reels/M04';work.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=week/'reels/batch_storyboard.json';story=read(p)
r=next(x for x in story['films'] if x['reel_id']=='2026-W41-M04-reel')
r['format_variant']='parallel_two_looks'
r['format_user_instruction']='之前還有一個是左右的，最後一支可以做成左右的嗎?'
r['nominal_output_seconds']=6
r['previous_format_preserved']={'format_variant':'A','nominal_output_seconds':11.25,'join':r['join']}
r['join']={'type':'none_simultaneous_panels','seconds':0,'basis':'Both complete outfits visible together throughout; no within-film shot switch. If later adding a switch, use0.75s dissolve.'}
r['parallel_layout']={'left':'2026-W41-005-L01','right':'2026-W41-005-L02','output':'portrait9:16','source_policy':'Separate native9:16 full-person sources; fixed proportional panel crops chosen after actual motion bounds QA, never stretch.','size_match':'Measure full hair, face, waist and shoe landmarks at opening and throughout; measure bag/skirt widest boundary. Same person height and panel image rectangle. Do not copy historical3.69% correction.','motion':'Independent ordinary-speed short same-side strap touch, settle and hand return; no forced timing synchronization or retiming.','reading_check':'Full outfit and cobalt bag readable at phone size; fine earrings detail belongs to proof asset.','identity':'Approved M04 v3 face/full anchors. Actual reference hair overrides conflicting general roster hairstyle.'}
for shot in r['shots']:
    shot['person_position']='Centered in own native frame; full hair/shoes and bag remain inside a narrow central motion envelope for later full-height side-by-side panel.'
    shot['action_start']='Feet grounded with small natural stance offset; arms relaxed, bag on image-right/left shoulder, hand not yet touching short strap.'
    shot['ending_handle']='No temporal join; retain clean same-duration portions of independent natural motion without freezing, reversing or retiming.'
write(p,story)
p=week/'reels/production_manifest.json';m=read(p)
r=next(x for x in m['reels'] if x['model_profile_id']=='M04')
r['status']='parallel_format_selected_first_frames_next';r['format_variant']='parallel_two_looks';r['format_user_instruction']=story['films'][-1]['format_user_instruction']
write(p,m)
p=ROOT/'10_automation/production_requests/2026-10-08_next_five_reels.json';req=read(p)
r=next(x for x in req['slots'] if x['model']=='M04');r.update(status='parallel_format_selected_first_frames_next',format_variant='parallel_two_looks')
write(p,req)
(work/'parallel_storyboard_2026-10-08.md').write_text('''# W41 M04 左右同框製作單

使用者指定最後一支改為先前的左右形式。只改M04，前四支保留。

## 整支視覺主題

同一鈷藍小肩包在黑白灰褲裝／裙裝中的亮色焦點。左L01白T／黑薄短外套／炭灰直筒褲，右L02白短袖襯衫／黑小腿A字裙；鞋與包完整可見。

## 分鏡與起始圖

兩套各生成一張原生9:16全身第一幀，核准後分別動畫，再組成左右並列的單一9:16片。淡灰書店門廊、木門框、石地、左側日光一致，人物置中且尺度／頭腰鞋位置匹配。手臂初始放鬆，鈷藍包在畫面右／左肩腰胯側，肩帶可觸碰且不遮白色領口。手、裙、包及鞋留在中間窄範圍並留動作空間。

每側一個自然動作：人物左手輕觸同側短肩帶、少量調整、放手收回。固定50mm平視機位，沒有走近、環繞或大轉身。兩邊自行自然進行，不為同步改速；差異需看片。以既有v3 face/full核准身分為基準，參照衣服／背景不作本週來源。

## 左右構圖與驗收

兩側畫面等寬且影像矩形一致；固定等比例裁切只去除側邊背景，保留整段髮頂、鞋底、手、裙與包的最大邊界。不拉伸、不動態追蹤裁切、不照搬歷史放大比例。依實際來源量人物大小與視線位置，再比較手機360px寬預覽。生成前不得宣稱裁切動態安全。

單片約6秒為預算，實長取決於兩段乾淨可用區間。兩套全程同時可見，沒有換鏡故不額外添加過場；若另加切換仍使用0.75秒疊化。無字無音，原動作／原速。先驗單側身分／衣服／手包／背景，再驗雙側尺度與整片舒服度。

每套直式proof與獨立Carousel A/B/C仍另需完成；左右片不能替代這些資產。新首幀需使用者視覺核准後才送Grok，成片另核准。不得因本次格式指示視為M03/M05影片核准。
''',encoding='utf-8')
p=week/'publishing_structure.md';s=p.read_text(encoding='utf-8');s=s.replace('M04已準備獨立Reel/Carousel工作單，尚未生成新素材。','M04依使用者新指示改左右同框：左褲裝、右裙裝，用同一鈷藍包比較；分鏡與窄幅動作範圍已更新，起始圖接續生成。')
s=s.replace('- 兩套約0.75秒柔和交叉溶接，','- M04改左右並列，兩套同時呈現且無片內切鏡；其餘兩套約0.75秒柔和交叉溶接，')
p.write_text(s,encoding='utf-8')
p=ROOT/'CURRENT_STATUS.md';s=p.read_text(encoding='utf-8');entry='''## W41 M04 selected as side-by-side comparison — 2026-10-08

User explicitly requests the final fifth Reel in the earlier left/right form. M04 storyboard updated before first-frame generation: left trouser look, right skirt look, same cobalt shoulder bag against neutral clothes and quiet bookstore porch. Separate native9:16 complete-person starting stills, matched head/waist/shoe positions, tight central motion envelope; independent same-side strap contact then return, ordinary source speed. Fixed proportional panel crops must be chosen after real motion QA and phone-size review; no copied historical scale correction, stretching or forced synchronized action. No within-film cut, therefore no extra dissolve; any later switch still defaults0.75s. New stills and film require separate visual approvals. This request does not approve pending M03/M05 films or overwrite old batch. M04 stills next; proof/Carousel incomplete.

''';p.write_text(s.replace('# Current Status - Mira AI Fashion Creator\n\n','# Current Status - Mira AI Fashion Creator\n\n'+entry,1),encoding='utf-8')
print('M04 parallel storyboard saved before image generation.')
