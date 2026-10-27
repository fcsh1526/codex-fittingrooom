from pathlib import Path
import json
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / 'output/pdf/Mira_日常片段與動態輪廓分鏡_2026-10-13.pdf'
pdfmetrics.registerFont(TTFont('MiraChinese', 'C:/Windows/Fonts/msjh.ttc', subfontIndex=0))
INK = colors.HexColor('#24363C')
TEAL = colors.HexColor('#276B70')
GRAY = colors.HexColor('#53656A')
STYLES = {
 'title': ParagraphStyle('title', fontName='MiraChinese', fontSize=23, leading=32, textColor=INK, spaceAfter=14, wordWrap='CJK'),
 'h': ParagraphStyle('h', fontName='MiraChinese', fontSize=16, leading=24, textColor=TEAL, spaceAfter=10, wordWrap='CJK'),
 'body': ParagraphStyle('body', fontName='MiraChinese', fontSize=12, leading=19, textColor=INK, spaceAfter=8, wordWrap='CJK'),
 'label': ParagraphStyle('label', fontName='MiraChinese', fontSize=10, leading=15, textColor=TEAL, spaceAfter=3, wordWrap='CJK'),
 'small': ParagraphStyle('small', fontName='MiraChinese', fontSize=10.5, leading=16, textColor=GRAY, spaceAfter=8, wordWrap='CJK')}

