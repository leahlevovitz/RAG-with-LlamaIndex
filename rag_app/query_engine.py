# import os
# import json
# import certifi
# import asyncio
# from typing import Tuple, List, Dict
# from dotenv import load_dotenv

# # טיפול בתעודות אבטחה ורשת
# os.environ['SSL_CERT_FILE'] = certifi.where()
# os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

# current_dir = os.path.dirname(os.path.abspath(__file__))
# env_path = os.path.abspath(os.path.join(current_dir, "..", ".env", ".env"))
# load_dotenv(dotenv_path=env_path)

# from pinecone import Pinecone
# from llama_index.vector_stores.pinecone import PineconeVectorStore
# from llama_index.core import VectorStoreIndex, Settings
# from llama_index.core.retrievers import VectorIndexRetriever
# from llama_index.core.response_synthesizers import get_response_synthesizer
# from llama_index.core.postprocessor import SimilarityPostprocessor
# from llama_index.embeddings.cohere import CohereEmbedding
# from llama_index.llms.cohere import Cohere
# from llama_index.core.workflow import Workflow, step, StartEvent, StopEvent, Event, Context
# from llama_index.utils.workflow import draw_all_possible_flows
# from llama_index.core.llms import ChatMessage

# Settings.embed_model = CohereEmbedding(
#     api_key=os.environ["COHERE_API_KEY"],
#     model_name="embed-multilingual-v3.0",
#     input_type="search_query"
# )

# llm = Cohere(
#     api_key=os.environ["COHERE_API_KEY"],
#     model="command-r-08-2024"
# )
# Settings.llm = llm

# pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
# pinecone_index = pc.Index(os.environ["PINECONE_INDEX_NAME"])
# vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
# index = VectorStoreIndex.from_vector_store(vector_store)

# retriever = VectorIndexRetriever(index=index, similarity_top_k=5)
# postprocessor = SimilarityPostprocessor(similarity_cutoff=0.5)
# response_synthesizer = get_response_synthesizer(response_mode="compact")

# class VectorSearchEvent(Event):
#     query: str

# class StructuredSearchEvent(Event):
#     query: str
#     category: str

# class RetrievedNodesEvent(Event):
#     nodes: list
#     query: str

# class FilteredNodesEvent(Event):
#     nodes: list
#     query: str

# class RAGWorkflow(Workflow):
    
#     @step
#     async def route_query(self, ctx: Context, ev: StartEvent) -> VectorSearchEvent | StructuredSearchEvent | StopEvent:
#         query = ev.get("query")
        
#         if not query or not query.strip():
#             return StopEvent(result=("אנא הכניסי שאלה חוקית.", []))
            
#         print(f"🚦 Router is checking query: '{query}'")
        
#         # === התיקון: פרומפט חכם וקשוח עם דוגמאות (Few-Shot Prompting) ===
#         prompt = f"""
#         You are a smart router for a RAG system.
#         Classify the user's query into ONE of these four exact categories: 'decisions', 'rules', 'warnings', or 'general'.
        
#         CRITICAL INSTRUCTIONS:
#         1. If the user asks a specific question about a detail, feature, color, how something works, or specific code -> reply 'general'.
#         2. ONLY if the user explicitly asks for a complete list like "all decisions", "list of decisions" -> reply 'decisions'.
#         3. ONLY if the user explicitly asks for "all rules", "guidelines list" -> reply 'rules'.
#         4. ONLY if the user explicitly asks for "all warnings", "risks list" -> reply 'warnings'.

#         EXAMPLES:
#         User: "מה הצבע העיקרי של המערכת?"
#         Answer: general
        
#         User: "איך עובד מסד הנתונים?"
#         Answer: general
        
#         User: "תציג לי את כל החוקים בפרויקט"
#         Answer: rules
        
#         User: "מהן ההחלטות הטכניות שהתקבלו?"
#         Answer: decisions
        
#         User: "אילו אזהרות מפתח יש כאן?"
#         Answer: warnings

