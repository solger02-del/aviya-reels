# Renderer for the "premium light" style: rounded speaker cards, light geometric background,
# pill layout, blurred focus moments, typography cards, word-by-word mixed-size captions.
import json, os, sys, subprocess, importlib.util, glob
import numpy as np, wave
sys.path.insert(0, "/home/claude/reel_scripts")
import style2_assets as A

RW = os.environ["RW"]
spec = importlib.util.spec_from_file_location("cuts2", f"{RW}/cuts2.py"); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
SEG = C.SEG
SRC = f"{RW}/seg25.mp4"
AS = f"{RW}/assets"; os.makedirs(AS, exist_ok=True); os.makedirs(f"{RW}/clips2", exist_ok=True)
words = json.load(open("/home/claude/reel_work/words.json"))
W, H, FPS = 1080, 1920, 30

# ---------------- layouts ----------------
L = {
    "card": dict(x=90, y=270, w=900, h=1380, r=56, pill=False, cap=(540, 1290), ks=150, ss=70),
    "big":  dict(x=40, y=130, w=1000, h=1660, r=48, pill=False, cap=(540, 1360), ks=156, ss=72),
    "pill": dict(x=60, y=170, w=700, h=1250, r=350, pill=True, cap=(410, 1090), ks=122, ss=58),
}
A.geo_background(f"{AS}/bg_geo.png", seed=3)
from PIL import Image
Image.new("RGB", (W, H), (243, 241, 240)).save(f"{AS}/bg_plain.png")
for name, g in L.items():
    g["pad"] = A.card_frame(f"{AS}/mask_{name}.png", f"{AS}/ov_{name}.png", g["w"], g["h"], g["r"], pill=g["pill"])

