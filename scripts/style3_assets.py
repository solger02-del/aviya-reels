# Assets for the merged style ("קצת אחרת – פרימיום"):
# dark colour-themed stage, neon line-art icons that draw on, watermark word, hook pill,
# black quote cards, focus text, beige comparison cards with a live avatar circle, glow rays.
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
import numpy as np, math, os

W, H = 1080, 1920
FONTS = "/home/claude/reel_work/fonts"
THEMES = {  # bg dark, glow, accent (RGB)
    "navy":   ((8, 13, 30), (38, 68, 140), (95, 175, 255)),
    "warm":   ((22, 13, 6), (130, 74, 18), (255, 183, 77)),
    "teal":   ((5, 22, 22), (18, 108, 92), (64, 224, 180)),
    "purple": ((16, 10, 34), (78, 48, 160), (176, 148, 255)),
    "rose":   ((28, 9, 18), (140, 40, 80), (255, 128, 176)),
}

def font(weight, size):
    return ImageFont.truetype(f"{FONTS}/Heebo-{weight}.ttf", size, layout_engine=ImageFont.Layout.RAQM)

def rtl(d, xy, text, f, fill, anchor="mm"):
    d.text(xy, text, font=f, fill=fill, anchor=anchor, direction="rtl", language="he")

# ---------------- backgrounds ----------------
def stage_bg(path, theme, watermark=None, wm_y=150):
    bg, glow, acc = THEMES[theme]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - 700) / (H * 0.55)) ** 2)
    g = np.clip(1 - r, 0, 1)[..., None] ** 1.6
    img = np.array(bg, np.float32)[None, None, :] * (1 - g) + np.array(glow, np.float32)[None, None, :] * g
    v = 1 - 0.55 * (((xx - W / 2) / (W / 2)) ** 2 * 0.5 + ((yy - H * 0.5) / (H / 2)) ** 2 * 0.35)
    img *= np.clip(v, 0.3, 1)[..., None]
    im = Image.fromarray(img.clip(0, 255).astype(np.uint8)).convert("RGBA")
    # faint UI grid lines (like the tech reference)
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(grid)
    for x in range(0, W, 90): gd.line([(x, 0), (x, H)], fill=acc + (10,), width=1)
    for y in range(0, H, 90): gd.line([(0, y), (W, y)], fill=acc + (10,), width=1)
    im.alpha_composite(grid)
    if watermark:
        wm = Image.new("RGBA", (W, H), (0, 0, 0, 0)); wd = ImageDraw.Draw(wm)
        f = font("Black", 290 if len(watermark) <= 5 else int(290 * 5 / len(watermark)))
        rtl(wd, (W / 2, wm_y), watermark, f, acc + (42,), anchor="mt")
        im.alpha_composite(wm.filter(ImageFilter.GaussianBlur(1.2)))
    im.convert("RGB").save(path)

def feather_mask(path, w=1080, h=1350, top=220, bottom=300, side=90):
    y = np.linspace(0, h - 1, h)[:, None]; x = np.linspace(0, w - 1, w)[None, :]
    a = np.minimum(np.clip(y / top, 0, 1), np.clip((h - 1 - y) / bottom, 0, 1))
    s = np.minimum(np.clip(x / side, 0, 1), np.clip((w - 1 - x) / side, 0, 1))
    a = a * (0.55 + 0.45 * s)
    Image.fromarray((a ** 1.2 * 255).astype(np.uint8)).save(path)

def black_bg(path):
    Image.new("RGB", (W, H), (6, 6, 8)).save(path)

def beige_bg(path):
    y = np.linspace(0, 1, H)[:, None, None]
    img = (np.array([241, 236, 228])[None, None, :] * (1 - 0.06 * y)) * np.ones((1, W, 1))
    Image.fromarray(img.astype(np.uint8)).save(path)

# ---------------- line-art icon library (unit square, y down) ----------------
def _arc(cx, cy, r, a0, a1, n=40):
    return [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in np.linspace(a0, a1, n)]
def _heart(cx, cy, s, n=80):
    pts = []
    for t in np.linspace(0, 2 * math.pi, n):
        x = 16 * math.sin(t) ** 3; y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x / 34 * s, cy - y / 34 * s))
    return pts
def _figure(cx, top, h):
    hr = h * 0.12
    return [_arc(cx, top + hr, hr, 0, 360), [(cx, top + 2 * hr), (cx, top + h * 0.62)],
            [(cx, top + h * 0.62), (cx - h * 0.14, top + h)], [(cx, top + h * 0.62), (cx + h * 0.14, top + h)],
            [(cx - h * 0.18, top + h * 0.42), (cx, top + h * 0.3), (cx + h * 0.18, top + h * 0.42)]]