#         Now, classify this query:
#         User: "{query}"
#         Answer (reply with one word only):
#         """
        
#         try:
#             msg = ChatMessage(role="user", content=prompt)
#             response = llm.chat([msg])
#             decision = str(response.message.content).strip().lower()
#         except Exception as e:
#             print(f"⚠️ Router Error: {e}. Defaulting to Vector Search.")
#             decision = "general"
        
#         # וידוא מחמיר שהתשובה היא באמת אחת מהאופציות
#         if "decisions" in decision:
#             print("🔀 Router decided: Structured Search (Decisions)")
#             return StructuredSearchEvent(query=query, category="decisions")
#         elif "rules" in decision:
#             print("🔀 Router decided: Structured Search (Rules)")
#             return StructuredSearchEvent(query=query, category="rules")
#         elif "warnings" in decision:
#             print("🔀 Router decided: Structured Search (Warnings)")
#             return StructuredSearchEvent(query=query, category="warnings")
#         else:
#             print("🔀 Router decided: Vector Search (Pinecone)")
#             return VectorSearchEvent(query=query)

#     @step
#     async def structured_search(self, ctx: Context, ev: StructuredSearchEvent) -> StopEvent:
#         json_path = os.path.abspath(os.path.join(current_dir, "..", "data", "Python Project", "structured_database.json"))
        
#         try:
#             with open(json_path, "r", encoding="utf-8") as f:
#                 data = json.load(f)
#         except Exception as e:
#             return StopEvent(result=("שגיאה בטעינת קובץ הנתונים המובנה.", []))
            
#         category = ev.category
#         items = data.get("items", {}).get(category, [])
        
#         if not items:
#             return StopEvent(result=(f"לא מצאתי פריטים מסוג {category} במאגר.", []))
            
#         response_text = f"הנה הרשימה המלאה של {category}:\n\n"
#         sources = []
#         seen_files = set()
        
#         for item in items:
#             title = item.get("title") or item.get("rule") or item.get("message", "ללא כותרת")
#             response_text += f"🔹 {title}\n"
            
#             source_info = item.get("source", {})
#             tool = source_info.get("tool", "unknown")
#             file_name = source_info.get("file", "unknown")
#             source_id = f"{tool}-{file_name}"
            
#             if source_id not in seen_files:
#                 sources.append({"tool": tool, "file": file_name})
#                 seen_files.add(source_id)
                
#         return StopEvent(result=(response_text, sources))

#     @step
#     async def retrieve(self, ctx: Context, ev: VectorSearchEvent) -> RetrievedNodesEvent | StopEvent:
#         nodes = retriever.retrieve(ev.query)
#         if not nodes:
#             return StopEvent(result=("לא נמצאו מסמכים כלל במערכת.", []))
#         return RetrievedNodesEvent(nodes=nodes, query=ev.query)

#     @step
#     async def postprocess(self, ctx: Context, ev: RetrievedNodesEvent) -> FilteredNodesEvent | StopEvent:
#         nodes = postprocessor.postprocess_nodes(ev.nodes)
#         if not nodes:
#             return StopEvent(result=("לא מצאתי מידע רלוונטי מספיק כדי לענות על שאלתך.", []))
#         return FilteredNodesEvent(nodes=nodes, query=ev.query)

#     @step
#     async def synthesize(self, ctx: Context, ev: FilteredNodesEvent) -> StopEvent:
#         response = response_synthesizer.synthesize(ev.query, ev.nodes)
        
#         sources = []
#         seen_files = set()
#         for node in ev.nodes:
#             metadata = node.node.metadata
#             tool = metadata.get("tool", "Unknown Tool")
#             file_name = metadata.get("file_name", "Unknown File")
#             source_id = f"{tool}-{file_name}"
#             if source_id not in seen_files:
#                 sources.append({"tool": tool, "file": file_name})
#                 seen_files.add(source_id)

#         return StopEvent(result=(str(response), sources))

# try:
#     my_workflow = RAGWorkflow(timeout=30.0)
#     draw_all_possible_flows(my_workflow, filename="final_rag_workflow.html")
# except Exception as e:
#     pass

