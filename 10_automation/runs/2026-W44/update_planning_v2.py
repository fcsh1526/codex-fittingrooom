"""Migrate the draft renderer to source-backed v2 input; preserve the v1 snapshot."""
from pathlib import Path
R=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent
p=RUN/'build_planning_review.py';t=p.read_text(encoding='utf-8')
start=t.index('materials=');end=t.index('for s in series:')
t=t[:start]+'''materials={e['source_row_id']:e['material_id'] for e in index['entries'] if e['availability']=='present'}
config=json.loads((RUN/'planning_input_v2.json').read_text(encoding='utf-8'))
sources=config['sources'];series=config['series']
dump(OUT/'research_receipt.json',{'checked_date':'2026-10-27','timezone':'Asia/Taipei','content_week':'2026-W44','version':'v2_source_verified','week_dates':['2026-10-26','2026-11-01'],'perplexity':{'url':'https://mika-lin-weekly.pplx.app/weeks/2026-W44.html','status':'browser_verified_and_original_csv_saved','missing_source_weeks':[],'new_source_csv_imported':True,'source_receipt':'10_automation/runs/2026-W44/source_receipt.json'},'pool_refresh':{'as_of':'2026-10-27','window_weeks':3,'current_source_candidates':60,'coverage':{'2026-W42':20,'2026-W43':20,'2026-W44':20}},'sources':sources,'editorial_basis':'W44最新研究＋W42/W43近期材料，依台灣天氣重組完整搭配；來源主張與編輯設計分開。','earlier_draft':'history/before_W44_source_retrieval_2026-10-27','source_articles':'紫色、洋裝、鞋、紅色與腰巾相關原文段落直接回讀；並非所有上游連結或商品均已核實。','generation_authorized':False})

'''+t[end:]
# A garment-aware schematic, with the same outfit design as the written list.
start=t.index('for s in series:\n im=Image.new');end=t.index('def camera_svg(frame):')
t=t[:start]+'''def dressed(s,look,mode='full'):
 r=s['render'];im=Image.new('RGB',(300,420),'white');d=ImageDraw.Draw(im)
 up,lo,bg=r['upper'][look],r['lower'][look],r['bag'][look]
 d.ellipse([132,18,168,54],outline='#26313b',width=2)
 d.polygon([(109,66),(191,66),(184,168),(116,168)],fill=up,outline='#26313b')
 d.line([(111,68),(96,206)],fill='#26313b',width=3);d.line([(189,68),(204,201)],fill='#26313b',width=3)
 if r['layer'][look]:
  d.polygon([(139,67),(161,67),(169,165),(131,165)],fill=r['inner'][look],outline='#59636b')
 if r.get('slip',[False,False])[look]:
  d.line([(127,76),(127,108)],fill=lo,width=5);d.line([(173,76),(173,108)],fill=lo,width=5)
  d.polygon([(124,105),(150,119),(176,105),(183,170),(117,170)],fill=lo,outline='#26313b')
 if r['skirt'][look]:
  d.polygon([(116,168),(184,168),(191,301),(109,301)],fill=lo,outline='#26313b')
  d.line([(132,302),(131,362)],fill='#26313b',width=3);d.line([(168,302),(171,362)],fill='#26313b',width=3)
 else:
  d.polygon([(116,168),(184,168),(184,350),(157,350),(150,194),(143,350),(116,350)],fill=lo,outline='#26313b')
 ov=r.get('overshirt',[None,None])[look]
 if ov:
  d.polygon([(108,64),(134,64),(129,208),(104,208)],fill=ov,outline='#26313b');d.polygon([(166,64),(192,64),(196,208),(172,208)],fill=ov,outline='#26313b')
  d.line([(110,69),(94,206)],fill=ov,width=9);d.line([(190,69),(206,204)],fill=ov,width=9)
 belt=r.get('belt',[None,None])[look]
 if belt:d.rectangle([116,165,184,173],fill=belt,outline='#26313b')
 scarf=r.get('scarf',[None,None])[look]
 if scarf:
  d.rectangle([114,165,183,174],fill=scarf,outline='#26313b');d.polygon([(119,170),(105,212),(123,207),(129,171)],fill=scarf,outline='#26313b')
  d.ellipse([112,165,126,179],fill=scarf,outline='#26313b')
  for xx in [132,161]:d.line([(xx,162),(xx,177)],fill='#e8e3d7',width=3)
 d.line([(120,363),(141,363)],fill='#e0e5e8' if s['id']=='03' else '#26313b',width=8);d.line([(159,363),(181,363)],fill='#e0e5e8' if s['id']=='03' else '#26313b',width=8)
 d.rectangle([192,162,222,202],fill=bg,outline='#26313b',width=2)
 d.line([(183,96),(209,162)],fill='#59636b',width=2)
 if mode=='lower_proof':im=im.crop((75,229,225,389))
 elif mode=='proof':im=im.crop((72,10,230,235))
 return im

from PIL import ImageOps
for s in series:
 im=Image.new('RGB',(1600,1000),'#f5f3ed');d=ImageDraw.Draw(im)
 txt(d,(55,28),f"MIRA / W44 v2 · {s['id']} {s['title']}",32,b=True)
 txt(d,(55,78),s['question'],23);txt(d,(55,120),'已補齊W42–W44來源 · 編輯提案待審 · 線稿不是AI身份／動態或實穿驗證',19)
 for k in range(4):
  x=55+k*385;d.rounded_rectangle((x,168,x+355,755),radius=12,fill='white',outline='#d3d4ce',width=2)
  if s['recipe']=='parallel_comparison':
   for look in [0,1]:
    tile=ImageOps.contain(dressed(s,look),(166,390));im.paste(tile,(x+10+look*174,220))
  else:
   look=0 if k<2 else 1
   mode='proof' if (s['id']=='04' and k in [0,3]) or (s['id']=='05' and k in [1,2]) else 'lower_proof' if s['id']=='03' and k in [1,2] else 'full'
   tile=ImageOps.contain(dressed(s,look,mode),(300,400));im.paste(tile,(x+(355-tile.width)//2,203+(400-tile.height)//2))
  d=ImageDraw.Draw(im);d.line([(x+22,624),(x+333,624)],fill='#bec7c9',width=2)
  for j,line in enumerate(wrap(s['beats'][k],17)):txt(d,(x+15,640+j*25),f'{k+1:02} '+line if j==0 else line,17)
  txt(d,(x+15,702),'人物 → 持續前進' if s['previs_required'] else '人物 → 自然短步／淺側轉',16)
  txt(d,(x+15,730),'相機 → 獨立曲線，見同步預演' if s['previs_required'] else '相機 → 固定／依資訊取景',15)
 y=782
 for look in [0,1]:
  for j,line in enumerate(wrap(s['looks'][look],68)):
   txt(d,(55,y),f'L0{look+1}  '+line if j==0 else '       '+line,17);y+=24
  y+=8
 txt(d,(55,934),'原速、無烙字；切換預設0.75秒柔接。讀衣時間、身份、實際步態與接點舒服度仍待驗收。',19)
 txt(d,(55,971),'01路線共用同場地同時間模型；02並排；03–05獨立鏡位。完整來源與逐鏡時序見企劃頁。',16)
 im.save(OUT/f"series_{s['id']}_storyboard.png")

'''+t[end:]
t=t.replace("'weeks':{'source':['2026-W41']","'weeks':{'source':sorted({'2026-'+x.split('-')[0] for x in s['source_rows']})")
t=t.replace("'source_asset_ids':['source_W41','research_receipt']","'source_asset_ids':['source_'+w,'research_receipt'] if False else ['source_'+w for w in sorted({'2026-'+x.split('-')[0] for x in s['source_rows']})]+['research_receipt']")
t=t.replace("for aid,path in [('source_W41',ROOT/'10_automation/runs/2026-W41/source_perplexity.csv'),('research_receipt',OUT/'research_receipt.json')]:", "for aid,path in [('source_'+w,ROOT/'10_automation/runs'/w/'source_perplexity.csv') for w in sorted({'2026-'+x.split('-')[0] for x in s['source_rows']})]+[('research_receipt',OUT/'research_receipt.json')]:")
t=t.replace("'plan_id':f\"2026-W44-{s['id']}-v1\"","'plan_id':f\"2026-W44-{s['id']}-v2\"")
t=t.replace('線稿提案 v1','線稿提案 v2')
start=t.index("body='''");end=t.index('for src in sources:',start)
t=t[:start]+'''body=\'\'\'<h1>MIRA · 本週製作提案 v2</h1><p>2026-W44｜10/26–11/1｜10/27來源補正<br><span class="tag">已讀W44原始週報 · 待確認企劃／分鏡 · 尚未生成起始圖</span></p><section><h2>來源已補齊，舊提案已封存</h2><p>你提供的W44頁面可以正常讀取。先前是網頁讀取器與受限命令環境無法取得，不能推為站點或週報不存在。瀏覽器確認後，已成功保存公開索引、W42–W44三週原始CSV與報告，並核對每份20列／5個來源方向，頁面內CSV逐列一致。</p><p>近期素材池現有60筆候選、缺週0。紫色在W43和W44重複，是可延續的來源訊號；W43棕丹寧／月牙包與W42膝長裙／平底鞋可作本週搭配素材。完整造型、場合與系列仍由Mira編輯，不直接照搬上游系列卡或其功能說法。</p><p>台灣天氣沿用本輪已查的逐日預報：北部可穿脫薄外層，中南部以短袖、薄襯衫與輕料為主。只表達可見衣長、層次、色塊與鞋型；不由AI圖推論透氣、防滑或實穿舒適。</p>\'\'\'
'''+t[end:]
t=t.replace('目前只驗空間，不模擬衣服混影','目前只驗空間，不模擬衣服混影')
t=t.replace('全身讀衣目標各6.25秒','兩套紫色外搭／灰褲與棕丹寧，全身讀衣目標各6.25秒')
t=t.replace('01第一套原生9:16全身候選一張','確認後所選系列的第一套原生9:16全身候選一張')
t=t.replace('先確認五個選題／兩套搭配，以及01的雙路徑和相機視角。','v1已因來源補正封存，本頁v2尚待確認。先確認五個選題／兩套搭配，以及01的雙路徑和相機視角。')
start=t.index("summary=['# W44");end=t.index("(RUN/'publishing_structure.md').write_text",start)
t=t[:start]+'''summary=['# W44 製作規劃 v2（來源已補齊，待使用者確認）','','規劃日：2026-10-27（台灣）；內容週：2026-W44，10/26–11/1。','', '## 本輪補正','','使用者提供W44直接報告後，瀏覽器成功讀到頁面；再以允許的直接網路存取保存索引與W42–W44原始CSV／HTML。三週各20列、5個來源方向，與頁面內CSV逐列一致。先前工具連線失敗不代表來源未發布。舊企劃保存在history/before_W44_source_retrieval_2026-10-27，已被本v2取代，尚未取得任何企劃核准。','', '素材池現有近三週60筆來源候選，缺週0。W44提供紫色、洋裝內搭、低筒鞋、紅配件、腰巾；W43棕丹寧／月牙包與W42膝長裙／平底鞋作跨週搭配材料。完整搭配是編輯提案，不是上游原始列或現成AI照片。','', '台灣逐日天氣已於本輪查核：北部有雨與回暖，中南部仍暖。以薄料、短袖和可脫外層安排；AI圖不驗證透氣、全天好走、防滑或材質觸感。','', '## 五系列、十套','','|系列|人物|方法|狀態|','|---|---|---|---|']
for s in series:summary.append(f"|{s['id']} {s['title']}|{s['model']}|{s['recipe']}|v2提案待審|")
summary+=['','正式契約保持五位各一次、每位兩套、五支Reel；每套native9:16全身＋proof、獨立Carousel A/B/C。完整穿搭和material_id見planning/proposed_look_plan.csv，人物雙參照檔案存在。','','## 分鏡／預演','','[打開企劃與同步預演](planning/review.html)。01為紫色外搭的工作日／週末連續路線，俯視與相機視角由同一shared_space.json投影，沿用的幾何是未測量示意；重新確認本週衣服閱讀價值，不冒稱M03原五套片已改好。02並排需要兩側各8秒可用原速來源，不以6秒循環湊長。03–05以獨立鏡位讀鞋口／紅色位置／腰巾褲耳，不需要共用空間軌道。','','01兩鏡[0,168)、[150,318)，24fps／13.25秒，18f柔接，每套6.25秒清楚全身。02同時兩側[0,192)，8秒。03–05四鏡[0,96)、[78,174)、[156,252)、[234,330)，13.75秒；各18f柔接，clear_read共11.5秒，每套5.75秒（含full/proof）。時間為計畫預算，實際可用片長需下載後重查。','','## 生成閘門','','來源補正不是企劃或照片核准。先確認本v2系列／兩套／分鏡與必要預演，再開始首張全身候選。新圖仍逐張視覺核准後才入動態。5份計畫結構檢查應無錯誤，ready_for_generation=false。尚無AI起始圖／新影片／外部上傳／發文或排程。','','W43已核准M03五套影片與快步／曲線／閃爍待改範圍保持；W42/W43本次補的是歷史研究來源，不重定其舊交付批次。發布日期、網址與成效未知者留空。']
'''+t[end:]
p.write_text(t,encoding='utf-8')
print('Renderer migrated to v2 source-backed input.')
