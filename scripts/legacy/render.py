import json, sys, subprocess, numpy as np, wave, os
sys.path.insert(0, "/home/claude/reel_scripts"); import os as _os; sys.path.insert(0, _os.environ.get("RW", "/home/claude/reel_work"))
from cuts import CUTS, FIX, SPLITS
import cuts as _cm
HOOK = getattr(_cm, 'HOOK', '״אני מפחד לחיות,\\Nלא למות״')
EXTRA = getattr(_cm, 'EXTRA', [])
SIZES = getattr(_cm, 'SIZES', None)
W = _os.environ.get("RW", "/home/claude/reel_work")
SRC = f"{W}/seg25.mp4"
BASE = 90.0
faces = json.load(open(f"{W}/faces.json"))
SG = json.load(open(f"{W}/speech_gains.json"))
words = json.load(open(f"{W}/words.json"))
TOPY = 300  # foreground top on 1080x1920

# ---------- timeline ----------
offs, t = [], 0.0
for a, b in CUTS:
    offs.append(t); t += (b - a)
TOTAL = t
if os.path.exists(f"{W}/clip_offs.json") and os.environ.get("USE_CLIP_OFFS"):
    _co = json.load(open(f"{W}/clip_offs.json")); offs = _co["offs"]; TOTAL = _co["total"]
print("total", round(TOTAL, 2))

