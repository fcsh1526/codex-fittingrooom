"""Render the two 12-second L01 director's previews from independent timelines."""
from pathlib import Path
import math
import subprocess
import tempfile
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageOps


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ASSETS = ROOT / "10_automation/runs/2026-W47/reels/M05/L01_berry_fitting"
FFMPEG = ROOT / "openmontage/.local/bin/ffmpeg.exe"
SIZE = (540, 960)
FPS = 24
DURATION = 12


def ease(time, start, end):
    u = max(0, min(1, (time - start) / (end - start)))
    return u * u * (3 - 2 * u)


def camera(im, x, y, width):
    # Use the same 300-unit reference width for blocking and both camera paths.
    k = im.width / 300
    height = width * 16 / 9
    return im.transform(SIZE, Image.Transform.EXTENT,
                        (k*(x-width/2), k*(y-height/2),
                         k*(x+width/2), k*(y+height/2)), Image.Resampling.BICUBIC)


def gallery(t, berry, knit):
    im = Image.new("RGB", (600, 1068), "#e8e0cf")
    d = ImageDraw.Draw(im)

    def shape(method, coords, fill, **kw):
        getattr(d, method)([round(v*2) for v in coords], fill=fill, **kw)

    def oval(coords, fill):
        shape("ellipse", coords, fill)

    def poly(coords, fill):
        shape("polygon", coords, fill)

    def rect(coords, fill):
        shape("rectangle", coords, fill)

    def line(coords, fill, width):
        shape("line", coords, fill, width=round(2*width))

    rect((0,425,300,534), "#c7baaa")
    rect((0,423,300,425), "#a89a8c")
    rect((0,82,92,229), "#74634e")
    rect((0,85,89,226), "#f3ebda")
    rect((0,94,80,216), "#d5c6b1")
    oval((-23,111,61,197), "#945b4b")
    poly((0,182,80,135,80,216,0,216), "#696f63")
    rect((68,238,85,241), "#b1a699")
    # A friend's shadow appears at the right before Mira reacts.
    other = 328 - 47*ease(t,0.55,2.2) - 12*ease(t,8.3,9.6)
    oval((other-14,204,other+12,240), "#ccc2b0")
    poly((other-7,236,other+8,236,other+36,288,other+45,423,
          other-32,423,other-18,265), "#ccc2b0")
    move = ease(t,2.6,4.85)
    x = 175-49*move
    left = 162-49*ease(t,2.55,3.65)
    right = 187-49*ease(t,3.55,4.85)
    swing = 11*(ease(t,2.55,4.6)-ease(t,5.05,6.4))
    swing -= 3*(ease(t,6.1,6.7)-ease(t,6.8,7.6))
    look = -3+8*ease(t,1.25,2.05)-8*ease(t,9.1,10.05)
    skin = "#d8ac91"
    oval((left-19,453,right+22,462), "#b2a596")
    for foot,hip in ((left,x-10),(right,x+10)):
        line((hip,337,foot,446),skin,7)
        oval((foot-7,443,foot+10,455),"#36312e")
    poly((x-19,245,x+19,245,x+26,351,x-26,351),berry)
    layer = Image.new("RGBA",im.size)
    ld = ImageDraw.Draw(layer)
    hem = [(x-20,245),(x+20,245),(x+32+swing,389),
           (x+12+swing,394),(x-12+swing,392),(x-34+swing,388)]
    ld.polygon([(round(a*2),round(b*2)) for a,b in hem], fill=(*berry,146))
    for offset in (-23,-11,9,22):
        ld.line((int((x+offset*.58)*2),500,int((x+offset+swing)*2),776),
                fill=(*berry,55),width=2)
    im.paste(layer,mask=layer.getchannel("A"))
    poly((x-9,166,x+8,166,x+9,185,x-9,185),skin)
    poly((x-22,182,x-9,178,x+9,178,x+22,183,x+18,244,x-18,244),knit)
    rect((x-19,241,x+19,248),berry)
    for sign in (-1,1):
        line((x+sign*19,188,x+sign*23,223,x+sign*26,256),knit,8)
        oval((x+sign*26-3,254,x+sign*26+3,264),skin)
    line((x-27,262,x-30,280,x-23,280,x-26,262),"#433a36",1.4)
    poly((x-36,277,x-19,277,x-17,298,x-38,298),"#403934")
    oval((x-15,132,x+14,175),"#342e2d")
    oval((x-11+look*.45,138,x+11+look*.45,171),skin)
    poly((x-13,154,x-12,137,x-3,132,x+9,136,x+11,142,x+2,140,x-5,145),"#342e2d")
    oval((x+look*1.6-1,151,x+look*1.6+1,153),"#40352e")
    line((x+look,162,x+look+3,161),"#9f6357",1)
    if t < 2.5:
        return camera(im,186,187,174)
    if 5 <= t < 8:
        return camera(im,132,371,124)
    return camera(im,150,267,300)


def window(t, photo):
    # Image coordinates measured on the approved 300 px wide inspection copy.
    up = ease(t,2,5.3)
    out = ease(t,6.4,10)
    width = 33+17*up+248*out
    return camera(photo,177-27*out,334-37*up-30*out,width)


def sound(route, path):
    rate = 44100
    times = np.arange(DURATION*rate)/rate
    mix = np.zeros_like(times)
    notes = ([(.7,112), (1.15,155), (3.4,138), (4.8,116),
              (8.7,158), (9.5,293.66), (9.64,369.99), (9.83,440)]
             if route == "A" else [(0.12,587.33),(2.2,739.99),
                                    (8.25,493.88),(9.7,587.33),(10.05,880)])
    for onset, freq in notes:
        age = np.maximum(0,times-onset)
        decay = 13 if freq<200 else 2.6
        env = (1-np.exp(-age*110))*np.exp(-age*decay)
        mix += .19*env*(np.sin(2*np.pi*freq*age)+.16*np.sin(4*np.pi*freq*age))
    with wave.open(str(path),"wb") as wav:
        wav.setparams((1,2,rate,0,"NONE",""))
        wav.writeframes((mix*32000).astype("<i2").tobytes())


def main():
    full = Image.open(ASSETS/"M05_L01_berry_full_v1.png").convert("RGB")
    proof = Image.open(ASSETS/"M05_L01_berry_window_B1_v1.png").convert("RGB")
    swatches = ImageOps.fit(full,(300,533))
    berry,knit = [swatches.getpixel(p) for p in [(144,301),(146,181)]]
    for route, name in [("A","A_mira_gallery_previs_v1"),("B","B_window_previs_v1")]:
        with tempfile.TemporaryDirectory(dir=ROOT/"tmp") as temp:
            wav = Path(temp)/"score.wav"
            sound(route,wav)
            args = [str(FFMPEG),"-v","error","-y","-f","rawvideo","-pix_fmt","rgb24",
                    "-s","540x960","-r",str(FPS),"-i","pipe:0","-i",str(wav),
                    "-c:v","libx264","-crf","18","-pix_fmt","yuv420p","-c:a","aac",
                    "-b:a","128k","-movflags","+faststart",str(HERE/(name+".mp4"))]
            with subprocess.Popen(args,stdin=subprocess.PIPE) as encoder:
                for frame in range(FPS*DURATION):
                    t = frame/FPS
                    im = gallery(t,berry,knit) if route=="A" else window(t,proof)
                    encoder.stdin.write(im.tobytes())
                encoder.stdin.close()
                if encoder.wait():
                    raise RuntimeError("Could not encode "+route)


if __name__ == "__main__":
    main()
