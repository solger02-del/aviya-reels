# Lesson 2 reel G: Esau came to bite - God flipped the switch, from enemy to lover
HK = ("יעקב פוגש את עשיו", "מאויב לאוהב")
KW = ("לנשוך", "הסוויץ", "לאויבים", "love", "מחליט", "ליבות", "לחץ", "קוד", "מאויב", "אחד", "בצוואר")
SEG = [
    dict(a=1436.48, b=1438.40, layout="stage", theme="purple", hook=HK, hook_out=False, icon="lightning"),
    dict(a=1438.98, b=1440.66, layout="stage", theme="navy", hook=HK, hook_in=False, hook_end=1.68, icon="arrow_up", punch=True),
    dict(a=1441.16, b=1443.32, layout="stage", theme="purple", wm="אויבים", icon="lightning", fix={"לאוינים": "לאויבים"}),
    dict(a=1443.76, b=1444.88, layout="stage", theme="purple", wm="סוויץ׳", punch=True, splits=[3], keys=[2], modes=["stack"]),
    dict(a=1445.58, b=1447.38, layout="stage", theme="rose", wm="LOVE", icon="heart"),
    dict(a=1448.92, b=1451.46, layout="stage", theme="navy", wm="מחליט", icon="heart", punch=True),
    dict(a=1452.42, b=1453.32, layout="anim", scene="switch", theme="rose", hud=("עשיו", "אהבה", 0.5, (245, 190, 60)), hud_in=True, ev={"th": "rose", "flip": 0.3, "zoom": 0}, modes=["stack"]),
    dict(a=1453.62, b=1455.12, layout="anim", scene="switch", theme="rose", hud=("עשיו", "אהבה", 1.0, (90, 210, 130)), ev={"th": "rose", "flip": -1, "zoom": 0}),
    dict(a=1458.24, b=1460.42, layout="stage", theme="purple", wm="אויב", icon="lightning", punch=True),
    dict(a=1461.16, b=1462.72, layout="endcard", theme="rose", big="לאוהב", small="הכי גדול", tail=0.5),
]
