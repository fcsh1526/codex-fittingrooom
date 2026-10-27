from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
FONT = Path(r"C:\Windows\Fonts\msjhbd.ttc")
OUT = ROOT / "M02_opening_caption.png"

canvas = Image.new("RGBA", (720, 1280), (0, 0, 0, 0))
draw = ImageDraw.Draw(canvas)
small = ImageFont.truetype(str(FONT), 29)
large = ImageFont.truetype(str(FONT), 30)

# Keep the typography in the window-side negative space of the first look.
draw.text((38, 126), "冷氣房多一層", font=small, fill=(28, 40, 56, 255))
draw.text((38, 172), "洋裝外加薄襯衫", font=large, fill=(28, 40, 56, 255))
canvas.save(OUT)
print(OUT)