# ---------------- face position per segment ----------------
import cv2
cap = cv2.VideoCapture(SRC)
casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
def face_cx(a, b):
    xs = []
    for k in range(5):
        cap.set(cv2.CAP_PROP_POS_MSEC, (a + (b - a) * (k + 0.5) / 5) * 1000); ok, fr = cap.read()
        if not ok: continue
        f = casc.detectMultiScale(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY), 1.1, 5, minSize=(40, 40))
        if len(f): x, y, w, h = max(f, key=lambda r: r[2] * r[3]); xs.append(x + w / 2)
    xs.sort(); return float(xs[len(xs) // 2]) if xs else 427.0

# ---------------- voice leveling ----------------
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", SRC, "-vn", "-ac", "1", "-ar", "16000", f"{RW}/aud16.wav"], check=True)
wv = wave.open(f"{RW}/aud16.wav"); aud = np.frombuffer(wv.readframes(wv.getnframes()), np.int16) / 32768.
def gain(a, b):
    seg = aud[int(a * 16000):int(b * 16000)]
    f = seg[:len(seg) // 800 * 800].reshape(-1, 800); r = np.sqrt((f ** 2).mean(1)); r = r[r > 10 ** (-45 / 20)]
    lv = 20 * np.log10(np.sqrt((r ** 2).mean()) + 1e-9) + 0.21 if len(r) else -20
    return round(float(max(-4, min(9, 0.7 * (-15 - lv)))), 2)

# ---------------- per-segment render ----------------
files = []; prev_layout = None
for i, s in enumerate(SEG):
    a, b = s["a"], s["b"]; d = b - a; lay = s["layout"]
    cx = face_cx(a, b); gdb = gain(a, b)
    z0 = 1.10 if s.get("punch") else 1.0; z1 = z0 + 0.05
    inputs = ["-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", SRC]
    fc = []
    def speaker(g, label, extra=""):
        asp = g["w"] / g["h"]; cw = int(round(480 * asp)); x = int(min(max(cx - cw / 2, 0), 854 - cw))
        fc.append(f"[0:v]crop={cw}:480:{x}:0,scale={g['w']}:{g['h']}:flags=lanczos,"
                  f"scale=w='{g['w']}*({z0}+{z1 - z0}*t/{d:.3f})':h=-2:eval=frame:flags=bicubic,"
                  f"crop={g['w']}:{g['h']}:(iw-{g['w']})/2:(ih-{g['h']})*0.12,unsharp=5:5:0.5,eq=saturation=1.08:contrast=1.03,format=rgba{extra}[{label}]")
    if lay in ("card", "big", "pill", "focus"):
        g = L["big" if lay == "focus" else lay]
        bgimg = f"{AS}/bg_plain.png" if lay == "pill" else f"{AS}/bg_geo.png"
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", bgimg,
                   "-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", f"{AS}/mask_{'big' if lay == 'focus' else lay}.png",
                   "-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", f"{AS}/ov_{'big' if lay == 'focus' else lay}.png"]
        speaker(g, "sp")
        fc.append("[2:v]format=gray[mk];[sp][mk]alphamerge[spm]")
        fc.append(f"[1:v][spm]overlay={g['x']}:{g['y']}[b1];[b1][3:v]overlay={g['x'] - g['pad']}:{g['y'] - g['pad']}[b2]")
        last = "b2"
        if lay == "pill":
            A.number_pill(f"{AS}/num_{i}.png", 380, 600, s.get("num", ""))
            inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", f"{AS}/num_{i}.png"]
            ystop = 1180; yexpr = f"if(lt(t\\,0.35)\\,{H}-({H}-{ystop})*t/0.35\\,{ystop})" if s.get("slide", True) else str(ystop)
            fc.append(f"[{last}][4:v]overlay=x=640:y='{yexpr}'[b3]"); last = "b3"
        if lay == "focus":
            A.focus_text(f"{AS}/focus_{i}.png", s["small"], s["big"])
            inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", f"{AS}/focus_{i}.png"]
            fc.append(f"[{last}]gblur=sigma=22,eq=brightness=-0.10[bl];[4:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1[ft];[bl][ft]overlay=0:0[b3]"); last = "b3"
    elif lay == "text":
        A.text_card(f"{AS}/text_{i}.png", s["title"], s.get("sub", ""), seed=s.get("seed", 7 + i))
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", f"{AS}/text_{i}.png"]
        fc.append(f"[1:v]scale=w='{W}*(1+0.04*t/{d:.3f})':h=-2:eval=frame,crop={W}:{H}:(iw-{W})/2:(ih-{H})/2[b2]"); last = "b2"
    # pop when the layout changes
    if lay != prev_layout and i > 0:
        fc.append(f"[{last}]scale=w='{W}*(1+0.06*max(0\\,1-t/0.22))':h=-2:eval=frame,crop={W}:{H}:(iw-{W})/2:(ih-{H})/2[pp]"); last = "pp"
    fc.append(f"[{last}]fps={FPS},format=yuv420p,setsar=1[v]")
    fc.append(f"[0:a]aresample=48000,volume={gdb}dB,afade=t=in:d=0.012,afade=t=out:st={d - 0.015:.3f}:d=0.015[aa]")
    o = f"{RW}/clips2/s{i:02d}.mkv"
    subprocess.run(["ffmpeg", "-y", "-v", "error"] + inputs + ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[aa]", "-t", f"{d:.3f}",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", o], check=True)
    files.append(o); prev_layout = lay
    print("seg", i, lay, round(d, 2), "gain", gdb)

# real durations -> offsets
durs = [float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", f], capture_output=True, text=True).stdout) for f in files]
offs = [0.0]
for dd in durs[:-1]: offs.append(offs[-1] + dd)
TOTAL = sum(durs)

# ---------------- captions ----------------
STOP = {"את", "של", "על", "זה", "אני", "הוא", "היא", "אם", "לא", "כי", "גם", "כן", "לי", "לו", "אבל", "מה", "אתה", "עם", "כל", "יש", "רק"}
def ts(x):
    x = max(0, x); return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"
def clean(t): return t.strip().rstrip(".,")
ev = []
for i, s in enumerate(SEG):
    if s["layout"] in ("focus", "text"): continue
    a, b = s["a"], s["b"]
    ws = [(w["text"], w["src_start_ms"] / 1000) for w in words if a - 0.02 <= w["src_start_ms"] / 1000 < b - 0.05]
    ws = [(s.get("fix", {}).get(t, t), tt) for t, tt in ws]
    splits = s.get("splits")
    if not splits:
        splits, cur, st0 = [], 0, None
        for j, (t, tt) in enumerate(ws):
            if cur == 0: st0 = tt
            cur += 1
            if cur == 3 or t.endswith((",", ".", "?")) or (j + 1 < len(ws) and ws[j + 1][1] - st0 > 1.3):
                splits.append(cur); cur = 0
        if cur: splits.append(cur)
    assert sum(splits) == len(ws), (i, splits, [t for t, _ in ws])
    g = L.get(s["layout"], L["card"]); keys = s.get("keys", [])
    k0 = 0
    for pi, n in enumerate(splits):
        page = ws[k0:k0 + n]; k0 += n
        if pi < len(keys) and keys[pi] is not None: k = keys[pi]
        else:
            cand = [(len(clean(t)) if clean(t) not in STOP else 0, -j) for j, (t, _) in enumerate(page)]
            k = -max(cand)[1]
        st = offs[i] + max(0, page[0][1] - a - 0.05)
        nxt = ws[k0][1] if k0 < len(ws) else b
        en = offs[i] + min(b, nxt) - a - 0.03
        def word(t, tt, big):
            dt = int(max(0, (offs[i] + tt - a) - st) * 1000)
            fn, fs = ("Heebo Regular", g["ks"]) if big else ("Heebo Light", g["ss"])
            if big and len(clean(t)) > 7: fs = int(fs * 7.5 / len(clean(t)) + fs * 0.25)
            return (f"{{\\fn{fn}\\fs{fs}\\1a&HFF&\\3a&HFF&\\4a&HFF&\\t({dt},{dt + 140},\\1a&H00&\\3a&H60&\\4a&HA0&)}}"
                    + (clean(t) if big or (page.index((t, tt)) == len(page) - 1) else t.rstrip(".")))
        lines = []
        if k > 0: lines.append(" ".join(word(t, tt, False) for t, tt in page[:k]))
        lines.append(word(*page[k], True))
        if k + 1 < len(page): lines.append(" ".join(word(t, tt, False) for t, tt in page[k + 1:]))
        txt = "\\N".join(lines)
        ev.append(f"Dialogue: 2,{ts(st)},{ts(en)},Cap,,0,0,0,,{{\\an5\\pos({g['cap'][0]},{g['cap'][1]})\\fad(0,90)}}{txt}")
hook = getattr(C, "HOOK", None)
if hook:
    ev.append(f"Dialogue: 3,{ts(0.05)},{ts(getattr(C, 'HOOK_END', 2.6))},Hook,,0,0,0,,{{\\an8\\pos(540,40)\\fad(250,250)\\fsp18\\t(0,600,\\fsp0)}}{hook}")
ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Heebo Light,60,&H00FFFFFF,&H00FFFFFF,&H60000000,&HA0000000,0,0,0,0,100,100,0,0,1,3,2,5,60,60,0,-1
Style: Hook,Heebo Light,200,&H002E2A2A,&H002E2A2A,&H00FFFFFF,&H00000000,0,0,0,0,100,100,0,0,1,0,0,8,40,40,0,-1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n"
open(f"{RW}/caps2.ass", "w").write(ass)
for e in ev[:3]: print(e[:160])

# ---------------- join + captions ----------------
open(f"{RW}/clips2/list.txt", "w").write("".join(f"file '{f}'\n" for f in files))
fc = (f"[0:v]ass={RW}/caps2.ass:fontsdir=/home/claude/reel_work/fonts:shaping=complex,fade=t=out:st={TOTAL - 0.5:.2f}:d=0.5,format=yuv420p[vout];"
      f"[0:a]aresample=48000,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=180:makeup=2,afade=t=out:st={TOTAL - 0.6:.2f}:d=0.6[aout]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{RW}/clips2/list.txt", "-filter_complex", fc,
                "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-c:a", "pcm_s16le", "-ar", "48000", f"{RW}/tmp2.mov"], check=True)
# loudness
out = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{RW}/tmp2.mov", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
m = json.loads(out[out.rindex("{"):out.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000,volume=0.6dB,alimiter=limit=0.84:level=disabled")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{RW}/tmp2.mov", "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                "-movflags", "+faststart", f"{RW}/out2.mp4"], check=True)
print("done", round(TOTAL, 2))
