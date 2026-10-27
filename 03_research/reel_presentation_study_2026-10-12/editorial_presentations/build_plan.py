from pathlib import Path
import json
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = json.loads((HERE / 'plan.json').read_text(encoding='utf-8'))
OUT = ROOT / 'output/pdf/Mira_Reel_呈現企劃_2026-10-12.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
pdfmetrics.registerFont(TTFont('MiraChinese', 'C:/Windows/Fonts/msjh.ttc', subfontIndex=0))
INK = colors.HexColor('#24363C')
TEAL = colors.HexColor('#276B70')
PAPER = colors.HexColor('#F4F1EA')
GRAY = colors.HexColor('#53656A')
styles = {
    'title': ParagraphStyle('title', fontName='MiraChinese', fontSize=23, leading=32, textColor=INK, spaceAfter=14, wordWrap='CJK'),
    'h': ParagraphStyle('h', fontName='MiraChinese', fontSize=16, leading=24, textColor=TEAL, spaceAfter=10, wordWrap='CJK'),
    'body': ParagraphStyle('body', fontName='MiraChinese', fontSize=12, leading=19, textColor=INK, spaceAfter=7, wordWrap='CJK'),
    'small': ParagraphStyle('small', fontName='MiraChinese', fontSize=10.5, leading=16, textColor=GRAY, spaceAfter=7, wordWrap='CJK'),
    'table': ParagraphStyle('table', fontName='MiraChinese', fontSize=10.5, leading=17, textColor=INK, wordWrap='CJK'),
    'label': ParagraphStyle('label', fontName='MiraChinese', fontSize=10, leading=15, textColor=TEAL, spaceAfter=3, wordWrap='CJK'),
}

def p(text, style='body'):
    return Paragraph(escape(text), styles[style])

def field(label, text):
    return [p(label, 'label'), p(text), Spacer(1, 3)]

def footer(canvas, doc):
    w, h = A4
    canvas.setStrokeColor(colors.HexColor('#D8DFDC'))
    canvas.line(42, 37, w-42, 37)
    canvas.setFont('MiraChinese', 9)
    canvas.setFillColor(GRAY)
    canvas.drawString(42, 22, 'Mira / 2026-10-12 / 呈現企劃・尚未試做')
    canvas.drawRightString(w-42, 22, str(doc.page))

story = [p(DATA['title'], 'title'), p('先選觀看走向，再設計鏡頭與起始圖。', 'h'), p(DATA['direction']), p(DATA['contract'])]
story += [Spacer(1, 12), p('六種企劃，一眼看懂', 'h')]
rows = [[p('方向', 'table'), p('觀眾看什麼', 'table'), p('目前定位', 'table')]]
for f in DATA['formats']:
    rows.append([p(f['id']+' '+f['name'], 'table'), p(f['viewer'], 'table'), p(f['role'], 'table')])
t = Table(rows, colWidths=[140, 240, 130], hAlign='LEFT')
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PAPER),('LINEBELOW',(0,0),(-1,0),1,TEAL),('LINEBELOW',(0,1),(-1,-1),.4,colors.HexColor('#D8DFDC')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),11),('BOTTOMPADDING',(0,0),(-1,-1),11)]))
story += [t, Spacer(1, 18)]
story += field('怎麼讀這份企劃', '這六種是內容編排方向。單畫面、左右並排、主次雙畫面屬版面；短走、轉身屬人物動作；固定鏡頭、推拉屬攝影機語言。可以組合，不把六份企劃稱為六種全新剪輯技術。')
story += field('本階段', '只做企劃。起始圖、Grok生成與剪輯均暫停；既有試片保留為研究資料。過去樣本只提供機制線索，沒有證明本帳號流量或現在IG的最佳做法。')
story.append(PageBreak())

labels = [('theme','整支主題'),('example','當週衣服範例'),('sequence','觀看順序'),('shots','鏡頭與節奏預算'),('scene','場景的用途'),('assets','起始圖與搭配重點畫面需求'),('join','銜接設計'),('test','整片要驗證什麼'),('risk','容易失效的地方')]
for f in DATA['formats']:
    story += [p(f['id']+'  '+f['name'],'title'), p(f['viewer'],'h'), p(f['role']+'｜'+f['basis'],'small'), Spacer(1,4)]
    for key, label in labels:
        story += field(label,f[key])
    story.append(PageBreak())

