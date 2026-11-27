# Flat 2D animated inserts for the merged reel style (own characters, inspired by minimal explainer animation).
# Cairo draws the vector scene, PIL adds Hebrew labels (raqm). Each scene is a function of local time t.
import math, os, sys, random, subprocess
import numpy as np, cairo
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude/reel_scripts")
import style3_assets as A

W, H, FPS = 1080, 1920, 30
SKIN = (250, 244, 236); OUT = (28, 30, 54); HAIR = (62, 44, 34); BEARD = (84, 59, 42)
ROBE = (222, 148, 60); ROBE_D = (176, 108, 40); LEG = (242, 236, 226); STAFF = (128, 88, 54)
LOOK = {"beard": True, "robe": ROBE, "robe_d": ROBE_D}
STONE = (98, 106, 134); STONE_HI = (150, 160, 190)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def smooth(x): x = clamp(x); return x * x * (3 - 2 * x)
def back(x):
    x = clamp(x); c1 = 1.9; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def pop(t, t0, d=0.32): return 0.0 if t < t0 else back((t - t0) / d)
def col(ctx, rgb, a=1.0): ctx.set_source_rgba(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, a)
def mix(c1, c2, k): return tuple(int(c1[i] + (c2[i] - c1[i]) * k) for i in range(3))

# ---------------- background ----------------
def night_bg(theme, moon=(260, 420), ground=None, seed=3):
    bg, glow, acc = A.THEMES[theme]
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    col(c, bg); c.paint()
    g = cairo.RadialGradient(540, 820, 50, 540, 820, 1150)
    g.add_color_stop_rgba(0, *(v / 255 for v in mix(bg, glow, 0.55)), 1); g.add_color_stop_rgba(1, *(v / 255 for v in bg), 1)
    c.set_source(g); c.paint()
    if moon:
        mx, my = moon
        g = cairo.RadialGradient(mx, my, 60, mx, my, 220)
        g.add_color_stop_rgba(0, 1, 0.96, 0.85, 0.18); g.add_color_stop_rgba(1, 1, 0.96, 0.85, 0)
        c.set_source(g); c.paint()
        # crescent: full disc, then cut a disc out of it on its own layer
        m = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); mc = cairo.Context(m)
        mc.arc(mx, my, 74, 0, 2 * math.pi); mc.set_source_rgba(1, 0.96, 0.86, 1); mc.fill()
        mc.set_operator(cairo.OPERATOR_CLEAR); mc.arc(mx + 34, my - 22, 66, 0, 2 * math.pi); mc.fill()
        c.set_source_surface(m); c.paint()
    if ground: ground(c)
    # vignette
    g = cairo.RadialGradient(540, 900, 600, 540, 900, 1350)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.55)
    c.set_source(g); c.paint()
    rnd = random.Random(seed)
    stars = [(rnd.uniform(40, 1040), rnd.uniform(120, 980), rnd.uniform(1.6, 3.6), rnd.uniform(0, 6.3)) for _ in range(70)]
    return s, stars

def draw_stars(c, stars, t):
    for x, y, r, ph in stars:
        a = 0.25 + 0.6 * (0.5 + 0.5 * math.sin(t * 2.2 + ph))
        c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, a); c.fill()

def flat_ground(y, theme):
    bg, glow, acc = A.THEMES[theme]
    def f(c):
        c.rectangle(0, y, W, H - y)
        g = cairo.LinearGradient(0, y, 0, H); g.add_color_stop_rgba(0, *(v / 255 for v in mix(bg, glow, 0.38)), 1)
        g.add_color_stop_rgba(1, *(v / 255 for v in mix(bg, (0, 0, 0), 0.3)), 1); c.set_source(g); c.fill()
        c.move_to(0, y); c.line_to(W, y); col(c, mix(glow, (255, 255, 255), 0.25), 0.5); c.set_line_width(4); c.stroke()
    return f

# ---------------- character (our own design: Jacob with beard, amber robe) ----------------
def limb(c, x0, y0, x1, y1, w, fill, out=OUT, ow=6):
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x0, y0); c.line_to(x1, y1); col(c, out); c.set_line_width(w + 2 * ow); c.stroke()
    c.move_to(x0, y0); c.line_to(x1, y1); col(c, fill); c.set_line_width(w); c.stroke()

def head(c, x, y, s=1.0, eyes="closed", mouth="smile", tilt=0.0):
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(s, s)
    r = 100
    c.arc(0, 0, r, 0, 2 * math.pi); col(c, SKIN); c.fill()
    # hair cap
    a0, a1 = math.radians(196), math.radians(344)
    c.arc(0, 0, r, a0, a1)
    c.curve_to(70, -40, 30, -58, 0, -50); c.curve_to(-30, -58, -70, -40, r * math.cos(a0), r * math.sin(a0))
    col(c, HAIR); c.fill()
    if LOOK["beard"]:
        # beard (lower band of the face, mouth stays on the skin above it)
        b0, b1 = math.radians(20), math.radians(160)
        c.arc(0, 0, r, b0, b1)
        c.curve_to(-60, 50, -30, 56, 0, 56); c.curve_to(30, 56, 60, 50, r * math.cos(b0), r * math.sin(b0))
        col(c, BEARD); c.fill()
    if not LOOK["beard"]:                      # kippah
        c.arc(0, -52, 60, math.radians(222), math.radians(318)); c.close_path(); col(c, (40, 52, 110)); c.fill_preserve(); col(c, OUT); c.set_line_width(4); c.stroke()
    c.arc(0, 0, r, 0, 2 * math.pi); col(c, OUT); c.set_line_width(7); c.stroke()
    # blush
    for sx in (-1, 1):
        c.save(); c.translate(sx * 58, 8); c.scale(1, 0.62); c.arc(0, 0, 17, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(1, 0.58, 0.62, 0.55); c.fill()
    c.set_line_cap(cairo.LINE_CAP_ROUND); col(c, OUT); c.set_line_width(6.5)
    for sx in (-1, 1):
        ex = sx * 36
        if eyes == "closed":
            c.arc(ex, -18, 15, math.radians(25), math.radians(155)); c.stroke()
        elif eyes == "happy":
            c.arc(ex, -8, 15, math.radians(205), math.radians(335)); c.stroke()
        else:
            c.arc(ex, -16, 9.5, 0, 2 * math.pi); c.fill()
            c.arc(ex + 3, -19, 3, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 0.9); c.fill(); col(c, OUT)
    col(c, OUT)
    if mouth == "smile":
        c.arc(0, 18, 15, math.radians(25), math.radians(155)); c.set_line_width(6); c.stroke()
    elif mouth == "big":
        c.arc(0, 16, 19, 0, math.pi); c.close_path(); c.set_source_rgba(0.5, 0.16, 0.2, 1); c.fill()
    else:
        c.move_to(-11, 28); c.line_to(11, 28); c.set_line_width(6); c.stroke()
    c.restore()

def staff_path(c, x, top, bottom):
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for w, clr in ((26, OUT), (14, STAFF)):
        c.move_to(x + 4, bottom); c.line_to(x, top)
        c.arc_negative(x - 30, top, 30, 0, -math.pi); c.line_to(x - 60, top + 18)
        col(c, clr); c.set_line_width(w); c.stroke()

def body(c, walk=0.0, amp=0.0, staff=False, arms_up=0.0, legs=True, rest=False):
    """standing body in local coords, feet at (0,0), head centre at (0,-575)."""
    hip = -250; man = not LOOK["beard"]      # modern everyday man: shirt + trousers; biblical figure: robe
    if legs:
        for sx, ph in ((-1, 0.0), (1, math.pi)):
            ang = amp * math.sin(walk + ph)
            fx, fy = sx * 24 + 240 * math.sin(ang), hip + 240 * math.cos(ang)
            if man:
                limb(c, sx * 30, hip, fx + sx * 6, fy - 14, 42, (48, 60, 108))
                c.save(); c.translate(fx + sx * 6 - 10, fy - 4); c.scale(1, 0.5); c.arc(0, 0, 36, 0, 2 * math.pi); c.restore(); col(c, (30, 32, 52)); c.fill()
            else: limb(c, sx * 24, hip, fx, fy, 28, LEG)
    if staff: staff_path(c, -128, -690, 0)
    if man:
        c.move_to(-62, -470); c.line_to(-70, -236); c.curve_to(-30, -226, 30, -226, 70, -236); c.line_to(62, -470)
        c.curve_to(30, -488, -30, -488, -62, -470); c.close_path()
        col(c, LOOK["robe"]); c.fill_preserve(); col(c, OUT); c.set_line_width(6); c.stroke()
        c.move_to(-68, -248); c.curve_to(-30, -240, 30, -240, 68, -248); col(c, (30, 32, 52)); c.set_line_width(12); c.stroke()
        c.move_to(0, -480); c.line_to(0, -262); col(c, LOOK["robe_d"]); c.set_line_width(5); c.stroke()
    else:
        # robe
        c.move_to(-60, -470); c.curve_to(-78, -380, -92, -300, -104, -214)
        c.curve_to(-40, -200, 40, -200, 104, -214); c.curve_to(92, -300, 78, -380, 60, -470)
        c.curve_to(30, -488, -30, -488, -60, -470); c.close_path()
        col(c, LOOK["robe"]); c.fill_preserve(); col(c, OUT); c.set_line_width(6); c.stroke()
        c.move_to(-84, -335); c.curve_to(-30, -322, 30, -322, 84, -335); col(c, LOOK["robe_d"]); c.set_line_width(12); c.stroke()
    # arms
    for sx in (-1, 1):
        if staff and sx == -1: hx, hy = -122, -318
        elif rest: hx, hy = sx * 26, -360
        else:
            hx = sx * (108 + 50 * arms_up); hy = -292 - 380 * arms_up
        limb(c, sx * 60, -448, hx, hy, 30, LOOK["robe_d"])
        c.arc(hx, hy, 19, 0, 2 * math.pi); col(c, SKIN); c.fill_preserve(); col(c, OUT); c.set_line_width(5); c.stroke()

def person(c, x, y, s=1.0, eyes="open", mouth="smile", walk=0.0, amp=0.0, staff=False, arms_up=0.0, bob=0.0):
    c.save(); c.translate(x, y + bob); c.scale(s, s)
    body(c, walk, amp, staff, arms_up)
    c.restore()
    head(c, x, y + bob - 575 * s, s, eyes, mouth)

# ---------------- props ----------------
def stone(c, x, y, rx, ry, k=1.0):
    if k <= 0: return
    c.save(); c.translate(x, y - (1 - min(k, 1)) * 70); c.scale(k, k)
    c.save(); c.scale(1, ry / rx); c.arc(0, 0, rx, 0, 2 * math.pi); c.restore()
    col(c, STONE); c.fill_preserve(); col(c, OUT); c.set_line_width(5); c.stroke()
    c.save(); c.scale(1, ry / rx); c.arc(-rx * 0.15, -rx * 0.1, rx * 0.62, math.radians(200), math.radians(280)); c.restore()
    col(c, STONE_HI); c.set_line_width(6); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.restore()

def zee(c, x, y, s, a):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-10, -10); c.line_to(10, -10); c.line_to(-10, 10); c.line_to(10, 10)
    c.set_source_rgba(1, 1, 1, a); c.set_line_width(4.5); c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.restore()

