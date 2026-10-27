"""Render a schematic paper edit, not photographic material or a motion preview."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
FONT = Path('C:/Windows/Fonts/msjh.ttc')
IMG = Image.new('RGB', (1800, 1190), '#f7f5ef')
D = ImageDraw.Draw(IMG)
INK = '#263942'

def font(n):
    return ImageFont.truetype(str(FONT), n)

def text(x, y, s, n=26, fill=INK):
    D.text((x, y), s, font=font(n), fill=fill)

def line(points, fill=INK, width=3):
    D.line(points, fill=fill, width=width)

def arrow(x, y, xx, yy, fill='#597b72', width=4):
    line([(x, y), (xx, yy)], fill, width)
    line([(xx-12, yy-7), (xx, yy), (xx-12, yy+7)], fill, width)

text(55, 32, '同一路線，五天穿搭｜整片紙上剪輯', 43)
text(55, 95, '18秒節拍草案；尚未拍攝或重剪。先讓五套衣服都有清楚的展示，再處理銜接。', 27)

text(55, 158, '現版的資訊分配', 27)
old = [2.5, .75, 4.541667, .75, 9.791666, .75, 4.541667, .75, 5.291666]
oldlabels = ['長西外', '', '棕丹寧', '', '短外套＋同套推近', '', '格紋近景', '', '黑裙／藍包']
colors = ['#c9bba3', '#c5c9c8', '#a7876c', '#c5c9c8', '#b8c1aa', '#c5c9c8', '#9aadb7', '#c5c9c8', '#99a9cc']
x = 55
for dur, lab, color in zip(old, oldlabels, colors):
    w = dur / sum(old) * 1690
    D.rectangle((round(x), 204, round(x+w), 256), fill=color)
    if lab:
        text(x+8, 215, lab, 22)
    x += w
text(55, 272, '第一套僅2.5秒；第三套約9.8秒；第四套看不到完整褲型與鞋。', 25)

text(55, 330, '新草案：五次明確的穿搭展示', 29)
text(55, 375, '每套保留可讀整體比例的片段；不另插一整段同套推近。四個接點各約0.75秒柔接。', 25)

titles = ['長西外／深褲', '白襯衫／棕丹寧', '短外套／灰褲', '格紋襯衫／灰褲', '白襯衫／黑裙／藍包']
times = ['0–2.50秒', '3.25–6.25秒', '7–10秒', '10.75–13.75秒', '14.50–18秒']
places = ['街角 → 柱廊', '柱廊 → 廣場', '廣場 → 公司側', '公司側鋪面', '入口前收束']
camera_labels = ['前側跟拍 → 側面', '側跟 → 略移前側', '前側 → 側面', '側面較廣，讀整套', '全套可讀 → 略拉開']
purposes = [
    ['先看長外套與深褲的', '整套層次，再往前走。'],
    ['看白上衣、棕丹寧的', '上下身色塊與比例。'],
    ['一次看清短衣長與高腰；', '不再多走一整段才推近。'],
    ['格紋之外也要看完整', '灰褲、鞋與全套比例。'],
    ['一開始便能讀裙裝；', '藍包與裙襬留到結尾。'],
]
notes = ['優先保留已接受開場', '剪短後仍須核對位置', '需重排銜接，不能只刪秒數', '素材缺口：現有只有近景', '素材缺口：全套需更早可讀']

for i in range(5):
    x = 55 + 342*i
    D.rounded_rectangle((x, 427, x+322, 1032), radius=12, fill='#fffefa', outline='#b9c2bd', width=2)
    text(x+14, 442, times[i], 26)
    text(x+14, 487, titles[i], 23)
    sx, sy = x+16, 534
    D.rectangle((sx, sy, sx+290, sy+307), fill='#eeefea', outline='#b9c2bd', width=2)
    # Same ground direction and grey-green office language across schematic panels.
    line([(sx, sy+265), (sx+290, sy+265)], '#acb5ad', 2)
    for px in range(sx+12, sx+290, 70):
        line([(px, sy+16), (px, sy+241)], '#c5cec8', 2)
    line([(sx, sy+119), (sx+290, sy+119)], '#c5cec8', 2)
    if i < 2:
        D.rectangle((sx+8, sy, sx+31, sy+265), fill='#d8d0c1')
    if i == 4:
        D.rectangle((sx+210, sy+61, sx+283, sy+265), outline='#a2b1ab', width=5)
        line([(sx+197, sy+56), (sx+289, sy+56)], '#7d8f87', 7)
    text(sx+8, sy+5, camera_labels[i], 18, '#48665d')
    cx = sx+141
    # Deliberately schematic full-person figure, no identity or photographic approval implied.
    D.ellipse((cx-14, sy+33, cx+14, sy+64), fill='#e5c9b7', outline=INK, width=2)
    line([(cx-13, sy+38), (cx-19, sy+83)], '#685247', 9)
    top = '#fcfbf4'
    if i == 3:
        top = '#dedfda'
    D.polygon([(cx-22,sy+70),(cx+20,sy+70),(cx+29,sy+146),(cx-28,sy+146)], fill=top, outline=INK)
    if i in (0, 2):
        end = 169 if i == 0 else 130
        D.polygon([(cx-24,sy+69),(cx-5,sy+77),(cx-9,sy+end),(cx-32,sy+end)], fill='#d6cdb9', outline=INK)
        D.polygon([(cx+21,sy+69),(cx+5,sy+77),(cx+9,sy+end),(cx+31,sy+end)], fill='#d6cdb9', outline=INK)
    if i == 3:
        for dy in (85,103,121,139):
            line([(cx-22,sy+dy),(cx+25,sy+dy)], '#526477', 2)
        for dx in (-15,0,15):
            line([(cx+dx,sy+75),(cx+dx,sy+144)], '#526477', 2)
    if i == 4:
        D.polygon([(cx-24,sy+147),(cx+25,sy+147),(cx+42,sy+229),(cx-38,sy+229)], fill='#34383a', outline=INK)
        line([(cx-13,sy+230),(cx-29,sy+261),(cx-16,sy+262)], INK, 5)
        line([(cx+21,sy+230),(cx+45,sy+257),(cx+59,sy+259)], INK, 5)
    else:
        pc = ['#3b4b5b', '#967256', '#696e73', '#696e73'][i]
        D.polygon([(cx-23,sy+147),(cx+25,sy+147),(cx+26,sy+176),(cx+5,sy+218),(cx-10,sy+212),(cx+1,sy+172),(cx-7,sy+177),(cx-31,sy+254),(cx-48,sy+252),(cx-32,sy+201)], fill=pc, outline=INK)
        line([(cx-47,sy+254),(cx-25,sy+260)], INK, 6)
        line([(cx+5,sy+218),(cx+38,sy+253),(cx+57,sy+255)], INK, 6)
    line([(cx-25,sy+80),(cx-34,sy+124),(cx-8,sy+164)], INK, 4)
    line([(cx+23,sy+80),(cx+35,sy+129),(cx+56,sy+157)], INK, 4)
    bagcolor = '#425f9c' if i == 4 else ('#795c44' if i == 0 else '#3e4445')
    line([(cx-16,sy+76),(cx-37,sy+148)], bagcolor, 5)
    D.rounded_rectangle((cx-54,sy+137,cx-19,sy+174), radius=6, fill=bagcolor, outline=INK)
    arrow(sx+199, sy+280, sx+272, sy+280)
    text(x+14, 855, places[i], 23)
    text(x+14, 895, purposes[i][0], 21)
    text(x+14, 929, purposes[i][1], 21)
    text(x+14, 986, notes[i], 18, '#9a4c32' if i >= 2 else '#48665d')

text(55, 1060, '線稿只交代資訊與鏡位，不代表已拍成、步態正確或場景精確重建。', 25)
text(55, 1104, '下一步先核對接點與缺口，再決定最少的新素材；原影片、已核准局部及Drive檔案保留。', 25)
IMG.save(OUT/'paper_edit_board.png')
print(OUT/'paper_edit_board.png')
