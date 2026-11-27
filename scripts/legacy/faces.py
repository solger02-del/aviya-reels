import cv2, json, sys
sys.path.insert(0, "/home/claude/reel_scripts"); import os as _os; sys.path.insert(0, _os.environ.get("RW", "/home/claude/reel_work"))
from cuts import CUTS
src = sys.argv[1]
cap = cv2.VideoCapture(src)
casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
res = []
for (a, b) in CUTS:
    xs, ys, hs = [], [], []
    for k in range(5):
        t = a + (b - a) * (k + 0.5) / 5
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, fr = cap.read()
        if not ok: continue
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        f = casc.detectMultiScale(g, 1.1, 5, minSize=(40, 40))
        if len(f):
            x, y, w, h = max(f, key=lambda r: r[2] * r[3])
            xs.append(x + w / 2); ys.append(y); hs.append(h)
    xs.sort(); ys.sort()
    cx = xs[len(xs) // 2] if xs else None
    res.append({"a": a, "b": b, "cx": cx, "top": ys[len(ys)//2] if ys else None, "n": len(xs)})
    print(a, b, cx, len(xs))
json.dump(res, open(sys.argv[2], "w"), default=float)
