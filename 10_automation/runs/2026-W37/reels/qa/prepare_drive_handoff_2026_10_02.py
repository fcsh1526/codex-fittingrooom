import json
from pathlib import Path

reels = Path(__file__).resolve().parents[1]
receipt = json.loads((reels / 'google_drive_archive_2026-10-02.json').read_text(encoding='utf-8'))
source = (reels / 'W37_REEL_HANDOFF.md').read_text(encoding='utf-8')
for item in receipt['files']:
    source = source.replace(item['local_path'].replace('\\', '/'), item['url'])
assert 'C:/Users/' not in source
source = source.replace('# W37 Reel 交付清單', '# W37 Reel 交付清單\n\n[開啟Google Drive資料夾](' + receipt['folder']['url'] + ')', 1)
(reels / 'W37_REEL_HANDOFF_DRIVE.md').write_text(source, encoding='utf-8')
print('Drive handoff prepared with ten verified cloud links.')
