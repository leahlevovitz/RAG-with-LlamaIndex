# ארכיטקטורת המערכת

## שפת תכנות וסביבה

הפרויקט כתוב ב-**Python** עם מסגרת העבודה **Django 5.2**.  
הממשק הקדמי (Frontend) בנוי על תבניות Django (Django Templates) בשילוב **Bootstrap 5.3**.

---

## מסד הנתונים

המערכת משתמשת ב-**SQLite** (קובץ `db.sqlite3` בשורש הפרויקט).  
זהו מסד נתונים מבוסס קובץ, מתאים לפיתוח ולסביבות קטנות.  
בסביבת ייצור מומלץ לעבור ל-PostgreSQL או MySQL.

---

## מבנה הפרויקט

```
Python_Project/          ← הגדרות Django (settings, urls, wsgi, asgi)
Django_App/              ← האפליקציה הראשית
    models.py            ← מודלים: CustomUser, Team, Task
    views.py             ← לוגיקת הבקשות (Views)
    urls.py              ← ניתוב URL-ים של האפליקציה
    form.py              ← טפסי Django
    admin.py             ← הגדרות פאנל ניהול
    migrations/          ← קבצי מיגרציה של מסד הנתונים
templates/               ← תבניות HTML
    home.html            ← דף הבית (רשימת משימות)
    register.html        ← דף הרשמה
    login.html           ← דף התחברות
    personalArea.html    ← בחירת צוות ותפקיד
    about.html           ← דף אודות
manage.py                ← כלי ניהול Django
db.sqlite3               ← קובץ מסד הנתונים
```

---

## זרימת הנתונים בין הקומפוננטים

```
Browser (HTTP Request)
        ↓
Python_Project/urls.py       ← ניתוב ראשי
        ↓
Django_App/urls.py           ← ניתוב ספציפי לאפליקציה
        ↓
Django_App/views.py          ← לוגיקה עסקית
        ↓
Django_App/models.py         ← גישה למסד הנתונים (ORM)
        ↓
db.sqlite3                   ← שמירה/שליפה של נתונים
        ↓
templates/*.html             ← רינדור HTML
        ↓
Browser (HTTP Response)
```

### תיאור מפורט של הזרימה

1. **בקשה נכנסת** - הדפדפן שולח בקשת HTTP (GET/POST) לשרת Django.
2. **ניתוב** - `Python_Project/urls.py` מפנה לאפליקציה, ו-`Django_App/urls.py` מפנה ל-View המתאים.
3. **View** - הפונקציה ב-`views.py` מטפלת בלוגיקה: בדיקת הרשאות, עיבוד טפסים, שאילתות ORM.
4. **ORM** - Django ORM מתרגם פעולות Python לשאילתות SQL ומתקשר עם SQLite.
5. **Template** - ה-View מעביר context לתבנית HTML שמרנדרת את הממשק.
6. **תגובה** - HTML מוחזר לדפדפן.

---

## מנגנון הזדהות

המערכת משתמשת במנגנון ה-Authentication המובנה של Django עם מודל `CustomUser` שמרחיב את `AbstractUser`.  
ניהול הסשן מתבצע דרך `django.contrib.sessions` עם cookies.  
הגנת CSRF מופעלת על כל הטפסים.