# ---------- video/audio graph ----------
fc = []
labels_v, labels_a = [], []
for i, ((a, b), f) in enumerate(zip(CUTS, faces)):
    s, e = a - BASE, b - BASE
    cx = f["cx"] or 427
    punch = (i % 3 == 1) or (i == len(CUTS) - 1)  # every third clip + the final punchline slightly tighter
    if punch:
        cw, ch = 344, 430
    else:
        cw, ch = 384, 480
    x = int(min(max(cx - cw / 2, 0), 854 - cw))
    fc.append(f"[0:v]trim={s:.3f}:{e:.3f},setpts=PTS-STARTPTS,split[v{i}a][v{i}b]")
    fc.append(f"[v{i}a]scale=-2:1920,crop=1080:1920,boxblur=28:2,eq=brightness=-0.24:saturation=0.6[bg{i}]")
    fc.append(f"[v{i}b]crop={cw}:{ch}:{x}:0,scale=1080:1350:flags=lanczos,unsharp=5:5:0.55[fg{i}]")
    fc.append(f"[bg{i}][fg{i}]overlay=0:{TOPY},setsar=1[c{i}]")
    d = b - a
    fc.append(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,volume={SG[i]}dB,afade=t=in:d=0.012,afade=t=out:st={d-0.015:.3f}:d=0.015[a{i}]")
    labels_v.append(f"[c{i}]"); labels_a.append(f"[a{i}]")
n = len(CUTS)
fc.append("".join(f"[c{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")

# ---------- captions (ASS) ----------
def ts(x):
    x = max(0, x); h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"
pages = []
for i, (a, b) in enumerate(CUTS):
    ws = [w for w in words if a - 0.02 <= w["src_start_ms"] / 1000 < b - 0.05]
    seq = [(FIX.get(w["text"], w["text"]), w["src_start_ms"] / 1000) for w in ws]
    assert sum(SPLITS[i]) == len(seq), (i, len(seq))
    groups, k0 = [], 0
    for c in SPLITS[i]:
        groups.append(seq[k0:k0 + c]); k0 += c
    for gi, g in enumerate(groups):
        st = max(a, g[0][1] - 0.06)
        en = groups[gi + 1][0][1] - 0.06 if gi + 1 < len(groups) else b
        parts = []
        for wi, (txt, ws_) in enumerate(g):
            nxt = g[wi + 1][1] if wi + 1 < len(g) else en
            k = max(1, int(round((nxt - max(ws_, st)) * 100)))
            clean = txt.rstrip(".,") if wi == len(g) - 1 else txt.rstrip(".")
            parts.append(f"{{\\k{k}}}{clean}")
        code = SIZES[i][gi] if SIZES else "M"
        plain = " ".join(t for t, _ in g)
        pages.append((offs[i] + st - a, offs[i] + en - a, " ".join(parts), code, plain))

HOOK_END = 3.3
ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Heebo Black,84,&H004EC1F2,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,6,3,2,90,90,500,-1
Style: Hook,Secular One,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H26000000,0,0,0,0,100,100,0,0,3,16,0,8,60,60,58,-1
Style: Name,Secular One,62,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,4,2,8,60,60,70,-1
Style: Big,Secular One,120,&H004EC1F2,&H004EC1F2,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,6,3,8,60,60,205,-1
Style: Sub,Heebo ExtraBold,42,&H004EC1F2,&H004EC1F2,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,3,1,8,60,60,152,-1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 1,{ts(0)},{ts(HOOK_END)},Hook,,0,0,0,,{{\\fad(0,250)}}{HOOK}
Dialogue: 1,{ts(HOOK_END)},{ts(TOTAL)},Name,,0,0,0,,{{\\fad(250,0)}}הרב אביה אוחיון
Dialogue: 1,{ts(HOOK_END)},{ts(TOTAL)},Sub,,0,0,0,,{{\\fad(250,0)}}שלישי קבוע
"""
FS = {"S": 64, "M": 86, "L": 112, "H": 132}
for st, en, txt, code, plain in pages:
    size = FS[code]
    size = int(min(size, 920 / (0.50 * max(1, len(plain)))))   # keep the line inside the safe width
    if code in ("L", "H"):
        pop = 118 if code == "L" else 130
        pre = f"{{\\fs{size}\\fscx{pop}\\fscy{pop}\\t(0,150,\\fscx100\\fscy100)}}"
    else:
        pre = f"{{\\fs{size}}}"
    if code == "H":
        pre = pre[:-1] + "\\2c&H004EC1F2&}"
    ass += f"Dialogue: 2,{ts(st)},{ts(en)},Cap,,0,0,0,,{pre}{txt}\n"
for (c0, c1, style, txt) in EXTRA:
    ass += f"Dialogue: 3,{ts(offs[c0])},{ts(offs[c1] if c1 < len(offs) else TOTAL)},{style},,0,0,0,,{txt}\n"
open(f"{W}/caps.ass", "w").write(ass)
json.dump({"offs": offs, "total": TOTAL, "pages": pages}, open(f"{W}/timeline.json", "w"), ensure_ascii=False, indent=0)

ILL = []  # illustrations removed at user request
prev = "vc0"
fc.append("[vc]fps=30[vc0]")
for name, inp, c0, c1, zadd, fx, fy in ILL:
    st, en = offs[c0], offs[c1]
    nf = int(round((en - st) * 30))
    zexpr = f"1+{zadd}*on/{nf}"
    fc.append(f"[{inp}:v]scale=4320:7680,zoompan=z='{zexpr}':x='max(0,min(iw-iw/zoom,{fx*4}-iw/zoom/2))':y='max(0,min(ih-ih/zoom,{fy*4}-ih/zoom/2))':d=1:s=1080x1920:fps=30,"
              f"trim=end_frame={nf},format=yuva420p,"
              + (f"fade=t=in:st=0:d=0.25:alpha=1," if name == "A" else "")
              + (f"fade=t=out:st={(nf/30)-0.25:.2f}:d=0.25:alpha=1," if name == "B" else "")
              + f"setpts=PTS-STARTPTS+{st:.3f}/TB[ill{name}]")
    fc.append(f"[{prev}][ill{name}]overlay=0:0:enable='between(t,{st:.3f},{en:.3f})':eof_action=pass[v{name}]")
    prev = f"v{name}"
fc.append(f"[{prev}]ass={W}/caps.ass:fontsdir={W}/fonts:shaping=complex,fade=t=out:st={TOTAL-0.6:.2f}:d=0.6,format=yuv420p[vout]")

# ---------- SFX: soft low hits in pauses ----------
sr = 48000
def hit(dur=1.1, f0=95, f1=38, amp=0.9):
    tt = np.arange(int(sr * dur)) / sr
    freq = f1 + (f0 - f1) * np.exp(-tt * 9)
    ph = 2 * np.pi * np.cumsum(freq) / sr
    env = np.exp(-tt * 4.2) * (1 - np.exp(-tt * 400))
    noise = np.random.default_rng(3).normal(0, 1, len(tt))
    k = np.exp(-np.arange(200) / 30.0); k /= k.sum()
    noise = np.convolve(noise, k, "same") * np.exp(-tt * 18) * 0.35
    return amp * (np.sin(ph) * env + noise)
sfx = np.zeros(int(sr * (TOTAL + 0.5)))
# after "לא למות" (clip 13 word end 211.88) and after the final line (290.60)
for src_t, clip_i in ([(211.92, 13)] if len(CUTS) > 13 and CUTS[13][0] == 210.12 else []):
    tl = offs[clip_i] + (src_t - CUTS[clip_i][0])
    h = hit()
    i0 = int(tl * sr); sfx[i0:i0 + len(h)] += h[:len(sfx) - i0]
sfx = np.clip(sfx / np.max(np.abs(sfx)) * 0.7, -1, 1)
with wave.open(f"{W}/sfx.wav", "w") as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(sr)
    wv.writeframes((sfx * 32767).astype(np.int16).tobytes())
fc.append(f"[ac]aresample=48000,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=180:makeup=2,asplit=2[sp][spsc];[2:a]aresample=48000,volume=0.32[mu0];[mu0][spsc]sidechaincompress=threshold=0.1:ratio=2:attack=80:release=700[mu];[1:a]volume=0[fx];[sp][fx][mu]amix=inputs=3:duration=first:normalize=0,afade=t=out:st={TOTAL-0.7:.2f}:d=0.7[aout]")
open(f"{W}/graph.txt", "w").write(";\n".join(fc))
print("pages", len(pages))
