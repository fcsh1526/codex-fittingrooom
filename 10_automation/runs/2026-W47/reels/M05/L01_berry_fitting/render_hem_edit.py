"""Render the M05 layered-hem cut and its original tonal music sketch."""

from array import array
from pathlib import Path
import math
import subprocess
import wave

folder = Path(__file__).resolve().parent
root = next(path for path in folder.parents if (path / "CURRENT_STATUS.md").exists())
ffmpeg = root / "openmontage/.local/bin/ffmpeg.exe"
duration = 7.5
sample_rate = 48000
notes = [(0.05, 587.33), (1.5, 440.0), (3.0, 659.25),
         (4.5, 739.99), (6.0, 587.33)]
samples = array("h")
for index in range(round(duration * sample_rate)):
    time = index / sample_rate
    value = 0.0
    for onset, frequency in notes:
        age = time - onset
        if 0 <= age < 2.0:
            envelope = (1 - math.exp(-age * 90)) * math.exp(-age * 3)
            tone = math.sin(2 * math.pi * frequency * age)
            tone += 0.18 * math.sin(2 * math.pi * frequency * 2 * age)
            value += 0.12 * envelope * tone
    fade = min(1.0, time / 0.3, (duration - time) / 0.5)
    bed = 0.012 * (math.sin(2 * math.pi * 146.83 * time)
                  + math.sin(2 * math.pi * 220 * time))
    samples.append(round(32767 * (value + bed) * max(0, fade)))

music = folder / "M05_hem_music_sketch_v1.wav"
with wave.open(str(music), "wb") as audio_file:
    audio_file.setnchannels(1)
    audio_file.setsampwidth(2)
    audio_file.setframerate(sample_rate)
    audio_file.writeframes(samples.tobytes())

filters = (
    "[0:v]split=2[a][b];"
    "[a]trim=start_frame=12:end_frame=48,setpts=PTS-STARTPTS,"
    "pad=720:1280:0:8:color=0xddd9d4,setsar=1[v0];"
    "[b]trim=start_frame=48:end_frame=120,setpts=PTS-STARTPTS,"
    "crop=450:800:140:440,scale=720:1280,setsar=1[v1];"
    "[1:v]trim=start_frame=24:end_frame=96,setpts=PTS-STARTPTS,"
    "pad=720:1280:0:8:color=0xddd9d4,setsar=1[v2];"
    "[v0][v1][v2]concat=n=3:v=1:a=0,fps=24[out]"
)
subprocess.run([
    str(ffmpeg), "-hide_banner", "-v", "error",
    "-i", str(folder / "M05_L01_window_half_step_v2.mp4"),
    "-i", str(folder / "M05_L01_full_smile_v1.mp4"),
    "-i", str(music), "-filter_complex", filters,
    "-map", "[out]", "-map", "2:a", "-t", str(duration),
    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
    "-n", str(folder / "M05_L01_hem_edit_v2.mp4")
], check=True)
