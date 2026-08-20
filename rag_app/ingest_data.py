import os
import certifi
from typing import Dict
from dotenv import load_dotenv
from pinecone import Pinecone
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.core.node_parser import MarkdownNodeParser

# טיפול בתעודות אבטחה (עבור נטפרי)
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

# טעינת משתני סביבה
env_path = os.path.join(os.path.dirname(__file__), "..", ".env", ".env")
load_dotenv(dotenv_path=env_path)

if not os.getenv("COHERE_API_KEY") or not os.getenv("PINECONE_API_KEY"):
    raise ValueError("⚠️ Missing API keys! Check your .env file.")

# הגדרת מודל הטמעה לאינדוקס (דרישה #3)
Settings.embed_model = CohereEmbedding(
    api_key=os.environ["COHERE_API_KEY"],
    model_name="embed-multilingual-v3.0",
    input_type="search_document" # חובה עבור אינדוקס ב-Cohere
)

def extract_metadata(file_path: str) -> Dict[str, str]:
    """
    מחלץ מידע על הכלי שממנו הגיע הקובץ על בסיס נתיב הקובץ.
    """
    tool_name = "unknown"
    lower_path = file_path.lower()
    if ".cursor" in lower_path:
        tool_name = "cursor"
    elif ".kiro" in lower_path:
        tool_name = "kiro"

    
    return {
        "tool": tool_name,
        "file_name": os.path.basename(file_path),
        "full_path": file_path
    }

def main():
    try:
        # 1. Loading
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "Python Project")
        print(f"📂 Loading markdown files from: {data_dir}")
        
        reader = SimpleDirectoryReader(
            input_dir=data_dir,
            required_exts=[".md"],
            recursive=True,
            exclude_hidden=False, 
            file_metadata=extract_metadata
        )
        documents = reader.load_data()
        print(f"✅ Loaded {len(documents)} documents.")

        # 2. Chunking (דרישה #2 - שימוש מפורש ב-Node Parser למסמכי MD)
        parser = MarkdownNodeParser()
        nodes = parser.get_nodes_from_documents(documents)
        print(f"✂️ Created {len(nodes)} chunks from markdown files.")

        # 3. VectorStore & Pinecone Setup
        print("🔌 Connecting to Pinecone...")
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        pinecone_index = pc.Index(os.environ["PINECONE_INDEX_NAME"])
        
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # 4. Indexing (Embedding & Uploading)
        print("🧠 Embedding and uploading to Pinecone...")
        # אנו מעבירים את ה-nodes במקום documents כי כבר חתכנו אותם
        index = VectorStoreIndex(
            nodes,
            storage_context=storage_context,
            show_progress=True
        )
        print("🎉 Success! All data is indexed.")
        
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")

if __name__ == "__main__":
    main()