"""Preserve the order-only test; make a separate static wider-framing revision."""
from pathlib import Path
P=Path(__file__).resolve().parent;Q=P.parent/'paired_review_v3';Q.mkdir(exist_ok=True)
t=(P/'render_reordered.py').read_text(encoding='utf-8')
t=t.replace('One local editorial test: reorder selected native intervals to end with readable fronts.','Reordered selected intervals with a wider fixed crop to retain hands.').replace("'main_variable':'Order of the same two selected intervals; no new provider call.'","'main_variable':'Order plus static framing, based on internal v2 review; not a single-variable causal comparison.'").replace("'crop':[135,0,450,1280]","'crop':[80,0,560,1280]").replace("'scale':356/450","'scale':356/560").replace('crop=450:1280:135:0','crop=560:1280:80:0').replace('M03_W45_parallel_selected_review_v2.mp4','M03_W45_parallel_selected_review_v3.mp4')
(Q/'render_reordered.py').write_text(t,encoding='utf-8')
print('Prepared separate v3. Earlier files preserved.')
