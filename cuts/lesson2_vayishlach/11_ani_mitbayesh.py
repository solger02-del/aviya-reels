# Lesson 2 reel K: Jacob's prayer - "I am ashamed to turn to You"
HK = ("התפילה של יעקב", "אני מתבייש")
KW = ("מתבייש", "שהבטחת", "שנים", "חטאתי", "רלוונטי", "התקלקלתי", "הרוחנית", "טובים", "במקלי", "הירדן", "מחנות", "אושר", "אולי", "התפילה")
Q = "רוחנית"
SEG = [
    dict(a=364.48, b=369.14, layout="stage", theme="navy", hook=HK, icon="bubble_heart"),
    dict(a=369.98, b=370.86, layout="stage", theme="purple", wm="מתבייש", punch=True, splits=[2], keys=[1], modes=["stack"]),
    dict(a=417.72, b=420.02, layout="stage", theme="navy", wm="הבטחת", icon="check_circle"),
    dict(a=421.06, b=422.54, layout="stage", theme="navy", wm="הבטחת", icon="check_circle", icon_draw=0, punch=True),
    dict(a=427.40, b=428.30, layout="stage", theme="purple", wm="אולי", icon="lightning", hud=("אולי", Q, 0.8, (245, 190, 60)), hud_in=True, splits=[2], keys=[1], modes=["stack"]),
    dict(a=429.50, b=433.66, layout="stage", theme="purple", wm="אולי", icon="lightning", icon_draw=0, punch=True, hud=("אולי", Q, 0.55, (245, 190, 60))),
    dict(a=438.02, b=441.50, layout="stage", theme="purple", wm="אולי", icon="lightning", icon_draw=0, hud=("אולי", Q, 0.25, (235, 80, 80))),
    dict(a=452.16, b=453.08, layout="stage", theme="teal", wm="טוב", icon="heart", punch=True),
    dict(a=454.40, b=456.42, layout="stage", theme="teal", wm="טוב", icon="heart", icon_draw=0),
    dict(a=457.24, b=458.86, layout="anim", scene="staff", theme="warm", avatar_size=220, avatar_pos=(830, 150), ev={"ring": 0.2, "label": 0.2, "zoom": 0.02}),
    dict(a=466.52, b=468.12, layout="anim", scene="camps", theme="warm", avatar_size=220, avatar_pos=(830, 150), ev={"tent": [0.66, 0.8], "label": 0.7, "label_text": "שני מחנות", "banks": 99, "coins": 99, "z0": 0.02, "zoom": 0.03}),
    dict(a=468.74, b=470.26, layout="burst", theme="warm", wm="אושר", splits=[2, 4], keys=[1, 1], modes=["line", "stack"], big=160),
    dict(a=355.16, b=357.86, layout="endcard", theme="warm", big="קטונתי", small="מכל החסדים ומכל האמת", tail=0.5),
]