PAGES = [
 {'title':'兩種觀看目的，兩份完整分鏡', 'subtitle':'親切的服裝雜誌感：先決定看什麼，再決定怎麼拍。', 'fields':[
 ('E01 日常片段', 'M03輕薄西外與棉T。看她走過、停下、再離開，讓服裝進入日常。畫面重點是穿出門的整體感，不做兩套優劣比較。'),
 ('E02 動態輪廓', 'M05短外套與直筒褲。重心移動看衣長，淺轉身看側面。動作的用途是增加服裝資訊，不演整理袖口或抓衣襬。'),
 ('本次交付範圍', '沿用W41已定案衣服作為企劃範例；不是開始新一週量產。兩份均為候選分鏡，尚未生成新圖或影片，也沒有取代已交付的五支Reel。'),
 ('共同畫面規則', '每支一位模特兒、她的兩套衣服。原生直式9:16；全身與鞋完整。畫面無文字，人物保留原速，固定攝影機優先；兩段約0.75秒柔和疊化。'),
 ('這次有什麼變化', '觀看目的、動作用途和段落次序更明確。仍可用單畫面依序呈現，不把這兩份企劃稱為新的剪輯技術。時長、角度、站位是試作預算，不能保證生成模型精準遵守。'),
 ('研究依據', '承接10/2細節與整體研究、10/5角度研究、10/6珍藏OOTD的固定鏡頭與人物近遠觀察，以及10/12光線／自然度回饋。本輪沒有新增IG流量查核；未驗證這兩份企劃的曝光成效。') ]},
 {'title':'E01 日常片段｜觀看路線', 'subtitle':'一件輕薄西外，穿進日常。', 'fields':[
 ('衣服與場景', 'M03；2026-W41-004-L01米白西外／白圓領棉T／深藍直筒褲／深棕肩包；L02深藍西外／淺灰棉T／奶油白直筒褲／黑肩包。兩套皆黑色低跟便鞋，袖口已翻一折。場景為午餐店旁安靜有頂走道，米灰牆、完整地面。'),
 ('第一段：走近，停下｜預算7秒', '起始：L01全身、正面可辨識臉，站在中央略遠處。開頭即開始一至兩步自然短走，走近一小段後落腳。終點：中央正面，身體放鬆，外套敞開。走動讓褲腳、衣襬與包的自然擺動可見；停下讓觀眾讀完整套。'),
 ('第二段：停留，離開｜預算7秒', '起始：L02中央全身，尺度接近上一段終點；先有自然重心移動，再沿走道斜向前走一至兩步，結束時仍完整留在畫面。這段是另一個穿搭片刻，不演同一瞬間換裝。步行是主要動作，不再加大轉身或手部整理。'),
 ('銜接與長度', 'A的落腳收束接B的放鬆站姿，疊化0.75秒。兩段各7秒時，成片約13.25秒；A約0–7秒，B約6.25–13.25秒。各自保有約6.25秒不被疊化覆蓋的畫面，實際採用時依可用動作調整。'),
 ('為什麼只有兩鏡', '每段是一個完整日常片刻。暫不加入空場景、無用途配件或快速插鏡；先檢查走動、落腳與離開能否讓服裝有生活感。音樂在畫面成立後再選，不靠節拍補掉無事發生的空等。') ]},
 {'title':'E01 日常片段｜起始圖與接點', 'subtitle':'先安排行走空間，避免生成後再猜。', 'fields':[
 ('攝影與光線', '固定、平視、自然透視；避免廣角拉長腿。全身約占畫面高度72–78%，上下留頭頂與鞋的安全空間，前進方向留路徑。柔和日光固定由畫面左側進入；兩套背景結構與曝光一致。這些是構圖目標，生成後仍要量看。'),
 ('四個可用畫面', 'L01全身起始圖：正面、重心可起步，包不遮領口。L01搭配重點：翻領／棉T圓領／已翻折袖口可讀。L02全身起始圖：與A终點相近大小及中央落點。L02搭配重點：深外套、淺灰圓領與淺褲腰線。重點畫面是資產要求，這版不強制剪入影片。'),
 ('已有素材怎麼用', 'W41原全身圖與10/12M03試片提供衣服、身分和光線參考；不能直接當成這份新分鏡已合格的起始圖。先審行走空間、垂直構圖及臉部資訊，能用才重用；不足列為補圖需求。新圖仍先等使用者視覺核准。'),
 ('接點控制', '選A落腳後與B起步前的短收束，人物頭部／腰線落點相近。剪輯可選時間、做0.75秒疊化；人物尺度優先由起始圖安排，不用大幅裁切來救鞋子。允許短暫雙影，不把兩段硬湊成無差別換裝。'),
 ('失敗時怎麼簡化', '若走路滑腳或場景漂移，先降為一步＋自然站姿，不增加運鏡。若B斜走出框，改成留在原位的重心移動。若兩段全是長時間等待，縮短無資訊停留，保留原速；仍無生活感便退回分鏡，不靠轉場裝飾補救。'),
 ('這支專屬驗收', '無文字播放時像兩個出門片刻嗎？領口、棉T、褲型與完整鞋在各段都可看清嗎？走動有實際位移與自然落腳嗎？場景服務行走且保持穩定嗎？接點舒適仍須看整片正常速度。') ]},
 {'title':'E02 動態輪廓｜觀看路線', 'subtitle':'短外套的比例，在身體移動中看清。', 'fields':[
 ('衣服與場景', 'M05；2026-W41-001-L01奶油白短版立領外套／白圓領短袖／可可棕高腰直筒褲；L02炭灰短版立領外套／奶油白圓領短袖／淺灰高腰直筒褲。兩套外套敞開，皆窄黑皮帶、黑低跟樂福鞋、黑小方肩包。背景用明亮有頂入口與平直米灰牆。'),
 ('第一段：正面比例｜預算6秒', 'L01正面全身、雙腳自然分立。重心從一側移到另一側，空手放鬆，最後回到舒適站姿。主動作僅重心移動。觀眾看短衣襬相對腰胯的位置、敞開外套內的短袖，以及直筒褲從腰到鞋的線條。'),
 ('第二段：側面輪廓｜預算6秒', 'L02正面全身開始，身體緩轉約25–35度，臉仍可辨識；稍留一刻再回正。主動作僅淺轉身，攝影機固定。觀眾新增看到外套側面衣長、下襬離身程度與褲管輪廓，不要求背面或360度轉圈。'),
 ('銜接與長度', 'A結尾與B開頭均正面全身，中央落點／人物高度相近，0.75秒疊化。6＋6－0.75＝約11.25秒；A約0–6秒，B約5.25–11.25秒。每套各約5.25秒不被疊化覆蓋，轉側停留必须放在B的清楚時段。'),
 ('與E01真正不同的地方', 'E01看行走片刻與生活氣氛；E02看輪廓變化。場景更安靜、人物留在原位，不用近遠走動搶走對腰線與褲型的注意。兩套是同一服裝主題的延伸，沒有更好／更差的結論。') ]},
 {'title':'E02 動態輪廓｜起始圖與接點', 'subtitle':'每一個動作都要增加可見的服裝資訊。', 'fields':[
 ('攝影與站位', '固定、平視、自然透視，人物全身約占高度76–82%，鞋周圍留空間。兩套同站位、同光向；肩包置於較不遮腰線的一側。轉身方向先依包的位置安排，讓外套側面能被看見。不得為轉身補造未確認的背面設計。'),
 ('四個可用畫面', 'L01全身：正面自然站姿，雙腳可做重心移動。L01搭配重點：立領、短衣襬、皮帶與褲腰同時可讀。L02全身：匹配尺度並留側轉空間，正面臉充分。L02搭配重點：炭灰短衣長、奶油白內搭與淺灰褲腰。既有圖需逐張檢查後才決定重用。'),
 ('動作階段預算', 'A開頭自然起動，中段重心移動，末段回到放鬆站姿。B起動轉側，中段讓側面清楚停留約1–2秒，再回正。秒數是剪輯與候選選段目標，不要求生成模型逐秒精準演出。先請模型只做一個主要動作，再從完整素材選段。'),
 ('接點控制', '接在A回穩與B尚未轉側的區間。兩段保持相近頭部、腰線與鞋位置；避免把最有資訊的側面輪廓放進疊化。0.75秒雙影可接受，背景本身變形、衣長跳變或包滑動仍需退件。'),
 ('失敗時怎麼簡化', '淺轉身若變成大側身或換臉，縮小角度；腳跟打滑就改為上身小幅轉側、腳掌穩定。若全片只是擺姿勢、衣服資訊沒有增加，先改鏡位或觀看目的，不增加更多姿勢。'),
 ('這支專屬驗收', '不看標題也能注意到短外套與長褲的比例嗎？轉側後比正面多看到了什麼？腰線沒有被包擋住嗎？每套保有充分清楚時段嗎？完整播放是否有模特兒在等下一個指令的停頓感？') ]},
 {'title':'參數可控，成果仍要整支驗收', 'subtitle':'把風格變成有理由的安排，保留生成的不確定性。', 'fields':[
 ('可由工作流直接決定', '造型編號、觀看目的、鏡頭順序、取用片段、原速、0.75秒疊化、無烙字、成片輸出規格。這些可保存成製作單並重複執行。'),
 ('只能提出目標，再檢查輸出', '人物動作幅度、落腳、臉孔／衣服／背景一致性、光線、尺度與精準時機。起始圖能減少不確定性；提示詞不能等同於已達成的畫面。每個主鏡候選最多重試一次，之後降低動作難度。'),
 ('共同動態檢查', '檢查開頭、四分之一、中段、四分之三、結尾及轉頭瞬間，再完整播放。確認身分、剪裁顏色、手鞋包與背景；記錄連續可用秒數、生成次數和主動／等待時間。單幀合格不等於整片合格。'),
 ('整支優先看三件事', '第一：每一段是否讓觀眾多看懂一件事。第二：眼睛能否沿著人物與服裝自然移動，不必反覆找焦點。第三：有沒有舒服且足夠的清楚時間，而非用長慢動作或過多插鏡湊長度。'),
 ('之後試作怎麼安排', '建議先做E02，兩段固定全身，較容易隔離動作與輪廓問題；E01再加入小幅位移。先通過一人兩套的完整觀看，再考慮擴到五位。不將不同模特兒、服裝與發布日期的單支曝光差異直接歸因剪輯方式。'),
 ('目前停在這裡', '兩份分鏡已完成規劃，沒有啟動媒體製作。後續若恢復試作，先檢查可重用素材與缺圖，再依新圖視覺核准流程進行。既有Drive发布包維持原交付紀錄。') ]}
]