def _ell(cx, cy, rx, ry, n=50):
    return [(cx + rx * math.cos(t), cy + ry * math.sin(t)) for t in np.linspace(0, 2 * math.pi, n)]
ICONS = {
    "paw": lambda: [_ell(0.5, 0.66, 0.2, 0.16)] + [_ell(x, y, 0.075, 0.095, 30) for x, y in [(0.25, 0.42), (0.4, 0.27), (0.6, 0.27), (0.75, 0.42)]],
    "stroller": lambda: [[(0.12, 0.46)] + _arc(0.42, 0.46, 0.3, 180, 270) + [(0.42, 0.46), (0.12, 0.46)],
                         [(0.12, 0.46), (0.18, 0.64), (0.72, 0.64), (0.78, 0.46), (0.42, 0.46)], [(0.78, 0.46), (0.9, 0.2)],
                         _arc(0.26, 0.8, 0.08, 0, 360), _arc(0.64, 0.8, 0.08, 0, 360)],
    "fingerprint": lambda: [_arc(0.5, 0.56, r, 150 + k * 8, 390 - k * 6, 40) for k, r in enumerate([0.06, 0.13, 0.2, 0.27, 0.34, 0.41])],
    "heart": lambda: [_heart(0.5, 0.52, 0.85)],
    "moon": lambda: [_arc(0.48, 0.52, 0.32, 70, 290, 60) + _arc(0.6, 0.44, 0.26, 265, 95, 60)[::-1][::-1],
                     [(0.8, 0.16), (0.8, 0.3)], [(0.73, 0.23), (0.87, 0.23)], [(0.88, 0.48), (0.88, 0.56)], [(0.84, 0.52), (0.92, 0.52)]],
    "stones": lambda: [_ell(0.3, 0.72, 0.17, 0.1), _ell(0.66, 0.74, 0.2, 0.11), _ell(0.48, 0.55, 0.15, 0.09)],
    "staff": lambda: [[(0.55, 0.78), (0.5, 0.3)] + _arc(0.42, 0.3, 0.08, 0, -180, 30) + [(0.34, 0.37)],
                      [(0.12 + 0.76 * k / 30, 0.86 + 0.03 * math.sin(k / 30 * 4 * math.pi)) for k in range(31)],
                      [(0.2 + 0.6 * k / 24, 0.94 + 0.025 * math.sin(k / 24 * 3 * math.pi)) for k in range(25)]],
    "bank": lambda: [[(0.12, 0.38), (0.5, 0.14), (0.88, 0.38), (0.12, 0.38)], [(0.24, 0.44), (0.24, 0.8)], [(0.41, 0.44), (0.41, 0.8)],
                     [(0.59, 0.44), (0.59, 0.8)], [(0.76, 0.44), (0.76, 0.8)], [(0.14, 0.84), (0.86, 0.84)], [(0.1, 0.9), (0.9, 0.9)]],
    "bubble_heart": lambda: [[(0.12, 0.18), (0.88, 0.18), (0.88, 0.66), (0.42, 0.66), (0.26, 0.84), (0.28, 0.66), (0.12, 0.66), (0.12, 0.18)],
                             _heart(0.5, 0.43, 0.36)],
    "couple": lambda: _figure(0.34, 0.3, 0.62) + _figure(0.66, 0.3, 0.62) + [[(0.43, 0.6), (0.57, 0.6)], _heart(0.5, 0.15, 0.2)],
    "lightning": lambda: [_arc(0.36, 0.34, 0.14, 150, 300) + _arc(0.56, 0.26, 0.17, 210, 360) + _arc(0.72, 0.38, 0.12, 270, 450) + [(0.3, 0.5)],
                          [(0.56, 0.5), (0.44, 0.7), (0.56, 0.7), (0.44, 0.92)]],
    "arrow_up": lambda: [[(0.5, 0.88), (0.5, 0.14)], [(0.3, 0.34), (0.5, 0.14), (0.7, 0.34)], [(0.2, 0.62), (0.2, 0.72)], [(0.15, 0.67), (0.25, 0.67)],
                         [(0.82, 0.48), (0.82, 0.58)], [(0.77, 0.53), (0.87, 0.53)]],
    "check_circle": lambda: [_arc(0.5, 0.5, 0.38, -90, 270, 70), [(0.32, 0.52), (0.45, 0.65), (0.7, 0.37)]],
    "graph_up": lambda: [[(0.12, 0.12), (0.12, 0.88), (0.9, 0.88)], [(0.18, 0.78), (0.36, 0.62), (0.5, 0.7), (0.68, 0.42), (0.86, 0.2)],
                         [(0.72, 0.2), (0.86, 0.2), (0.86, 0.34)]],
    "house_heart": lambda: [[(0.14, 0.5), (0.5, 0.16), (0.86, 0.5)], [(0.24, 0.42), (0.24, 0.88), (0.76, 0.88), (0.76, 0.42)], _heart(0.5, 0.62, 0.3)],
    "gift": lambda: [[(0.16, 0.42), (0.84, 0.42), (0.84, 0.88), (0.16, 0.88), (0.16, 0.42)], [(0.5, 0.42), (0.5, 0.88)],
                     [(0.12, 0.3), (0.88, 0.3), (0.88, 0.42), (0.12, 0.42), (0.12, 0.3)], _arc(0.4, 0.22, 0.1, 0, 300), _arc(0.6, 0.22, 0.1, 240, 540)],
}

