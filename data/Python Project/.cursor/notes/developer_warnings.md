# אזהרות למפתחים

## אזהרה: מנגנון הזדהות

> **אל תשנה את מנגנון ה-Authentication ללא בדיקה מקיפה.**

המערכת משתמשת ב-`CustomUser` שמרחיב את `AbstractUser`. שינויים במודל זה עלולים לשבור:
- את כל הסשנים הקיימים של משתמשים מחוברים.
- את הקשרים בין `CustomUser` ל-`Team` ו-`Task`.
- את פאנל הניהול (`/admin/`).

**לפני כל שינוי ב-`CustomUser`:**
1. גבה את מסד הנתונים (`db.sqlite3`).
2. בדוק שהמיגרציה נוצרת בצורה תקינה עם `makemigrations --dry-run`.
3. בדוק שהתחברות, הרשמה ושיוך צוות עדיין עובדים.

---

## אזהרה: שינוי מבנה טבלאות

> **אל תשנה מודלים קיימים ללא יצירת מיגרציה.**

כל שינוי ב-`models.py` (הוספת שדה, שינוי סוג, מחיקת שדה) חייב להיות מלווה ב:

```bash
python manage.py makemigrations
python manage.py migrate
```

**סיכונים:**
- שינוי ללא מיגרציה יגרום לשגיאות `OperationalError` בזמן ריצה.
- מחיקת שדה עם נתונים קיימים תגרום לאובדן נתונים בלתי הפיך.
- שינוי `on_delete` בשדות FK משפיע על התנהגות מחיקת נתונים.

**שדות FK קריטיים לשים לב אליהם:**

| שדה                    | התנהגות מחיקה | השפעה                                      |
|------------------------|---------------|--------------------------------------------|
| `Task.team`            | CASCADE       | מחיקת צוות מוחקת את כל המשימות שלו        |
| `Task.worker`          | SET_NULL      | מחיקת עובד מאפסת את שדה worker במשימות    |
| `Task.created_by`      | CASCADE       | מחיקת יוצר המשימה מוחקת את המשימה         |
| `Team.admin`           | CASCADE       | מחיקת מנהל מוחקת את הצוות                 |
| `CustomUser.team`      | SET_NULL      | מחיקת צוות מנתקת את המשתמשים ממנו         |

---

## אזהרה: לוגיקת הרשאות

> **היזהר משינויים בלוגיקת ההרשאות — שגיאה עלולה לאפשר גישה לא מורשית.**

הרשאות מנהל נבדקות ב-Views כך:

```python
if request.user.team and request.user.team.admin_id == request.user.id:
    # פעולת מנהל
```

**אזהרות ספציפיות:**
- אל תסיר את `@login_required` מ-Views — זה יאפשר גישה ללא התחברות.
- אל תשנה את בדיקת `admin_id` ללא בדיקה מלאה של כל הפעולות (יצירה, עדכון, מחיקה).
- בדיקת `request.user.team` חייבת להיות לפני `request.user.team.admin_id` — אחרת תקבל `AttributeError`.
- אל תאפשר למשתמש לשנות `role` או `team` לאחר ההגדרה הראשונית — זה מכוון ומוגן ב-`personal_area` view.

---

## אזהרה: SECRET_KEY

> **אל תעלה את ה-`SECRET_KEY` ל-Git בסביבת ייצור.**

הקובץ `Python_Project/settings.py` מכיל כרגע `SECRET_KEY` חשוף.  
לפני deployment לייצור:

```python
# settings.py
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
```

---

## אזהרה: DEBUG=True

> **אל תפרוס לייצור עם `DEBUG=True`.**

`DEBUG=True` חושף מידע רגיש בדפי שגיאה (stack traces, הגדרות, נתיבי קבצים).  
בסביבת ייצור: `DEBUG=False` ו-`ALLOWED_HOSTS=['your-domain.com']`.
