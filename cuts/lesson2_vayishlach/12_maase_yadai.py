# Lesson 2 reel L: "My handiwork is drowning in the sea" - rejoice in the salvation, not in the fall
HK = ("בן אדם עשה לי רע", "והוא קיבל כאפה")
KW = ("כאפה", "הכוכבים", "שירה", "שירה?", "טובעים", "המכה", "מכה", "הישועה", "ההצלה", "משמעותי", "קטן", "רע", "בים")
SEG = [
    dict(a=867.60, b=870.04, layout="stage", theme="navy", hook=HK, icon="lightning"),
    dict(a=876.85, b=880.28, layout="stage", theme="purple", wm="הגיע לו", icon="lightning", punch=True),
    dict(a=895.28, b=896.97, layout="stage", theme="navy", wm="שירה", icon="bubble_heart"),
    dict(a=901.88, b=905.24, layout="stage", theme="navy", wm="שירה", icon="bubble_heart", icon_draw=0, punch=True, fix={"טובים": "טובעים"}),
    dict(a=911.60, b=913.70, layout="quote", theme="navy", lines=["מעשה ידיי טובעים בים", "ואתם אומרים שירה?"]),
    dict(a=997.16, b=1000.40, layout="stage", theme="purple", wm="המכה", icon="lightning"),
    dict(a=1000.70, b=1004.84, layout="anim", scene="switch", theme="rose", ev={"th": "teal", "off": "על המכה", "on": "על הישועה", "flip": 0.8, "zoom": 0}),
    dict(a=1005.08, b=1007.06, layout="stage", theme="teal", wm="הבדל", icon="check_circle", punch=True),
    dict(a=1010.04, b=1011.80, layout="focus", theme="purple", small="בנפול אויביך", big="אל תשמח."),
    dict(a=1173.70, b=1175.30, layout="endcard", theme="warm", big="ישועת השם", small="^אני אשמח על", tail=0.5),
]
