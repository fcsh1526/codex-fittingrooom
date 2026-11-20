# W46 M01 S01 雲端後製測試

請在雲端工作解壓此包，在解壓資料夾執行下列步驟。只使用既有 Grok 原片，無須影片 API、Grok 登入或本機存取。所需工具為 FFmpeg 與 FFprobe（含 libx264）。

```sh
set -eu
printf '%s  source.mp4\n' ba30f3caa2a6e759c8b83a83f11def52b8306623c31968988d40d0bee35ee33f | sha256sum -c -
ffmpeg -hide_banner -loglevel error -xerror -i source.mp4 -map 0:v:0 -f null -
ffmpeg -hide_banner -loglevel error -xerror -n -i source.mp4 -map 0:v:0 -an -frames:v 144 -c:v libx264 -pix_fmt yuv420p -movflags +faststart post_test.mp4
ffmpeg -hide_banner -loglevel error -xerror -i post_test.mp4 -map 0:v:0 -f null -
ffprobe -v error -count_frames -show_entries stream=codec_type,width,height,r_frame_rate,nb_read_frames,duration -of json post_test.mp4 > post_test_probe.json
sha256sum post_test.mp4
```

預期原片完整解碼。輸出只含一條視訊軌，720×1280、24 fps、144 格、6.000 秒。保留原速，裁掉最後一格來驗證剪輯輸出。這是技術測試片。

存入另設的 Drive 測試資料夾前，請確認有該次上傳授權。上傳後重新讀回檔案，核對檔案大小與 SHA-256，再記錄雲端執行環境、雲端輸出及 Drive 回讀結果。沒有回讀就把該項標為待驗證。此測試不涵蓋新生成或原速視覺審查。
