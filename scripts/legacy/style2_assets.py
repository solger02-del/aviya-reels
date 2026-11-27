# Graphic assets for the "premium light" reel style (rounded cards, geometric light background, text cards).
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
import numpy as np, os

W, H = 1080, 1920
FONTS = "/home/claude/reel_work/fonts"

def font(weight, size):
    return ImageFont.truetype(f"{FONTS}/Heebo-{weight}.ttf", size, layout_engine=ImageFont.Layout.RAQM)

def rounded_mask(w, h, r, ss=3):
    m = Image.new("L", (w * ss, h * ss), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w * ss - 1, h * ss - 1], radius=r * ss, fill=255)
    return m.resize((w, h), Image.LANCZOS)

def geo_background(path, seed=0, tint=(246, 244, 245)):
    """Light gradient with soft diagonal rounded bars (gray/black/pink), like the reference."""
    rng = np.random.default_rng(seed)
    y = np.linspace(0, 1, H)[:, None]
    base = np.array(tint, float)[None, None, :] * (1 - 0.05 * y[..., None]) * np.ones((1, W, 1))
    img = Image.fromarray(base.clip(0, 255).astype(np.uint8)).convert("RGBA")
    bars = [((-120, 80), 520, 170, (40, 40, 44), 210), ((760, -60), 420, 150, (120, 120, 126), 150),
            ((820, 1500), 560, 190, (30, 30, 34), 200), ((-80, 1640), 480, 150, (232, 150, 178), 150),
            ((640, 360), 360, 120, (236, 170, 196), 110), ((-60, 1180), 300, 110, (150, 150, 156), 120)]
    for (x0, y0), L, T, col, a in bars:
        layer = Image.new("RGBA", (L + 400, L + 400), (0, 0, 0, 0))
        g = Image.new("RGBA", (L, T), col + (a,))
        # gradient along the bar
        grad = np.linspace(1.0, 0.45, L)[None, :] * np.ones((T, 1))
        alpha = (grad * a).astype(np.uint8)
        g.putalpha(Image.fromarray(alpha))
        m = rounded_mask(L, T, T // 2)
        g.putalpha(ImageChops.multiply(g.getchannel("A"), m))
        layer.paste(g, (200, 200 + (L - T) // 2), g)
        layer = layer.rotate(-38 + rng.uniform(-3, 3), resample=Image.BICUBIC)
        img.alpha_composite(layer, (int(x0) - 200, int(y0) - 200))
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    img.convert("RGB").save(path)

def card_frame(path_mask, path_overlay, w, h, r, border=6, pill=False):
    """Mask for the speaker inside the card + overlay (thin white border + soft drop shadow)."""
    rr = min(w, h) // 2 if pill else r
    rounded_mask(w, h, rr).save(path_mask)
    pad = 60
    ov = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("L", ov.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle([pad, pad + 14, pad + w, pad + h + 14], radius=rr, fill=110)
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    shadow = Image.new("RGBA", ov.size, (0, 0, 0, 0)); shadow.putalpha(sh)
    ov.alpha_composite(shadow)
    bd = Image.new("RGBA", ((w + 2 * pad) * 3, (h + 2 * pad) * 3), (0, 0, 0, 0))
    ImageDraw.Draw(bd).rounded_rectangle([pad * 3 - border * 3, pad * 3 - border * 3, (pad + w) * 3 + border * 3, (pad + h) * 3 + border * 3],
                                         radius=(rr + border) * 3, outline=(255, 255, 255, 235), width=border * 3)
    ov.alpha_composite(bd.resize(ov.size, Image.LANCZOS))
    # cut the inside out of the shadow so the speaker stays clean
    inner = Image.new("L", ov.size, 0); inner.paste(rounded_mask(w, h, rr), (pad, pad))
    a = ImageChops.subtract(ov.getchannel("A"), inner); ov.putalpha(a)
    ov.save(path_overlay)
    return pad

def number_pill(path, w, h, num):
    """Small pill with a warm gradient and a big thin number (stands in for the reference's photo pill)."""
    y = np.linspace(0, 1, h)[:, None]
    top, bot = np.array([246, 205, 170]), np.array([226, 120, 150])
    g = (top[None, None, :] * (1 - y[..., None]) + bot[None, None, :] * y[..., None]) * np.ones((1, w, 1))
    img = Image.fromarray(g.astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img)
    f = font("Light", int(h * 0.62))
    d.text((w / 2, h * 0.48), num, font=f, fill=(255, 255, 255, 255), anchor="mm")
    img.putalpha(rounded_mask(w, h, w // 2))
    img.save(path)

def text_card(path, title, sub, seed=1, title_size=176, sub_size=88):
    """Full-screen typography card on the geometric background: dark bold title + light subtitle (RTL)."""
    geo_background(path, seed=seed)
    img = Image.open(path).convert("RGBA")
    d = ImageDraw.Draw(img)
    ft, fs = font("Bold", title_size), font("Light", sub_size)
    y = 800
    for line in title.split("\n"):
        d.text((W - 140, y), line, font=ft, fill=(34, 34, 38), anchor="ra", direction="rtl", language="he"); y += int(title_size * 1.18)
    y += 30
    for line in sub.split("\n"):
        d.text((W - 140, y), line, font=fs, fill=(80, 80, 88), anchor="ra", direction="rtl", language="he"); y += int(sub_size * 1.3)
    img.convert("RGB").save(path)

def focus_text(path, small, big):
    """Transparent overlay for the blurred-speaker moment: small word, big word, thin line."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.text((W / 2, 760), small, font=font("Light", 64), fill=(255, 255, 255, 235), anchor="mm", direction="rtl", language="he")
    d.text((W / 2, 900), big, font=font("Regular", 150), fill=(255, 255, 255, 255), anchor="mm", direction="rtl", language="he")
    d.line([(W / 2 - 150, 1030), (W / 2 + 150, 1030)], fill=(255, 255, 255, 230), width=4)
    img.save(path)
