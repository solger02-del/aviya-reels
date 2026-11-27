# Lesson 2 reel E: every period in life is a piece of the puzzle
HK = ("כל תקופה בחיים", "חתיכה מהפאזל")
KW = ("מהפאזל", "חתיכה", "חלק", "בזוגיות", "בבריאות", "הכלכלי", "הפה", "מרות", "רציני", "עצמך", "שהזוגיות", "שהעבודה", "שהבוס", "לסתום", "יציב", "שחסר", "אוסף", "משלים")
N = ["זוגיות", "עבודה", "הבוס", "כל אירוע"]; Z = "הפאזל"
SEG = [
    dict(a=2338.56, b=2340.04, layout="stage", theme="navy", hook=HK, hook_out=False, icon="arrow_up"),
    dict(a=2340.92, b=2342.18, layout="stage", theme="navy", hook=HK, hook_in=False, hook_end=1.26, icon="couple", punch=True),
    dict(a=2342.46, b=2344.96, layout="stage", theme="navy", wm="תקופה", icon="graph_up"),
    dict(a=2348.64, b=2349.40, layout="focus", theme="teal", small="אתה עובר תקופה", big="לא נפלת."),
    dict(a=2354.08, b=2356.36, layout="stage", theme="teal", wm="פאזל", icon="check_circle", punch=True),
    dict(a=2364.38, b=2367.62, layout="anim", scene="puzzle", theme="teal", hud=("חלק 1", Z, 0.25), hud_in=True, ev={"th": "teal", "names": N, "placed": [], "new": (0, 2.56), "zoom": 0}),
    dict(a=2368.16, b=2369.94, layout="stage", theme="rose", wm="זוגיות", icon="couple", hud=("חלק 1", Z, 0.25)),
    dict(a=2371.02, b=2376.74, layout="anim", scene="puzzle", theme="teal", hud=("חלק 2", Z, 0.5), ev={"th": "teal", "names": N, "placed": [0], "new": (1, 3.1), "zoom": 0}),
    dict(a=2380.52, b=2383.20, layout="stage", theme="purple", wm="הבוס", icon="lightning", hud=("חלק 3", Z, 0.5)),
    dict(a=2383.56, b=2384.68, layout="anim", scene="puzzle", theme="teal", hud=("חלק 3", Z, 0.75), ev={"th": "teal", "names": N, "placed": [0, 1], "new": (2, 0.66), "zoom": 0}, splits=[3], keys=[2], modes=["stack"]),
    dict(a=2387.72, b=2388.66, layout="stage", theme="teal", wm="אוסף", icon="check_circle", hud=("חלק 3", Z, 0.75)),
    dict(a=2389.60, b=2390.70, layout="stage", theme="teal", wm="אוסף", icon="check_circle", icon_draw=0, punch=True, hud=("חלק 3", Z, 0.75)),
    dict(a=2391.64, b=2393.68, layout="stage", theme="warm", wm="אירוע", icon="heart", hud=("חלק 4", Z, 0.75)),
    dict(a=2394.60, b=2396.50, layout="anim", scene="puzzle", theme="warm", hud=("חלק 4", Z, 1.0, (90, 210, 130)), ev={"th": "warm", "names": N, "placed": [0, 1, 2], "new": (3, 0.5), "zoom": 0}),
    dict(a=2397.44, b=2399.30, layout="endcard", theme="warm", big="מי שאתה", small="^בשביל להיות"),
]