def heart_path(c, x, y, s):
    c.move_to(x, y + 0.35 * s)
    c.curve_to(x - 1.1 * s, y - 0.35 * s, x - 0.5 * s, y - 1.05 * s, x, y - 0.5 * s)
    c.curve_to(x + 0.5 * s, y - 1.05 * s, x + 1.1 * s, y - 0.35 * s, x, y + 0.35 * s); c.close_path()

def tent(c, x, base, k, acc):
    if k <= 0: return
    c.save(); c.translate(x, base); c.scale(k, k)
    c.move_to(-130, 0); c.line_to(0, -230); c.line_to(130, 0); c.close_path()
    col(c, (206, 146, 74)); c.fill_preserve(); col(c, OUT); c.set_line_width(6); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    c.move_to(-44, 0); c.line_to(0, -118); c.line_to(44, 0); c.close_path(); col(c, (60, 36, 22)); c.fill()
    c.move_to(-130, 0); c.line_to(0, -230); col(c, (240, 186, 110)); c.set_line_width(5); c.stroke()
    c.move_to(0, -230); c.line_to(0, -290); col(c, OUT); c.set_line_width(6); c.stroke()
    c.move_to(0, -290); c.line_to(48, -274); c.line_to(0, -258); col(c, acc); c.fill()
    c.restore()

def bank(c, x, base, k, acc):
    if k <= 0: return
    c.save(); c.translate(x, base); c.scale(k, k)
    stonec, shade = (238, 228, 206), (204, 190, 164)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    def box(x0, y0, x1, y1, f=stonec):
        c.rectangle(x0, y0, x1 - x0, y1 - y0); col(c, f); c.fill_preserve(); col(c, OUT); c.set_line_width(5); c.stroke()
    box(-150, -22, 150, 0); box(-132, -42, 132, -22)
    for cx in (-96, -32, 32, 96):
        box(cx - 17, -178, cx + 17, -42, stonec)
        c.rectangle(cx + 5, -176, 10, 132); col(c, shade); c.fill()
    box(-140, -204, 140, -178)
    c.move_to(-150, -204); c.line_to(0, -290); c.line_to(150, -204); c.close_path()
    col(c, stonec); c.fill_preserve(); col(c, OUT); c.set_line_width(5); c.stroke()
    c.arc(0, -236, 19, 0, 2 * math.pi); col(c, acc); c.fill_preserve(); col(c, OUT); c.set_line_width(4); c.stroke()
    c.restore()

def coin(c, x, y, r, a=1.0, spin=0.0):
    c.save(); c.translate(x, y); c.scale(max(0.15, abs(math.cos(spin))), 1)
    c.arc(0, 0, r, 0, 2 * math.pi); c.set_source_rgba(1, 0.78, 0.25, a); c.fill_preserve()
    c.set_source_rgba(0.55, 0.36, 0.05, a); c.set_line_width(4); c.stroke()
    c.arc(0, 0, r * 0.62, 0, 2 * math.pi); c.set_source_rgba(0.85, 0.6, 0.12, a); c.set_line_width(3); c.stroke()
    c.restore()

def sparkle(c, x, y, s, a):
    if s <= 0.05 or a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, -1); c.curve_to(0.1, -0.1, 0.1, -0.1, 1, 0); c.curve_to(0.1, 0.1, 0.1, 0.1, 0, 1)
    c.curve_to(-0.1, 0.1, -0.1, 0.1, -1, 0); c.curve_to(-0.1, -0.1, -0.1, -0.1, 0, -1)
    c.set_source_rgba(1, 0.95, 0.75, a); c.fill(); c.restore()

def dashed_ring(c, x, y, r, k, t, acc):
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(t * 0.8); c.scale(k, k)
    c.arc(0, 0, r, 0, 2 * math.pi); c.set_dash([22, 16]); col(c, acc); c.set_line_width(7); c.stroke(); c.set_dash([])
    c.restore()

