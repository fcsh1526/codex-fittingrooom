"""Plan a motivated single-repositioning performance using the exact approved stills."""
import json,hashlib,sys,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).resolve().parent;ROOT=P.parents[5];W=ROOT/'10_automation/runs/2026-W45'
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
old=W/'reels/M03/expressive_parallel_2026-11-05';base=read(old/'trial_02/submission.json')
identity=['02_brand/reference_models/M03_start_v3_face.png','02_brand/reference_models/M03_start_v3_full.png'];assert all((ROOT/x).is_file() for x in identity)
still1=ROOT/base['source_still'];a2=read(W/'approvals/M03_L02_still_approval_2026-11-04.json');still2=ROOT/a2['asset_path']
assert h(still1)==base['source_still_sha256'] and h(still2)==a2['target_sha256']
prompt='''Continue naturally from the supplied first image. This is a casual outfit photo before heading out: a friend just behind the camera is ready to take her picture. She listens, responds to her friend with a brief warm smile, and makes one clear, ordinary repositioning to show the clothes: turn her whole body about45degrees to her right with one grounded foot adjustment, let the jacket reveal its side line, then return to a comfortable front-facing stance. Her face stays naturally responsive to the person filming. Her arms rest loosely beside her body and move only with the turn; both shoulders and hips settle together. Give the side view and final frontal outfit a readable moment. No repeated left-right swaying, dancing, high arm gestures or exaggerated fixed grin.

One continuous six-second real-time full-person shot. Keep the original locked, level chest-height50mm camera and subject distance, exact M03 face, normal body proportions and long wavy brown hair. Preserve the open deep-navy blazer, white crewneck tee, charcoal straight trousers, black loafers, small black bag on her left shoulder and silver necklace. Preserve the original shaded office windows, bench, paving and daylight. Keep the complete hair, hands, bag and shoes visible with relaxed arms near the torso. No camera move, slow motion, cut, outfit change or text.'''
for look,still,first,wardrobe in [('L01',still1,'2e8df556-7034-4788-92d8-3a769fcdfed3','deep-navy blazer, white tee, charcoal trousers, black loafers'),('L02',still2,'1499ae56-08c0-4503-b88f-898a373738e0','deep-navy blazer, cream knit top, cream A-line skirt and white-grey sneakers')]:
    folder=P/(look+'_trial_01');folder.mkdir(exist_ok=True)
    text=prompt if look=='L01' else prompt.replace('white crewneck tee, charcoal straight trousers, black loafers','cream-white short-sleeve fine-knit top, cream-white calf-length A-line skirt, white-grey low-top sneakers')
    (folder/'video_prompt.txt').write_text(text+'\n',encoding='utf-8')
    plan={'date':'2026-11-05','status':'prepared_not_submitted','look':look,'source_still':rel(still),'source_still_sha256':h(still),'first_frame_asset_id':first,'identity_asset_ids':base['identity_asset_ids'],'duration_requested':6,'resolution_requested':'720p','aspect_requested':'9:16','last_frame_asset_id':None,'keyframes':None,'prompt_sha256':h(folder/'video_prompt.txt'),'max_new_jobs':1,'new_jobs_submitted':0,'new_still_calls':0,'user_authorization':'Latest ok continues natural motivated performance correction within M03, A layout already selected; not a new still or film/publication approval.','remaining_quota':'unknown','seed':'unknown','model_version':'unknown'}
    put(folder/'shot_plan.json',plan)
    request=f'''W45 M03自然表演改案，這次只生成{look}一支獨立6秒720p9:16原片。使用者最新明確說「我不喜歡搖擺跳舞」，又對改成自然情境、轉身與反應回覆ok。原414c5d81／64c9236b多姿態與舊四秒合片不是本輪目標。保留原片；不改刪任何媒體，不補新照片、不重試、不追加另一套、不加購／升級／換服務。
精確First: {first}，已核准M03 {look}原圖，{wardrobe}，原辦公遮簷場景，完整頭鞋。identity asset_ids: ["26e03f42-2907-488c-b75c-239a2a19b9c8","15c720b2-46b6-45e0-a150-60290e3290e6"]，只鎖身份與普通比例。
先實際查看三個UUID與可用控制。duration:"6",resolution_name:"720p",aspect_ratio:"9:16"；不設last/keyframes。若來源不符／不可用、額度不足或需要額外費用，停止回報，不代換、不送別的生成。
以下英文逐字作prompt，標記不傳入：
PROMPT_BEGIN
{text}
PROMPT_END
這是回應拍攝者後一次完整轉向與回正，不是節奏舞蹈或連續擺姿；手臂近身保留窄欄空間，不用大幅外展。保留實際自然變體，不強制逐秒機械編舞。音訊有實際開關才關，沒有則如實記錄。完成列實際First/identity IDs、設定是否接受、新影片UUID、實際時長／尺寸／音軌。參數接受、可見觀察與物理／真人感分開記錄，不自行宣稱通過。只此一支，後續由我檢查。
'''
    (folder/'grok_request.txt').write_text(request,encoding='utf-8')
