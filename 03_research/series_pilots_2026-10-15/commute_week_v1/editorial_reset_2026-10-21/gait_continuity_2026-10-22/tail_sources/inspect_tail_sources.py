from pathlib import Path
import hashlib,json,sys
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'CURRENT_STATUS.md').exists())
RESET=HERE.parent.parent
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
import imageio_ffmpeg
from PIL import Image,ImageDraw
records=[]
specs=[('F04',RESET/'F04_motion_01/F04_source.mp4','e32ee2f282b80dec8b8666d6755c9d2e77e5def6850bc53c89b5333927cd2208',108),('F05',RESET/'F05_half_motion_01/F05_half_source.mp4','c2d9f0442ea0d9b9c50674fb959b96ae53a8264c3947c509aa91f05e4bec9aa9',82)]
for name,src,expected,limit in specs:
    digest=hashlib.sha256(src.read_bytes()).hexdigest()
    assert digest==expected
    rd=imageio_ffmpeg.read_frames(str(src),pix_fmt='rgb24',output_params=['-vsync','0']);meta=next(rd)
    w,h=meta['size'];fps=meta['fps']
    frames=[Image.frombytes('RGB',(w,h),b) for b in rd]
    def sheet(indices,filename,crop=None):
        tw=230;ch=(crop[3]-crop[1]) if crop else h;cw=(crop[2]-crop[0]) if crop else w
        th=round(ch*tw/cw);rh=th+28
        cv=Image.new('RGB',(5*tw,((len(indices)+4)//5)*rh),'#eeeeee');d=ImageDraw.Draw(cv)
        for k,i in enumerate(indices):
            im=frames[i].crop(crop) if crop else frames[i]
            x=k%5*tw;y=k//5*rh
            cv.paste(im.resize((tw,th)),(x,y));d.text((x+4,y+th+5),f'{name} f{i:03d} {i/fps:.3f}s',fill='black')
        p=HERE/filename;assert not p.exists();cv.save(p,quality=97)
        return str(p)
    feet_indices=list(range(0,limit,3));whole_indices=list(range(0,len(frames),6))
    if whole_indices[-1]!=len(frames)-1:whole_indices.append(len(frames)-1)
    feet=sheet(feet_indices,f'{name}_feet_every3.jpg',(0,740,720,1280))
    whole=sheet(whole_indices,f'{name}_whole_every6.jpg')
    records.append({'name':name,'source':str(src),'source_sha256':digest,'metadata':meta,'decoded_frames':len(frames),'feet_qa':{'path':feet,'indices':feet_indices,'crop_xyxy':[0,740,720,1280]},'whole_qa':{'path':whole,'indices':whole_indices},'diagnostic_images_only':True,'source_unchanged':hashlib.sha256(src.read_bytes()).hexdigest()==expected,'video_mutation':False,'retiming':False,'continuous_visual_playback':False})
p=HERE/'extraction_receipt.json';assert not p.exists();p.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(records,ensure_ascii=False))
