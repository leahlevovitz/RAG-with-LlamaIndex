import os
import json
import certifi
import time  # הוספנו כדי לעשות הפסקות בין בקשות
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, Field

from llama_index.core import SimpleDirectoryReader
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.llms import ChatMessage  # שימוש בממשק הצ'אט החדש
from llama_index.llms.cohere import Cohere

# Setup certificates and environment variables
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.abspath(os.path.join(current_dir, "..", ".env", ".env"))
load_dotenv(dotenv_path=env_path)

# ==========================================
# 1. Pydantic Schema
# ==========================================
class SourceInfo(BaseModel):
    tool: str = Field(default="unknown", description="Tool name")
    file: str = Field(default="unknown", description="File name")
    anchor: str = Field(default="General", description="Location in file")

class Decision(BaseModel):
    id: str = Field(default="N/A", description="Unique ID")
    title: str = Field(default="N/A", description="Decision title")
    summary: str = Field(default="N/A", description="Decision summary")
    tags: List[str] = Field(default_factory=list, description="Tags")
    source: SourceInfo = Field(default_factory=SourceInfo, description="Source info")

class Rule(BaseModel):
    id: str = Field(default="N/A", description="Unique ID")
    rule: str = Field(default="N/A", description="The rule")
    scope: str = Field(default="N/A", description="Scope")
    source: SourceInfo = Field(default_factory=SourceInfo, description="Source info")

class WarningInfo(BaseModel):
    id: str = Field(default="N/A", description="Unique ID")
    area: str = Field(default="N/A", description="Area")
    message: str = Field(default="N/A", description="Warning")
    severity: str = Field(default="N/A", description="Severity")
    source: SourceInfo = Field(default_factory=SourceInfo, description="Source info")

class ExtractedData(BaseModel):
    decisions: List[Decision] = Field(default_factory=list)
    rules: List[Rule] = Field(default_factory=list)
    warnings: List[WarningInfo] = Field(default_factory=list)

def main():
    print("🚀 Starting OFFICIAL LlamaIndex Structured Extraction (Slow & Steady Mode)...")
    llm = Cohere(api_key=os.environ["COHERE_API_KEY"], model="command-r-08-2024")

    data_dir = os.path.abspath(os.path.join(current_dir, "..", "data", "Python Project"))
    reader = SimpleDirectoryReader(input_dir=data_dir, required_exts=[".md"], recursive=True, exclude_hidden=False)
    documents = reader.load_data()
    print(f"📂 Loaded {len(documents)} documents. This will take about ~3 minutes to avoid API blocks.\n")

    final_json = {
        "schema_version": "1.0",
        "items": {"decisions": [], "rules": [], "warnings": []}
    }

    parser = PydanticOutputParser(ExtractedData)
    format_instructions = parser.get_format_string()

    for i, doc in enumerate(documents):
        file_path = doc.metadata.get('file_path', 'unknown.md')
        file_name = os.path.basename(file_path)
        tool_name = "cursor" if ".cursor" in file_path.lower() else "kiro" if ".kiro" in file_path.lower() else "unknown"
        
        print(f"[{i+1}/{len(documents)}] 🔍 Scanning: {file_name}...")
        
        prompt_text = (
            f"Extract technical decisions, rules, and warnings from the text below.\n"
            f"The source file is '{file_name}' and the tool is '{tool_name}'.\n\n"
            f"If a category is empty, leave its list empty.\n\n"
            f"{format_instructions}\n\n"
            f"IMPORTANT: You must return ONLY the raw JSON object. Do not include markdown tags like ```json.\n\n"
            f"Text to process:\n{doc.text}"
        )

        try:
            # שימוש בממשק ה-chat שעובד מושלם (פותר את ה-404)
            msg = ChatMessage(role="user", content=prompt_text)
            response = llm.chat([msg])
            
            # ניקוי מהיר למקרה שהמודל עדיין מתעקש להוסיף ```json
            clean_text = str(response.message.content).replace("```json", "").replace("```", "").strip()
            
            # הפארסר של LlamaIndex מוודא סכמה
            result: ExtractedData = parser.parse(clean_text)
            
            for d in result.decisions: final_json["items"]["decisions"].append(d.model_dump())
            for r in result.rules: final_json["items"]["rules"].append(r.model_dump())
            for w in result.warnings: final_json["items"]["warnings"].append(w.model_dump())
            
            print("   ✅ Extracted successfully.")
            
        except Exception as e:
            print(f"   ⚠️ Could not extract strictly formatted data from {file_name}. Skipping.")

        # המתנה כדי ש-Cohere לא יחסום אותנו על בקשות מהירות מדי (פותר את ה-429)
        if i < len(documents) - 1:
            print("   ⏳ Sleeping 12 seconds to respect API limits...")
            time.sleep(12)

    output_path = os.path.join(data_dir, "structured_database.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_json, f, ensure_ascii=False, indent=4)
        
    print(f"\n✅ SUCCESS! Data saved to: {output_path}")
    print(f"📊 Total items extracted:")
    print(f"   🔹 Decisions: {len(final_json['items']['decisions'])}")
    print(f"   🔹 Rules: {len(final_json['items']['rules'])}")
    print(f"   🔹 Warnings: {len(final_json['items']['warnings'])}")

if __name__ == "__main__":
    main()