story += [p('下一步：把企劃變成分鏡','title'), p('先挑兩個不同的觀看目的深化','h')]
story += field('建議先深化E01與E02', 'E01檢查親切的生活氣氛能否成立；E02檢查動作能否增加衣服資訊。兩者可沿用已定案衣服與已測動作，不先把技術複雜度堆高。E03／E05待鏡頭焦點及搭配重點畫面素材更清楚；E04作色彩專題；E06留給真正需要比較的主題。這是企劃建議，尚未選定試做或帳號固定模板。')
story += field('每份完整分鏡必須寫', '一句整支主題；每鏡新增的服裝資訊；造型編號與來源；景別、人物落點、光向；動作起點／終點；至多一個運鏡；相鄰接點；未被疊化覆蓋的閱讀時間；缺圖清單；失敗時的簡化方案。')
story += field('保留的製作條件', '每支一人兩套、每套原生9:16全身與可用搭配重點畫面；搭配重點畫面不必全部入片。新圖先視覺核准。無烙字，必要文字另由IG手動加入。人物原速。鏡頭／服裝切換約0.75秒疊化；並排無切鏡便無需加轉場。Carousel仍按每套A/B/C獨立製作。')
story += field('節奏怎麼控制', '先控制鏡頭數、觀看順序、每段動作的起動／落腳／收束、人物尺度和亮度。預算公式：成片長度約為各段可用時長總和減去交疊時間；中間鏡頭要扣前後兩次交疊。音樂節奏留待畫面成立後再配，不預設每分鐘節拍數或用音樂掩蓋停頓。')
story += field('驗收整支，而非只驗收參數', '無字看得懂主題嗎？兩套完整服裝都可讀嗎？每鏡新增了什麼？眼睛是否反覆重新找人物？動作與觀看節奏是否自然？單鏡臉／衣／背景穩定，接點及整片仍需正常速度播放。用參數描述風格，最後仍以組合成果判斷。')
story += field('疊化的目標', '柔和進入下一個畫面，允許短暫雙影。此次回饋不改掉0.75秒全域規則；不承諾兩個獨立AI來源能做到零差異換裝。不同段落的合理變化可以保留，背景飄移則另行退件。')
story += [p('沿用的研究資料','label'), p('10/2穿搭剪輯研究：細節與整體順序；10/5角度／並排研究；10/6珍藏OOTD：人物近遠與日常動作；10/12試片：光線與自然度正向回饋、接點仍待評估。全部是既有觀察，非本輪新增IG查核或逐幀／音訊分析。','small')]

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=48, title=DATA['title'], author='Mira')
doc.build(story, onFirstPage=footer, onLaterPages=footer)

md = ['# '+DATA['title'], '', '狀態：只規劃，暫停起始圖／影片生成與剪輯。', '', DATA['direction'], '', DATA['contract'], '', '這些是企劃方向，不是六種新剪輯技術。原三類版面分類保持獨立。', '']
for f in DATA['formats']:
    md += ['## '+f['id']+' '+f['name'], '', f['viewer'], '']
    for key,label in labels:
        md += ['- **'+label+'：** '+f[key]]
    md += ['- **研究狀態：** '+f['basis'], '']
md += ['## 深化次序與條件', '', '建議先深化E01與E02，先看生活感與動態輪廓。新圖及新片皆未啟動。時長、角度為候選預算，不是IG最佳規則；每份分鏡須寫服裝資訊、場景用途、動作端點、光向、相鄰銜接、閱讀時間與缺圖。0.75秒柔和疊化、無字、原速保留，整片正常速度驗收仍必要。', '', '## 既有研究來源', '', '- `03_research/ig_styling_edit_study_2026-10-02/README.md`', '- `03_research/ig_styling_edit_study_2026-10-05/orientation_study/README.md`', '- `03_research/ig_saved_ootd_study_2026-10-06/README.md`', '- `03_research/reel_presentation_study_2026-10-12/PRESENTATION_TYPES.md`', '- `03_research/reel_presentation_study_2026-10-12/continuous_distance_pose/two_looks_receipt.json`', '', '本輪未新增網路查核、未提供新IG成效或精確音樂／切點推論。PDF：`output/pdf/Mira_Reel_呈現企劃_2026-10-12.pdf`。']
(HERE/'README.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(str(OUT))
