# הנחיות עיצוב ממשק המשתמש

## תמיכה ב-RTL

הממשק כתוב בעברית ומחייב כיוון ימין-לשמאל בכל הדפים.

כל תבנית HTML חייבת לפתוח עם:
```html
<html lang="he" dir="rtl">
```

Bootstrap 5 תומך ב-RTL מובנה — אין צורך בספרייה נוספת.
אל תוסיף `dir="ltr"` לאלמנטים בודדים אלא אם מדובר בתוכן טכני (קוד, מספרים).

---

## פלטת צבעים

המערכת משתמשת בגרדיאנטים רכים ועקביים. אין להוסיף צבעים חדשים שאינם מהפלטה.

| שימוש             | ערך                                                            |
|-------------------|----------------------------------------------------------------|
| רקע הדף           | `linear-gradient(135deg, #e0f7fa, #e8f5e9, #fffde7, #fce4ec)` |
| כפתור ראשי        | `linear-gradient(90deg, #90caf9, #a5d6a7)`                    |
| כפתור הוספה       | `linear-gradient(90deg, #90caf9, #a5d6a7, #f8bbd0)`           |
| כפתור סיום        | `linear-gradient(90deg, #c8e6c9, #fff9c4, #f8bbd0)`           |
| כותרות            | `#355f6b`                                                      |
| טקסט משני         | `#6d5a7a`                                                      |

---

## כרטיסיות (Cards)

כל בלוק תוכן עצמאי מוצג בתוך כרטיסייה עם עיצוב אחיד:

```css
.soft-card {
  background: #fff;
  border: 0;
  border-radius: 22px;
  box-shadow: 0 18px 40px rgba(0,0,0,.08);
}
```

- אין להשתמש ב-`border` ישיר — רק `box-shadow`.
- `border-radius`: `22px` לכרטיסיות, `14px` לכפתורים, `999px` לאלמנטים עגולים.

---

## כפתורים וטפסים

```css
.soft-btn  { border-radius: 14px; padding: 10px 14px; }
.soft-pill { border-radius: 999px; }
```

- כפתורי פעולה ראשיים: `.btn.soft-btn` עם גרדיאנט, ללא border.
- כפתורי ביטול: `.btn.btn-outline-secondary.soft-btn`.
- כפתורי מחיקה: `.btn.btn-outline-danger.soft-btn`.
- כפתורים מושבתים: להשתמש ב-`disabled` attribute — לא להסתיר.
- כל טופס POST חייב לכלול `{% csrf_token %}`.
- שדות select: `.form-select.soft-pill`.

---

## הודעות למשתמש

```html
{% for message in messages %}
  <div class="alert alert-{{ message.tags }}">{{ message }}</div>
{% endfor %}
```

- הודעות שגיאה: `messages.error(request, "...")`
- הודעות הצלחה: `messages.success(request, "...")`
- מוצגות בראש הדף, מעל כל התוכן.

---

## ממשק פשוט וברור

- כל הפעולות נגישות מדף הבית — אין ניווט מורכב.
- כפתורים לא רלוונטיים מושבתים (disabled) ולא מוסתרים — המשתמש מבין מה אפשרי.
- משוב מיידי לכל פעולה דרך הודעות.
- פריסה רספונסיבית: `col-lg-8` למשימות, `col-lg-4` לטופס הוספה, `col-12` במובייל.
