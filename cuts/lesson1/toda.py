# Reel 4 (תודה) in the merged style
CARDS = [("1", "מרימה לי", "כיף לי, נעים לי", "arrow_up"), ("2", "נותנת אישור", "אתה בכיוון הנכון", "check_circle")]
SEG = [
    dict(a=1375.36, b=1379.92, layout="stage", theme="navy", hook=("לאשתך · לבעלך", "תודה רבה"), icon="bubble_heart", icon_pos=(760, 330),
         splits=[3,2,3,4,3,3,4], keys=[2,1,2,3,0,1,3], modes=["line","line","line","line","stack","line","line"]),
    dict(a=1380.80, b=1383.96, layout="stage", theme="navy", punch=True, wm="תודה", icon="couple",
         splits=[4,3,3,4], keys=[3,0,1,3], modes=["line","stack","line","line"]),
    dict(a=1386.32, b=1389.06, layout="stage", theme="purple", wm="הטבע", icon="lightning",
         splits=[4,3], keys=[2,1], modes=["line","stack"]),
    dict(a=1389.06, b=1390.86, layout="quote", theme="warm", lines=["אני נתתי", "ולא קיבלתי תמורה"]),
    dict(a=1313.00, b=1314.30, layout="focus", theme="navy", small="התודה עושה", big="שתי פעולות"),
    dict(a=1317.16, b=1318.94, layout="cards", active="1", appear={"1": 0.0, "2": 0.35}, splits=[2,4], keys=[1,2]),
    dict(a=1319.34, b=1320.40, layout="cards", active="1", splits=[2,3], keys=[0,1]),
    dict(a=1320.96, b=1322.95, layout="cards", active="2", appear={"2": 0.0}, splits=[2,4], keys=[1,3]),
    dict(a=1323.26, b=1325.78, layout="stage", theme="teal", punch=True, wm="אישור", icon="check_circle",
         splits=[3,3,3], keys=[1,1,0], modes=["line","line","stack"]),
    dict(a=1393.20, b=1395.24, layout="stage", theme="teal", wm="גדול", icon="graph_up",
         splits=[4,3,2], keys=[3,1,0], modes=["line","line","stack"]),
    dict(a=1395.86, b=1396.78, layout="focus", theme="teal", small="מה אני צריך", big="לעשות?"),
    dict(a=1397.28, b=1397.68, layout="burst", theme="warm", wm="לתת", splits=[2], keys=[1], modes=["hero"], big=170),
    dict(a=1414.50, b=1415.05, layout="burst", theme="warm", wm="לתת", splits=[1], modes=["line"]),
    dict(a=1415.72, b=1418.40, layout="stage", theme="warm", punch=True, wm="בית", icon="house_heart",
         splits=[4,3], keys=[3,2], modes=["line","stack"]),
]
