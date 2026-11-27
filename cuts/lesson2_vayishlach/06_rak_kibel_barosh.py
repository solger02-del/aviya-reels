# Lesson 2 reel F: from the moment he got the blessings - not one minute of peace
HK = ("יעקב קיבל את הברכות", "ורק קיבל בראש")
KW = ("בראש", "עשיו", "נשדד", "עקץ", "בלאה", "משכורתו", "הלידה", "בסדר", "ההורים", "להרוג", "לבן", "הברכה")
def nh(k, p): return ("מכה %d" % k, "נחת", p, (90, 210, 130) if p > 0.66 else (245, 190, 60) if p > 0.33 else (235, 80, 80))
SEG = [
    dict(a=1566.10, b=1569.58, layout="stage", theme="navy", hook=HK, icon="gift"),
    dict(a=1574.20, b=1575.40, layout="stage", theme="purple", icon="house_heart", punch=True, hud=nh(1, 0.86), hud_in=True),
    dict(a=1576.00, b=1577.08, layout="stage", theme="navy", icon="lightning", hud=nh(2, 0.72)),
    dict(a=1579.28, b=1581.20, layout="stage", theme="purple", icon="staff", punch=True, hud=nh(3, 0.58), modes=["line", "stack"]),
    dict(a=1582.44, b=1583.68, layout="stage", theme="navy", icon="house_heart", hud=nh(4, 0.58)),
    dict(a=1583.98, b=1584.96, layout="stage", theme="navy", icon="lightning", punch=True, hud=nh(4, 0.44), splits=[3], keys=[1], modes=["stack"]),
    dict(a=1587.10, b=1588.72, layout="stage", theme="rose", icon="couple", hud=nh(5, 0.30)),
    dict(a=1590.22, b=1592.16, layout="stage", theme="purple", icon="graph_up", punch=True, hud=nh(6, 0.20)),
    dict(a=1595.04, b=1597.12, layout="stage", theme="navy", icon="staff", hud=nh(7, 0.20)),
    dict(a=1598.52, b=1599.22, layout="focus", theme="purple", small="מי מחכה לו שם?", big="עשיו."),
    dict(a=1601.48, b=1603.80, layout="stage", theme="rose", icon="heart", punch=True, hud=nh(8, 0.06)),
    dict(a=1620.18, b=1622.70, layout="stage", theme="teal", wm="אוהלים", icon="check_circle", fix={"אשתו": "איש־תם"}),
    dict(a=1623.02, b=1624.62, layout="stage", theme="warm", wm="הברכה", icon="gift", punch=True),
    dict(a=1624.60, b=1626.86, layout="endcard", theme="warm", big="דקה של נחת", small="^אין לו"),
]