# ---------------- Hebrew label pills (PIL) ----------------
_label_cache = {}
def label_img(text, acc, pointer="down"):
    key = (text, acc, pointer)
    if key in _label_cache: return _label_cache[key]
    f = A.font("Bold", 64)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    bb = tmp.textbbox((0, 0), text, font=f, direction="rtl", language="he"); tw = bb[2] - bb[0]
    pw, ph = tw + 84, 104; pad = 40
    im = Image.new("RGBA", (pw + 2 * pad, ph + 2 * pad + 34), (0, 0, 0, 0))
    oy = pad + (34 if pointer == "up" else 0)
    glow = Image.new("RGBA", im.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.rounded_rectangle([pad, oy, pad + pw, oy + ph], radius=ph // 2, outline=acc + (200,), width=10)
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(im)
    cx = pad + pw / 2
    if pointer == "down": tri = [(cx - 20, oy + ph - 3), (cx + 20, oy + ph - 3), (cx, oy + ph + 26)]
    else: tri = [(cx - 20, oy + 3), (cx + 20, oy + 3), (cx, oy - 26)]
    d.polygon(tri, fill=(18, 20, 36, 240), outline=acc + (255,))
    d.rounded_rectangle([pad, oy, pad + pw, oy + ph], radius=ph // 2, fill=(18, 20, 36, 240), outline=acc + (255,), width=5)
    d.polygon([(cx - 15, oy + (ph - 6 if pointer == "down" else 6)), (cx + 15, oy + (ph - 6 if pointer == "down" else 6)), (cx, oy + (ph + 16 if pointer == "down" else -16))], fill=(18, 20, 36, 255))
    A.rtl(d, (cx, oy + ph / 2 + 2), text, f, acc + (255,))
    anchor = (cx, oy + ph + 26) if pointer == "down" else (cx, oy - 26)
    _label_cache[key] = (im, anchor); return im, anchor

def put_label(img, text, x, y, k, acc, pointer="down"):
    """x,y = tip of the pointer."""
    if k <= 0.01: return
    im, (ax, ay) = label_img(text, acc, pointer)
    w, h = im.size; s = max(0.01, k)
    sm = im.resize((max(1, int(w * s)), max(1, int(h * s))), Image.BICUBIC)
    if k < 1: sm.putalpha(sm.getchannel("A").point(lambda v: int(v * clamp(k * 1.6))))
    img.alpha_composite(sm, (int(x - ax * s), int(y - ay * s)))

# ---------------- HUD (status bar), live counter, end card ----------------
def _pill(d, box, acc, fill=(14, 16, 30, 235)):
    d.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=fill, outline=acc + (255,), width=3)

def bar_colour(p, rising_good=True):
    stops = [(235, 80, 80), (245, 190, 60), (90, 210, 130)] if rising_good else [(90, 210, 130), (245, 190, 60), (235, 80, 80)]
    p = clamp(p); return mix(stops[0], stops[1], p * 2) if p < 0.5 else mix(stops[1], stops[2], p * 2 - 1)

def draw_hud(img, left, label, pct, colour, acc, k=1.0, pulse=0.0):
    """top status bar: small pill (left text) + bar pill (label on the right, bar, percent)."""
    if k <= 0.01: return
    lay = Image.new("RGBA", (W, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f = A.font("Bold", 38); y0, y1 = 62, 132
    _pill(d, [60, y0, 300, y1], acc); A.rtl(d, (180, (y0 + y1) / 2 + 1), left, f, (255, 255, 255, 255))
    _pill(d, [320, y0, 770, y1], acc)
    bb = d.textbbox((0, 0), label, font=f, direction="rtl", language="he"); lw = bb[2] - bb[0]
    A.rtl(d, (746 - lw / 2, (y0 + y1) / 2 + 1), label, f, (255, 255, 255, 255))
    d.text((346, (y0 + y1) / 2 + 1), f"{int(round(pct * 100))}%", font=f, fill=(255, 255, 255, 255), anchor="lm")
    bx0, bx1 = 452, 746 - lw - 24; by = (y0 + y1) / 2
    d.rounded_rectangle([bx0, by - 9, bx1, by + 9], radius=9, fill=(70, 74, 96, 255))
    w = max(18, (bx1 - bx0) * clamp(pct)); cc = mix(colour, (255, 255, 255), 0.25 * pulse)
    d.rounded_rectangle([bx1 - w, by - 9, bx1, by + 9], radius=9, fill=cc + (255,))
    if k < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * clamp(k))))
    img.alpha_composite(lay, (0, int(-40 * (1 - clamp(k)))))

def hud_png(path, left, label, pct, colour, acc):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); draw_hud(img, left, label, pct, colour, acc); img.save(path)

def draw_counter(img, text, num, acc, y=1345, k=1.0):
    if k <= 0.01: return
    f = A.font("Bold", 54); s = f"{text}: {num:,}"
    lay = Image.new("RGBA", (W, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    bb = d.textbbox((0, 0), f"{text}: " + "8" * len(f"{num:,}"), font=f, direction="rtl", language="he"); tw = bb[2] - bb[0]
    _pill(d, [W / 2 - tw / 2 - 44, 22, W / 2 + tw / 2 + 44, 118], acc)
    A.rtl(d, (W / 2, 71), s, f, (255, 220, 120, 255))
    if k < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * clamp(k))))
    img.alpha_composite(lay, (0, y - 70))

def endcard(path, big, small, theme, sub=None):
    bg, glow, acc = A.THEMES[theme]
    img = Image.new("RGBA", (W, H), mix(bg, (0, 0, 0), 0.45) + (255,))
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse([40, 420, 1040, 1300], fill=glow + (70,)); img.alpha_composite(g.filter(ImageFilter.GaussianBlur(170)))
    size = 250; f = A.font("Black", size)
    tmp = ImageDraw.Draw(img)
    while tmp.textbbox((0, 0), big, font=f, direction="rtl", language="he")[2] > 960: size -= 10; f = A.font("Black", size)
    for blur, a in ((46, 150), (18, 200), (6, 255)):
        t = Image.new("RGBA", (W, H), (0, 0, 0, 0)); A.rtl(ImageDraw.Draw(t), (W / 2, 800), big, f, acc + (a,))
        img.alpha_composite(t.filter(ImageFilter.GaussianBlur(blur)))
    d = ImageDraw.Draw(img); A.rtl(d, (W / 2, 800), big, f, mix(acc, (255, 255, 255), 0.35) + (255,))
    if small.startswith("^"): A.rtl(d, (W / 2, 600), small[1:], A.font("Bold", 74), (255, 255, 255, 255))
    else: A.rtl(d, (W / 2, 1010), small, A.font("Bold", 74), (255, 255, 255, 255))
    if sub: A.rtl(d, (W / 2, 1110), sub, A.font("Light", 50), (200, 200, 205, 255))
    img.convert("RGB").save(path)

