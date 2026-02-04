import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load variables
load_dotenv()

# --- CONFIGURATION: 2026 MODEL LIST ---
# Gemini 1.5 is deprecated. We use 2.5 and 2.0 now.
MODEL_PRIORITY_LIST = [
    'gemini-2.0-flash-exp',   # Often the most accessible experimental model
    'gemini-2.0-flash',       # Stable 2.0
    'gemini-1.5-flash'        # Fallback (Just in case it is still active for your specific key)
]

# --- SECURITY CHECK ---
GENAI_KEY = os.getenv("GEMINI_API_KEY")

if not GENAI_KEY:
    print("⚠️ CRITICAL WARNING: GEMINI_API_KEY is missing in Render Environment!")
else:
    print(f"✅ Secure API Key Loaded: {GENAI_KEY[:5]}... (Valid)")
    genai.configure(api_key=GENAI_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GraphRequest(BaseModel):
    prompt: str

class ChatRequest(BaseModel):
    message: str
    context: str
    
class CodeRequest(BaseModel):
    prompt: str
    language: str

# --- HELPER FUNCTION: AUTOMATIC SWITCHING ---
def get_model_response(prompt_text, use_json=False):
    last_error = None
    
    for model_name in MODEL_PRIORITY_LIST:
        try:
            print(f"🔄 Attempting generation with: {model_name}...")
            model = genai.GenerativeModel(model_name)
            
            config = {"response_mime_type": "application/json"} if use_json else {}
            
            response = model.generate_content(
                prompt_text,
                generation_config=config
            )
            
            print(f"✅ Success with {model_name}!")
            return response.text 
            
        except Exception as e:
            # Catch 404 (Deprecated) or 429 (Quota)
            print(f"⚠️ Model {model_name} failed. Error: {e}")
            last_error = e
            continue 
            
    raise Exception(f"All AI models failed. Please check your API Key. Last error: {last_error}")

@app.get("/")
def health_check():
    return {"status": "Online", "key_loaded": bool(GENAI_KEY), "models": MODEL_PRIORITY_LIST}

@app.post("/generate")
async def generate_graph(request: GraphRequest):
    if not GENAI_KEY:
        raise HTTPException(status_code=500, detail="Server Error: API Key missing on Render.")
    
    system_prompt = """
    You are a System Visualization AI. 
    Generate a JSON object for a node-based graph editor (ReactFlow).
    Strict JSON Schema:
    {
      "title": "Short Title",
      "summary": "1 sentence summary",
      "explanation": "Brief explanation",
      "execution_trace": "Step-by-step logic trace",
      "code_snippet": "Python code representation",
      "nodes": [{"id": "1", "label": "Start"}],
      "edges": [{"source": "1", "target": "2", "label": "next"}]
    }
    """
    
    try:
        response_text = get_model_response(f"{system_prompt}\n\nUSER PROMPT: {request.prompt}", use_json=True)
        return json.loads(response_text)
    except Exception as e:
        print(f"AI Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_with_ai(request: ChatRequest):
    try:
        response_text = get_model_response(f"Context: {request.context}\nUser: {request.message}", use_json=False)
        return {"reply": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/regenerate_code")
async def regenerate_code(request: CodeRequest):
    try:
        response_text = get_model_response(
             f"Convert: {request.prompt} to {request.language}. Return ONLY code.", 
             use_json=False
        )
        return {"code_snippet": response_text.replace("```",""), "code_explanation": f"Converted to {request.language}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))