# Instagram reel cover (1080x1920, key content inside the centre 3:4 area) in the merged style.
import sys, subprocess
sys.path.insert(0, "/home/claude/reel_scripts")
import style3_assets as A
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
W, H = 1080, 1920

def glow_text(img, xy, text, f, acc, core=None):
    for blur, a in ((40, 150), (16, 210), (5, 255)):
        t = Image.new("RGBA", img.size, (0, 0, 0, 0)); A.rtl(ImageDraw.Draw(t), xy, text, f, acc + (a,)); img.alpha_composite(t.filter(ImageFilter.GaussianBlur(blur)))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); A.rtl(ImageDraw.Draw(sh), (xy[0], xy[1] + 6), text, f, (0, 0, 0, 200)); img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    A.rtl(ImageDraw.Draw(img), xy, text, f, (core or tuple(int(c + (255 - c) * 0.3) for c in acc)) + (255,))

def fit(text, weight, size, maxw):
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    while True:
        f = A.font(weight, size); bb = d.textbbox((0, 0), text, font=f, direction="rtl", language="he")
        if bb[2] - bb[0] <= maxw or size < 60: return f
        size -= 6

def cover(out, src, t, theme, chip, small, big, icon=None, face_y=0.30, name="הרב אביה אוחיון", logo=None):
    bg, glow, acc = A.THEMES[theme]
    A.stage_bg("/tmp/cov_bg.png", theme); img = Image.open("/tmp/cov_bg.png").convert("RGBA")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", src, "-frames:v", "1", "/tmp/cov_fr.png"], check=True)
    fr = Image.open("/tmp/cov_fr.png").convert("RGB"); sw, sh = fr.size
    cw = min(sw, int(sh * 0.8)); ch = int(cw * 1.25); y0 = max(0, min(sh - ch, int(sh * face_y - ch * 0.36)))
    ph = fr.crop(((sw - cw) // 2, y0, (sw - cw) // 2 + cw, y0 + ch)).resize((1080, 1350), Image.LANCZOS).filter(ImageFilter.UnsharpMask(3, 90, 2))
    ph = ImageEnhance.Contrast(ImageEnhance.Color(ph).enhance(1.08)).enhance(1.06)
    tint = Image.new("RGB", ph.size, acc); ph = Image.blend(ph, Image.composite(tint, ph, Image.new("L", ph.size, 40)), 0.35)
    A.feather_mask("/tmp/cov_mask.png"); m = Image.open("/tmp/cov_mask.png").convert("L")
    img.paste(ph, (0, 150), m)
    # dark gradient for the text
    g = Image.new("L", (1, H), 0)
    for y in range(H): g.putpixel((0, y), int(235 * max(0, min(1, (y - 1000) / 360))))
    shade = Image.new("RGBA", (W, H), tuple(int(c * 0.45) for c in bg) + (255,)); img.paste(shade, (0, 0), g.resize((W, H)))
    d = ImageDraw.Draw(img)
    # chip
    f = A.font("Bold", 46); bb = d.textbbox((0, 0), chip, font=f, direction="rtl", language="he"); tw = bb[2] - bb[0]
    box = [W / 2 - tw / 2 - 40, 262, W / 2 + tw / 2 + 40, 346]
    gl = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).rounded_rectangle(box, radius=42, outline=acc + (190,), width=8); img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(9)))
    d = ImageDraw.Draw(img); d.rounded_rectangle(box, radius=42, fill=(14, 16, 30, 235), outline=acc + (255,), width=4); A.rtl(d, (W / 2, 305), chip, f, (255, 255, 255, 255))
    if icon:
        ic = A.draw_icon(icon, 230, 1.0, acc); img.alpha_composite(ic, (800, 380))
    # title
    lines = big if isinstance(big, (list, tuple)) else [big]
    ytop = 1275 if len(lines) == 1 else 1195
    d = ImageDraw.Draw(img); fs = fit(small, "Medium", 66, 940)
    sh_ = Image.new("RGBA", img.size, (0, 0, 0, 0)); A.rtl(ImageDraw.Draw(sh_), (W / 2, ytop + 4), small, fs, (0, 0, 0, 220)); img.alpha_composite(sh_.filter(ImageFilter.GaussianBlur(7)))
    A.rtl(ImageDraw.Draw(img), (W / 2, ytop), small, fs, (255, 255, 255, 255))
    y = ytop + 135
    for k, ln in enumerate(lines):
        fb = fit(ln, "Black", 158, 960)
        glow_text(img, (W / 2, y), ln, fb, acc if k == len(lines) - 1 else (255, 255, 255), core=None if k == len(lines) - 1 else (255, 255, 255)) if k == len(lines) - 1 else None
        if k < len(lines) - 1:
            s2 = Image.new("RGBA", img.size, (0, 0, 0, 0)); A.rtl(ImageDraw.Draw(s2), (W / 2, y + 6), ln, fb, (0, 0, 0, 220)); img.alpha_composite(s2.filter(ImageFilter.GaussianBlur(8)))
            A.rtl(ImageDraw.Draw(img), (W / 2, y), ln, fb, (255, 255, 255, 255))
        y += 160
    # signature / logo
    d = ImageDraw.Draw(img); ys = 1640
    if logo:
        lg = Image.open(logo).convert("RGBA"); r = min(420 / lg.width, 130 / lg.height); lg = lg.resize((int(lg.width * r), int(lg.height * r)), Image.LANCZOS)
        img.alpha_composite(lg, ((W - lg.width) // 2, ys - lg.height // 2 + 20))
    else:
        d.line([(W / 2 - 250, ys - 44), (W / 2 - 40, ys - 44)], fill=acc + (255,), width=3); d.line([(W / 2 + 40, ys - 44), (W / 2 + 250, ys - 44)], fill=acc + (255,), width=3)
        d.regular_polygon((W / 2, ys - 44, 11), 4, rotation=45, fill=acc + (255,))
        A.rtl(d, (W / 2, ys + 14), name, A.font("Bold", 56), (255, 255, 255, 255))
    img.convert("RGB").save(out, quality=95)

if __name__ == "__main__":
    S = "/home/claude/lesson2/src.mov"; C = "פרשת וישלח"
    cover("cover_01_hamasa_shel_yaakov.jpg", S, 1890.2, "rose", C, "המסע של כל אחד מאיתנו", ["זאת לא רחל", "זאת לאה"], "couple")
    cover("cover_02_lama_lo_hayita_aviya.jpg", S, 2471.3, "warm", C, "אחרי מאה ועשרים ישאלו", ["למה לא", "היית אביה?"], "fingerprint")
    cover("cover_03_ma_ze_bracha.jpg", S, 1796.0, "navy", C, "אנחנו רצים לרבנים להתברך", ["מה זה", "ברכה בכלל?"], "gift")
