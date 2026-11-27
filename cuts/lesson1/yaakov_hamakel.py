# Reel 8: Jacob - from a staff to two camps ("שני בנקים")
CARDS = [("1", "אז", "רק עם המקל", "staff"), ("2", "עכשיו", "שתי מחנות", "bank")]
HK = ("יעקב אבינו", "מהמקל לשני בנקים")
SEG = [
    dict(a=712.14, b=714.24, layout="stage", theme="navy", hook=HK, hook_out=False, icon="moon", splits=[4], keys=[1], modes=["line"]),
    dict(a=715.14, b=716.62, layout="stage", theme="navy", hook=HK, hook_in=False, icon="moon", icon_draw=0, splits=[3], keys=[2], modes=["stack"]),
    dict(a=719.02, b=722.24, layout="anim", scene="stones", theme="navy", ev={"st": [0.44, 0.6, 1.16, 2.04, 2.32], "label": 0.46}, splits=[3,4], keys=[2,3], modes=["line","line"]),
    dict(a=722.90, b=724.56, layout="focus", theme="navy", small="אפילו שק שינה לא נשאר לו", big="כלום."),
    dict(a=725.62, b=726.54, layout="stage", theme="teal", wm="לימים", icon="staff", splits=[3], keys=[0], modes=["line"]),
    dict(a=727.16, b=731.06, layout="quote", theme="warm", lines=["במקלי עברתי את הירדן הזה", "ועתה הייתי לשני מחנות"]),
    dict(a=732.74, b=734.58, layout="stage", theme="purple", wm="תודה", icon="heart", splits=[4,3], keys=[1,0], modes=["line","line"]),
    dict(a=734.86, b=737.46, layout="stage", theme="purple", wm="תודה", meter={"t0": 0.08, "t1": 0.8}, punch=True, splits=[4,6], keys=[3,3], modes=["stack","line"]),
    dict(a=738.29, b=742.46, layout="anim", scene="river", theme="purple", ev={"x0": 860, "x1": 230, "jordan": 1.07, "house": 2.6}, cap_y=1575, splits=[3,2,2,3], keys=[2,1,0,0], modes=["line","line","line","line"]),
    dict(a=742.76, b=744.40, layout="anim", scene="staff", theme="warm", ev={"ring": 0.58, "label": 0.34, "zoom": 0.02}, splits=[4,4], keys=[3,2], modes=["stack","line"]),
    dict(a=744.76, b=748.86, layout="anim", scene="camps", theme="warm", ev={"tent": [0.92, 1.05], "label": 0.95, "banks": 2.0, "coins": 2.72, "z0": 0.02, "zoom": 0.05}, splits=[4,5,3,3], keys=[3,4,1,0], modes=["stack","stack","line","line"]),
    dict(a=749.04, b=750.30, layout="stage", theme="warm", wm="תודה", icon="heart", punch=True, splits=[5], keys=[3], modes=["stack"]),
    dict(a=755.32, b=756.62, layout="stage", theme="warm", wm="זכויות", icon="heart", icon_draw=0, splits=[3,4], keys=[2,3], modes=["line","line"]),
    dict(a=756.74, b=759.00, layout="burst", theme="warm", wm="טוב", splits=[3,2,3], keys=[1,1,2], modes=["line","stack","line"], big=160),
]
