# Renderer for the merged style ("קצת אחרת – פרימיום"). Reads $RW/cuts3.py (SEG list), writes $RW/out3.mp4.
import json, os, sys, subprocess, importlib.util, math
import numpy as np, wave
sys.path.insert(0, "/home/claude/reel_scripts")
import style3_assets as A
import style3_anim as AN

RW = os.environ["RW"]
spec = importlib.util.spec_from_file_location("cuts3", f"{RW}/cuts3.py"); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
SEG = C.SEG
SRC = os.environ.get("SRC", f"{RW}/seg25.mp4")
AS = f"{RW}/assets3"; CL = f"{RW}/clips3"
os.makedirs(AS, exist_ok=True); os.makedirs(CL, exist_ok=True)
words = json.load(open(os.environ.get("WORDS", "/home/claude/reel_work/words.json")))
W, H, FPS = 1080, 1920, 30
WIN_Y = 330                     # top of the speaker window on the stage
A.feather_mask(f"{AS}/feather.png")
A.circle_mask(f"{AS}/circle300.png", 300); A.avatar_ring(f"{AS}/ring300.png", 300)
A.circle_mask(f"{AS}/circle220.png", 220); A.avatar_ring(f"{AS}/ring220.png", 220)
A.beige_bg(f"{AS}/beige.png"); A.black_bg(f"{AS}/black.png")
TINT = {"navy": "rs=-0.04:gs=0:bs=0.10:rm=-0.02:bm=0.04", "warm": "rs=0.10:gs=0.02:bs=-0.08:rm=0.05:bm=-0.04",
        "teal": "rs=-0.06:gs=0.06:bs=0.04", "purple": "rs=0.03:gs=-0.05:bs=0.10", "rose": "rs=0.08:gs=-0.03:bs=0.03"}

