from pathlib import Path
import json, hashlib, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT=Path.cwd(); P=Path(__file__).resolve().parent
SRC=P.parent/'performance_revision_2026-11-06'
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',n)
def dump(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

concepts=[
 {'id':'A','title':'她在等你一起走','hook':'回望與笑容帶來親近感','expectation':'她會如何回應、邀你同行？','method':'single_shot_performance','beats':['0–1秒｜側身已回望你','1–3秒｜笑容展開，肩膀隨反應放鬆','3–5秒｜轉向街道，回望同行者'],'wardrobe':'同套深底花襯衫＋黑直褲','assets':'先做既有來源的5秒草剪；沒有補圖。素材不含明確「認出你」起因，不能宣稱完整達成。','risk':'笑容較大，是否自然及親近仍需原速觀看；不能只用動機文字保證觀眾看懂。','next':'先呈現一個原速草剪，若觀看理由仍不成立，回到開場設計而非繼續縮短微調。'},
 {'id':'B','title':'花放上面，還是下面？','hook':'花襯衫黑褲 → 素白上衣花裙','expectation':'第二套會把氣質改成什麼樣？','method':'sequential_lookbook','beats':['0–1秒｜花襯衫＋黑直褲，造型清楚','1–3秒｜柔和換到白上衣＋花裙','3–5秒｜看清第二套輪廓、姿態'],'wardrobe':'沿用W45 M04原有L01及L02完整搭配，並非同一件襯衫兩種搭法','assets':'L01已存在；未找到L02生成首圖，需補圖並逐張核准，再生成第二套來源。','risk':'兩套是否有足夠第一眼反差尚未驗證；不恢復左右並排。換段預留0.75秒，不能占滿讀衣時間。','next':'先確認視覺對比方案，再補L02；本輪不新增圖或影片。'},
 {'id':'C','title':'一眼看花，再看整套','hook':'臉與花卉在第一眼清楚可見','expectation':'這件花襯衫搭起來是什麼樣？','method':'sequential_lookbook','beats':['0–1秒｜臉＋上衣中景，花卉清楚','1–3秒｜身體轉側，露出腰線與包','3–5秒｜轉入全身，看完整黑褲比例'],'wardrobe':'同套深底花襯衫＋黑直褲','assets':'現有720p全身來源可試裁，但中景細節不足時需新圖與新來源；全身原片只能作待審素材。','risk':'現有深底花樣未必足以吸引第一眼；中景／全身接點可能重影。不預設推近或裁切本身就是看點。','next':'先用分鏡檢查花樣與整套的揭示是否值得等待；本輪不生成。'}]

plan={'date':'2026-11-09','content_week':'2026-W45','calendar_week':'2026-W46','stage':'opening_concepts_and_one_local_rough_cut','status':'proposed_not_user_accepted','user_reply':'ok','scope':'Proceed with concrete opening proposals following the discussion of first-glance attention. No unseen image/film approval inferred.','purpose':'讓陌生人先停留，再持續看人物與穿搭，逐步建立對Mira的興趣。','timing_note':'0–1/1–3/3–5秒為企劃檢查窗口，不是普遍注意力定律或精確生成承諾。','recommended':'A','recommendation_reason':'先用現有素材驗證人物反應能否形成觀看理由，無新生成成本；B的穿搭資訊最明確，但缺第二套影像。','concepts':concepts,'new_stills':0,'new_video_jobs':0,'previs':'固定鏡頭與簡單單人短步，本輪使用示意分鏡；無複雜共享空間運鏡。','evidence_limits':['既有來源49張抽格及完整解碼，不等於連續原速視覺通過。','草剪同時改開頭區間和固定構圖，屬方向試看，不是能分離因果的A/B。','未取得IG留存數據，不宣稱停留率提升。'],'decision_checks':['不看說明，第一秒是否能指出吸引自己的具體元素？','第三秒是否仍期待一個尚未完整呈現的反應或穿搭資訊？','第五秒是否真的得到相應回報？','若只有動作更多卻沒有觀看期待，不繼續同機制微調。'],'after_publication':'有實際發布權限及數據時，記錄可取得的留存/觀看時間與收藏分享追蹤，記錄分母；區分主觀偏好與觀眾成效。'}
dump(P/'opening_plan.json',plan)

# Schematic production board; no AI-generated or modified photography.
W,H=1500,1720
im=Image.new('RGB',(W,H),'#f4f1ea'); d=ImageDraw.Draw(im)
d.text((40,22),'M04｜陌生人為什麼願意多看幾秒？',font=font(38),fill='#233e40')
d.text((40,78),'三個開場提案｜示意分鏡，非生成結果｜0–5秒是設計窗口，不是成效承諾',font=font(23),fill='#54605f')
def person(x,y,pose,look,medium=False):
    # 150x250 portrait figure; visible neckline, waist and shape.
    cx=x+77; hy=y+42
    d.ellipse((cx-18,hy-24,cx+18,hy+24),outline='#273f40',width=3)
    d.arc((cx-11,hy-7,cx+12,hy+13),0,165,fill='#273f40',width=2)
    for ex in [-7,7]:d.ellipse((cx+ex-2,hy-5,cx+ex+2,hy-1),fill='#273f40')
    sw=23 if pose=='side' else 33
    top=[(cx-sw,hy+31),(cx+sw,hy+31),(cx+25,hy+104),(cx-25,hy+104)]
    d.polygon(top,fill='#f4e8cc' if look=='skirt' else '#3c3038',outline='#273f40')
    if look!='skirt':
        for dx,dy in [(-15,47),(13,61),(-10,83),(15,94)]:d.ellipse((cx+dx-5,hy+dy-5,cx+dx+5,hy+dy+5),fill='#be596a')
    d.line((cx-sw,hy+34,cx-sw-14,hy+89,cx-sw-10,hy+124),fill='#273f40',width=4)
    d.line((cx+sw,hy+34,cx+sw+12,hy+91,cx+sw+8,hy+119),fill='#273f40',width=4)
    if not medium:
        if look=='skirt':
            d.polygon([(cx-25,hy+105),(cx+25,hy+105),(cx+31,hy+183),(cx-31,hy+183)],fill='#3c3038')
            for dx,dy in [(-13,120),(12,139),(-8,160),(14,175)]:d.ellipse((cx+dx-5,hy+dy-5,cx+dx+5,hy+dy+5),fill='#be596a')
            d.line((cx-13,hy+183,cx-14,hy+205),fill='#273f40',width=4);d.line((cx+13,hy+183,cx+17,hy+205),fill='#273f40',width=4)
        else:
            shift=15 if pose=='step' else 0
            d.polygon([(cx-25,hy+105),(cx-2,hy+105),(cx-8-shift,hy+203),(cx-27-shift,hy+203)],fill='#30343b')
            d.polygon([(cx+1,hy+105),(cx+25,hy+105),(cx+30,hy+203),(cx+10,hy+203)],fill='#30343b')
    if pose=='step':d.line((x+100,y+245,x+148,y+245),fill='#c37b42',width=4);d.polygon([(x+148,y+245),(x+135,y+237),(x+135,y+253)],fill='#c37b42')
for i,c in enumerate(concepts):
    y=137+i*505
    d.rounded_rectangle((30,y,1470,y+480),radius=18,fill='#fffcf7',outline='#c9d0c8',width=2)
    d.text((55,y+18),f"{c['id']}  {c['title']}"+('  ← 優先試看' if i==0 else ''),font=font(29),fill='#233e40')
    d.text((55,y+65),'第一眼：'+c['hook']+'　｜　期待：'+c['expectation'],font=font(22),fill='#54605f')
    for j,beat in enumerate(c['beats']):
        x=62+j*468
        d.rounded_rectangle((x,y+110,x+430,y+385),radius=8,fill='#ecece5')
        d.line((x+30,y+120,x+30,y+350,x+400,y+360),fill='#c8ccc4',width=3)
        pose=('side' if j==0 else 'front') if i==0 else ('side' if j==1 else 'front')
        if i==0 and j==2:pose='step'
        if i==2 and j==0:
            canvas_draw=d
            close=Image.new('RGB',(210,300),'#ecece5');d=ImageDraw.Draw(close)
            person(25,0,pose,'blouse')
            d=canvas_draw
            im.paste(close.crop((45,0,160,155)).resize((180,243)),(x+125,y+118))
        else:
            person(x+139,y+120,pose,'skirt' if i==1 and j>0 else 'blouse')
        if i==2 and j==0:d.text((x+15,y+340),'中景：臉與花卉優先',font=font(18),fill='#754e40')
        d.text((x+5,y+397),beat,font=font(21),fill='#233e40')
    note=['既有素材先試剪；回望不自動等於「認出你」，笑容自然度仍待看。','須補第二套首圖與原片；順序比較，左右並排維持暫停。','先檢查花樣是否值得看；不以裁切、推近本身當成看點。'][i]
    d.text((55,y+443),note,font=font(20),fill='#7d5943')
d.text((40,1662),'同一位模特兒；無字原速成片。分鏡註記不會烙入影片。內容週沿用 W45，未開新週製作。',font=font(21),fill='#54605f')
im.save(P/'opening_storyboards.png')
import sys
if '--board-only' in sys.argv:
    print('Storyboard rebuilt; no video or current-state records changed.')
    sys.exit(0)

ff=ROOT/'openmontage/.local/bin/ffmpeg.exe'
out=P/'A_existing_source_opening_rough_v1.mp4'
# 120 consecutive original frames, fixed 580x1032 crop. No retiming/reordering.
vf='trim=start_frame=18:end_frame=138,setpts=PTS-STARTPTS,crop=580:1032:70:80,scale=720:1280:flags=lanczos'
args=[str(ff),'-v','error','-y','-i',str(SRC/'S01_source.mp4'),'-vf',vf,'-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
r=subprocess.run(args,capture_output=True,text=True);assert r.returncode==0,r.stderr
r=subprocess.run([str(ff),'-v','error','-i',str(out),'-f','null','-'],capture_output=True,text=True);assert r.returncode==0,r.stderr
dump(P/'rough_cut_receipt.json',{'source':str((SRC/'S01_source.mp4').relative_to(ROOT)),'source_uuid':'8e660c39-6175-4491-8bcb-2cda03f4eb3a','source_sha256':sha(SRC/'S01_source.mp4'),'source_frames_half_open':[18,138],'fps':24,'seconds':5,'crop_xywh':[70,80,580,1032],'output_size':[720,1280],'output_sha256':sha(out),'native_speed':True,'audio':False,'baked_text':False,'new_generation':False,'full_decode':True,'visual_native_speed_pass':False,'purpose':'Opening composition and reaction timing study; not a final film or defect repair. Full uncropped source retained for physical QA.','user_acceptance':None})

report='''# M04 開場研究｜2026-11-09

本輪是三個具體開場提案及一個既有來源草剪，不是三支新生成影片，也不是發布版。內容週仍是W45；11/9為W46日曆週，未啟動W46週企劃。

## 為什麼先做A

先用人物的回望、笑容與離開動作測試親近感。現有來源可以有界試剪，無需額外生成。B的花卉上／下身對比最直接傳達穿搭資訊，但缺L02影像；C仍需證明花樣本身足以吸引觀看，不能僅憑改景別成立。

## 現有素材的觀察

11/6已生成並下載6.041667秒原片，11/9完成本機解碼及49張每3格抽樣。約0–0.75秒以正面站姿為主；其後轉側，約2.125–2.5秒嘴張開，3–4.5秒笑容持續，後段轉向騎樓邁步。這是可見動作；「朋友回應」「認出你」「邀你同行」是企劃動機，不是影像已證實的事件。較大的開口笑是否自然需原速觀看，不以抽格宣稱成功。

A草剪取原片0.75–5.75秒，固定裁去部分外圍與下身，讓臉及花襯衫更易讀；原速、連續、不調換、不重複。裁切是開場構圖選擇，不能證明被裁掉的足部品質通過。全長無音副本與原始帶音來源均保留。此草剪並未新增更明確的反應起因，因此不宣稱完整做出「認出你」。

## 如何判斷

先看沒有文案解釋的草剪：第一眼是否有吸引力；第三秒是否仍期待人物的下一個反應；第五秒是否得到相應回報。若只是看見她笑，卻不想繼續看，就不要把這個方向當作已成立。未做完整連續原速視覺驗收，未獲使用者接受，未有IG數據。

素材盤點：B沿用週企劃的花襯衫＋黑褲與白T＋花裙；並不是同件襯衫兩種搭法。L02新圖仍需視覺核准。左右比較維持暫停；無新圖、無新影片生成、無額外付費服務、無發布。

本次優先方案是編輯建議，三方案並未獲逐項核准。既有六種方法及兩種研究分類維持；不把吸引力機制另加成剪輯方法。沒有把本次討論自動改寫成全專案已驗證的新規則。
'''
(P/'REVIEW.md').write_text(report,encoding='utf-8')
dump(P/'user_direction.json',{'date':'2026-11-09','quote':'ok','preceding_proposal':'先做出幾個能看見差異的開場方案，再決定人物如何表演。','scope':'Proceed with opening study; not image/film acceptance or publication approval.'})
qpath=ROOT/'10_automation/runs/2026-W45/production_queue.json'; q=json.loads(qpath.read_text(encoding='utf-8-sig'))
q.update(status='M04_opening_concepts_and_existing_source_rough_pending_review',video_jobs_completed=18,latest_editorial_proposal=(P/'opening_plan.json').relative_to(ROOT).as_posix(),latest_edit_receipt=(P/'rough_cut_receipt.json').relative_to(ROOT).as_posix(),active_reviews=[out.relative_to(ROOT).as_posix()],next={'model':'M04','action':'Review the three opening concepts and the A existing-source rough. No new generation until the chosen design and any new still meet current approval scope.'})
dump(qpath,q)
sp=SRC/'source_plan.json';s=json.loads(sp.read_text(encoding='utf-8-sig'));s.update(status='downloaded_technical_checked_editorially_reassessed',reviewed_at='2026-11-09',technical_review='technical_review.json',current_editorial_proposal=(P/'opening_plan.json').relative_to(ROOT).as_posix());dump(sp,s)
note='''## 2026-11-09 現行接續：開場吸引力研究

使用者同意先具體規劃讓陌生人停留的開場。仍接續W45 M04，沒有開啟W46製作。三個提案為人物親近感、花卉上／下身對比、花樣到整套揭示；編輯優先A，已用11/6來源製作5秒原速固定裁切草剪，非新生成／非發布版。詳 `10_automation/runs/2026-W45/reels/M04/opening_study_2026-11-09/REVIEW.md`。11/6第18支原片已下載，11/9完成解碼與抽格；累計9次靜態、18支原片、2支已接受。原速整片視覺檢查與使用者接受未完成。下一步評估開場的觀看理由，不沿用舊待生成狀態。左右比較暫停、新圖逐張核准、六種方法＋兩種研究維持。此節優先於下方11/6的17支原片摘要；本次無新生成、無發布。

'''
for rel in ['CURRENT_STATUS.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W45/publishing_structure.md']:
    path=ROOT/rel;t=path.read_text(encoding='utf-8-sig')
    if '## 2026-11-09 現行接續：開場吸引力研究' not in t:
        title,tail=t.split('\n',1);path.write_text(title+'\n\n'+note+tail.lstrip('\n'),encoding='utf-8')
print(json.dumps({'board':str(P/'opening_storyboards.png'),'preview':str(out),'source_sha256':sha(SRC/'S01_source.mp4'),'new_generations':0},ensure_ascii=False))
