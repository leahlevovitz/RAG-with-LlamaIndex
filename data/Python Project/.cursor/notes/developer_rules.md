# הנחיות למפתחים

## הרצת הפרויקט מקומית

### דרישות מקדימות
- Python 3.10+
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

# 5. יצירת superuser (אופציונלי)
python manage.py createsuperuser

# 6. הרצת השרת
python manage.py runserver
```

הפרויקט יהיה זמין בכתובת: `http://127.0.0.1:8000/`

---

## הוספת פיצ'ר חדש

### 1. הוספת מודל חדש

ב-`Django_App/models.py` הוסף את המחלקה החדשה:

```python
class NewModel(models.Model):
    name = models.CharField(max_length=255)
    # שדות נוספים...
```

לאחר מכן הרץ מיגרציה:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. הוספת View חדש

ב-`Django_App/views.py` הוסף פונקציה:

```python
@login_required(login_url="login")
def my_new_view(request):
    # לוגיקה
    return render(request, 'my_template.html', {'context': data})
```

### 3. רישום URL

ב-`Django_App/urls.py` הוסף:

```python
path("my-path/", my_new_view, name="my_view_name"),
```

### 4. יצירת תבנית HTML

צור קובץ חדש ב-`templates/` עם:
- `<html lang="he" dir="rtl">` בראש הקובץ
- ייבוא Bootstrap 5.3
- שימוש בעיצוב הקיים (soft-card, soft-btn וכו')
- `{% csrf_token %}` בכל טופס POST

### 5. הוספת טופס (אם נדרש)

ב-`Django_App/form.py` הוסף:

```python
class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ["field1", "field2"]
```

---

## בדיקות לפני העלאת קוד

### בדיקות פונקציונליות ידניות

לפני כל commit, בדוק את הזרימות הבאות:

1. **הרשמה והתחברות** — צור משתמש חדש, התחבר, בחר צוות ותפקיד.
2. **יצירת משימה** — התחבר כמנהל, צור משימה חדשה.
3. **שיוך משימה** — התחבר כעובד, שייך משימה לעצמך.
4. **סיום משימה** — סמן משימה כהושלמה.
5. **מחיקת משימה** — מחק משימה פנויה (ללא עובד).
6. **פילטרים** — בדוק סינון לפי סטטוס ועובד.

### הרצת בדיקות אוטומטיות

```bash
python manage.py test Django_App
```

### בדיקת מיגרציות

```bash
# ודא שאין מיגרציות שלא הורצו
python manage.py showmigrations

# בדוק שהמיגרציות תקינות
python manage.py migrate --check
```

### בדיקת שגיאות נפוצות

```bash
# בדיקת תקינות הפרויקט
python manage.py check

# בדיקת תקינות הפרויקט כולל deployment
python manage.py check --deploy
```
