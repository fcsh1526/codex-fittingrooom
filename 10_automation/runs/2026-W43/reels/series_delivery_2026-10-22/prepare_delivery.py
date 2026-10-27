from pathlib import Path
import datetime, hashlib, json, shutil
ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
SOURCE=ROOT/'03_research/series_pilots_2026-10-15/commute_week_v1/editorial_reset_2026-10-21/pace_rebuild_2026-10-22/context_review_v2/review.mp4'
EXPECTED='e5e8a90878b00bab29ecf4da32a6fe5472e1376f1b835b999beaa9a812e225c2'
def hash_file(p,algorithm):
    with p.open('rb') as f:return hashlib.file_digest(f,algorithm).hexdigest()
assert hash_file(SOURCE,'sha256')==EXPECTED
assert datetime.date(2026,10,22).isocalendar().week==43
video=HERE/'01_同一路線五套通勤_Reel.mp4'
assert not video.exists()
shutil.copy2(SOURCE,video)
assert hash_file(video,'sha256')==EXPECTED
caption='一週通勤，先用幾個常穿的顏色安排五天穿搭。\n\n米白、深藍和灰色輪流出現，再換長短外套、襯衫或裙裝，保留熟悉的配色，每天也能有變化。'
caption_path=HERE/'01_同一路線五套通勤_文案.txt'
assert not caption_path.exists()
caption_path.write_text(caption+'\n',encoding='utf-8')
manifest={
 'delivery_week':'2026-W43','content_pool_week':'2026-W41','date':'2026-10-22',
 'series':'SERIES_COMMUTE_WEEK','editing_subtype':'同一路線・連續行進換裝',
 'status':'publication_approved_preparing_drive_handoff_not_posted',
 'model_internal':'M03','looks':5,'formal_weekly_contract_changed':False,
 'source':str(SOURCE),'video':str(video),'sha256':EXPECTED,'md5':hash_file(video,'md5'),'bytes':video.stat().st_size,
 'frames':511,'fps':24,'pixels':[720,1280],'duration_seconds':511/24,
 'caption':caption,'caption_path':str(caption_path),'caption_Chinese_characters':sum('\u4e00'<=c<='\u9fff' for c in caption),
 'no_text':True,'silent':True,'native_speed':True,'new_creative_export':False,
 'approval':str(SOURCE.parent/'user_publication_approval_2026-10-22.json'),
 'IG_status':'not_posted','scheduled_at':None,'posted_at':None,'instagram_url':None,
 'drive_folder':{'id':'1eZsL7PjRcf3FtvRq-DwiI3J5nCedWFBB','url':'https://drive.google.com/drive/folders/1eZsL7PjRcf3FtvRq-DwiI3J5nCedWFBB'},
 'video_drive':None,'caption_doc':None,
 'future_refinements':['brisker walking','separate curved character and ground-track camera trajectories','reduce double-image flicker'],
 'notes':'Delivery week is an archive/handoff label, not a claim of newly researchedW43 fashion. Prior files preserved. Music selected separately inIG. Missing performance metrics remain null.'
}
(HERE/'local_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'video':str(video),'sha256':EXPECTED,'md5':manifest['md5'],'bytes':manifest['bytes'],'caption_Chinese_characters':manifest['caption_Chinese_characters']},ensure_ascii=False))
