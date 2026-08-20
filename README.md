# 🚀 AI Developer Assistant (RAG System)

מערכת RAG (Retrieval-Augmented Generation) חכמה המשמשת כ"סוכן חכם" (Agent) עבור מפתחים. 
המערכת מאפשרת תשאול על מסמכי פיתוח, ארכיטקטורה, חוקי UI והחלטות טכניות של פרויקט תוכנה.

## 🏗️ ארכיטקטורה ויכולות
המערכת בנויה באמצעות **LlamaIndex Workflows** וכוללת נתב (Router) חכם שמפצל את הבקשות:
1. **Vector Search (Pinecone)**: שאלות ידע פתוחות נשלחות למסד נתונים וקטורי לצורך חיפוש סמנטי.
2. **Structured Search**: שאלות ממוקדות לגבי "רשימות" (חוקים, החלטות, אזהרות) מנותבות ישירות למסד נתונים מובנה (JSON) לחילוץ מדויק ומהיר של 100% מהנתונים ללא פספוסים.
3. **LLM & Embeddings**: שימוש במודלים המתקדמים של Cohere (`command-r-08-2024` ו-`embed-multilingual-v3.0`).

## 🛠️ טכנולוגיות
* Python 3
* LlamaIndex (Core & Workflows)
* Pinecone (Vector Database)
* Cohere (LLM & Embeddings)
* Gradio (Web UI)

## 🚀 איך להריץ את הפרויקט?

1. **שכפול המאגר:**
   ```bash
   git clone <YOUR_REPO_URL>
   cd <PROJECT_FOLDER>

התקנת תלויות:

bash

Copy code
pip install -r requirements.txt

הגדרת משתני סביבה:
צרו קובץ .env בתיקייה הראשית והוסיפו את המפתחות הבאים:

env

Copy code
COHERE_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
PINECONE_INDEX_NAME=your_index_here

הפעלת הממשק (Gradio):

bash

Copy code
python ui/chat_app.py

הממשק ייפתח בדפדפן בכתובת המקומית (לרוב http://127.0.0.1:7860)

💡 דוגמאות לשאלות שה-Agent יודע לענות (QA):
שאלות שעוברות לחיפוש וקטורי (Pinecone):

"מה קורה כשמנהל צוות נמחק מהמערכת?"
"איך עובד מנגנון ההתחברות במערכת?"
"מה הצבע העיקרי של הדיזיין?"

שאלות שמנותבות לחיפוש מובנה (Structured JSON):

"תציג לי את כל החוקים שיש בפרויקט" (Rules)
"מהן כל ההחלטות הטכניות שהתקבלו?" (Decisions)
"אילו אזהרות מפתח קיימות במערכת?" (Warnings)

📊 תרשים ה-Workflow
תרשים הזרימה של המערכת (Router, Retrieve, Postprocess, Synthesize) מצורף בפרויקט בקובץ final_rag_workflow.html.
כאן ניתן לראות את זרימת המידע במערכת, הכוללת את הנתב (Router) ואת מסלולי השליפה השונים:

![תרשים Workflow המלא](workflow.png)

*(הערה לבודק: מצורף גם קובץ אינטראקטיבי בשם `final_rag_workflow.html`. ניתן להוריד אותו ולפתוח בדפדפן כדי לראות את התרשים בצורה דינמית).*