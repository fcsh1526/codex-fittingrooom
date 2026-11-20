from pathlib import Path
from http.server import HTTPServer,BaseHTTPRequestHandler
import time
P=Path(__file__).resolve().parent
video=(P/'A_existing_source_opening_rough_v1.mp4').read_bytes()
page='''<!doctype html><meta charset="utf-8"><title>M04 原速成片檢查</title>
<style>body{background:#f4f1eb;color:#233e40;font:17px sans-serif;margin:20px;display:flex;gap:28px}video{height:650px;max-height:85vh;background:#111}button{padding:12px;margin:8px 4px 8px 0;font:inherit}aside{max-width:350px}output{display:block;white-space:pre-wrap}</style>
<video id="v" src="/video.mp4" controls preload="auto" playsinline></video><aside><h2>M04｜五秒原速候選</h2><p>沿用已接受開場。畫面無字、無音、無變速。</p><button id="play">從頭原速播放</button><button id="pause">暫停</button><output id="s">等待載入</output><p>檢查：臉與表情、手與肩包、衣料連續性、收尾。</p><p>開場吸引力已接受；成片檢查與發布接受分開記錄。</p></aside>
<script>const v=document.getElementById('v'),s=document.getElementById('s');let starts=0,ends=0;document.getElementById('play').onclick=()=>{v.currentTime=0;v.playbackRate=1;starts++;v.play()};document.getElementById('pause').onclick=()=>v.pause();v.onended=()=>ends++;function draw(){s.textContent='時間 '+v.currentTime.toFixed(3)+' / '+(v.duration||0).toFixed(3)+' 秒\\n速度 '+v.playbackRate+'x\\n狀態 '+(v.ended?'播放結束':v.paused?'暫停':'播放中')+'\\n開始 '+starts+' 次，結束 '+ends+' 次';requestAnimationFrame(draw)}draw();</script>'''.encode('utf-8')
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/':data=page;mime='text/html; charset=utf-8'
        elif self.path=='/video.mp4':data=video;mime='video/mp4'
        else:self.send_error(404);return
        start=0;end=len(data)-1;partial=False
        rng=self.headers.get('Range')
        if rng and self.path=='/video.mp4':
            a,b=rng.removeprefix('bytes=').split('-',1);start=int(a or 0);end=min(int(b) if b else end,end);partial=True
        self.send_response(206 if partial else 200);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(end-start+1));self.send_header('Accept-Ranges','bytes')
        if partial:self.send_header('Content-Range',f'bytes {start}-{end}/{len(data)}')
        self.end_headers();self.wfile.write(data[start:end+1])
    def log_message(self,*args):pass
server=HTTPServer(('127.0.0.1',4762),Handler);server.timeout=.5
print('Local review player ready; limited to this video; expires after 180 seconds.',flush=True)
deadline=time.monotonic()+180
while time.monotonic()<deadline:server.handle_request()
server.server_close()