def capsule(c, x, y, ang, acc, s=1.0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    def shape():
        c.new_path(); c.arc(-20, 0, 17, math.pi / 2, 3 * math.pi / 2); c.arc(20, 0, 17, -math.pi / 2, math.pi / 2); c.close_path()
    shape(); col(c, (246, 244, 240)); c.fill()
    c.save(); shape(); c.clip(); c.rectangle(0, -20, 40, 40); col(c, acc); c.fill(); c.restore()
    shape(); col(c, OUT); c.set_line_width(4.5); c.stroke()
    c.move_to(-22, -8); c.line_to(-8, -8); c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(4); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.restore()

def gift(c, x, base, acc, open_k=0.0, glow_t=0.0):
    g = cairo.RadialGradient(x, base - 70, 10, x, base - 70, 230)
    a = 0.22 + 0.10 * math.sin(glow_t * 3) + 0.35 * open_k
    g.add_color_stop_rgba(0, 1, 0.82, 0.4, a); g.add_color_stop_rgba(1, 1, 0.82, 0.4, 0); c.set_source(g); c.paint()
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.rectangle(x - 66, base - 104, 132, 104); col(c, (230, 84, 96)); c.fill_preserve(); col(c, OUT); c.set_line_width(5); c.stroke()
    c.rectangle(x - 12, base - 104, 24, 104); col(c, (255, 214, 110)); c.fill()
    c.save(); c.translate(x - 76, base - 104); c.rotate(-0.55 * open_k); c.translate(0, -70 * open_k)
    c.rectangle(0, -34, 152, 34); col(c, (242, 104, 114)); c.fill_preserve(); col(c, OUT); c.stroke()
    c.rectangle(64, -34, 24, 34); col(c, (255, 214, 110)); c.fill()
    for sx in (-1, 1):
        c.move_to(76, -34); c.curve_to(76 + sx * 50, -90, 76 + sx * 70, -30, 76, -34); col(c, (255, 214, 110)); c.fill_preserve(); col(c, OUT); c.set_line_width(4); c.stroke()
    c.restore()

def flag(c, x, base, k, acc):
    if k <= 0: return
    c.move_to(x, base); c.line_to(x, base - 150 * k); col(c, (236, 240, 240)); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.move_to(x, base - 150 * k); c.line_to(x - 62 * k, base - 128 * k); c.line_to(x, base - 104 * k); c.close_path(); col(c, acc); c.fill_preserve(); col(c, OUT); c.set_line_width(4); c.stroke()

def xmark(c, x, y, r, k):
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for w, clr in ((54, OUT), (36, (238, 76, 80))):
        c.move_to(-r, -r); c.line_to(r, r); c.move_to(r, -r); c.line_to(-r, r); col(c, clr); c.set_line_width(w); c.stroke()
    c.restore()

# ---------------- scenes ----------------
def to_pil(surf):
    a = np.ndarray((H, W, 4), np.uint8, buffer=surf.get_data())
    return Image.fromarray(a[..., [2, 1, 0, 3]].copy(), "RGBA")

def camera(c, t, d, cx=540, cy=1100, z=0.06, z0=0.0):
    k = 1 + z0 + z * smooth(t / max(d, 0.01)) * 0.7 + z * 0.3 * (t / max(d, 0.01))
    c.translate(cx, cy); c.scale(k, k); c.translate(-cx, -cy)

class Scene:
    def __init__(self, name, d, ev): self.name, self.d, self.ev = name, d, ev; self.setup()
    def setup(self):
        n = self.name
        if n == "stones":
            self.th = "navy"; self.bg, self.stars = night_bg("navy", (250, 430), flat_ground(1235, "navy"))
        elif n == "river":
            self.th = "purple"; self.bg, self.stars = night_bg("purple", (220, 400), self.river_ground, seed=7)
        elif n == "pills":
            self.th = "purple"; self.bg, self.stars = night_bg("purple", None, flat_ground(1215, "purple"), seed=4)
            rnd = random.Random(9); self.pills = []
            j = 0
            for r, cnt in enumerate((11, 10, 9, 8, 7, 6, 5, 4)):
                for q in range(cnt):
                    self.pills.append((540 + (q - (cnt - 1) / 2) * 80 + rnd.uniform(-8, 8), 1192 - r * 42, rnd.uniform(-0.5, 0.5), rnd.random()))
            order = list(range(len(self.pills))); rnd.shuffle(order); order.sort(key=lambda q: -self.pills[q][1] + rnd.uniform(-50, 50))
            self.pills = [self.pills[q] for q in order]
        elif n in ("item", "doors", "wall", "puzzle", "switch"):
            self.th = self.ev.get("th", "purple"); self.bg, self.stars = night_bg(self.th, None, flat_ground(1262, self.th), seed=8)
        elif n == "path":
            self.th = self.ev.get("th", "teal"); self.bg, self.stars = night_bg(self.th, None, flat_ground(1262, self.th), seed=6)
        elif n in ("staff", "camps"):
            self.th = "warm"; self.bg, self.stars = night_bg("warm", None, flat_ground(1262, "warm"), seed=11)

    def river_ground(self, c):
        bg, glow, acc = A.THEMES["purple"]
        c.move_to(0, 1230); c.line_to(300, 1230); c.curve_to(330, 1232, 345, 1330, 380, 1332); c.line_to(690, 1332)
        c.curve_to(725, 1330, 740, 1232, 770, 1230); c.line_to(W, 1230); c.line_to(W, H); c.line_to(0, H); c.close_path()
        g = cairo.LinearGradient(0, 1230, 0, H); g.add_color_stop_rgba(0, *(v / 255 for v in mix(bg, glow, 0.38)), 1)
        g.add_color_stop_rgba(1, *(v / 255 for v in mix(bg, (0, 0, 0), 0.3)), 1); c.set_source(g); c.fill()
        c.move_to(0, 1230); c.line_to(300, 1230); c.move_to(770, 1230); c.line_to(W, 1230)
        col(c, mix(glow, (255, 255, 255), 0.25), 0.5); c.set_line_width(4); c.stroke()
        # father's house on the right bank
        x0, x1, y0 = 800, 950, 1230
        c.rectangle(x0, y0 - 120, x1 - x0, 120); col(c, (62, 50, 88)); c.fill_preserve(); col(c, OUT); c.set_line_width(5); c.stroke()
        c.move_to(x0 - 18, y0 - 116); c.line_to((x0 + x1) / 2, y0 - 206); c.line_to(x1 + 18, y0 - 116); c.close_path()
        col(c, (118, 70, 66)); c.fill_preserve(); col(c, OUT); c.stroke()
        g = cairo.RadialGradient(905, 1160, 5, 905, 1160, 120); g.add_color_stop_rgba(0, 1, 0.77, 0.43, 0.45); g.add_color_stop_rgba(1, 1, 0.77, 0.43, 0)
        c.set_source(g); c.paint()
        c.rectangle(880, 1140, 46, 40); c.set_source_rgba(1, 0.8, 0.45, 1); c.fill()
        c.rectangle(816, 1160, 42, 70); col(c, (40, 30, 52)); c.fill()

    def bed(self, c):
        c.move_to(300, 1230); c.curve_to(330, 1232, 345, 1330, 380, 1332); c.line_to(690, 1332)
        c.curve_to(725, 1330, 740, 1232, 770, 1230); c.close_path()
    def water(self, c, t, front):
        c.save(); self.bed(c); c.clip()
        x0, x1, ys = 290, 780, 1240
        c.move_to(x0, ys)
        for k in range(0, 61):
            x = x0 + (x1 - x0) * k / 60; c.line_to(x, ys + 6 * math.sin(x / 34 - t * 3.2))
        c.line_to(x1, 1335); c.line_to(x0, 1335); c.close_path()
        g = cairo.LinearGradient(0, ys, 0, 1335); g.add_color_stop_rgba(0, 0.30, 0.48, 0.92, 0.80 if front else 1)
        g.add_color_stop_rgba(1, 0.16, 0.24, 0.58, 0.92 if front else 1); c.set_source(g); c.fill()
        if front:
            for yy, a in ((ys, 0.9), (ys + 34, 0.45), (ys + 62, 0.3)):
                c.move_to(x0 + 14, yy)
                for k in range(0, 61):
                    x = x0 + 14 + (x1 - x0 - 28) * k / 60; c.line_to(x, yy + 6 * math.sin(x / 34 - t * 3.2 + yy))
                c.set_source_rgba(0.68, 0.82, 1, a); c.set_line_width(5 if yy == ys else 4); c.stroke()
        c.restore()

    def frame(self, t):
        ev = self.ev; d = self.d; acc = A.THEMES[self.th][2]
        self.hud = None; self.counter = None; self.texts = []
        if self.name in ("stones", "river", "camps"): LOOK.update(beard=True, robe=ROBE, robe_d=ROBE_D)
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
        labels = []
        c.save(); camera(c, t, d, *ev.get("cam", (560, 1120)), z=ev.get("zoom", 0.06), z0=ev.get("z0", 0.0))
        c.set_source_surface(self.bg); c.paint(); draw_stars(c, self.stars, t)
        if self.name == "stones":
            ks = [pop(t, ev["st"][j], 0.3) for j in range(5)]
            stone(c, 668, 1196, 40, 30, ks[3]); stone(c, 812, 1190, 46, 34, ks[4])
            c.save(); c.translate(250, 1150); c.rotate(math.pi / 2); c.scale(0.82, 0.82); body(c, rest=True); c.restore()
            breath = 3 * math.sin(t * 2.4)
            head(c, 735, 1146 + breath * 0.3, 0.82, "closed", "smile", tilt=-0.10)
            stone(c, 610, 1214, 48, 32, ks[0]); stone(c, 858, 1212, 54, 38, ks[1]); stone(c, 942, 1222, 40, 27, ks[2])
            for j in range(4):
                ph = ((t + j * 0.75) % 3.0) / 3.0
                zee(c, 700 - 80 * ph + 10 * math.sin(ph * 6), 1040 - 200 * ph, 1.0 + 1.2 * ph, 0.9 * math.sin(ph * math.pi))
            labels.append(("אבנים", 930, 1168, pop(t, ev["label"], 0.35), "down"))
        elif self.name == "river":
            x = ev["x0"] + (ev["x1"] - ev["x0"]) * clamp(t / d)
            def depth(xx):
                if xx > 760 or xx < 310: return 0.0
                if xx > 700: return 70 * (760 - xx) / 60
                if xx < 370: return 70 * (xx - 310) / 60
                return 70.0
            wk = t * 2 * math.pi * 1.7; bob = -7 * abs(math.sin(wk))
            self.water(c, t, False)
            person(c, x, 1230 + depth(x), 0.8, "open", "flat", walk=wk, amp=0.34, staff=True, bob=bob)
            self.water(c, t, True)
            if depth(x) > 10:
                for j in range(2):
                    rr = ((t * 1.4 + j * 0.5) % 1.0)
                    c.save(); c.translate(x, 1250); c.scale(1, 0.25); c.arc(0, 0, 60 + 90 * rr, 0, 2 * math.pi); c.restore()
                    c.set_source_rgba(0.75, 0.88, 1, 0.6 * (1 - rr)); c.set_line_width(4); c.stroke()
            labels.append(("הירדן", 535, 1352, pop(t, ev["jordan"], 0.35), "up"))
            labels.append(("הבית של אבא", 815, 1010, pop(t, ev["house"], 0.35), "down"))
        elif self.name == "pills":
            LOOK.update(beard=False)
            n = len(self.pills)
            for j, (px, py, ang, rr) in enumerate(self.pills):
                t0 = 0.2 + (d - 0.9) * (j / n) ** 0.8
                if t < t0: continue
                q = clamp((t - t0) / 0.42); y = py - 1100 * (1 - q) ** 2 if q < 1 else py - 10 * max(0, 1 - (t - t0 - 0.42) / 0.12) * 0
                capsule(c, px, y, ang + (1 - q) * 4 * (rr - 0.5), acc, 1.15)
            xmark(c, 540, 1010, 150, pop(t, ev["x"], 0.3))
            self.hud = ("כדורים", ev.get("bar", "כאב ראש"), 1.0, (235, 80, 80), 0.5 + 0.5 * math.sin(t * 9))
            self.counter = ("כדורים", int(10 ** (6 * clamp(t / (d - 0.25)))))
        elif self.name == "item":
            LOOK.update(beard=False, robe=(70, 176, 156), robe_d=(42, 124, 110))
            kind = ev["kind"]; fl = 10 * math.sin(t * 1.8); k0 = pop(t, ev.get("in", 0.0), 0.35)
            g = cairo.RadialGradient(540, 1000, 20, 540, 1000, 420); g.add_color_stop_rgba(0, *(v / 255 for v in acc), 0.22); g.add_color_stop_rgba(1, *(v / 255 for v in acc), 0); c.set_source(g); c.paint()
            c.save(); c.translate(540, 1000 + fl); c.scale(max(k0, 0.01), max(k0, 0.01)); c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_line_cap(cairo.LINE_CAP_ROUND)
            if kind == "doc":
                c.rotate(-0.08); c.rectangle(-150, -200, 300, 400); col(c, (246, 244, 238)); c.fill_preserve(); col(c, OUT); c.set_line_width(7); c.stroke()
                for j, w in enumerate((200, 150, 220, 120, 190, 160)):
                    c.move_to(110, -140 + j * 46); c.line_to(110 - w, -140 + j * 46); col(c, (150, 156, 176)); c.set_line_width(12); c.stroke()
                c.arc(-80, 140, 44, 0, 2 * math.pi); col(c, (255, 200, 80)); c.fill_preserve(); col(c, OUT); c.set_line_width(5); c.stroke()
                c.move_to(-98, 160); c.line_to(-98, 124); c.line_to(-80, 124); c.move_to(-62, 120); c.line_to(-62, 156); c.line_to(-80, 156); col(c, OUT); c.set_line_width(6); c.stroke()
            elif kind == "keys":
                c.arc(0, -130, 70, 0, 2 * math.pi); col(c, (210, 214, 228)); c.set_line_width(16); c.stroke()
                c.rotate(0.25); c.rectangle(-22, -70, 44, 230); col(c, (255, 200, 80)); c.fill_preserve(); col(c, OUT); c.set_line_width(6); c.stroke()
                for yy in (90, 130): c.rectangle(22, yy, 34, 18); col(c, (255, 200, 80)); c.fill_preserve(); col(c, OUT); c.stroke()
                c.rotate(-0.7); c.new_path(); c.rectangle(-48, -60, 96, 150); col(c, (52, 56, 84)); c.fill_preserve(); col(c, OUT); c.stroke()
                c.arc(0, 20, 20, 0, 2 * math.pi); col(c, (238, 76, 80)); c.fill()
            elif kind == "book":
                for sx in (-1, 1):
                    c.move_to(0, -150); c.curve_to(sx * 80, -190, sx * 220, -180, sx * 300, -140); c.line_to(sx * 300, 170); c.curve_to(sx * 220, 130, sx * 80, 120, 0, 160); c.close_path()
                    col(c, (246, 242, 230)); c.fill_preserve(); col(c, OUT); c.set_line_width(7); c.stroke()
                    for j in range(5):
                        yy = -100 + j * 48; c.move_to(sx * 40, yy + 4); c.curve_to(sx * 110, yy - 14, sx * 190, yy - 12, sx * 262, yy + 10); col(c, (150, 156, 176)); c.set_line_width(9); c.stroke()
                c.move_to(0, -150); c.line_to(0, 160); col(c, OUT); c.set_line_width(7); c.stroke()
            elif kind == "plate":
                c.save(); c.scale(1, 0.42); c.arc(0, 200, 330, 0, 2 * math.pi); c.restore(); col(c, (240, 240, 246)); c.fill_preserve(); col(c, OUT); c.set_line_width(7); c.stroke()
                c.save(); c.scale(1, 0.42); c.arc(0, 200, 240, 0, 2 * math.pi); c.restore(); col(c, (206, 210, 224)); c.set_line_width(5); c.stroke()
                c.move_to(-200, 60); c.curve_to(-230, -40, -120, -90, -20, -70); c.curve_to(60, -110, 190, -80, 210, 0); c.curve_to(240, 80, 150, 140, 40, 120); c.curve_to(-60, 150, -170, 130, -200, 60); c.close_path()
                col(c, (214, 150, 60)); c.fill_preserve(); col(c, OUT); c.set_line_width(7); c.stroke()
                for (qx, qy) in ((-110, 10), (-30, 50), (60, -10), (130, 50), (-40, -30), (20, 80)):
                    c.arc(qx, qy, 9, 0, 2 * math.pi); col(c, (176, 112, 40)); c.fill()
                c.move_to(-150, -20); c.curve_to(-100, -60, -40, -50, 0, -56); col(c, (240, 190, 100)); c.set_line_width(8); c.stroke()
            elif kind == "car":
                c.scale(1.35, 1.35)
                c.move_to(-300, 60); c.curve_to(-290, -10, -200, -20, -150, -30); c.curve_to(-90, -110, 60, -110, 130, -34); c.curve_to(220, -24, 300, -10, 310, 60); c.close_path()
                col(c, (255, 196, 40)); c.fill_preserve(); col(c, OUT); c.set_line_width(7); c.stroke()
                c.move_to(-120, -34); c.curve_to(-70, -86, 40, -86, 92, -34); c.close_path(); col(c, (150, 210, 240)); c.fill_preserve(); col(c, OUT); c.set_line_width(5); c.stroke()
                for wx in (-180, 190):
                    c.arc(wx, 62, 56, 0, 2 * math.pi); col(c, (36, 38, 58)); c.fill_preserve(); col(c, OUT); c.set_line_width(6); c.stroke()
                    c.arc(wx, 62, 24, 0, 2 * math.pi); col(c, (210, 214, 228)); c.fill()
                c.rectangle(270, 10, 34, 16); col(c, (255, 250, 220)); c.fill()
            c.restore()
            if kind == "gifts":
                for j, tg in enumerate(ev["times"]):
                    kk = pop(t, tg, 0.35)
                    if kk > 0:
                        gx = (790, 540, 290)[j % 3]; c.save(); c.translate(gx, 1262); c.scale(1.25 * kk, 1.25 * kk); c.translate(-150, -1262); gift(c, 150, 1262, acc, 0.0, t + j); c.restore()
            if ev.get("counter"):
                ct, target, c0, c1 = ev["counter"]; self.counter = (ct, int(target * smooth((t - c0) / max(c1 - c0, 0.01))))
            if kind == "me":
                okt = ev.get("ok", 9e9); hp = t >= okt
                person(c, 540, 1262, 0.95, "happy" if hp else "open", "big" if hp else "smile", arms_up=smooth((t - okt) / 0.25) if hp else 0, bob=(-12 * abs(math.sin((t - okt) * 7)) if hp and t < okt + 0.9 else 0))
            if ev.get("x") is not None: xmark(c, 540, 1000, 170, pop(t, ev["x"], 0.3))
            if ev.get("ok") is not None and t >= ev["ok"]:
                kk = max(pop(t, ev["ok"], 0.35), 0.01); c.save(); c.translate(790, 760); c.scale(kk, kk)
                c.arc(0, 0, 78, 0, 2 * math.pi); col(c, (90, 210, 130)); c.fill_preserve(); col(c, OUT); c.set_line_width(7); c.stroke()
                c.move_to(-36, 2); c.line_to(-8, 30); c.line_to(40, -28); c.set_source_rgba(1, 1, 1, 1); c.set_line_width(16); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke(); c.restore()
                for m in range(10):
                    q = clamp((t - ev["ok"]) / 0.7); an = m * math.pi / 5; sparkle(c, 540 + (120 + 260 * q) * math.cos(an), 900 + (120 + 260 * q) * math.sin(an), 28 * (1 - q), 1 - q)
            for text, tl, lx, ly in ev.get("labels", []): labels.append((text, lx, ly, pop(t, tl, 0.35), "down"))
        elif self.name == "switch":
            fl = ev.get("flip"); k = 0.0 if fl is None else smooth((t - fl) / 0.28); k = 1.0 if fl is not None and fl < 0 else k
            offc, onc = (235, 80, 80), (255, 128, 176); cc = mix(offc, onc, k)
            g = cairo.RadialGradient(540, 980, 40, 540, 980, 560); g.add_color_stop_rgba(0, *(v / 255 for v in cc), 0.35); g.add_color_stop_rgba(1, *(v / 255 for v in cc), 0); c.set_source(g); c.paint()
            c.new_path(); c.arc(360, 1000, 130, math.pi / 2, 3 * math.pi / 2); c.arc(720, 1000, 130, -math.pi / 2, math.pi / 2); c.close_path()
            col(c, cc); c.fill_preserve(); col(c, OUT); c.set_line_width(9); c.stroke()
            kx = 720 - 360 * k
            c.arc(kx, 1000, 104, 0, 2 * math.pi); col(c, (250, 250, 252)); c.fill_preserve(); col(c, OUT); c.set_line_width(7); c.stroke()
            if k > 0.5: heart_path(c, kx, 1010, 46); col(c, onc); c.fill()
            else:
                c.move_to(kx - 28, 972); c.line_to(kx + 28, 1028); c.move_to(kx + 28, 972); c.line_to(kx - 28, 1028); col(c, offc); c.set_line_width(14); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
            self.texts.append((ev.get("off", "אויב"), 540, 720, 150, 1 - clamp(k * 2))); self.texts.append((ev.get("on", "אוהב"), 540, 720, 150, clamp(k * 2 - 1)))
            if k >= 1:
                t0 = max(fl, 0) + 0.28
                for m in range(9):
                    q = ((t - t0) * 0.7 + m / 9) % 1.0
                    heart_path(c, 240 + m * 76 + 16 * math.sin(q * 6 + m), 860 - 420 * q, 22 + 6 * (m % 3)); c.set_source_rgba(1, 0.5, 0.66, math.sin(q * math.pi)); c.fill()
                if fl is not None and fl >= 0:
                    for m in range(10):
                        q = clamp((t - fl - 0.2) / 0.6); an = m * math.pi / 5; sparkle(c, kx + (130 + 240 * q) * math.cos(an), 1000 + (130 + 240 * q) * math.sin(an), 28 * (1 - q), 1 - q)
        elif self.name == "wall":
            LOOK.update(beard=False, robe=(70, 176, 156), robe_d=(42, 124, 110))
            r0, r1 = ev.get("r0", 0), ev.get("r1", 6); n = r0 * 3 + (r1 - r0) * 3 * clamp(t / (d * 0.85))
            for j in range(int(r1 * 3)):
                row, cc = divmod(j, 3); k = 1.0 if j < r0 * 3 else pop(n, j, 1.0) if n > j else 0.0
                if k <= 0: continue
                bx = 150 + cc * 124 + (62 if row % 2 else 0) - 31; by = 1262 - row * 62
                c.save(); c.translate(bx + 60, by - 30 - (1 - min(k, 1)) * 60); c.scale(max(k, 0.01), max(k, 0.01))
                c.rectangle(-60, -29, 120, 58); col(c, (188, 92, 70) if (row + cc) % 2 else (168, 78, 60)); c.fill_preserve(); col(c, OUT); c.set_line_width(5); c.stroke(); c.restore()
            sad = t > d * 0.5 or r0 > 0
            person(c, 740, 1262, 0.72, "open", "flat", bob=1.5 * math.sin(t * 2))
            if sad:
                for m in range(2):
                    q = (t * 1.3 + m / 2) % 1.0; c.save(); c.translate(820 + 20 * m, 800 + 70 * q); c.scale(1, 1.5); c.arc(0, 0, 8, 0, 2 * math.pi); c.restore(); c.set_source_rgba(0.55, 0.8, 1, 0.9 * math.sin(q * math.pi)); c.fill()
            for text, tl, lx, ly in ev.get("labels", []): labels.append((text, lx, ly, pop(t, tl, 0.35), "down"))
        elif self.name == "puzzle":
            P = 230; cx0, cy0 = 540, 980; cols = [(64, 200, 170), (255, 128, 176), (95, 165, 255), (255, 183, 77)]
            pos = [(cx0 + P / 2, cy0 - P / 2), (cx0 - P / 2, cy0 - P / 2), (cx0 + P / 2, cy0 + P / 2), (cx0 - P / 2, cy0 + P / 2)]
            names = ev["names"]; new = ev.get("new"); placed = list(ev.get("placed", []))
            done = new is not None and len(placed) == 3 and t >= new[1] + 0.35
            if done:
                g = cairo.RadialGradient(cx0, cy0, 60, cx0, cy0, 560); g.add_color_stop_rgba(0, 1, 0.9, 0.6, 0.4); g.add_color_stop_rgba(1, 1, 0.9, 0.6, 0); c.set_source(g); c.paint()
            def piece(i, x, y, a_=1.0, sc=1.0):
                c.save(); c.translate(x, y); c.scale(sc, sc); h = P / 2 - 4
                c.new_path(); c.rectangle(-h, -h, 2 * h, 2 * h)
                if i in (0, 2): c.new_sub_path(); c.arc(-h - 18, 0, 34, 0, 2 * math.pi)
                if i in (0, 1): c.new_sub_path(); c.arc(0, h + 18, 34, 0, 2 * math.pi)
                c.set_fill_rule(cairo.FILL_RULE_WINDING); col(c, cols[i], a_); c.fill_preserve(); col(c, OUT, a_); c.set_line_width(6); c.stroke(); c.restore()
            for i in range(4):
                x, y = pos[i]; c.rectangle(x - P / 2 + 4, y - P / 2 + 4, P - 8, P - 8); c.set_dash([18, 14]); c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(5); c.stroke(); c.set_dash([])
            for i in sorted(placed, reverse=True):
                piece(i, *pos[i]); self.texts.append((names[i], pos[i][0], pos[i][1], 50, 1.0))
            if new is not None and t >= new[1] - 0.45:
                i, tn = new; q = smooth((t - (tn - 0.45)) / 0.45); x, y = pos[i]
                sx, sy = x + (1 - q) * (160 if i % 2 == 0 else -160), y - (1 - q) * 520
                piece(i, sx, sy, clamp(q * 3), 1 + 0.25 * math.sin(clamp((t - tn) / 0.25) * math.pi) if t >= tn else 1.0)
                self.texts.append((names[i], sx, sy, 50, clamp(q * 3)))
                if t >= tn:
                    for m in range(8):
                        qq = clamp((t - tn) / 0.6); an = m * math.pi / 4; sparkle(c, x + (90 + 170 * qq) * math.cos(an), y + (90 + 170 * qq) * math.sin(an), 24 * (1 - qq), 1 - qq)
            if done:
                for m in range(12):
                    qq = ((t - new[1]) * 0.8 + m / 12) % 1.0; an = m * math.pi / 6; sparkle(c, cx0 + (260 + 160 * qq) * math.cos(an), cy0 + (260 + 160 * qq) * math.sin(an), 26 * math.sin(qq * math.pi), math.sin(qq * math.pi))
            for text, tl, lx, ly in ev.get("labels", []): labels.append((text, lx, ly, pop(t, tl, 0.35), "down"))
        elif self.name == "doors":
            LOOK.update(beard=False, robe=(70, 176, 156), robe_d=(42, 124, 110))
            ob = ev.get("open_b", 9e9); ko = smooth((t - ob) / 0.5) if t >= ob else 0.0
            def door(x, openk, lit):
                if lit and openk > 0:
                    g = cairo.RadialGradient(x, 1080, 30, x, 1080, 520); g.add_color_stop_rgba(0, 1, 0.86, 0.5, 0.55 * openk); g.add_color_stop_rgba(1, 1, 0.86, 0.5, 0); c.set_source(g); c.paint()
                c.rectangle(x - 118, 882, 236, 380); col(c, (40, 34, 60) if not lit else mix((40, 34, 60), (255, 236, 170), openk)); c.fill_preserve(); col(c, OUT); c.set_line_width(8); c.stroke()
                w = 216 * (1 - 0.82 * openk)
                c.rectangle(x - 108, 892, w, 370); col(c, (150, 96, 62)); c.fill_preserve(); col(c, OUT); c.set_line_width(5); c.stroke()
                if w > 80:
                    c.rectangle(x - 108 + 20, 912, w - 40, 150); col(c, (126, 78, 50)); c.fill(); c.rectangle(x - 108 + 20, 1082, w - 40, 160); c.fill()
                c.arc(x - 108 + w - 24, 1080, 10, 0, 2 * math.pi); col(c, (255, 208, 90)); c.fill()
            door(830, 0, False); door(250, ko, True)
            if ko > 0.3:
                q = smooth((t - ob - 0.25) / 0.6); gx = 250 + 130 * q
                c.save(); c.translate(gx, 1262); c.scale(0.9, 0.9); c.translate(-150, -1262); gift(c, 150, 1262, acc, 0.0, t); c.restore()
                for m in range(8):
                    qq = clamp((t - ob - 0.2) / 0.8); an = m * math.pi / 4; sparkle(c, 250 + (80 + 220 * qq) * math.cos(an), 1070 + (80 + 220 * qq) * math.sin(an), 26 * (1 - qq), 1 - qq)
            hp = t >= ob + 0.7
            person(c, 560, 1262, 0.6, "happy" if hp else "open", "big" if hp else "flat", arms_up=smooth((t - ob - 0.7) / 0.25) if hp else 0, bob=2 * math.sin(t * 2.2))
            if not hp:
                for m in range(3):
                    a_ = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * 5 - m * 1.1)); c.arc(526 + m * 34, 820, 9, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, a_); c.fill()
            for text, tl, lx, ly in ev.get("labels", []): labels.append((text, lx, ly, pop(t, tl, 0.35), "down"))
        elif self.name == "path":
            LOOK.update(beard=False, robe=(70, 176, 156), robe_d=(42, 124, 110))
            p = ev["p0"] + (ev["p1"] - ev["p0"]) * smooth(t / ev.get("move", d)); x = 930 - 620 * p
            T = ev.get("T0", 0) + t; moving = t < ev.get("move", d)
            c.set_dash([26, 22]); c.move_to(960, 1305); c.line_to(150, 1305); c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(7); c.stroke(); c.set_dash([])
            c.move_to(960, 1305); c.line_to(x, 1305); col(c, acc); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
            for fx in (700, 480):
                fp = (930 - fx) / 620; flag(c, fx + 60, 1262, back(clamp((p - fp) / 0.06)) if p > fp else 0, acc)
            ok = ev.get("open"); okk = pop(t, ok, 0.4) if ok is not None else 0.0
            rob = ev.get("rob"); gone = ev.get("gone")
            if not gone and (rob is None or t < rob + 0.25):
                c.save()
                if rob is not None and t >= rob:
                    q = (t - rob) / 0.25; c.translate(150, 1210); c.scale(1 - q, 1 - q); c.rotate(q * 2); c.translate(-150, -1210)
                gift(c, 150, 1262, acc, okk, T); c.restore()
            if rob is not None and t >= rob:
                for m in range(8):
                    q = clamp((t - rob) / 0.5); an = m * math.pi / 4
                    c.arc(150 + (40 + 120 * q) * math.cos(an), 1200 + (40 + 120 * q) * math.sin(an), 16 * (1 - q) + 0.1, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 0.6 * (1 - q)); c.fill()
            if ev.get("xgift") is not None: xmark(c, 150, 1195, 85, pop(t, ev["xgift"], 0.3))
            happy = ok is not None and t >= ok
            wk = T * 2 * math.pi * ev.get("pace", 1.7)
            person(c, x, 1262, 0.72, "happy" if happy else "open", "big" if happy else ("flat" if not ev.get("smile") else "smile"), walk=wk, amp=(0.34 if ev.get("pace", 1.7) < 2.5 else 0.5) if moving else 0.0,
                   bob=(-6 * abs(math.sin(wk)) if moving else (-12 * abs(math.sin((t - ok) * 7)) if happy and t < ok + 0.9 else 0)), arms_up=smooth((t - ok) / 0.25) if happy else 0.0)
            if ev.get("sweat") is not None and t >= ev["sweat"]:
                for m in range(3):
                    q = ((t - ev["sweat"]) * 1.6 + m / 3) % 1.0
                    c.save(); c.translate(x + 78 + 26 * m * q, 1262 - 520 + 90 * q); c.scale(1, 1.5); c.arc(0, 0, 8, 0, 2 * math.pi); c.restore()
                    c.set_source_rgba(0.55, 0.8, 1, 0.9 * math.sin(q * math.pi)); c.fill()
            if happy:
                for m in range(10):
                    q = clamp((t - ok) / 0.7); an = m * math.pi / 5; rr = 50 + 200 * q
                    sparkle(c, 150 + rr * math.cos(an), 1150 + rr * math.sin(an) * 0.8, 26 * (1 - q), 1 - q)
                for m in range(6):
                    q = ((t - ok) * 0.9 + m / 6) % 1.0
                    heart_path(c, 150 + 90 * math.sin(m * 2.1) + 14 * math.sin(q * 6 + m), 1080 - 330 * q, 20 + 5 * (m % 3)); c.set_source_rgba(1, 0.5, 0.56, math.sin(q * math.pi)); c.fill()
            for text, tl in ev.get("labels", []):
                if isinstance(tl, tuple): labels.append((text, tl[1], tl[2], pop(t, tl[0], 0.35), "down"))
                else: labels.append((text, min(max(x, 290), 790), 1262 - 0.72 * 690, pop(t, tl, 0.35), "down"))
            self.hud = None if ev.get("no_hud") else (ev.get("left", "שלב 1"), ev.get("hud_label", "מסלול החיים"), p, bar_colour(p), 0.0)
        elif self.name == "staff":
            LOOK.update(beard=True, robe=ROBE, robe_d=ROBE_D)
            person(c, 545, 1262, 0.92, "open", "flat", staff=True)
            dashed_ring(c, 455, 640, 92, pop(t, ev["ring"], 0.3), t, acc)
            labels.append(("רק עם המקל", 540, 450, pop(t, ev["label"], 0.35), "down"))
        elif self.name == "camps":
            tb = ev["banks"]; happy = t >= tb
            kt = [pop(t, ev["tent"][0], 0.34), pop(t, ev["tent"][1], 0.34)]
            if t > tb: kt = [k * (1 - smooth((t - tb) / 0.18)) for k in kt]
            kb = pop(t, tb + 0.08, 0.4)
            for j, xx in enumerate((205, 885)):
                tent(c, xx, 1262, kt[j], acc); bank(c, xx, 1262, kb, acc)
                if tb <= t < tb + 0.6:
                    q = (t - tb) / 0.6
                    for m in range(8):
                        an = m * math.pi / 4; rr = 60 + 170 * q
                        sparkle(c, xx + rr * math.cos(an), 1140 + rr * math.sin(an) * 0.8, 22 * (1 - q), 1 - q)
            person(c, 545, 1262, 0.92, "happy" if happy else "open", "big" if happy else "smile", staff=True, bob=(-10 * abs(math.sin((t - tb) * 7)) if happy and t < tb + 0.9 else 0))
            tc = ev["coins"]
            if t >= tc:
                rnd = random.Random(5)
                for m in range(18):
                    t0 = tc + m * 0.075; xx = (205, 885)[m % 2] + rnd.uniform(-60, 60)
                    if t < t0: continue
                    q = (t - t0) / 1.1
                    if q > 1: continue
                    yy = 1080 - 330 * (1 - (1 - q) ** 2); xx += rnd.uniform(-90, 90) * q
                    coin(c, xx, yy, 24, 1 - smooth((q - 0.6) / 0.4), spin=t * 6 + m)
                for m in range(6):
                    ph = (t * 1.3 + m * 0.37) % 1.0
                    sparkle(c, (205, 885)[m % 2] + (m - 3) * 40, 980 - 40 * m % 120, 16 * math.sin(ph * math.pi), 0.9 * math.sin(ph * math.pi))
            if t < tb: labels.append((ev.get("label_text", "שתי מחנות"), 545, 470, pop(t, ev["label"], 0.35), "down"))
            else:
                labels.append(("שני בנקים", 545, 470, pop(t, tb + 0.12, 0.35), "down"))
        c.restore()
        img = to_pil(s)
        for text, x, y, k, pt in labels: put_label(img, text, x, y, k, acc, pt)
        for text, x, y, size, a_ in self.texts:
            if a_ > 0.02:
                lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); A.rtl(ImageDraw.Draw(lay), (x, y), text, A.font("Bold", size), (255, 255, 255, int(255 * clamp(a_)))); img.alpha_composite(lay)
        if self.hud: draw_hud(img, *self.hud[:4], acc, k=clamp(t / 0.25) if ev.get("hud_in") else 1.0, pulse=self.hud[4])
        if self.counter: draw_counter(img, self.counter[0], self.counter[1], acc, y=ev.get("counter_y", 1345), k=clamp(t / 0.25))
        return img