# async def query_rag(question: str) -> Tuple[str, List[Dict[str, str]]]:
#     workflow = RAGWorkflow(timeout=30.0, verbose=False)
#     try:
#         result = await workflow.run(query=question)
#         return result
#     except Exception as e:
#         print(f"Workflow error: {e}")
#         return f"אירעה שגיאה בעת עיבוד הבקשה: {str(e)}", []


import os
import json
import certifi
import asyncio
from typing import Tuple, List, Dict
from dotenv import load_dotenv

# טיפול בתעודות אבטחה ורשת
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.abspath(os.path.join(current_dir, "..", ".env", ".env"))
load_dotenv(dotenv_path=env_path)

from pinecone import Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.cohere import Cohere
from llama_index.core.workflow import Workflow, step, StartEvent, StopEvent, Event, Context
from llama_index.utils.workflow import draw_all_possible_flows
from llama_index.core.llms import ChatMessage

Settings.embed_model = CohereEmbedding(
    api_key=os.environ["COHERE_API_KEY"],
    model_name="embed-multilingual-v3.0",
    input_type="search_query"
)

llm = Cohere(
    api_key=os.environ["COHERE_API_KEY"],
    model="command-r-08-2024"
)
Settings.llm = llm

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
pinecone_index = pc.Index(os.environ["PINECONE_INDEX_NAME"])
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
index = VectorStoreIndex.from_vector_store(vector_store)

retriever = VectorIndexRetriever(index=index, similarity_top_k=5)
postprocessor = SimilarityPostprocessor(similarity_cutoff=0.5)
response_synthesizer = get_response_synthesizer(response_mode="compact")

class VectorSearchEvent(Event):
    query: str

class StructuredSearchEvent(Event):
    query: str
    category: str

class RetrievedNodesEvent(Event):
    nodes: list
    query: str

class FilteredNodesEvent(Event):
    nodes: list
    query: str

