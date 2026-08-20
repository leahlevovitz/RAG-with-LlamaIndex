# מבנה מסד הנתונים

## סקירה כללית

המערכת משתמשת ב-SQLite עם Django ORM. קובץ המסד נמצא ב-`db.sqlite3` בשורש הפרויקט.  
המודלים מוגדרים ב-`Django_App/models.py`.

---

## טבלאות

### 1. `Django_App_team` — צוותים

| שדה    | סוג          | תיאור                                      |
|--------|--------------|--------------------------------------------|
| id     | INTEGER (PK) | מזהה ייחודי אוטומטי                        |
| name   | VARCHAR(255) | שם הצוות                                   |
| admin_id | INTEGER (FK) | מפתח זר ל-`CustomUser` — מנהל הצוות (אחד לאחד) |

**הערות:**
- שדה `admin` הוא `OneToOneField` — לכל צוות יכול להיות מנהל אחד בלבד.
- ניתן ליצור צוות ללא מנהל (`null=True, blank=True`).

---

### 2. `Django_App_customuser` — משתמשים

יורש מ-`AbstractUser` של Django, כולל את כל שדות המשתמש הסטנדרטיים בנוסף לשדות הבאים:

| שדה     | סוג          | תיאור                                         |
|---------|--------------|-----------------------------------------------|
| id      | INTEGER (PK) | מזהה ייחודי אוטומטי                           |
| username | VARCHAR     | שם משתמש (ייחודי, מ-AbstractUser)             |
| password | VARCHAR     | סיסמה מוצפנת (מ-AbstractUser)                |
| role    | VARCHAR(255) | תפקיד: `admin` או `user`                      |
| team_id | INTEGER (FK) | מפתח זר ל-`Team` — הצוות אליו שייך המשתמש    |

**ערכי `role`:**
- `admin` — מנהל צוות, יכול ליצור/לעדכן/למחוק משימות
- `user` — עובד רגיל, יכול לשייך משימות לעצמו ולסמן כהושלם

**הערות:**
- `team` יכול להיות `null` — משתמש שטרם בחר צוות.
- לאחר בחירת צוות ותפקיד, לא ניתן לשנות (אלא אם נרשמים מחדש).

---

### 3. `Django_App_task` — משימות

| שדה         | סוג          | תיאור                                              |
|-------------|--------------|-----------------------------------------------------|
| id          | INTEGER (PK) | מזהה ייחודי אוטומטי                                |
| name        | VARCHAR(255) | שם המשימה                                          |
| description | TEXT         | תיאור מפורט (אופציונלי)                            |
| worker_id   | INTEGER (FK) | מפתח זר ל-`CustomUser` — העובד האחראי (אופציונלי) |
| team_id     | INTEGER (FK) | מפתח זר ל-`Team` — הצוות שהמשימה שייכת אליו       |
| created_by_id | INTEGER (FK) | מפתח זר ל-`CustomUser` — מי יצר את המשימה        |
| finishDate  | DATE         | תאריך יעד לסיום                                    |
| status      | VARCHAR(255) | סטטוס: `new`, `in_progress`, `completed`           |

**ערכי `status`:**
- `new` — משימה חדשה, טרם שויכה לעובד
- `in_progress` — שויכה לעובד, בתהליך
- `completed` — הושלמה על ידי העובד

**הערות:**
- `worker` יכול להיות `null` — משימה פנויה שטרם שויכה.
- מחיקת צוות מוחקת את כל המשימות שלו (`CASCADE`).
- מחיקת עובד מאפסת את שדה `worker` במשימות שלו (`SET_NULL`).

---

## קשרים בין הטבלאות

```
Team ──────────────────── CustomUser
 │  (OneToOne: admin)         │
 │                            │ (ForeignKey: team)
 │                            │
 └──────────── Task ──────────┘
               │  (ForeignKey: team → CASCADE)
               │  (ForeignKey: worker → SET_NULL)
               │  (ForeignKey: created_by → CASCADE)
```

### סיכום הקשרים

| קשר                          | סוג         | התנהגות מחיקה |
|------------------------------|-------------|----------------|
| Team → CustomUser (admin)    | OneToOne    | CASCADE        |
| CustomUser → Team            | ForeignKey  | SET_NULL       |
| Task → Team                  | ForeignKey  | CASCADE        |
| Task → CustomUser (worker)   | ForeignKey  | SET_NULL       |
| Task → CustomUser (created_by) | ForeignKey | CASCADE       |

---

## מיגרציות

קבצי המיגרציה נמצאים ב-`Django_App/migrations/`:

| קובץ                                    | תיאור                                      |
|-----------------------------------------|--------------------------------------------|
| `0001_initial.py`                       | יצירת הטבלאות הראשוניות                   |
| `0002_alter_customuser_team.py`         | שינוי שדה `team` ב-CustomUser             |
| `0003_alter_task_finishdate.py`         | שינוי שדה `finishDate` ב-Task             |
