# Lesson 2 (Vayishlach) reel A: everyone walks Jacob's journey - "זאת לא רחל, זאת לאה"
HK = ("כל אחד מאיתנו", "המסע של יעקב")
KW = ("רחל", "לאה", "בורח", "חלומות", "כלום", "דלפון", "שקל", "היעד", "מהילדות", "המסע", "מההורים", "להתחתן", "החלום", "חזק")
J = "המסע"; RED = (235, 80, 80)
SEG = [
    dict(a=1876.58, b=1880.16, layout="stage", theme="navy", hook=HK, icon="staff"),
    dict(a=1881.94, b=1882.74, layout="stage", theme="navy", icon="house_heart", hud=("בורח", J, 0.10), hud_in=True),
    dict(a=1883.80, b=1884.90, layout="stage", theme="navy", icon="house_heart", icon_draw=0, punch=True, hud=("בורח", J, 0.10)),
    dict(a=1887.92, b=1888.96, layout="stage", theme="navy", icon="house_heart", icon_draw=0, hud=("בורח", J, 0.12), modes=["stack"]),
    dict(a=1889.62, b=1891.24, layout="stage", theme="navy", icon="house_heart", icon_draw=0, punch=True, hud=("בורח", J, 0.14)),
    dict(a=1895.04, b=1901.38, layout="anim", scene="path", theme="teal", hud=("יוצא לעולם", J, 0.28),
         ev={"p0": 0.0, "p1": 0.78, "T0": 0.0, "smile": True, "no_hud": True, "zoom": 0, "labels": [("יוצא לעולם", 1.78), ("כל הטוב", (4.3, 290, 1090))]}),
    dict(a=1901.60, b=1904.66, layout="anim", scene="path", theme="teal", hud=("נשדד", J, 0.28, RED),
         ev={"p0": 0.78, "p1": 0.86, "move": 1.0, "T0": 6.34, "rob": 1.44, "no_hud": True, "zoom": 0, "labels": [("בלי כלום", 2.54)]}),
    dict(a=1907.92, b=1910.42, layout="stage", theme="purple", icon="lightning", hud=("בלי שקל", J, 0.34, RED)),
    dict(a=1915.76, b=1917.42, layout="stage", theme="rose", icon="heart", hud=("חלומות", J, 0.46)),
    dict(a=1917.94, b=1920.36, layout="stage", theme="rose", icon="couple", punch=True, hud=("חלומות", J, 0.50)),
    dict(a=1922.40, b=1924.86, layout="stage", theme="rose", icon="couple", icon_draw=0, hud=("רחל", J, 0.60), modes=["line", "stack"]),
    dict(a=1925.80, b=1929.64, layout="stage", theme="purple", icon="lightning", punch=True, hud=("רחל", J, 0.62, RED)),
    dict(a=1934.68, b=1935.82, layout="focus", theme="purple", small="זאת לא רחל", big="זאת לאה."),
    dict(a=1936.94, b=1938.64, layout="stage", theme="navy", icon="arrow_up", hud=("לאה", J, 0.72)),
    dict(a=1939.08, b=1940.14, layout="anim", scene="path", theme="navy", hud=("רץ", J, 0.80),
         ev={"th": "navy", "p0": 0.0, "p1": 0.62, "T0": 0.0, "pace": 3.4, "no_hud": True, "zoom": 0}, modes=["stack"]),
    dict(a=1940.50, b=1942.88, layout="anim", scene="path", theme="navy", hud=("היעד", J, 0.86, RED),
         ev={"th": "navy", "p0": 0.62, "p1": 1.0, "move": 0.85, "T0": 1.06, "pace": 3.4, "xgift": 1.42, "no_hud": True, "zoom": 0, "labels": [("לא היעד שלך", (1.5, 400, 770))]}),
    dict(a=1951.60, b=1954.72, layout="stage", theme="warm", icon="heart", hud=("ממשיך", J, 0.92)),
    dict(a=1954.78, b=1956.50, layout="stage", theme="warm", icon="heart", icon_draw=0, punch=True, hud=("ממשיך", J, 1.0)),
    dict(a=1957.58, b=1959.92, layout="endcard", theme="warm", big="הבחירות", small="שלא בחרת לבחור"),
]