class RAGWorkflow(Workflow):
    
    @step
    async def route_query(self, ctx: Context, ev: StartEvent) -> VectorSearchEvent | StructuredSearchEvent | StopEvent:
        query = ev.get("query")
        
        if not query or not query.strip():
            return StopEvent(result=("אנא הכניסי שאלה חוקית.", []))
            
        print(f"🚦 Router is checking query: '{query}'")
        
        # === התיקון: פרומפט הרבה יותר נוקשה + השאלה הספציפית שלך כדוגמה ===
        prompt = f"""
        You are a strict router for a RAG system.
        Classify the user's query into EXACTLY ONE of these categories: 'decisions', 'rules', 'warnings', or 'general'.
        
        CRITICAL RULES:
        - If the user asks a specific question about how something works, what happens if X occurs, or details about the system -> reply 'general'.
        - ONLY reply 'decisions' if the user explicitly asks for the FULL LIST of all decisions.
        - ONLY reply 'rules' if the user explicitly asks for the FULL LIST of all rules or guidelines.
        - ONLY reply 'warnings' if the user explicitly asks for the FULL LIST of all warnings or risks.

        EXAMPLES:
        User: "מה הצבע העיקרי של המערכת?" -> Answer: general
        User: "מה קורה כשמנהל צוות נמחק מהמערכת?" -> Answer: general
        User: "איך עובד מנגנון ההתחברות?" -> Answer: general
        User: "תציג לי את כל החוקים שיש בפרויקט" -> Answer: rules
        User: "מהן כל ההחלטות הטכניות שהתקבלו?" -> Answer: decisions

        Now, classify this query:
        User: "{query}"
        Answer (reply with one word only):
        """
        
        try:
            msg = ChatMessage(role="user", content=prompt)
            response = llm.chat([msg])
            decision = str(response.message.content).strip().lower()
        except Exception as e:
            print(f"⚠️ Router Error: {e}. Defaulting to Vector Search.")
            decision = "general"
        
        if "decisions" in decision:
            print("🔀 Router decided: Structured Search (Decisions)")
            return StructuredSearchEvent(query=query, category="decisions")
        elif "rules" in decision:
            print("🔀 Router decided: Structured Search (Rules)")
            return StructuredSearchEvent(query=query, category="rules")
        elif "warnings" in decision:
            print("🔀 Router decided: Structured Search (Warnings)")
            return StructuredSearchEvent(query=query, category="warnings")
        else:
            print("🔀 Router decided: Vector Search (Pinecone)")
            return VectorSearchEvent(query=query)

    @step
    async def structured_search(self, ctx: Context, ev: StructuredSearchEvent) -> StopEvent:
        json_path = os.path.abspath(os.path.join(current_dir, "..", "data", "Python Project", "structured_database.json"))
        
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            return StopEvent(result=("שגיאה בטעינת קובץ הנתונים המובנה.", []))
            
        category = ev.category
        items = data.get("items", {}).get(category, [])
        
        if not items:
            return StopEvent(result=(f"לא מצאתי פריטים מסוג {category} במאגר.", []))
            
        # === התיקון: עטיפת התשובה ב-HTML כדי לאלץ יישור לימין (RTL) ב-Gradio ===
        response_text = f"<div dir='rtl' style='text-align: right;'>\n\n**הנה הרשימה המלאה של {category}:**\n\n"
        sources = []
        seen_files = set()
        
        for item in items:
            title = item.get("title") or item.get("rule") or item.get("message", "ללא כותרת")
            response_text += f"🔹 {title}\n\n"
            
            source_info = item.get("source", {})
            tool = source_info.get("tool", "unknown")
            file_name = source_info.get("file", "unknown")
            source_id = f"{tool}-{file_name}"
            
            if source_id not in seen_files:
                sources.append({"tool": tool, "file": file_name})
                seen_files.add(source_id)
                
        response_text += "</div>"
        return StopEvent(result=(response_text, sources))

    @step
    async def retrieve(self, ctx: Context, ev: VectorSearchEvent) -> RetrievedNodesEvent | StopEvent:
        nodes = retriever.retrieve(ev.query)
        if not nodes:
            return StopEvent(result=("לא נמצאו מסמכים כלל במערכת.", []))
        return RetrievedNodesEvent(nodes=nodes, query=ev.query)

    @step
    async def postprocess(self, ctx: Context, ev: RetrievedNodesEvent) -> FilteredNodesEvent | StopEvent:
        nodes = postprocessor.postprocess_nodes(ev.nodes)
        if not nodes:
            return StopEvent(result=("לא מצאתי מידע רלוונטי מספיק כדי לענות על שאלתך.", []))
        return FilteredNodesEvent(nodes=nodes, query=ev.query)

    @step
    async def synthesize(self, ctx: Context, ev: FilteredNodesEvent) -> StopEvent:
        response = response_synthesizer.synthesize(ev.query, ev.nodes)
        
        sources = []
        seen_files = set()
        for node in ev.nodes:
            metadata = node.node.metadata
            tool = metadata.get("tool", "Unknown Tool")
            file_name = metadata.get("file_name", "Unknown File")
            source_id = f"{tool}-{file_name}"
            if source_id not in seen_files:
                sources.append({"tool": tool, "file": file_name})
                seen_files.add(source_id)

        # וידוא שגם התשובה הרגילה מיושרת לימין
        rtl_response = f"<div dir='rtl' style='text-align: right;'>{str(response)}</div>"
        return StopEvent(result=(rtl_response, sources))

try:
    my_workflow = RAGWorkflow(timeout=30.0)
    draw_all_possible_flows(my_workflow, filename="final_rag_workflow.html")
except Exception as e:
    pass

async def query_rag(question: str) -> Tuple[str, List[Dict[str, str]]]:
    workflow = RAGWorkflow(timeout=30.0, verbose=False)
    try:
        result = await workflow.run(query=question)
        return result
    except Exception as e:
        print(f"Workflow error: {e}")
        return f"אירעה שגיאה בעת עיבוד הבקשה: {str(e)}", []