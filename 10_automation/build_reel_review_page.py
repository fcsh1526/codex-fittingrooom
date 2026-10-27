"""Create a local comparison page from recorded Grok outputs; never assign QA."""
import argparse
import html
import json
import os
from pathlib import Path

def build(pilot):
    pilot=Path(pilot).resolve()
    root=Path(__file__).resolve().parents[1]
    outputs=json.loads((pilot/'generation_outputs.json').read_text(encoding='utf-8'))
    titles={'T01':'非正面・無人物參照','T02':'非正面・加入人物參照','T03':'非正面・鎖首幀重複驗證','T04':'正面・無人物參照','T05':'正面・加入人物參照','T06':'小幅轉頭','T07':'鏡頭橫移','T08':'第二套・獨立生成','T09':'兩套・同次生成','T10':'兩套・同次生成重複'}
    cards=[]
    for row in outputs:
        tid=row['trial_id'];attempt=row.get('attempt_id','01')
        path=root/row['path'] if row.get('path') else None
        note='待完整動態驗收與人物複核'
        if tid=='T02' and attempt=='01':note='操作差異：穿搭圖被改為一般參照，首幀重構；不列入嚴格對照。'
        if tid=='T02' and attempt=='02':note='首幀已恢復原圖；後半段自行轉頭，動作遵循不通過，人物複核待完成。'
        if tid=='T06':note='原始結果頁仍保留；下載尚未取得，不列為已驗收。'
        if tid=='T10' and attempt=='01':note='曾顯示生成進度，結果隨後消失並跳回 T09；原因不明。'
        if tid=='T10' and attempt=='02':note='中段約 3.02 秒出現兩套與場景疊影，不通過直接切鏡要求。'
        media=f'<video controls muted playsinline preload="metadata" src="{html.escape(Path(os.path.relpath(path,pilot)).as_posix())}"></video>' if path and path.is_file() else '<div class="pending">尚未保存本機影片</div>'
        cards.append(f'<article><h2>{tid} · {attempt}　{titles.get(tid,tid)}</h2>{media}<p>{note}</p><a href="{html.escape(row["url"])}" target="_blank" rel="noopener">Grok 原始結果 ↗</a></article>')
    page='''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Mira · M02 動態測試</title><style>
    *{box-sizing:border-box}body{margin:0;background:#f4f1ea;color:#292b29;font-family:system-ui,"Microsoft JhengHei",sans-serif}main{max-width:1200px;margin:auto;padding:36px 24px}h1{font-size:30px}header p{max-width:780px;line-height:1.8}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}article{background:#fff;padding:18px;border-radius:14px}h2{font-size:16px;min-height:44px;line-height:1.5}video{width:100%;height:430px;object-fit:contain;background:#eeece7;border-radius:8px}article p{font-size:14px;line-height:1.6;min-height:48px}a{color:#466850}.pending{height:430px;display:grid;place-items:center;background:#eeece7}.badge{font-size:13px;background:#e5ddc9;padding:6px 12px;border-radius:20px;display:inline-block}footer{margin-top:24px;line-height:1.8;color:#64665f}</style><main><header><span class="badge">技術測試 · 非發布成片</span><h1>Mira M02｜起始圖與人物參照</h1><p>先比較臉孔、領口與肩帶、鞋包和手物接觸，再看動作。每支完整播放一次；抽幀只能輔助檢查。此頁不會自動核准影片，也不代表 W37 已恢復量產。</p></header><section class="grid">'''+''.join(cards)+'''</section><footer>第一輪設定為約 6 秒／720p；實際尺寸與片長以各片 qa/metadata.json 為準。音訊預設靜音播放，並非原始檔無音軌。<br>兩套正式試片仍待重點圖視覺核准、影片完整動態驗收與選段完成。</footer></main></html>'''
    path=pilot/'review.html';path.write_text(page,encoding='utf-8');return path

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('pilot',type=Path)
    print(build(parser.parse_args().pilot))
