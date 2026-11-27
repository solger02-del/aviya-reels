# Lesson 2 reel J: Jacob prepares for Esau - scenario 1 gift, scenario 2 prayer
HK = ("יעקב נערך לעשיו", "שלושה תרחישים")
KW = ("תרחישים", "דורון", "הפתעות", "כבשים", "עיזים", "גמלים", "לרכך", "כסאח", "שקל", "העברה", "חיבוק", "שתיים", "הרוחניים", "אחלה", "ראשון")
SEG = [
    dict(a=277.72, b=280.18, layout="stage", theme="navy", hook=HK, icon="arrow_up"),
    dict(a=281.26, b=283.42, layout="stage", theme="warm", wm="דורון", icon="gift", punch=True, hud=("תרחיש 1", "דורון", 0.33), hud_in=True, modes=["line", "stack"], splits=[2, 1], keys=[0, 0]),
    dict(a=285.72, b=287.68, layout="stage", theme="warm", wm="דורון", icon="gift", icon_draw=0, hud=("תרחיש 1", "דורון", 0.33)),
    dict(a=291.36, b=294.90, layout="anim", scene="item", theme="warm", hud=("תרחיש 1", "דורון", 0.33), ev={"kind": "gifts", "th": "warm", "times": [0.06, 1.28, 2.64], "counter": ("מתנות", 3, 0.0, 2.9), "zoom": 0}, splits=[1, 1, 1], keys=[0, 0, 0], modes=["stack", "stack", "stack"]),
    dict(a=305.72, b=307.18, layout="stage", theme="warm", wm="דורון", icon="heart", punch=True, hud=("תרחיש 1", "דורון", 0.33)),
    dict(a=320.52, b=325.40, layout="anim", scene="item", theme="teal", hud=("תרחיש 1", "דורון", 0.33), ev={"kind": "doc", "th": "teal", "counter": ("העברה", 200000, 1.7, 3.1), "labels": [("העברה לחשבון", 1.76, 540, 740)]}),
    dict(a=326.96, b=330.36, layout="stage", theme="rose", wm="חיבוק", icon="couple", hud=("תרחיש 1", "דורון", 0.33)),
    dict(a=336.28, b=337.42, layout="stage", theme="navy", wm="שתיים", icon="arrow_up", punch=True, hud=("תרחיש 2", "תפילה", 0.66)),
    dict(a=339.46, b=340.96, layout="stage", theme="navy", wm="רוחני", icon="lightning", hud=("תרחיש 2", "תפילה", 0.66)),
    dict(a=341.56, b=343.20, layout="endcard", theme="navy", big="תפילה.", small="^מה עושים?", tail=0.5),
]
