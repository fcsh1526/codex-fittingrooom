import json
from pathlib import Path
from PIL import Image, ImageDraw
HERE=Path(__file__).resolve().parent
receipt=json.loads((HERE/'extraction_receipt.json').read_text(encoding='utf-8'))
frames=receipt['checkpoint_frames']
board=Image.new('RGB',(5*140,5*344),'white'); d=ImageDraw.Draw(board)
for i,f in enumerate(frames):
    with Image.open(HERE/f'frame_{f:03}.png') as im:
        crop=im.crop((145,0,615,1280)); crop.save(HERE/f'wide_crop_{f:03}.png')
        crop.thumbnail((140,320),Image.Resampling.LANCZOS)
        x=(i%5)*140; y=(i//5)*344
        d.text((x+4,y+4),f'{f/24:.3f}s / f{f}',fill='black')
        board.paste(crop,(x+(140-crop.width)//2,y+24))
board.save(HERE/'wider_crop_25_checkpoints.jpg',quality=95)
print('Wider fixed-window checkpoint board created; no video mutation.')
