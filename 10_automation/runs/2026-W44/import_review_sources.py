from pathlib import Path
import csv, json, hashlib, shutil, sys, subprocess, re
from html.parser import HTMLParser
R=Path(__file__).resolve().parents[3]; RUN=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
history=RUN/'history/before_W44_source_retrieval_2026-10-27'
history.mkdir(parents=True,exist_ok=True)
if not (history/'planning').exists():
 shutil.copytree(RUN/'planning',history/'planning')
 for name in ['publishing_structure.md','build_planning_review.py','finalize_planning.py']:
  shutil.copy2(RUN/name,history/name)
 dump(history/'SUPERSEDED.json',{'status':'superseded','reason':'Public W44, W42 and W43 source files successfully retrieved after browser verification and using the permitted network route. Earlier tool failure did not mean the reports were absent.','new_generation_approvals':0})
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.pre=False;self.parts=[];self.blocks=[];self.links=[]
 def handle_starttag(self,t,a):
  if t=='pre':self.pre=True;self.parts=[]
  if t=='a':
   d=dict(a)
   if d.get('href','').startswith('http'):self.links.append(d['href'])
 def handle_data(self,s):
  if self.pre:self.parts.append(s)
 def handle_endtag(self,t):
  if t=='pre':self.pre=False;self.blocks.append(''.join(self.parts))
summary=[]
for w in ['2026-W42','2026-W43','2026-W44']:
 d=R/'10_automation/runs'/w;f=d/'source_perplexity.csv'; report=d/'source_report.html'
 rows=list(csv.DictReader(f.open(encoding='utf-8-sig',newline='')))
 assert len(rows)==20 and len({r['id'] for r in rows})==20
 assert all(r['week']==w and None not in r and all(v is not None for v in r.values()) for r in rows)
 p=Parser();p.feed(report.read_text(encoding='utf-8-sig'))
 embedded=next((b for b in p.blocks if b.startswith('id,week,')),None)
 if embedded:
  import io
  assert list(csv.DictReader(io.StringIO(embedded)))==rows
 receipt={'week':w,'report_url':f'https://mika-lin-weekly.pplx.app/weeks/{w}.html','csv_url':f'https://mika-lin-weekly.pplx.app/data/{w}.csv','retrieved_date':'2026-10-27','method':'W44 verified in in-app browser, then original CSV/report fetched over permitted direct network access; no re-encoding or manual CSV reconstruction','sha256':sha(f),'rows':len(rows),'themes':len({r['trend_name'] for r in rows}),'report_sha256':sha(report),'csv_matches_embedded_report_rows':embedded is not None,'external_claims_verified':False,'evidence_limit':'保存原始週報與20筆原列、頁面內CSV逐列核對。上游配搭卡是研究輸入，不是本專案企劃／照片／商品或使用者核准；材質舒適度與止滑主張不能由AI示意圖驗證。'}
 dump(d/'source_receipt.json',receipt)
 dump(d/'source_links.json',sorted(set(p.links)))
 summary.append({'week':w,'rows':len(rows),'themes':list(dict.fromkeys(r['trend_name'] for r in rows)),'items':[{'id':r['id'],'item':r['clothing_item']} for r in rows]})
subprocess.run([sys.executable,str(R/'10_automation/build_material_pool.py'),'--as-of','2026-10-27','--window-weeks','3'],cwd=R,check=True)
dump(RUN/'source_retrieval_correction.json',{'date':'2026-10-27','user_provided_url':'https://mika-lin-weekly.pplx.app/weeks/2026-W44.html','earlier_failure':'web reader and restricted shell could not reach the host','resolved':'In-app browser loaded the report; permitted direct network retrieval succeeded for public index and W42–W44 CSV/report files.','source_weeks':summary,'prior_missing_claim_superseded':True,'prior_proposals':'history/before_W44_source_retrieval_2026-10-27','ai_stills_generated':0})
print(json.dumps(summary,ensure_ascii=False))
