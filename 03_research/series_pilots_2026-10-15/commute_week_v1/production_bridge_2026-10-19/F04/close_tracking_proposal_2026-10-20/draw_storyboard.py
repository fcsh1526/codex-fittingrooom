from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[6] / '10_automation' / '.video_dependencies'))
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path(__file__).resolve().parent
FONT = 'C:/Windows/Fonts/msjh.ttc'
ink = '#343b3b'
paper = '#faf9f5'
canvas = Image.new('RGB', (1240, 900), paper)
draw = ImageDraw.Draw(canvas)
def font(n): return ImageFont.truetype(FONT, n)
draw.text((52, 24), '第四鏡改案｜先推近，再換裝', font=font(34), fill=ink)
draw.text((52, 78), '構圖線稿・非生成影片・人物繼續向右走', font=font(22), fill='#606b6b')

def panel(close=False, checked=False):
    img = Image.new('RGB', (720, 1280), paper)
    bg = Image.new('RGB', img.size, paper)
    b = ImageDraw.Draw(bg)
    for x in (-80, 175, 430, 685):
        b.rectangle((x, 0, x + 230, 1050), fill='#e5eae7', outline='#aebbb6', width=3)
        b.line((x, 500, x + 230, 500), fill='#bac4be', width=4)
    if not close:
        b.rectangle((0, 780, 190, 1030), fill='#e8e4db', outline='#b9b9b0', width=3)
        for y in (1050, 1130, 1240):
            b.line((0, y, 720, y - 30), fill='#c2c5be', width=3)
    else:
        bg = bg.filter(ImageFilter.GaussianBlur(14))
    img.paste(bg)
    d = ImageDraw.Draw(img)
    scale = 1.75 if close else 1
    def p(pt):
        x, y = pt
        return (360 + scale * (x - 360), 115 + scale * (y - 240)) if close else pt
    def line(points, fill=ink, width=4):
        d.line([p(v) for v in points], fill=fill, width=max(2, round(width*scale)), joint='curve')
    def poly(points, fill=paper):
        q = [p(v) for v in points]
        d.polygon(q, fill=fill)
        d.line(q+[q[0]], fill=ink, width=max(2, round(3*scale)), joint='curve')
    # Sideward walking pose; outlines indicate clothing rather than anatomy simulation.
    poly([(316,640),(375,650),(438,870),(576,1095),(535,1125),(390,924),(330,790)], '#d8dcda')
    poly([(314,638),(368,655),(325,870),(223,1107),(175,1097),(253,835)], '#d8dcda')
    poly([(174,1097),(220,1102),(249,1131),(191,1131),(158,1122)], '#c3cac7')
    poly([(532,1102),(572,1090),(621,1122),(613,1139),(552,1134)], '#c3cac7')
    poly([(309,365),(365,356),(391,394),(403,626),(318,660),(271,610),(275,412)], '#f3f2eb')
    if checked:
        # The grid is clipped to the torso polygon so it remains clearly a shirt.
        mask = Image.new('L', img.size, 0)
        md = ImageDraw.Draw(mask)
        md.polygon([p(v) for v in [(309,365),(365,356),(391,394),(403,626),(318,660),(271,610),(275,412)]], fill=255)
        grid = Image.new('RGB', img.size, paper)
        gd = ImageDraw.Draw(grid)
        for x in range(265, 410, 20):
            gd.line([p((x,350)),p((x,670))], fill='#8b999d', width=2)
        for y in range(355, 665, 20):
            gd.line([p((265,y)),p((410,y))], fill='#8b999d', width=2)
        # Overlay grid lines only, preserving original shirt fill.
        lines = Image.new('RGBA', img.size, (0,0,0,0))
        ld = ImageDraw.Draw(lines)
        for x in range(265,410,20): ld.line([p((x,350)),p((x,670))],fill='#829196',width=2)
        for y in range(355,665,20): ld.line([p((265,y)),p((410,y))],fill='#829196',width=2)
        alpha = lines.getchannel('A')
        from PIL import ImageChops
        lines.putalpha(ImageChops.multiply(alpha, mask))
        img = Image.alpha_composite(img.convert('RGBA'), lines).convert('RGB')
        d = ImageDraw.Draw(img)
        line([(333,367),(348,398),(369,363)])
        line([(351,399),(362,638)], width=2)
    else:
        line([(312,367),(329,420),(345,382),(351,620)], width=3)
        line([(375,378),(367,420),(386,450)], width=3)
        line([(277,600),(317,618)], width=3)
    line([(308,388),(280,525),(337,596),(369,607)], width=17)
    line([(308,388),(280,525),(337,596),(369,607)], fill=paper, width=10)
    line([(386,406),(405,556),(441,647)], width=15)
    line([(386,406),(405,556),(441,647)], fill=paper, width=8)
    line([(295,385),(254,576)], width=6)
    poly([(228,552),(288,551),(317,658),(217,658)], '#9ea8a5')
    # Profile, hair and neck.
    poly([(337,320),(337,366),(360,380),(377,352),(365,320)], paper)
    head = [p((325,245)),p((403,342))]
    d.ellipse((*head[0],*head[1]), fill=paper, outline=ink, width=max(2,round(3*scale)))
    line([(385,275),(400,290),(414,300),(400,307),(401,325),(383,339)], width=3)
    line([(397,288),(389,288)], width=3)
    poly([(388,250),(359,237),(329,249),(314,285),(318,351),(302,408),(328,441),(346,392),(345,335),(356,289)], '#d1d6d1')
    line([(328,267),(327,350),(312,400)], fill='#7a8681', width=2)
    return img.resize((300, 533), Image.Resampling.LANCZOS)

labels = [
    ('① 第三套原全身', '已接受的行走方向', '同套延續，準備推近'),
    ('② 同套推近後', '頭頂至大腿中段', '背景漸成柔焦；先穩住景別'),
    ('③ 第四套近景跟拍', '同大小、同方向換成格紋', '衣服清楚；腳與斑馬線在畫外'),
]
for x, close, checked, text in zip((52,470,888),(False,True,True),(False,False,True),labels):
    draw.text((x,132),text[0],font=font(25),fill=ink)
    canvas.paste(panel(close,checked),(x,178))
    draw.rectangle((x,178,x+300,711),outline='#9fa9a4',width=2)
    draw.text((x,735),text[1],font=font(20),fill=ink)
    draw.text((x,773),text[2],font=font(18),fill='#606b6b')
for x, text in ((365,'連續推近'),(783,'0.75 秒柔接')):
    draw.line((x,430,x+76,430),fill='#71877f',width=3)
    draw.line((x+76,430,x+62,421),fill='#71877f',width=3)
    draw.line((x+76,430,x+62,439),fill='#71877f',width=3)
    # Labels sit beneath each arrow with enough room for the longer transition label.
    box = draw.textbbox((0,0),text,font=font(17))
    draw.text((x+38-(box[2]-box[0])/2,451),text,font=font(17),fill=ink)
draw.text((52,842),'新橋鏡待製作；原前三鏡保留。此稿只確認景別與銜接，不代表動態已通過。',font=font(20),fill='#606b6b')
canvas.save(OUT / 'F04_close_tracking_storyboard_v1.png')
print(OUT / 'F04_close_tracking_storyboard_v1.png')
