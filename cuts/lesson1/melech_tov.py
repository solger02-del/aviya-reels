# Reel 9: why was the world created - "מלך טוב ורוצה להיטיב"
HK = ("אחת השאלות", "למה ברא את העולם?")
FX = {"הכבול": "אקמול"}
SEG = [
    dict(a=1014.40, b=1015.21, layout="stage", theme="navy", hook=HK, hook_out=False, icon="bubble_heart", splits=[5], keys=[4], modes=["line"]),
    dict(a=1016.08, b=1017.80, layout="stage", theme="navy", hook=HK, hook_in=False, hook_end=1.72, icon="bubble_heart", icon_draw=0, punch=True, splits=[4,3,4], keys=[1,2,2], modes=["line","line","line"]),
    dict(a=1019.14, b=1021.30, layout="stage", theme="purple", wm="כאב", meter={"t0": 0.5, "t1": 1.5, "label": "כאב ראש"}, splits=[4,2,3], keys=[2,1,0], modes=["stack","line","line"]),
    dict(a=1022.60, b=1026.32, layout="anim", scene="pills", theme="purple", fix=FX, ev={"x": 1.64, "zoom": 0.04}, cap_y=1560, splits=[4,2,2,2,3], keys=[2,1,0,1,0], modes=["line","line","line","line","line"]),
    dict(a=1035.70, b=1037.66, layout="stage", theme="teal", wm="הגדול", icon="check_circle", splits=[3,3], keys=[2,2], modes=["line","stack"]),
    dict(a=1037.82, b=1039.24, layout="stage", theme="teal", wm="חז״ל", icon="check_circle", icon_draw=0, punch=True, splits=[2,2], keys=[1,0], modes=["line","line"]),
    dict(a=1039.26, b=1041.72, layout="quote", theme="warm", lines=["הקדוש ברוך הוא מלך טוב", "והוא רוצה להיטיב"]),
    dict(a=1043.30, b=1044.60, layout="stage", theme="warm", wm="להיטיב", icon="gift", splits=[3,2], keys=[2,1], modes=["stack","line"]),
    dict(a=1044.62, b=1046.94, layout="anim", scene="path", theme="teal", ev={"p0": 0.0, "p1": 0.42, "T0": 0.0, "left": "שלב 1", "labels": [("עובדים קשה", 1.40)], "sweat": 1.40, "zoom": 0, "hud_in": True}, splits=[4,2,3], keys=[2,0,2], modes=["line","line","stack"]),
    dict(a=1047.32, b=1048.30, layout="anim", scene="path", theme="teal", ev={"p0": 0.42, "p1": 0.62, "T0": 2.32, "left": "שלב 2", "labels": [("מתנסים", 0.08)], "zoom": 0}, splits=[2], keys=[0], modes=["stack"]),
    dict(a=1048.62, b=1049.91, layout="anim", scene="path", theme="teal", ev={"p0": 0.62, "p1": 0.88, "T0": 3.30, "left": "שלב 3", "zoom": 0}, splits=[2,3], keys=[0,2], modes=["line","line"]),
    dict(a=1049.91, b=1051.16, layout="anim", scene="path", theme="teal", ev={"p0": 0.88, "p1": 1.0, "T0": 4.59, "move": 0.4, "open": 0.42, "left": "שלב 3", "labels": [("לפנק אותנו", 0.5)], "zoom": 0}, splits=[5], keys=[3], modes=["stack"]),
    dict(a=1052.84, b=1054.40, layout="stage", theme="warm", wm="העולם", icon="heart", splits=[3,3], keys=[2,2], modes=["line","line"]),
    dict(a=1054.80, b=1056.58, layout="endcard", theme="warm", big="להיטיב", small="כי הוא רוצה"),
]