def _len(poly): return sum(math.dist(poly[i], poly[i + 1]) for i in range(len(poly) - 1))

def draw_icon(icon, size, p, acc, core=(255, 255, 255), lw=7, ss=3):
    """Icon drawn to progress p (0..1) along its total stroke length, with neon glow."""
    strokes = ICONS[icon]() if isinstance(icon, str) else icon
    total = sum(_len(s) for s in strokes); target = p * total
    S = size * ss; pad = 0.06
    def P(pt): return ((pad + pt[0] * (1 - 2 * pad)) * S, (pad + pt[1] * (1 - 2 * pad)) * S)
    layer = Image.new("L", (S, S), 0); d = ImageDraw.Draw(layer); done = 0.0
    for s in strokes:
        L = _len(s)
        if done >= target: break
        if done + L <= target: pts = s
        else:
            rem = target - done; pts = [s[0]]
            for i in range(len(s) - 1):
                seg = math.dist(s[i], s[i + 1])
                if rem <= seg:
                    t = rem / seg if seg else 0; pts.append((s[i][0] + (s[i + 1][0] - s[i][0]) * t, s[i][1] + (s[i + 1][1] - s[i][1]) * t)); break
                pts.append(s[i + 1]); rem -= seg
        if len(pts) >= 2:
            d.line([P(q) for q in pts], fill=255, width=lw * ss, joint="curve")
            for q in (pts[0], pts[-1]):
                x, y = P(q); r = lw * ss / 2; d.ellipse([x - r, y - r, x + r, y + r], fill=255)
        done += L
    layer = layer.resize((size, size), Image.LANCZOS)
    glow = layer.filter(ImageFilter.GaussianBlur(9)); glow2 = layer.filter(ImageFilter.GaussianBlur(3))
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    g = Image.new("RGBA", (size, size), acc + (0,)); g.putalpha(glow.point(lambda v: min(255, int(v * 1.6))))
    out.alpha_composite(g)
    g2 = Image.new("RGBA", (size, size), acc + (0,)); g2.putalpha(glow2); out.alpha_composite(g2)
    c = Image.new("RGBA", (size, size), tuple(int(core[i] * 0.75 + acc[i] * 0.25) for i in range(3)) + (0,)); c.putalpha(layer)
    out.alpha_composite(c)
    return out

def icon_sequence(outdir, icon, theme, dur, size=300, draw_time=0.75, fps=30, t_offset=0.0):
    os.makedirs(outdir, exist_ok=True)
    acc = THEMES[theme][2]; n = max(1, int(round(dur * fps)))
    full = None
    for i in range(n):
        t = i / fps + t_offset
        if draw_time > 0 and t < draw_time:
            im = draw_icon(icon, size, (t / draw_time) ** 0.8, acc)
        else:
            if full is None: full = draw_icon(icon, size, 1.0, acc)
            pulse = 0.88 + 0.12 * math.sin((t - draw_time) * 3.0)
            im = full.copy(); a = im.getchannel("A").point(lambda v: int(v * pulse)); im.putalpha(a)
        im.save(f"{outdir}/{i:04d}.png")
    return n

# ---------------- overlays ----------------
def hook_pill(path, small, pill, theme):
    acc = THEMES[theme][2]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    rtl(d, (W / 2, 110), small, font("Medium", 56), (235, 235, 240, 255))
    f = font("Bold", 92); bb = d.textbbox((0, 0), pill, font=f, direction="rtl", language="he"); tw = bb[2] - bb[0]
    x0, x1 = W / 2 - tw / 2 - 48, W / 2 + tw / 2 + 48; y0, y1 = 158, 290
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([x0, y0 + 8, x1, y1 + 8], radius=34, fill=(0, 0, 0, 120))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    d.rounded_rectangle([x0, y0, x1, y1], radius=34, fill=(232, 236, 245, 235), outline=acc + (255,), width=3)
    rtl(d, (W / 2, (y0 + y1) / 2 + 2), pill, f, (24, 30, 48, 255))
    img.save(path)

