# Lesson 2 reel D: Esau returns = your fears from childhood
HK = ("יעקב פוגש את עשיו", "הפחדים שלך")
KW = ("עשיו", "הפחדים", "הדמיונות", "הקירות", "מפחד", "בילדות", "חזק", "השדים", "יעקב", "חיבקו", "עובר", "עושה", "המלחמות", "ומהמלחמות", "להתמודד")
RED = (235, 80, 80); Q = "הקירות"
SEG = [
    dict(a=1978.28, b=1981.38, layout="stage", theme="navy", hook=HK, icon="arrow_up"),
    dict(a=1982.48, b=1985.46, layout="stage", theme="purple", wm="עשיו", icon="lightning", punch=True),
    dict(a=1986.38, b=1987.36, layout="stage", theme="purple", wm="פחד", icon="lightning", icon_draw=0, splits=[3], keys=[1], modes=["stack"]),
    dict(a=1988.08, b=1989.10, layout="stage", theme="purple", wm="פחד", icon="lightning", icon_draw=0, punch=True, splits=[3], keys=[1], modes=["stack"]),
    dict(a=1989.72, b=1993.60, layout="anim", scene="wall", theme="purple", hud=("פחד", Q, 0.45, RED), hud_in=True, ev={"th": "purple", "r0": 0, "r1": 6, "zoom": 0, "labels": [("לא עובר", 3.3, 330, 870)]}),
    dict(a=1994.14, b=1995.12, layout="anim", scene="wall", theme="purple", hud=("פחד", Q, 0.7, RED), ev={"th": "purple", "r0": 6, "r1": 8, "zoom": 0, "labels": [("לא עושה", 0.4, 330, 750)]}),
    dict(a=1995.44, b=1997.62, layout="anim", scene="wall", theme="purple", hud=("פחד", Q, 1.0, RED), ev={"th": "purple", "r0": 8, "r1": 10, "zoom": 0, "labels": [("גדול עליי", 0.2, 330, 620), ("מפחד", 1.46, 330, 480)]}),
    dict(a=1998.80, b=2003.62, layout="stage", theme="rose", wm="ילדות", icon="house_heart", fix={"לא,": ""}),
    dict(a=2004.34, b=2007.96, layout="stage", theme="purple", wm="הילדות", icon="lightning", punch=True),
    dict(a=2008.68, b=2009.96, layout="stage", theme="navy", wm="עשיו", icon="couple"),
    dict(a=2011.14, b=2013.02, layout="stage", theme="navy", wm="עשיו", icon="couple", icon_draw=0, punch=True),
    dict(a=2014.88, b=2016.08, layout="burst", theme="warm", wm="יעקב", splits=[2], keys=[0], modes=["stack"], big=130),
    dict(a=2017.06, b=2018.90, layout="endcard", theme="warm", big="יעקב", small="^יצא ממך"),
]
