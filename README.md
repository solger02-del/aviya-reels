# aviya-reels

כלי העריכה של הרילים של הרב אביה אוחיון, בסגנון העריכה המשולב.

## מה יש כאן

| תיקייה | תוכן |
|---|---|
| `scripts/` | הסקריפטים הפעילים: `style3_render.py` (רינדור ריל), `style3_anim.py` (קטעי אנימציה, סרגל מצב, מונה, מסך סיום), `style3_assets.py` (רקעים, אייקוני ניאון, כרטיסים), `cover.py` (קאוור לכל ריל) |
| `scripts/legacy/` | הגרסאות הקודמות של סגנון העריכה (לפני הסגנון המשולב) |
| `cuts/lesson1/` | רשימות החיתוך של הרילים מהשיעור הראשון |
| `cuts/lesson2_vayishlach/` | רשימות החיתוך של 12 הרילים מפרשת וישלח |
| `fonts/` | הפונטים: Heebo (6 משקלים) ו-Secular One |

## מה אין כאן

קובצי הווידאו, התמלולים המלאים והרילים המוגמרים לא נשמרים במאגר.

## איך מריצים ריל

צריך ffmpeg עם libass, Python 3 עם Pillow (עם raqm), pycairo, numpy ו-opencv-python-headless (גרסה מתחת ל-5).

```bash
mkdir work && cp cuts/lesson2_vayishlach/01_hamasa_shel_yaakov.py work/cuts3.py
SRC=/path/to/lesson.mov WORDS=/path/to/words.json RW=$PWD/work python3 scripts/style3_render.py
```

- `SRC` הוא קובץ השיעור המקורי.
- `WORDS` הוא קובץ JSON של מילים עם זמנים (`text`, `src_start_ms`, `src_end_ms`).
- התוצאה נכתבת ל-`work/out3.mp4`.

הנתיבים לפונטים ולסקריפטים בתוך הקבצים כתובים כרגע כנתיבים מוחלטים של סביבת העבודה שבה נוצרו (`/home/claude/...`). בהרצה במקום אחר צריך לעדכן אותם.

## פונטים

Heebo ו-Secular One מופצים ברישיון SIL Open Font License 1.1 (מקור: Google Fonts). משקלי Heebo כאן הם מופעים סטטיים שנגזרו מהפונט המשתנה.