def render(name, d, ev, out):
    sc = Scene(name, d, ev); n = int(round(d * FPS)) + 1
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(sc.frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    return out

# ---------------- gratitude meter (overlay for the stage, transparent frames) ----------------
def meter_sequence(outdir, theme, dur, t0=0.3, t1=1.4, label="תודה", fps=30):
    os.makedirs(outdir, exist_ok=True)
    acc = A.THEMES[theme][2]; n = max(1, int(round(dur * fps)))
    Wm, Hm = 300, 470; x0, x1, top, bot = 112, 188, 70, 370
    lab = Image.new("RGBA", (Wm, Hm), (0, 0, 0, 0)); ld = ImageDraw.Draw(lab)
    A.rtl(ld, (Wm / 2 + 1, 422), label, A.font("Bold", 56), (255, 255, 255, 255))
    for i in range(n):
        t = i / fps
        f = 0.12 + 0.88 * smooth((t - t0) / (t1 - t0))
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wm, Hm); c = cairo.Context(s)
        def capsule(inset=0):
            r = (x1 - x0) / 2 - inset
            c.new_path(); c.arc(Wm / 2, top + r + inset, r, math.pi, 2 * math.pi); c.arc(Wm / 2, bot - r - inset, r, 0, math.pi); c.close_path()
        capsule(); c.set_source_rgba(0.05, 0.05, 0.12, 0.55); c.fill()
        lvl = bot - 10 - (bot - top - 20) * f
        c.save(); capsule(10); c.clip()
        g = cairo.LinearGradient(0, bot, 0, top); g.add_color_stop_rgba(0, *(v / 255 for v in acc), 1); g.add_color_stop_rgba(1, 1, 1, 1, 1)
        c.rectangle(0, lvl + 4 * math.sin(t * 6), Wm, Hm); c.set_source(g); c.fill(); c.restore()
        for w, a in ((16, 0.25), (9, 0.45)):
            capsule(); c.set_source_rgba(*(v / 255 for v in acc), a); c.set_line_width(w); c.stroke()
        capsule(); c.set_source_rgba(1, 1, 1, 1); c.set_line_width(5); c.stroke()
        for k in range(1, 5):
            y = bot - (bot - top) * k / 5; c.move_to(x1 + 14, y); c.line_to(x1 + 34, y)
            c.set_source_rgba(1, 1, 1, 0.7); c.set_line_width(4); c.stroke()
        if t > t1 - 0.1:
            rnd = random.Random(2)
            for m in range(7):
                q = ((t - t1 + 0.1) * 0.9 + m / 7) % 1.0
                hx = Wm / 2 + rnd.uniform(-70, 70) + 18 * math.sin(q * 6 + m); hy = top - 10 - 60 * q
                heart_path(c, hx, hy + 40, 16 + 8 * rnd.random()); c.set_source_rgba(*(v / 255 for v in acc), math.sin(q * math.pi)); c.fill()
        a = np.ndarray((Hm, Wm, 4), np.uint8, buffer=s.get_data()).astype(np.float32)
        al = a[..., 3:4]; rgb = np.where(al > 0, a[..., :3] * 255 / np.maximum(al, 1), 0)
        im = Image.fromarray(np.concatenate([rgb[..., [2, 1, 0]], al], -1).clip(0, 255).astype(np.uint8), "RGBA")
        im.alpha_composite(lab); im.save(f"{outdir}/{i:04d}.png", compress_level=1)
    return n

if __name__ == "__main__":
    # still preview: python3 style3_anim.py still <out.png>
    if sys.argv[1] == "still":
        tiles = [Scene("stones", 3.2, {"st": [0.45, 0.6, 1.16, 2.04, 2.32], "label": 0.45}).frame(2.9),
                 Scene("river", 4.17, {"x0": 860, "x1": 230, "jordan": 1.07, "house": 2.6}).frame(2.55),
                 Scene("camps", 4.1, {"tent": [0.92, 1.05], "label": 0.95, "banks": 2.0, "coins": 2.72}).frame(3.3)]
        sheet = Image.new("RGB", (W * 3 + 40, H), (255, 255, 255))
        for j, im in enumerate(tiles): sheet.paste(im.convert("RGB"), (j * (W + 20), 0))
        sheet.resize((sheet.width // 2, sheet.height // 2), Image.LANCZOS).save(sys.argv[2], quality=90)
