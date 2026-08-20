# שיפורים עתידיים

## 1. מעבר ל-PostgreSQL בסביבת ייצור

SQLite מתאים לפיתוח מקומי בלבד. עם גידול הצוות וכמות הנתונים, יש לעבור ל-PostgreSQL.

**שלבי המעבר:**
1. התקן `psycopg2-binary`: `pip install psycopg2-binary`
2. עדכן `DATABASES` ב-`settings.py`:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "db_name",
        "USER": "db_user",
        "PASSWORD": "db_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```
3. הרץ `python manage.py migrate` על המסד החדש.
4. העבר נתונים קיימים עם `dumpdata` / `loaddata`.

---

## 2. מערכת התראות בזמן אמת

כרגע אין שום התראה כאשר משימה נוצרת, משויכת או מושלמת.

**שיפורים מוצעים:**
- התראה לעובד כאשר משימה חדשה זמינה בצוות.
- התראה למנהל כאשר עובד מסיים משימה.
- תזכורת אוטומטית יום לפני תאריך היעד.

**טכנולוגיות מוצעות:** Django Signals לאירועים פנימיים, Celery Beat לתזכורות תקופתיות, Django Channels ל-WebSockets.

---

## 3. אינטגרציה עם אימייל

**שימושים מוצעים:**
- אימות אימייל בהרשמה.
- סיכום שבועי למנהל עם סטטוס כל המשימות.
- התראות על משימות שתאריך היעד שלהן עבר.

**יישום:** הגדרת `EMAIL_BACKEND` ב-`settings.py` + `django.core.mail.send_mail`.

---

## 4. Pagination על רשימת המשימות

כרגע כל המשימות נטענות בבת אחת. בצוותים גדולים זה יאט את הדף.

```python
from django.core.paginator import Paginator

paginator = Paginator(tasks, 20)
page = request.GET.get("page")
tasks = paginator.get_page(page)
```

---

## 5. REST API עם Django REST Framework

לאפשר שימוש מאפליקציות מובייל או אינטגרציות חיצוניות.

**endpoints מוצעים:**
- `GET /api/tasks/` — רשימת משימות
- `POST /api/tasks/` — יצירת משימה
- `PATCH /api/tasks/<id>/` — עדכון סטטוס
- `GET /api/teams/` — רשימת צוותים

---

## 6. היסטוריית שינויים למשימה

תיעוד כל שינוי: מי שינה, מתי, מה השתנה.

**יישום מוצע:** מודל `TaskHistory` עם Django Signals שמתעדכן אוטומטית בכל שמירה.

---

## 7. שיפור ביצועי שאילתות

הוספת `select_related` למניעת N+1:
```python
Task.objects.filter(team=user.team).select_related('worker', 'created_by', 'team')
```

הוספת אינדקסים לשדות שמסוננים לעתים קרובות:
```python
class Task(models.Model):
    status = models.CharField(..., db_index=True)
    team = models.ForeignKey(..., db_index=True)
```

---

## 8. אפשרות לשינוי צוות ותפקיד

כרגע לאחר בחירת צוות ותפקיד אין אפשרות לשנות — חייבים להירשם מחדש.
שיפור חוויית המשתמש: אפשר לאפשר שינוי עם אישור מנהל בלבד.

---

## 9. העברת SECRET_KEY למשתנה סביבה

לפני כל deployment לייצור:
```python
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
```
