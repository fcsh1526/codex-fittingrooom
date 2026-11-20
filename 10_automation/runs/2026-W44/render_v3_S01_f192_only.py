from pathlib import Path
source=Path('10_automation/runs/2026-W44/build_editorial_reset_v3.py').read_text(encoding='utf-8-sig')
namespace={'__file__':str(Path('10_automation/runs/2026-W44/build_editorial_reset_v3.py').resolve())}
exec(compile(source.split('\nsamples=[]')[0],namespace['__file__'],'exec'),namespace)
out=Path('10_automation/runs/2026-W44/editorial_reset_v3_2026-10-28/camera_S01_f192_8s.png')
namespace['camera'](192,1,540).save(out)
print(out)