def quote_card(path, lines, theme, quote=True):
    acc = THEMES[theme][2]
    img = Image.new("RGB", (W, H), (6, 6, 8)); d = ImageDraw.Draw(img)
    y = 860 - len(lines) * 70
    if quote:
        rtl(d, (W / 2, y - 110), "״", font("Black", 190), acc)
    for i, ln in enumerate(lines):
        sz = 104 if i == 0 else 78
        while True:
            f = font("Bold" if i == 0 else "Light", sz)
            bb = d.textbbox((0, 0), ln, font=f, direction="rtl", language="he")
            if bb[2] - bb[0] <= 930 or sz < 50: break
            sz -= 4
        rtl(d, (W / 2, y), ln, f, (245, 245, 245) if i == 0 else (200, 200, 205)); y += 140
    img.save(path)

def focus_text(path, small, big, theme):
    acc = THEMES[theme][2]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    rtl(d, (W / 2, 790), small, font("Light", 66), (255, 255, 255, 235))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    rtl(gd, (W / 2, 925), big, font("Bold", 150), acc + (255,))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(16)))
    rtl(d, (W / 2, 925), big, font("Bold", 150), (255, 255, 255, 255))
    d.line([(W / 2 - 150, 1060), (W / 2 + 150, 1060)], fill=acc + (255,), width=5)
    img.save(path)

def rays(path, theme, size=1500, n=28):
    acc = THEMES[theme][2]
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(img); c = size / 2
    for k in range(n):
        a0 = 2 * math.pi * k / n; w = 0.045
        pts = [(c, c), (c + size * math.cos(a0 - w), c + size * math.sin(a0 - w)), (c + size * math.cos(a0 + w), c + size * math.sin(a0 + w))]
        d.polygon(pts, fill=acc + (70,))
    yy, xx = np.mgrid[0:size, 0:size]; r = np.sqrt((xx - c) ** 2 + (yy - c) ** 2) / c
    fade = np.clip(1.15 - r, 0, 1) ** 1.3
    a = (np.asarray(img.getchannel("A")).astype(np.float32) * fade).astype(np.uint8)
    core = np.clip(1 - r * 2.2, 0, 1) * 200
    img.putalpha(Image.fromarray(np.maximum(a, core.astype(np.uint8))))
    img.filter(ImageFilter.GaussianBlur(6)).save(path)

# ---------------- comparison cards (bot/secretary reference) ----------------
def circle_mask(path, s):
    m = Image.new("L", (s * 3, s * 3), 0); ImageDraw.Draw(m).ellipse([0, 0, s * 3 - 1, s * 3 - 1], fill=255); m.resize((s, s), Image.LANCZOS).save(path)

def avatar_ring(path, s, color=(201, 160, 72)):
    img = Image.new("RGBA", (s + 40, s + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([20, 28, s + 20, s + 28], fill=(0, 0, 0, 90))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d.ellipse([20 - 7, 20 - 7, s + 20 + 7, s + 20 + 7], outline=color + (255,), width=9)
    inner = Image.new("L", img.size, 0); ImageDraw.Draw(inner).ellipse([20, 20, s + 20, s + 20], fill=255)
    img.putalpha(ImageChops.subtract(img.getchannel("A"), inner)); img.save(path)

def compare_card(path, num, title, sub, icon, color, active):
    w, h = 380, 470; s = 2
    img = Image.new("RGBA", ((w + 60) * s, (h + 60) * s), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([30 * s, 42 * s, (30 + w) * s, (42 + h) * s], radius=34 * s, fill=(0, 0, 0, 70 if active else 30))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16 * s)))
    d = ImageDraw.Draw(img)
    fill = (252, 251, 249, 255) if active else (246, 244, 240, 200)
    d.rounded_rectangle([30 * s, 30 * s, (30 + w) * s, (30 + h) * s], radius=34 * s, fill=fill, outline=color + ((255,) if active else (120,)), width=(5 if active else 3) * s)
    cx = (30 + w / 2) * s
    d.ellipse([cx - 34 * s, 62 * s, cx + 34 * s, 130 * s], fill=color + ((255,) if active else (140,)))
    rtl(d, (cx, 96 * s), num, font("Bold", 44 * s), (255, 255, 255, 255))
    ic = draw_icon(icon, 150 * s, 1.0, color, core=color, lw=8)
    if not active: ic.putalpha(ic.getchannel("A").point(lambda v: int(v * 0.5)))
    img.alpha_composite(ic, (int(cx - 75 * s), int(150 * s)))
    rtl(d, (cx, 365 * s), title, font("Bold", 52 * s), (40, 40, 46, 255) if active else (120, 120, 126, 255))
    rtl(d, (cx, 422 * s), sub, font("Regular", 44 * s), (90, 90, 96, 255) if active else (150, 150, 156, 255))
    img.resize((w + 60, h + 60), Image.LANCZOS).save(path)
