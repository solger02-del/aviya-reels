# Lesson 2 reel H: coming to God with an invoice
HK = ("התפללתי היום טוב?", "בא עם חשבונית")
KW = ("חשבונית", "מתפלל", "התפללתי", "קדימה", "מאיץ", "הבקשה", "התיק", "לסוגיה", "הספר", "רשימה", "ברשימה", "טוב", "יפה")
RED = (235, 80, 80)
SEG = [
    dict(a=649.46, b=654.18, layout="stage", theme="navy", hook=HK, icon="bubble_heart"),
    dict(a=661.08, b=662.16, layout="anim", scene="item", theme="purple", ev={"kind": "doc", "th": "purple", "labels": [("חשבונית", 0.44, 540, 740)]}, splits=[4], keys=[3], modes=["stack"]),
    dict(a=663.18, b=665.26, layout="stage", theme="purple", wm="חשבונית", icon="bubble_heart", punch=True),
    dict(a=667.10, b=667.98, layout="stage", theme="purple", wm="חשבונית", icon="check_circle", splits=[2], keys=[0], modes=["stack"]),
    dict(a=674.22, b=675.70, layout="anim", scene="item", theme="purple", ev={"kind": "doc", "th": "purple", "in": -1, "x": 0.9, "labels": [("חשבונית", -1, 540, 740)]}),
    dict(a=683.38, b=685.44, layout="stage", theme="navy", wm="מאיץ", icon="lightning", punch=True),
    dict(a=685.66, b=687.06, layout="stage", theme="navy", wm="מאיץ", icon="lightning", icon_draw=0),
    dict(a=689.02, b=689.86, layout="focus", theme="teal", small="אומרים לו", big="חכה רגע."),
    dict(a=691.22, b=692.86, layout="stage", theme="teal", wm="התיק", icon="arrow_up"),
    dict(a=693.96, b=695.70, layout="stage", theme="teal", wm="התיק", icon="arrow_up", icon_draw=0, punch=True),
    dict(a=696.00, b=697.42, layout="anim", scene="item", theme="purple", hud=("נפתח", "הספר", 0.5, (245, 190, 60)), hud_in=True, ev={"kind": "book", "th": "purple", "labels": [("הספר של בן אדם", 0.4, 540, 740)]}),
    dict(a=698.04, b=699.80, layout="anim", scene="item", theme="purple", hud=("נפתח", "הספר", 1.0, RED), ev={"kind": "book", "th": "purple", "in": -1, "x": 1.36, "z0": 0.03, "labels": [("הספר של בן אדם", -1, 540, 740)]}),
    dict(a=732.94, b=736.14, layout="stage", theme="warm", wm="מגיע", icon="graph_up"),
    dict(a=737.20, b=740.72, layout="stage", theme="warm", wm="מגיע", icon="graph_up", icon_draw=0, punch=True),
    dict(a=741.40, b=742.48, layout="endcard", theme="warm", big="הפתעות", small="^עוד כל מיני", tail=0.7),
]