# ---------------- face position ----------------
import cv2
cap = cv2.VideoCapture(SRC)
SW, SH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
CW = int(min(SW, SH * 0.8)) // 2 * 2; CH = int(CW * 1.25) // 2 * 2     # 4:5 speaker crop
SQ = 230 if SW > SH else int(SW * 0.6)                                # avatar crop
casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
def face(a, b):
    xs, ys = [], []
    for k in range(5):
        cap.set(cv2.CAP_PROP_POS_MSEC, (a + (b - a) * (k + 0.5) / 5) * 1000); ok, fr = cap.read()
        if not ok: continue
        f = casc.detectMultiScale(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY), 1.1, 5, minSize=(max(40, SW // 9), max(40, SW // 9)))
        f = [r for r in f if r[1] + r[3] / 2 < SH * 0.54]      # faces are in the upper part; ignore false hits on the shirt/mic
        if len(f): x, y, w, h = max(f, key=lambda r: r[2] * r[3]); xs.append(x + w / 2); ys.append(y + h / 2)
    xs.sort(); ys.sort()
    return (float(xs[len(xs) // 2]) if xs else SW / 2, float(ys[len(ys) // 2]) if ys else SH * 0.27)

# ---------------- voice leveling ----------------
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", SRC, "-vn", "-ac", "1", "-ar", "16000", f"{RW}/aud16.wav"], check=True)
wv = wave.open(f"{RW}/aud16.wav"); aud = np.frombuffer(wv.readframes(wv.getnframes()), np.int16) / 32768.
def gain(a, b):
    seg = aud[int(a * 16000):int(b * 16000)]
    f = seg[:len(seg) // 800 * 800].reshape(-1, 800); r = np.sqrt((f ** 2).mean(1)); r = r[r > 10 ** (-45 / 20)]
    lv = 20 * np.log10(np.sqrt((r ** 2).mean()) + 1e-9) + 0.21 if len(r) else -20
    return round(float(max(-4, min(9, 0.7 * (-15 - lv)))), 2)

def loop(path, d): return ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", path]

# ---------------- per-segment render ----------------
files = []; prev = None
for i, s in enumerate(SEG):
    a, b = s["a"], s["b"]; d = b - a; lay = s["layout"]; th = s.get("theme", "navy")
    cx, cy = face(a, b); gdb = gain(a, b)
    z0 = 1.10 if s.get("punch") else 1.0; z1 = z0 + 0.05
    inputs = ["-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", SRC]; fc = []; n_in = 1
    def add(args):
        global n_in
        inputs.extend(args); n_in += 1; return n_in - 1
    def stage(bgpath, extra_bg=None):
        """speaker window (feathered, tinted) over a themed background; returns output label."""
        ib = add(loop(bgpath, d)); im = add(loop(f"{AS}/feather.png", d))
        x = int(min(max(cx - CW / 2, 0), SW - CW)); y = int(min(max(cy - CH * 0.36, 0), SH - CH)) if SH > CH else 0
        fc.append(f"[0:v]setpts=PTS-STARTPTS,crop={CW}:{CH}:{x}:{y},scale=1080:1350:flags=lanczos,"
                  f"scale=w='1080*({z0}+{z1 - z0}*t/{d:.3f})':h=-2:eval=frame:flags=bicubic,crop=1080:1350:(iw-1080)/2:(ih-1350)*0.12,"
                  f"unsharp=5:5:0.55,eq=saturation=1.06:contrast=1.05:brightness=-0.02,colorbalance={TINT[th]},format=rgba[sp{i}]")
        fc.append(f"[{im}:v]format=gray[mk{i}];[sp{i}][mk{i}]alphamerge[spm{i}]")
        base = f"{ib}:v"
        if extra_bg:
            ir = add(loop(extra_bg, d))
            fc.append(f"[{ir}:v]format=rgba,rotate=a='t*0.25':c=none:ow=1500:oh=1500[ry{i}];[{ib}:v][ry{i}]overlay=x=-210:y={WIN_Y + 350 - 750}[bgr{i}]")
            base = f"bgr{i}"
        fc.append(f"[{base}][spm{i}]overlay=0:{WIN_Y}[st{i}]")
        last = f"st{i}"
        if s.get("icon"):
            ipath = f"{AS}/icon_{i}"; A.icon_sequence(ipath, s["icon"], th, d, size=s.get("icon_size", 300), draw_time=s.get("icon_draw", 0.75), t_offset=0.0 if s.get("icon_draw", 0.75) else 1.0)
            ii = add(["-framerate", str(FPS), "-i", f"{ipath}/%04d.png"])
            ix, iy = s.get("icon_pos", (745, 300))
            fc.append(f"[{last}][{ii}:v]overlay={ix}:{iy}:eof_action=repeat[ic{i}]"); last = f"ic{i}"
        if s.get("meter"):
            mpath = f"{AS}/meter_{i}"; mt = s["meter"]; AN.meter_sequence(mpath, th, d, mt.get("t0", 0.2), mt.get("t1", 1.0), mt.get("label", "תודה"))
            mi = add(["-framerate", str(FPS), "-i", f"{mpath}/%04d.png"])
            mx, my = mt.get("pos", (770, 250))
            fc.append(f"[{mi}:v]format=rgba,fade=t=in:st=0:d=0.2:alpha=1[mtf{i}];[{last}][mtf{i}]overlay={mx}:{my}:eof_action=repeat[mt{i}]"); last = f"mt{i}"
        return last
    if lay in ("stage", "burst", "focus"):
        bgp = f"{AS}/bg_{i}.png"; A.stage_bg(bgp, th, s.get("wm"))
        rays = None
        if lay == "burst": rays = f"{AS}/rays_{th}.png"; A.rays(rays, th)
        last = stage(bgp, rays)
        if lay == "burst":
            fc.append(f"[{last}]curves=all='0/0 0.5/0.56 1/1',eq=brightness=0.03[bu{i}]"); last = f"bu{i}"
        if lay == "focus":
            A.focus_text(f"{AS}/focus_{i}.png", s["small"], s["big"], th)
            it = add(loop(f"{AS}/focus_{i}.png", d))
            fc.append(f"[{last}]gblur=sigma=24,eq=brightness=-0.12[bl{i}];[{it}:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1[ft{i}];[bl{i}][ft{i}]overlay=0:0[fo{i}]")
            last = f"fo{i}"
    elif lay == "quote":
        A.quote_card(f"{AS}/quote_{i}.png", s["lines"], th)
        iq = add(loop(f"{AS}/quote_{i}.png", d))
        fc.append(f"[{iq}:v]scale=w='{W}*(1+0.035*t/{d:.3f})':h=-2:eval=frame,crop={W}:{H}:(iw-{W})/2:(ih-{H})/2,fade=t=in:st=0:d=0.2[qq{i}]"); last = f"qq{i}"
    elif lay == "endcard":
        AN.endcard(f"{AS}/end_{i}.png", s["big"], s["small"], th, s.get("sub"))
        dt_ = d + s.get("tail", 0)
        iq = add(loop(f"{AS}/end_{i}.png", dt_))
        fc.append(f"[{iq}:v]scale=w='{W}*(1+0.04*t/{dt_:.3f})':h=-2:eval=frame,crop={W}:{H}:(iw-{W})/2:(ih-{H})/2,fade=t=in:st=0:d=0.2[qq{i}]"); last = f"qq{i}"
    elif lay == "anim":
        ap = f"{AS}/anim_{i}.mp4"; AN.render(s["scene"], d, s.get("ev", {}), ap)
        ia = add(["-i", ap]); last = f"{ia}:v"
        if s.get("avatar", True):
            asz = s.get("avatar_size", 320)
            A.circle_mask(f"{AS}/circle{asz}.png", asz); A.avatar_ring(f"{AS}/ring{asz}.png", asz)
            sq = SQ; ax = int(min(max(cx - sq / 2, 0), SW - sq)); ay = int(min(max(cy - sq * 0.48, 0), SH - sq))
            imk = add(loop(f"{AS}/circle{asz}.png", d)); irg = add(loop(f"{AS}/ring{asz}.png", d))
            px, py = s.get("avatar_pos", (1080 - asz - 40, 165))
            fc.append(f"[0:v]setpts=PTS-STARTPTS,crop={sq}:{sq}:{ax}:{ay},scale={asz}:{asz}:flags=lanczos,unsharp=5:5:0.6,format=rgba[av{i}];[{imk}:v]format=gray[cm{i}];[av{i}][cm{i}]alphamerge[avm{i}]")
            fc.append(f"[{last}][avm{i}]overlay={px}:{py}[an0{i}];[an0{i}][{irg}:v]overlay={px - 20}:{py - 20}[an1{i}]"); last = f"an1{i}"
    elif lay == "cards":
        ib = add(loop(f"{AS}/beige.png", d))
        # live avatar in a gold ring (circle crop around the face)
        sq = SQ; ax = int(min(max(cx - sq / 2, 0), SW - sq)); ay = int(min(max(cy - sq * 0.48, 0), SH - sq))
        imk = add(loop(f"{AS}/circle300.png", d)); irg = add(loop(f"{AS}/ring300.png", d))
        fc.append(f"[0:v]setpts=PTS-STARTPTS,crop={sq}:{sq}:{ax}:{ay},scale=300:300:flags=lanczos,unsharp=5:5:0.5,format=rgba[av{i}];[{imk}:v]format=gray[cm{i}];[av{i}][cm{i}]alphamerge[avm{i}]")
        fc.append(f"[{ib}:v][avm{i}]overlay=390:170[c0{i}];[c0{i}][{irg}:v]overlay=370:150[c1{i}]")
        last = f"c1{i}"
        cols = {"1": (124, 92, 230), "2": (30, 150, 130)}
        for k, (num, title, sub, icon) in enumerate(C.CARDS):
            if num in s.get("hidden", []): continue
            active = (s["active"] == num)
            p = f"{AS}/card_{num}_{int(active)}.png"; A.compare_card(p, num, title, sub, icon, cols[num], active)
            ic = add(loop(p, d))
            x = 575 if num == "1" else 65
            appear = s.get("appear", {}).get(num)
            if appear is not None:
                fc.append(f"[{ic}:v]format=rgba,fade=t=in:st={appear}:d=0.3:alpha=1[cd{i}{k}]")
                yexpr = f"if(lt(t\\,{appear})\\,700\\,if(lt(t\\,{appear}+0.3)\\,700-70*(t-{appear})/0.3\\,630))"
                fc.append(f"[{last}][cd{i}{k}]overlay=x={x}:y='{yexpr}'[cc{i}{k}]")
            else:
                fc.append(f"[{last}][{ic}:v]overlay={x}:630[cc{i}{k}]")
            last = f"cc{i}{k}"
    if s.get("hud"):
        hl, hlab, hp = s["hud"][:3]; hcol = s["hud"][3] if len(s["hud"]) > 3 else A.THEMES[th][2]
        AN.hud_png(f"{AS}/hud_{i}.png", hl, hlab, hp, hcol, A.THEMES[th][2])
        ih = add(loop(f"{AS}/hud_{i}.png", d))
        fin = ",fade=t=in:st=0:d=0.3:alpha=1" if s.get("hud_in") else ""
        fc.append(f"[{ih}:v]format=rgba{fin}[hd{i}];[{last}][hd{i}]overlay=0:0[hdo{i}]"); last = f"hdo{i}"
    if s.get("hook"):
        A.hook_pill(f"{AS}/hook_{i}.png", s["hook"][0], s["hook"][1], th)
        ih = add(loop(f"{AS}/hook_{i}.png", d))
        hend = min(d, s.get("hook_end", 3.2))
        fin = "fade=t=in:st=0.05:d=0.3:alpha=1," if s.get("hook_in", True) else ""
        fout = f"fade=t=out:st={hend - 0.3:.2f}:d=0.3:alpha=1," if s.get("hook_out", True) else ""
        fc.append(f"[{ih}:v]format=rgba,{fin}{fout}null[hk{i}];[{last}][hk{i}]overlay=0:0[hh{i}]"); last = f"hh{i}"
    key = (lay, th)
    if i > 0 and key != prev:
        fc.append(f"[{last}]scale=w='{W}*(1+0.05*max(0\\,1-t/0.22))':h=-2:eval=frame,crop={W}:{H}:(iw-{W})/2:(ih-{H})/2[pp{i}]"); last = f"pp{i}"
        if s.get("flash", lay in ("quote", "burst", "endcard")):
            fc.append(f"[{last}]fade=t=in:st=0:d=0.16:color=white[fl{i}]"); last = f"fl{i}"
    fc.append(f"[{last}]fps={FPS},format=yuv420p,setsar=1[v]")
    fc.append(f"[0:a]aresample=48000,volume={gdb}dB,afade=t=in:d=0.012,afade=t=out:st={d - 0.015:.3f}:d=0.015,apad=pad_dur={s.get('tail', 0) if lay == 'endcard' else 0}[aa]")
    o = f"{CL}/s{i:02d}.mkv"
    if os.environ.get("SKIP_SEGS") and os.path.exists(o):
        files.append(o); prev = key; continue
    r = subprocess.run(["ffmpeg", "-y", "-v", "error"] + inputs + ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[aa]", "-t", f"{d + (s.get('tail', 0) if lay == 'endcard' else 0):.3f}",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", o], capture_output=True, text=True)
    if r.returncode: print(";".join(fc)); print(r.stderr[-2000:]); sys.exit(1)
    files.append(o); prev = key
    print("seg", i, lay, th, round(d, 2), "gain", gdb, flush=True)

durs = [float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", f], capture_output=True, text=True).stdout) for f in files]
offs = [0.0]
for dd in durs[:-1]: offs.append(offs[-1] + dd)
TOTAL = sum(durs)

# ---------------- captions ----------------
def bgr(rgb): return f"&H00{rgb[2]:02X}{rgb[1]:02X}{rgb[0]:02X}&"
STOP = {"ואתה", "שאתה", "ואז", "הזה", "שלך", "כמו", "שלי", "או", "עד", "בין", "אחרי", "איזה", "משהו", "שזה", "זאת", "אז", "אותך", "אותי", "שלנו", "להיות", "היה", "יכול", "צריך", "בשביל", "איתך", "איתו", "ממך", "לך", "אנחנו", "הם", "מי", "שם", "פה", "כך", "עוד", "כבר", "ועם", "אל", "את", "של", "על", "זה", "אני", "הוא", "היא", "אם", "לא", "כי", "גם", "כן", "לי", "לו", "אבל", "מה", "אתה", "עם", "כל", "יש", "רק", "הנה"}
def ts(x): x = max(0, x); return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"
def clean(t): return t.strip().rstrip(".,")
ev = []
for i, s in enumerate(SEG):
    if s["layout"] in ("focus", "quote", "endcard") or s.get("nocap"): continue
    a, b = s["a"], s["b"]; th = s.get("theme", "navy"); acc = A.THEMES[th][2]
    ws = [(s.get("fix", {}).get(w["text"], w["text"]), w["src_start_ms"] / 1000) for w in words if a - 0.02 <= w["src_start_ms"] / 1000 < b - 0.05]
    ws = [w for w in ws if w[0] != ""]
    cards = s["layout"] == "cards"
    auto = not s.get("splits")
    if auto:                      # greedy pages: break on punctuation, <= 4 words, <= 20 chars
        splits = []; n = 0; ln = 0
        for j, (t, _) in enumerate(ws):
            if n and (n >= 4 or ln + 1 + len(t) > 20): splits.append(n); n = 0; ln = 0
            n += 1; ln += len(t) + (1 if ln else 0)
            if t[-1] in ".,?!" and n >= 2: splits.append(n); n = 0; ln = 0
        if n: splits.append(n)
        if len(splits) > 1 and splits[-1] == 1 and splits[-2] <= 3: splits[-2:] = [splits[-2] + 1]
    else: splits = s["splits"]
    assert sum(splits) == len(ws), (i, splits, [t for t, _ in ws])
    modes = s.get("modes") or ["cstack" if cards else "line"] * len(splits)
    keys = s.get("keys", [])
    KW = s.get("kw", getattr(C, "KW", ()))
    y = s.get("cap_y", 1500 if cards or s["layout"] == "anim" else 1440)
    k0 = 0
    for pi, n in enumerate(splits):
        page = ws[k0:k0 + n]; k0 += n
        if pi < len(keys) and keys[pi] is not None: k = keys[pi]
        else:
            cand = [((100 if clean(t).rstrip("?!") in KW else 0) + (len(clean(t)) if clean(t).rstrip("?!") not in STOP else 0), -j) for j, (t, _) in enumerate(page)]; k = -max(cand)[1]
        st = offs[i] + max(0, page[0][1] - a - 0.05)
        nxt = ws[k0][1] if k0 < len(ws) else b
        en = offs[i] + min(b, nxt) - a - 0.03
        mode = modes[pi]
        if auto and not s.get("modes") and not cards:
            if k == len(page) - 1 and len(page) <= 3 and pi - s.get("_ls", -9) >= 2 and len(clean(page[k][0])) >= 3 and (len(clean(page[k][0])) <= 7): mode = "stack"; s["_ls"] = pi
        def rev(tt, a3="&H50&"):
            dt = int(max(0, (offs[i] + tt - a) - st) * 1000)
            return f"\\1a&HFF&\\3a&HFF&\\t({dt},{dt + 130},\\1a&H00&\\3a{a3})"
        def txt(j, t): return clean(t) if j == len(page) - 1 or j == k else t.rstrip(".")
        if mode == "line":
            parts = []
            for j, (t, tt) in enumerate(page):
                if j == k: parts.append(f"{{{rev(tt)}\\c{bgr(acc)}\\u1}}{txt(j, t)}{{\\c&H00FFFFFF&\\u0}}")
                else: parts.append(f"{{{rev(tt)}}}{txt(j, t)}")
            body = "{\\fnHeebo Bold\\fs86\\blur6}" + " ".join(parts)
        elif mode in ("stack", "hero"):
            pre = " ".join(f"{{{rev(tt)}}}{txt(j, t)}" for j, (t, tt) in enumerate(page) if j < k)
            post = " ".join(f"{{{rev(tt)}}}{txt(j, t)}" for j, (t, tt) in enumerate(page) if j > k)
            t, tt = page[k]
            big = (f"{{\\fnHeebo Black\\fs{s.get('big', 152)}\\c{bgr(acc)}\\3c{bgr(acc)}\\bord6\\blur14{rev(tt, '&H40&')}"
                   f"\\fscx120\\fscy120\\t(0,160,\\fscx100\\fscy100)}}{txt(k, t)}")
            sfmt = "{\\fnHeebo Medium\\fs68\\blur5\\c&H00FFFFFF&\\3c&H00000000&\\bord4\\fscx100\\fscy100}" if mode == "stack" else "{\\fnHeebo Medium\\fs62\\blur5\\bord4\\c&H00FFFFFF&\\3c&H00000000&\\fscx100\\fscy100}"
            body = (sfmt + pre + "\\N" if pre else "") + big + ("\\N" + sfmt + post if post else "")
        elif mode == "cstack":
            def cw(j, t, tt):
                d0 = int(max(0, (offs[i] + tt - a) - st) * 1000)
                return f"{{\\1a&HFF&\\t({d0},{d0 + 130},\\1a&H00&)}}{txt(j, t)}"
            pre = " ".join(cw(j, t, tt) for j, (t, tt) in enumerate(page) if j < k)
            post = " ".join(cw(j, t, tt) for j, (t, tt) in enumerate(page) if j > k)
            t, tt = page[k]; dt = int(max(0, (offs[i] + tt - a) - st) * 1000)
            big = f"{{\\fnHeebo Black\\fs124\\c&H00126A9A&\\1a&HFF&\\t({dt},{dt + 130},\\1a&H00&)\\fscx115\\fscy115\\t({dt},{dt + 160},\\fscx100\\fscy100)}}{txt(k, t)}"
            sfmt = "{\\fnHeebo Medium\\fs62\\c&H00333333&\\fscx100\\fscy100}"
            body = (sfmt + pre + "\\N" if pre else "") + big + ("\\N" + sfmt + post if post else "")
        style = "CapDark" if mode == "cstack" else "Cap"
        ev.append(f"Dialogue: 2,{ts(st)},{ts(en)},{style},,0,0,0,,{{\\an5\\pos(540,{y})\\fad(0,80)}}{body}")
ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Heebo Bold,76,&H00FFFFFF,&H00FFFFFF,&H50000000,&H80000000,0,0,0,0,100,100,0,0,1,5,0,5,60,60,0,-1
Style: CapDark,Heebo Medium,62,&H00333333,&H00333333,&H00FFFFFF,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,60,60,0,-1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n"
open(f"{RW}/caps3.ass", "w").write(ass)
json.dump({"offs": offs, "total": TOTAL}, open(f"{RW}/offs3.json", "w"))

open(f"{CL}/list.txt", "w").write("".join(f"file '{f}'\n" for f in files))
fc = (f"[0:v]ass={RW}/caps3.ass:fontsdir=/home/claude/reel_work/fonts:shaping=complex,fade=t=out:st={TOTAL - 0.45:.2f}:d=0.45,format=yuv420p[vout];"
      f"[0:a]aresample=48000,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=180:makeup=2,afade=t=out:st={TOTAL - 0.5:.2f}:d=0.5[aout]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{CL}/list.txt", "-filter_complex", fc,
                "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-c:a", "pcm_s16le", "-ar", "48000", f"{RW}/tmp3.mov"], check=True)
out = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{RW}/tmp3.mov", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
m = json.loads(out[out.rindex("{"):out.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000,volume=0.6dB,alimiter=limit=0.84:level=disabled")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{RW}/tmp3.mov", "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                "-movflags", "+faststart", f"{RW}/out3.mp4"], check=True)
print("done", round(TOTAL, 2))
