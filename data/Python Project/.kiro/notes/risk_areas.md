# אזורים רגישים במערכת

## 1. מנגנון ההזדהות

**מיקום:** `Django_App/models.py` (CustomUser), `Django_App/form.py` (LoginForm, RegisterForm), `Django_App/views.py` (login, register)

**למה זה רגיש:**
המערכת משתמשת ב-`CustomUser` שמרחיב את `AbstractUser`. שינוי במודל זה לאחר המיגרציה הראשונה הוא מורכב מאוד ועלול לשבור את כל הסשנים הקיימים, את הקשרים בין המשתמשים לצוותים ולמשימות, ואת פאנל הניהול.

בנוסף, `RegisterForm` מכריח `is_superuser=False` ו-`is_staff=False` — שינוי כאן עלול לאפשר הרשמה עם הרשאות מוגברות.

**כללים:**
- אל תשנה את `CustomUser` ללא גיבוי מסד הנתונים.
- אל תסיר את `@login_required` מ-Views.
- אל תשנה את `AUTH_USER_MODEL` לאחר יצירת הנתונים הראשונים.

---

## 2. לוגיקת הרשאות

**מיקום:** `Django_App/views.py` — כל View שמבצע פעולת כתיבה

**למה זה רגיש:**
הרשאות נבדקות ב-View level בלבד, ללא middleware מרכזי. כל View מבצע את הבדיקה בנפרד:

```python
if request.user.team and request.user.team.admin_id == request.user.id:
```

שגיאה בבדיקה אחת עלולה לאפשר לעובד רגיל לבצע פעולות מנהל (יצירה, מחיקה, עדכון).

בנוסף, `personal_area` מונע שינוי צוות ותפקיד לאחר ההגדרה — שינוי הלוגיקה שם עלול לאפשר לעובד להפוך למנהל ללא בדיקה.

**כללים:**
- בדוק את `request.user.team` לפני `request.user.team.admin_id` — אחרת `AttributeError`.
- אל תשנה את `Personal_areaForm.clean()` ללא בדיקה — הוא מונע שני מנהלים לאותו צוות.
- כל View חדש שמבצע פעולת כתיבה חייב לכלול בדיקת הרשאות.

---

## 3. עדכון סטטוס משימות

**מיקום:** `Django_App/views.py` — `assignment_task`, `update_task_status`

**למה זה רגיש:**
מעבר הסטטוס הוא חד-כיווני ובלתי הפיך: `new` → `in_progress` → `completed`.
אין אפשרות לאפס סטטוס — לא דרך הממשק ולא דרך הקוד.

`assignment_task` מגדיר גם את `worker` וגם את `status` בו-זמנית:
```python
task.worker = request.user
task.status = Status.IN_PROGRESS
task.save(update_fields=["worker", "status"])
```

שינוי כאן עלול לאפשר שיוך כפול (שני עובדים לאותה משימה) או מעבר סטטוס לא חוקי.

`update_task_status` מאפשר רק לעובד המשויך לסמן כהושלם — שינוי הבדיקה עלול לאפשר לכל עובד לסמן משימות של אחרים.

**כללים:**
- אל תשנה את `update_fields` ב-`save()` ללא בדיקה שכל השדות הנדרשים כלולים.
- אל תוסיף מעבר סטטוס חדש ללא עדכון כל הבדיקות הקשורות.
- בדוק תמיד ש-`task.worker is None` לפני שיוך, ו-`task.worker == request.user` לפני סיום.