put(P/'production_plan.json',{'date':'2026-11-05','status':'single_side_test_prepared_not_generated','viewer_purpose':'Same navy blazer: compare charcoal work trousers/loafers versus cream skirt/sneakers.','layout':'A parallel','model':'M03','target_seconds':6,'fps_target':24,'per_panel':'one continuous source, no internal edit join planned','story':'Friend behind camera prepares outfit photo; brief response and one45degree turn with return to standing.','panel_schedule':[{'seconds':[0,1.5],'action':'listen/respond with brief smile','clothing':'front silhouette'},{'seconds':[1.5,4],'action':'one whole-body turn, arms relaxed','clothing':'blazer side line and trouser/skirt outline'},{'seconds':[4,6],'action':'front-facing comfortable stance','clothing':'full silhouette and shoe contrast'}],'camera':'fixed, independent source scenes; shared-world routes not required','crop_proposal_source720':[135,0,450,1280],'panel_width':356,'gutter':8,'preflight':'Still mockup inspected; dynamic actual envelope and scale must be rechecked, no promise of motion success.','reuse_assessment':'Existing approved stills fit. Old dance-pose videos do not cover the new motivated continuous scene; no recut or retiming to fabricate it.','new_stills_required':0,'new_video_sources_needed':2,'generation_order':'one L01 test, inspect exact result; L02 only if direction visibly useful and in-scope. No automatic repeat L01.','user_film_acceptance':None,'publication_approval':None})
# Diagnostic layouts use approved image bytes; this is not an AI still edit or new still candidate.
panel=[]
for src in [still1,still2]:
    im=Image.open(src).convert('RGB').resize((720,1280));im=im.crop((135,0,585,1280));im=im.resize((356,1012));tile=Image.new('RGB',(356,1280),'#f1eee6');tile.paste(im,(0,134));panel.append(tile)
canvas=Image.new('RGB',(720,1280),'#f1eee6');canvas.paste(panel[0],(0,0));canvas.paste(panel[1],(364,0));canvas.save(P/'approved_stills_layout.png')
font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',22);small=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',17)
board=Image.new('RGB',(1200,680),'#f1eee6');d=ImageDraw.Draw(board);d.text((22,15),'M03｜自然拍攝情境・固定鏡頭／A並排・示意線稿',font=font,fill='#233b46')
for i,(title,angle,description) in enumerate([('0–1.5秒｜回應拍攝者',0,'短暫微笑，身體自然站穩'),('1.5–4秒｜單次轉向',45,'完整轉向，讀西外側線／褲裙'),('4–6秒｜回正收尾',0,'舒服站姿，保留完整服裝')]):
    x=i*400;d.rounded_rectangle((x+15,65,x+385,590),radius=10,outline='#8e938e',width=2);d.text((x+28,78),title,font=font,fill='#233b46')
    for j in range(2):
        cx=x+110+j*165;cy=190;lean=18 if angle else 0
        d.ellipse((cx-19,cy-40,cx+19,cy-2),outline='#233b46',width=3);d.line([(cx,cy),(cx+lean,cy+135)],fill='#233b46',width=5)
        d.line([(cx+lean,cy+135),(cx-20,cy+270)],fill='#233b46',width=5);d.line([(cx+lean,cy+135),(cx+30,cy+270)],fill='#233b46',width=5)
        d.line([(cx,cy+30),(cx-30,cy+130)],fill='#233b46',width=4);d.line([(cx,cy+30),(cx+35,cy+130)],fill='#233b46',width=4)
        if j:d.polygon([(cx-20,cy+120),(cx+30,cy+120),(cx+48,cy+230),(cx-42,cy+230)],outline='#233b46',width=3)
        if angle:d.arc((cx-48,cy+55,cx+55,cy+100),0,170,fill='#aa6b47',width=3)
    d.text((x+26,525),description,font=small,fill='#233b46')
d.text((22,620),'兩側各一段連續原片；不刻意鏡像同步。無反覆搖擺／舞蹈式串姿。',font=small,fill='#233b46');board.save(P/'storyboard.png')
print(json.dumps({'prepared':True,'new_still_calls':0,'old_dance_sources_reused':False,'first_job':rel(P/'L01_trial_01/grok_request.txt')}))
