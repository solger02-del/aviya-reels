# Lesson 2 reel C: what is a blessing - "לא מהדלת שחשבנו"
HK = ("אנחנו רצים לרבנים", "מה זה ברכה?")
KW = ("ברכה", "הברכה", "הברכות", "מהדלת", "הדלת", "למבורגיני", "כסף", "ישראל", "כולנו", "עמוקה", "להתברך", "ההתמודדויות", "והייסורים", "והאתגרים", "והמסע", "מזווית")
SEG = [
    dict(a=1717.20, b=1718.32, layout="stage", theme="navy", hook=HK, hook_out=False, icon="gift", splits=[4], keys=[2], modes=["line"]),
    dict(a=1706.78, b=1708.02, layout="stage", theme="navy", hook=HK, hook_in=False, hook_end=1.24, icon="gift", icon_draw=0, punch=True),
    dict(a=1710.24, b=1711.62, layout="stage", theme="navy", wm="ברכה", icon="gift", icon_draw=0),
    dict(a=1737.14, b=1738.68, layout="stage", theme="teal", wm="ברכה", icon="check_circle", punch=True),
    dict(a=1739.02, b=1740.96, layout="anim", scene="item", theme="warm", ev={"kind": "car", "th": "warm", "in": 1.0, "labels": [("בחניה", 1.5, 540, 800)]}),
    dict(a=1742.60, b=1744.16, layout="stage", theme="teal", wm="הברכות", icon="check_circle", icon_draw=0),
    dict(a=1780.74, b=1781.80, layout="stage", theme="navy", wm="ברכה", icon="gift", punch=True),
    dict(a=1782.68, b=1786.36, layout="anim", scene="doors", theme="navy", hud=("מחכים", "ברכה", 0.05, (235, 80, 80)), hud_in=True, ev={"th": "navy", "zoom": 0, "labels": [("הדלת שחשבנו", 2.04, 800, 850)]}),
    dict(a=1787.52, b=1791.26, layout="anim", scene="doors", theme="navy", hud=("הגיעה", "ברכה", 1.0, (90, 210, 130)), ev={"th": "navy", "zoom": 0, "open_b": 0.3, "labels": [("הדלת שחשבנו", -1, 800, 850), ("מזווית אחרת", 0.7, 280, 850)]}),
    dict(a=1794.66, b=1797.74, layout="stage", theme="purple", wm="כסף", icon="graph_up"),
    dict(a=1798.44, b=1799.28, layout="focus", theme="purple", small="אבל זה", big="לא נכון."),
    dict(a=1800.52, b=1802.78, layout="stage", theme="warm", wm="הברכה", icon="heart"),
    dict(a=1803.66, b=1804.64, layout="stage", theme="warm", wm="כולנו", icon="heart", icon_draw=0, punch=True),
    dict(a=1806.04, b=1806.90, layout="burst", theme="warm", wm="ישראל", splits=[2], keys=[1], modes=["stack"], big=170),
    dict(a=1865.60, b=1867.90, layout="stage", theme="purple", wm="דווקא", icon="lightning"),
    dict(a=1868.46, b=1869.36, layout="stage", theme="purple", wm="דווקא", icon="lightning", icon_draw=0, punch=True),
    dict(a=1869.78, b=1870.72, layout="stage", theme="purple", wm="דווקא", icon="lightning", icon_draw=0),
    dict(a=1871.10, b=1872.34, layout="stage", theme="purple", wm="המסע", icon="staff", punch=True),
    dict(a=1872.64, b=1874.50, layout="endcard", theme="warm", big="הברכה", small="^משמה באה"),
]