def p(text, style='body'):
    return Paragraph(escape(text), STYLES[style])

def footer(canvas, doc):
    w, h = A4
    canvas.setStrokeColor(colors.HexColor('#D8DFDC'))
    canvas.line(42, 37, w-42, 37)
    canvas.setFont('MiraChinese', 9)
    canvas.setFillColor(GRAY)
    canvas.drawString(42, 22, 'Mira / 2026-10-13 / 分鏡規劃・尚未試做')
    canvas.drawRightString(w-42, 22, str(doc.page))

story = []
for idx, page in enumerate(PAGES):
    if idx: story.append(PageBreak())
    story += [p(page['title'], 'title'), p(page['subtitle'], 'h'), Spacer(1, 5)]
    for label, content in page['fields']:
        story += [p(label, 'label'), p(content), Spacer(1, 4)]
OUT.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=42, rightMargin=42, topMargin=42, bottomMargin=48, title='Mira 日常片段與動態輪廓分鏡', author='Mira')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
data = {'date':'2026-10-13', 'status':'planning_only_media_execution_paused', 'wardrobe_week':'2026-W41', 'pages':PAGES,
        'formats':[{'id':'E01','model':'M03','look_ids':['2026-W41-004-L01','2026-W41-004-L02'],'shot_budgets_seconds':[7,7],'dissolve_seconds':0.75,'total_budget_seconds':13.25},
                   {'id':'E02','model':'M05','look_ids':['2026-W41-001-L01','2026-W41-001-L02'],'shot_budgets_seconds':[6,6],'dissolve_seconds':0.75,'total_budget_seconds':11.25}],
        'new_media_created':False, 'new_external_writes':False, 'pdf':OUT.relative_to(ROOT).as_posix()}
(HERE/'storyboards_2026-10-13.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
md = ['# Mira 日常片段與動態輪廓分鏡', '', '2026-10-13｜只做規劃，媒體製作維持暫停。', '']
for page in PAGES:
    md += ['## '+page['title'], '', page['subtitle'], '']
    for label, content in page['fields']: md += ['### '+label, '', content, '']
(HERE/'STORYBOARDS_2026-10-13.md').write_text('\n'.join(md), encoding='utf-8')
print('Created storyboard PDF and structured planning records.')
