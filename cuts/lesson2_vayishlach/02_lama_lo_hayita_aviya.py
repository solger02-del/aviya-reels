# Lesson 2 reel B: after 120 - "למה לא היית אביה?"
HK = ("אחרי מאה ועשרים", "מה הבאתם לי?")
KW = ("אביה", "אותנו", "ירייה", "הבאתם", "מעלה", "עולם", "בעולם", "אחד", "להיות", "חשבון", "המפתחות", "רלוונטי", "עובד", "הוא", "שחסר")
RED = (235, 80, 80); GRN = (90, 210, 130); R = "רלוונטי"
SEG = [
    dict(a=2409.08, b=2411.16, layout="stage", theme="navy", hook=HK, hook_out=False, icon="arrow_up"),
    dict(a=2412.50, b=2413.72, layout="stage", theme="navy", hook=HK, hook_in=False, hook_end=1.22, icon="arrow_up", icon_draw=0, punch=True),
    dict(a=2414.74, b=2416.12, layout="stage", theme="navy", wm="למעלה", icon="arrow_up", icon_draw=0),
    dict(a=2417.44, b=2418.72, layout="stage", theme="purple", wm="הבאתם", punch=True, splits=[4, 3], keys=[2, 1], modes=["line", "stack"]),
    dict(a=2420.54, b=2421.80, layout="anim", scene="item", theme="purple", hud=("פריט 1", R, 0.5, (245, 190, 60)), hud_in=True, ev={"kind": "doc", "th": "purple", "labels": [("פירוט חשבון", 0.44, 540, 740)]}),
    dict(a=2422.54, b=2423.50, layout="anim", scene="item", theme="purple", hud=("פריט 1", R, 0.04, RED), ev={"kind": "doc", "th": "purple", "in": -1, "x": 0.08, "z0": 0.03, "labels": [("פירוט חשבון", -1, 540, 740)]}, modes=["stack"]),
    dict(a=2426.62, b=2427.92, layout="anim", scene="item", theme="purple", hud=("פריט 2", R, 0.5, (245, 190, 60)), ev={"kind": "keys", "th": "purple", "labels": [("המפתחות", 0.3, 540, 740)]}),
    dict(a=2431.96, b=2432.72, layout="anim", scene="item", theme="purple", hud=("פריט 2", R, 0.04, RED), ev={"kind": "keys", "th": "purple", "in": -1, "x": 0.08, "z0": 0.03, "labels": [("המפתחות", -1, 540, 740)]}, modes=["stack"]),
    dict(a=2434.20, b=2435.72, layout="stage", theme="teal", wm="להביא", icon="check_circle"),
    dict(a=2437.20, b=2438.36, layout="anim", scene="item", theme="warm", hud=("פריט 3", R, 1.0, GRN), ev={"kind": "me", "th": "warm", "ok": 0.4, "labels": [("אותנו", 0.4, 540, 560)]}, splits=[3], keys=[2], modes=["stack"]),
    dict(a=2439.50, b=2441.48, layout="stage", theme="purple", wm="ישאלו", icon="bubble_heart"),
    dict(a=2447.90, b=2448.78, layout="stage", theme="purple", wm="ישאלו", icon="bubble_heart", icon_draw=0, punch=True),
    dict(a=2449.68, b=2450.74, layout="stage", theme="warm", wm="אביה", punch=True, splits=[4], keys=[3], modes=["stack"], big=170),
    dict(a=2458.24, b=2461.66, layout="stage", theme="warm", wm="אתה", icon="fingerprint", splits=[3, 4, 4], keys=[2, 0, 3], modes=["line", "line", "line"]),
    dict(a=2462.84, b=2464.02, layout="stage", theme="warm", wm="אתה", icon="fingerprint", icon_draw=0, punch=True),
    dict(a=2468.04, b=2469.74, layout="burst", theme="warm", wm="אחד", splits=[3, 3], keys=[1, 1], modes=["line", "stack"], big=160),
    dict(a=2470.56, b=2471.94, layout="stage", theme="warm", wm="אחת", icon="fingerprint", icon_draw=0, punch=True, splits=[5], keys=[3], modes=["stack"]),
    dict(a=2472.98, b=2474.80, layout="endcard", theme="warm", big="ירייה אחת", small="פספסת, נסעת."),
]
