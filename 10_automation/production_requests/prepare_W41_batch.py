"""Initialize the authorized W41 batch from the downloaded report, without touching W37."""
import csv
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / '10_automation/runs/2026-W41'
SOURCE = Path('C:/Users/Brandon_ChangChien/Downloads/2026-W41.csv')
WEEK = '2026-W41'
sys.path.insert(0, str(ROOT / '10_automation'))
from build_weekly_look_plan import LOOK_FIELDS
from build_weekly_packet import note_fields

RUN.mkdir(parents=True, exist_ok=True)
saved_source = RUN / 'source_perplexity.csv'
if saved_source.exists() and saved_source.read_bytes() != SOURCE.read_bytes():
    raise RuntimeError('A different W41 source already exists; preserve it and reconcile first.')
if not saved_source.exists():
    shutil.copyfile(SOURCE, saved_source)
source_rows = list(csv.DictReader(saved_source.open(encoding='utf-8-sig', newline='')))
assert len(source_rows) == 20
assert {r['week'] for r in source_rows} == {WEEK}
assert len({r['trend_name'] for r in source_rows}) == 5
receipt = {
    'week': WEEK,
    'report_url': 'https://mika-lin-weekly.pplx.app/weeks/2026-W41.html',
    'csv_url': 'https://mika-lin-weekly.pplx.app/data/2026-W41.csv',
    'retrieved_date': '2026-10-08',
    'method': 'user-opened local IAB homepage -> visible W41 archive link -> CSV download',
    'sha256': hashlib.sha256(saved_source.read_bytes()).hexdigest(),
    'rows': 20,
    'themes': 5,
    'editorial_review': 'Five daily dressing rules retained; second complete outfits are Codex editorial expansions, not additional Perplexity rows.',
    'evidence_limit': 'Report clothing input read. External trend articles not independently verified; do not repeat their popularity or product claims as verified facts.'
}
(RUN / 'source_receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
subprocess.run([sys.executable, str(ROOT / '10_automation/run_weekly_pipeline.py'),
    '--week', WEEK, '--perplexity-source', str(saved_source), '--skip-image-jobs',
    '--skip-validation', '--skip-asset-template', '--skip-status'], cwd=ROOT, check=True)
packets = list(csv.DictReader((RUN / 'weekly_content_packet.csv').open(encoding='utf-8-sig', newline='')))

# Each theme's second outfit preserves its dressing rule while adding a distinct wearable solution.
pairs = [
    [
      ('奶油白短外套配可可棕長褲', '奶油白短版無鋪棉立領外套，敞開；白色圓領棉短袖；可可棕高腰直筒斜紋長褲；黑色低跟樂福鞋；黑色小方肩包；窄黑皮帶', '奶油白／白／可可棕／黑', '薄斜紋棉外層／中薄棉上衣／輕薄斜紋長褲', '短立領與腰胯上方衣長；敞開外套內的短袖、直筒褲腳及鞋面'),
      ('炭灰短外套配淺灰直筒褲', '炭灰短版無鋪棉立領外套，敞開；奶油白圓領棉短袖；淺灰高腰直筒斜紋長褲；黑色低跟樂福鞋；黑色小方肩包；窄黑皮帶', '炭灰／奶油白／淺灰／黑', '薄斜紋棉外層／中薄棉上衣／輕薄斜紋長褲', '同樣短衣長、短立領和短袖內搭，改為淺灰下身的明暗關係')
    ],
    [
      ('奶油白海軍藍格紋配炭灰褲', '奶油白海軍藍薄棉格紋襯衫，尖領、袖口翻一折、下襬整齊紮入；炭灰高腰直筒長褲；黑色低跟便鞋；黑色小方肩包；小型銀耳針', '奶油白／海軍藍／炭灰／黑', '薄棉府綢／輕薄西裝混紡', '格紋只在上衣；整段素色褲鞋包清楚可見'),
      ('可可棕奶油白格紋配深藍褲', '可可棕奶油白細格薄棉襯衫，尖領、袖口翻一折、下襬整齊紮入；深海軍藍高腰直筒長褲；深棕低跟便鞋；深棕小方肩包；小型銀耳針', '可可棕／奶油白／海軍藍／深棕', '薄棉府綢／輕薄西裝混紡', '細格僅在上衣；深色褲鞋包與格紋形成留白')
    ],
    [
      ('奶油白棉T配可可棕丹寧', '奶油白圓領棉短袖，整齊紮入；可可棕高腰直筒丹寧褲，無刷破、褲腳停在鞋面；米白薄短外套敞開；黑色低跟便鞋；黑色小方肩包；黑色窄皮帶', '奶油白／可可棕／黑', '中薄棉／中薄丹寧／薄棉斜紋外套', '白上衣、棕色丹寧和黑鞋包的三色分工，能辨認腰頭與直筒褲腳'),
      ('白短袖襯衫配可可棕丹寧', '白色棉質短袖尖領襯衫，整齊紮入；可可棕高腰直筒丹寧褲，無刷破、褲腳停在鞋面；黑色低跟便鞋；黑色小方肩包；黑色窄皮帶', '白／可可棕／黑', '薄棉府綢／中薄丹寧', '相同棕色直筒丹寧，白棉T換成白襯衫，腰線和鞋包保持清楚')
    ],
    [
      ('米白西外配白T深藍褲', '米白無鋪棉輕薄單排扣西裝外套，敞開、袖口翻一折；白色圓領棉短袖紮入；深藍高腰直筒長褲；黑色低跟便鞋；深棕肩背包；小型銀耳針', '米白／白／深藍／深棕／黑', '輕薄西裝混紡／中薄棉', '外套翻領、棉T圓領、翻折袖口與直筒褲的正式／日常關係'),
      ('深藍西外配淺灰T奶油白褲', '深藍無鋪棉輕薄單排扣西裝外套，敞開、袖口翻一折；淺灰圓領棉短袖紮入；奶油白高腰直筒長褲；黑色低跟便鞋；黑色肩背包；小型銀耳針', '深藍／淺灰／奶油白／黑', '輕薄西裝混紡／中薄棉', '相同西外配圓領棉T的規則，以深外層和淺色直筒褲形成第二套')
    ],
    [
      ('白T炭灰長褲配鈷藍小包', '白色圓領棉短袖紮入；炭灰高腰直筒長褲；黑色無鋪棉薄短外套敞開；黑色低跟便鞋；鈷藍霧面小肩包、短肩帶；小型銀色幾何耳針', '白／炭灰／黑／鈷藍／銀', '中薄棉／輕薄斜紋／霧面合成皮', '鈷藍包為唯一亮色；白灰黑衣服和小銀耳針不搶焦點'),
      ('白襯衫黑中長裙配鈷藍小包', '白色短袖棉襯衫整齊紮入；黑色高腰小腿中長A字棉裙；黑色圓方頭平底便鞋；鈷藍霧面小肩包、短肩帶；小型銀色幾何耳針', '白／黑／鈷藍／銀', '薄棉府綢／不透膚棉裙／霧面合成皮', '褲裝改裙裝，唯一鈷藍包焦點保留；裙長與完整鞋包可見')
    ]
]
scenes = [
    '社區辦公樓的明亮有頂入口，淺灰牆、短木長椅與完整地面；用於出門前整理可敞開薄外層，兩套沿用同一光向與拍攝位置',
    '書店外有頂人行入口，素米灰牆面與一小段木窗框；圖案衣服靠素背景及素色下身讀清，兩套沿用同一鏡位',
    '街角咖啡店外的遮蔭步道，灰米色牆面與石地；短距離移重心展示牛仔褲腰線與褲腳，兩套保留同一光向',
    '辦公區午餐店旁的安靜有頂走道，米灰牆與一張簡單長椅；西外配棉T能連接上班與午餐，兩套同機位同光向',
    '週末書店旁的淡灰門廊，背景少量木框且沒有彩色物；中性色背景讓鈷藍包成唯一亮色，兩套維持同一機位'
]
actions = [
    '空手在外套腰側前緣輕扶一下後自然放下，露出短袖與短衣長；包在另一側且不遮腰線',
    '空手輕順已翻折的襯衫袖口後放下，保留格紋上衣與素色下身的完整關係',
    '往前短跨一步後自然停住，褲腳與鞋子保持可見，手臂放鬆不插口袋',
    '空手輕順已翻折的西外袖口後放下，外套敞開，棉T圓領全程可見',
    '空手輕扶肩包短帶一次後放下，鈷藍包仍停在腰胯旁、不跨到衣服中央'
]
looks = []
films = []
for i, packet in enumerate(packets):
    matching = next(r for r in source_rows if r['trend_name'] == packet['trend_name'])
    editorial = note_fields(matching['notes'])
    ids = []
    for order, (name, outfit, colors, fabric, proof) in enumerate(pairs[i], 1):
        look_id = f"{packet['carousel_id']}-L{order:02d}"
        ids.append(look_id)
        looks.append(dict(week_id=WEEK, carousel_id=packet['carousel_id'], model_profile_id=packet['model_profile_id'],
            look_id=look_id, look_order=order, theme_name=packet['trend_name'], opening_hook=editorial['opening_hook'],
            look_name=name, dressing_decision=editorial['editorial_answer'], occasion=packet['occasion'],
            clothing_item=outfit, color_palette=colors, fabric=fabric,
            fit='自然健康比例；下身不拖地；外層可敞開；完整鞋包可讀', styling_rules=editorial['practical_rule'],
            visual_proof=proof, practical_rule=editorial['practical_rule'], scene=scenes[i], visible_action=actions[i],
            frame_plan='carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16+styling_proof',
            required_frames=3, status='editorial_approved', next_action='Generate Reel full A; new still remains candidate until user visual approval'))
    films.append(dict(reel_id=f"{WEEK}-{packet['model_profile_id']}-reel", look_ids=ids,
        audience_problem=editorial['audience_problem'], visual_theme=editorial['opening_hook'], scene_purpose=scenes[i],
        format_variant='A', nominal_output_seconds=11.25,
        shots=[dict(shot_id=s, look_id=l, starting_view='native_9x16_full_person', framing='full_person',
            person_position='same image center; head and shoe bounds matched across both looks',
            face='front or slight three-quarter; readable at opening; no large turn',
            light='soft daylight from camera left; similar exposure in both looks',
            action_start='feet grounded; free hand relaxed before the gesture or short step',
            action=actions[i], action_end='hand relaxed; clothes unobscured; brief natural settle',
            camera='fixed level 50mm view', generation_budget_seconds=6,
            source_speed='unchanged', outfit_information=pairs[i][j][4],
            ending_handle='reserve readable late frames; select actual clean interval after generation')
            for j, (s, l) in enumerate(zip(['A', 'B'], ids))],
        join=dict(type='cross_dissolve', seconds=0.75, basis='similar full-person scale, face/waist/shoe position, light and settled gesture phase',
            note='Actual cut timing chosen from motion sources; overlap is intentional. No speed change, freeze or reverse.'),
        proof_policy='Prepare one reviewed vertical proof per look after full-image approval; use separately unless it adds visible information without a disruptive scene/scale change.',
        carousel_status='separate A/B/C assets required; not generated or approved',
        output_status='planned_only', actual_duration=None, output_path=None, user_video_approval=None))
look_path = ROOT / '03_research/editorial_look_plans/2026-W41.csv'
look_path.parent.mkdir(parents=True, exist_ok=True)
if look_path.exists():
    raise RuntimeError('Look source already exists; do not overwrite.')
with look_path.open('w', encoding='utf-8', newline='') as stream:
    writer = csv.DictWriter(stream, fieldnames=LOOK_FIELDS)
    writer.writeheader()
    writer.writerows(looks)
subprocess.run([sys.executable, str(ROOT / '10_automation/run_weekly_pipeline.py'), '--week', WEEK,
    '--look-source', str(look_path)], cwd=ROOT, check=True)
manifest_path = RUN / 'reels/production_manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
by_id = {f['reel_id']: f for f in films}
for record in manifest['reels']:
    plan = by_id[record['reel_id']]
    record.update(audience_problem=plan['audience_problem'], visual_theme=plan['visual_theme'],
        format_variant=plan['format_variant'], storyboard=plan['shots'],
        join=plan['join'], status='storyboard_prepared_new_stills_pending',
        proof_policy=plan['proof_policy'])
manifest['mass_production_gate'] = 'W37_M02_technical_pilot_passed_2026-09-29; current_new_stills_and_final_films_require_separate_visual_approval'
manifest['prior_batch'] = 'W37 first-wave five preserved; no replacement authorized'
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(RUN / 'reels/batch_storyboard.json').write_text(json.dumps(dict(week=WEEK, films=films), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
lines = ['# W41 五支 Reel 製作結構', '', '來源：2026-W41（10/5–10/11）週報，2026-10-08 本機瀏覽器已成功讀取並下载20列CSV。',
    '', '目標：五位各一支、每支兩套。新批獨立保存；W37 第一波五支與Drive檔案不覆蓋。上一批數據另行整理。',
    '', '當前狀態：十套編輯方案與五份分鏡已備妥；尚無新週影片、尚未上傳或發布。新圖與成片各自等待視覺核准。',
    '', '## 五支內容', '', '| 模特兒（內部） | 主題 | 第一套 | 第二套 |', '| --- | --- | --- | --- |']
for i, packet in enumerate(packets):
    lines.append(f"| {packet['model_profile_id']} | {packet['trend_name']} | {pairs[i][0][0]} | {pairs[i][1][0]} |")
lines += ['', '## 剪輯與驗收', '',
    '- 先以兩段全身固定鏡位安排整套穿搭；每鏡一個服務衣服的動作。證據近景另備，不為湊鏡頭而加入。',
    '- 兩套約0.75秒柔和交叉溶接，保持來源動作與速度；約11.25秒只是兩段6秒來源的名義預算，实际时長依可用片段決定。',
    '- 起始圖先匹配臉、腰、鞋位置、人物尺度與背景明暗；單鏡穩定與完整成片舒服度分別驗收。',
    '- 適度疊化重影可保留；不掩蓋單鏡換臉、混衣、手包崩壞或背景飄移。',
    '- 成片與封面無烙字，先交乾淨無音母版。音樂由IG選擇；若確需畫面文字，另通知使用者在IG自行加入。',
    '- 每套仍需可用直式搭配proof與獨立Carousel A/B/C；尚未生成的資產留待完成，不冒充已交付。',
    '- 週報列出的外部流行報導未獨立查核；服裝是虛擬穿搭靈感，不宣稱實際商品性能或實穿體驗。']
(RUN / 'publishing_structure.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
request_path = ROOT / '10_automation/production_requests/2026-10-08_next_five_reels.json'
request = json.loads(request_path.read_text(encoding='utf-8'))
request.update(editorial_scope='new_current_week_from_user_opened_weekly_report', content_week=WEEK,
    source=receipt['report_url'], source_observation='User opened homepage successfully; W41 page and downloadable CSV read. Earlier login redirects are historical failed attempts.')
for slot in request['slots']:
    packet = next(p for p in packets if p['model_profile_id'] == slot['model'])
    slot.update(theme=packet['trend_name'], looks=[x['look_id'] for x in looks if x['model_profile_id'] == slot['model']], status='storyboard_prepared_new_stills_pending')
request_path.write_text(json.dumps(request, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'week': WEEK, 'source_rows':20, 'looks':len(looks), 'films':len(films),
    'model_assignments':[(p['model_profile_id'],p['trend_name']) for p in packets]}, ensure_ascii=False))
