# Lesson 2 reel I: sentences better kept unsaid - mom's schnitzels
HK = ("יש משפטים", "שכדאי לגנוז")
KW = ("לגנוז", "שניצל", "השניצלים", "שניצלים", "שניצלים?", "אמא", "טעימים", "הביתה", "צהריים", "טוב", "משפטים", "רגע")
SEG = [
    dict(a=787.36, b=788.90, layout="stage", theme="navy", hook=HK, hook_out=False, icon="bubble_heart"),
    dict(a=792.02, b=793.42, layout="stage", theme="navy", hook=HK, hook_in=False, hook_end=1.4, icon="house_heart", punch=True),
    dict(a=793.60, b=794.86, layout="stage", theme="rose", wm="צהריים", icon="couple"),
    dict(a=795.42, b=796.02, layout="anim", scene="item", theme="warm", ev={"kind": "plate", "th": "warm", "labels": [("שניצל", 0.1, 540, 760)]}, nocap=True),
    dict(a=796.36, b=798.72, layout="stage", theme="purple", wm="אמא", icon="lightning", punch=True),
    dict(a=802.14, b=803.26, layout="stage", theme="purple", wm="אמא", icon="lightning", icon_draw=0),
    dict(a=804.04, b=805.02, layout="stage", theme="purple", wm="לא טוב", icon="lightning", icon_draw=0, punch=True),
    dict(a=806.26, b=808.40, layout="anim", scene="item", theme="warm", ev={"kind": "plate", "th": "warm", "in": -1, "x": 0.2, "labels": [("שניצל", -1, 540, 760)]}, fix={"יתעשה": "ייעשו"}),
    dict(a=820.42, b=822.78, layout="endcard", theme="warm", big="לגנוז", small="^יש משפטים שכדאי", tail=0.6),
]
