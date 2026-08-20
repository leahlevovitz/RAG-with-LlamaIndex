# הערות פיתוח

## הרצת הפרויקט מקומית

### דרישות מקדימות
- Python 3.10 ומעלה
- pip

### שלבי התקנה

```bash
# 1. שכפול הפרויקט
git clone <repo-url>
cd <project-folder>

# 2. יצירת סביבה וירטואלית
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. התקנת תלויות
pip install django

# 4. הרצת מיגרציות
python manage.py migrate

# 5. יצירת superuser (אופציונלי — לגישה ל-/admin/)
python manage.py createsuperuser

# 6. הרצת השרת
python manage.py runserver
```

הפרויקט זמין בכתובת: `http://127.0.0.1:8000/`

---

## מבנה התיקיות המרכזיות

```
Python_Project/        ← הגדרות Django (settings, urls, wsgi, asgi)
Django_App/            ← האפליקציה הראשית
    models.py          ← מודלים: CustomUser, Team, Task
    views.py           ← לוגיקת הבקשות
    urls.py            ← ניתוב URL-ים
    form.py            ← טפסי Django
    admin.py           ← הגדרות פאנל ניהול
    migrations/        ← קבצי מיגרציה
templates/             ← תבניות HTML
    home.html          ← דף הבית
    register.html      ← הרשמה
    login.html         ← התחברות
    personalArea.html  ← בחירת צוות ותפקיד
    about.html         ← דף אודות
manage.py              ← כלי ניהול Django
db.sqlite3             ← מסד הנתונים
```

---

## הוספת מודול חדש

### 1. הוסף מודל ב-`Django_App/models.py`

```python
class NewModel(models.Model):
    name = models.CharField(max_length=255)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
```

### 2. צור מיגרציה

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. הוסף טופס ב-`Django_App/form.py`

```python
class NewModelForm(forms.ModelForm):
    class Meta:
        model = NewModel
        fields = ["name"]
```

### 4. הוסף View ב-`Django_App/views.py`

```python
@login_required(login_url="login")
def new_view(request):
    # לוגיקה
    return render(request, 'new_template.html', {})
```

### 5. רשום URL ב-`Django_App/urls.py`

```python
path("new-path/", new_view, name="new_view"),
```

### 6. צור תבנית ב-`templates/new_template.html`

השתמש ב-`<html lang="he" dir="rtl">` ובעיצוב הקיים (soft-card, soft-btn).

---

## הרצת בדיקות

```bash
# הרצת כל הבדיקות
python manage.py test Django_App

# בדיקת תקינות הפרויקט
python manage.py check

# בדיקת מיגרציות ממתינות
python manage.py showmigrations
```

### בדיקות ידניות לפני commit

1. הרשמה והתחברות של משתמש חדש.
2. בחירת צוות ותפקיד (מנהל ועובד).
3. יצירת משימה כמנהל.
4. שיוך משימה כעובד.
5. סימון משימה כהושלמה.
6. מחיקת משימה פנויה.
7. סינון לפי סטטוס ועובד.
