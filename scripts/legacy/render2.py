# Memory-safe renderer: each clip rendered separately, then joined + captions + music in one pass.
import json, sys, subprocess, os
sys.path.insert(0, "/home/claude/reel_scripts"); import os as _os; sys.path.insert(0, _os.environ.get("RW", "/home/claude/reel_work"))
from cuts import CUTS
W = _os.environ.get("RW", "/home/claude/reel_work")
music = sys.argv[1]; out = sys.argv[2]
faces = json.load(open(f"{W}/faces.json")); SG = json.load(open(f"{W}/speech_gains.json"))
tl = json.load(open(f"{W}/clip_offs.json")) if os.path.exists(f"{W}/clip_offs.json") else json.load(open(f"{W}/timeline.json")); TOTAL = tl["total"]
os.makedirs(f"{W}/clips", exist_ok=True)
lst = []
for i, ((a, b), f) in enumerate(zip(CUTS, faces)):
    cx = f["cx"] or 427
    punch = (i % 3 == 1) or (i == len(CUTS) - 1)
    cw, ch = (344, 430) if punch else (384, 480)
    x = int(min(max(cx - cw / 2, 0), 854 - cw)); d = b - a
    vf = (f"[0:v]split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=28:2,eq=brightness=-0.24:saturation=0.6[bg];"
          f"[b]crop={cw}:{ch}:{x}:0,scale=1080:1350:flags=lanczos,unsharp=5:5:0.55[fg];[bg][fg]overlay=0:300,setsar=1,fps=30[v];"
          f"[0:a]aresample=48000,volume={SG[i]}dB,afade=t=in:d=0.012,afade=t=out:st={d-0.015:.3f}:d=0.015[aa]")
    o = f"{W}/clips/c{i:02d}.mkv"
    if not (os.environ.get("SKIP_CLIPS") and os.path.exists(o)): subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{a:.3f}", "-i", f"{W}/seg25.mp4", "-t", f"{d:.3f}",
                    "-filter_complex", vf, "-map", "[v]", "-map", "[aa]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "12",
                    "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", o], check=True)
    lst.append(f"file '{o}'")
open(f"{W}/clips/list.txt", "w").write("\n".join(lst) + "\n")
fc = (f"[0:v]fps=30,ass={W}/caps.ass:fontsdir={W}/fonts:shaping=complex,fade=t=out:st={TOTAL-0.6:.2f}:d=0.6,format=yuv420p[vout];"
      f"[0:a]aresample=48000,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=180:makeup=2,asplit=2[sp][spsc];"
      f"[1:a]aresample=48000,volume=0.32[mu0];[mu0][spsc]sidechaincompress=threshold=0.1:ratio=2:attack=80:release=700[mu];"
      f"[sp][mu]amix=inputs=2:duration=first:normalize=0,afade=t=out:st={TOTAL-0.7:.2f}:d=0.7[aout]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{W}/clips/list.txt", "-i", music,
                "-filter_complex", fc, "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                "-c:a", "pcm_s16le", "-ar", "48000", out], check=True)
print("rendered", out)
