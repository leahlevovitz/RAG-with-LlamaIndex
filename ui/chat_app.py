import sys
import os
import gradio as gr

# 1. מציאת התיקייה הראשית (rag with llamaindex) והוספתה לנתיב
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)

# 2. עכשיו פייתון מבין מה זה "rag_app" ויכול לייבא מתוכו!
from rag_app.query_engine import query_rag

# הוספנו async כדי ש-Gradio ידע להמתין בסבלנות
async def chat_interface(message: str, history: list) -> str:
    # הוספנו await כי מנוע החיפוש עכשיו אסינכרוני
    answer, sources = await query_rag(message)

    if not sources:
        return answer
    
    sources_text = "\n\nמקורות המידע עליהם התבססתי:\n"
    for s in sources:
        sources_text += f"• {s['tool']}: {s['file']}\n"
    
    return answer + sources_text

demo = gr.ChatInterface(
    fn=chat_interface,
    title="Agentic Coding - RAG Assistant",
    description="שאלי אותי על החלטות טכניות, ארכיטקטורה, והנחיות מתוך קבצי התיעוד של הפרויקט.",
    examples=[
        "מה הצבע העיקרי שנבחר לדיזיין של המערכת?",
        "איזה רכיב במערכת הוגדר כבעייתי או רגיש במיוחד?"
    ]
)

if __name__ == "__main__":
    demo.launch()