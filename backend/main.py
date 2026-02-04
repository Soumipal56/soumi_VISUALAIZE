import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load variables (HARDCODED FOR TESTING)
load_dotenv()

# --- SECURITY FIX: Use Environment Variable Only ---
GENAI_KEY = os.getenv("GEMINI_API_KEY")

if not GENAI_KEY:
    print("⚠️ CRITICAL WARNING: GEMINI_API_KEY is missing in Render Environment!")
else:
    print(f"✅ Secure API Key Loaded: {GENAI_KEY[:5]}... (Valid)")
    genai.configure(api_key=GENAI_KEY)

MODEL_NAME = 'gemini-2.0-flash'

app = FastAPI()

# 3. Enable CORS for Vercel
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

@app.get("/")
def health_check():
    # This simple route allows Render to see the app is "alive"
    return {"status": "Online", "key_loaded": bool(GENAI_KEY)}

@app.post("/generate")
async def generate_graph(request: GraphRequest):
    # We configure the AI here, just in case the key was added late
    current_key = os.getenv("GEMINI_API_KEY")
   # Use the global hardcoded key
    current_key = GENAI_KEY 
    if not current_key:
        raise HTTPException(status_code=500, detail="Server Error: Key is empty.")
    
    genai.configure(api_key=current_key)
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
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
          "nodes": [
             {"id": "1", "label": "Start"},
             {"id": "2", "label": "Process"}
          ],
          "edges": [
             {"source": "1", "target": "2", "label": "next"}
          ]
        }
        """
        
        response = model.generate_content(
            f"{system_prompt}\n\nUSER PROMPT: {request.prompt}",
            generation_config={"response_mime_type": "application/json"}
        )
        
        return json.loads(response.text)

    except Exception as e:
        print(f"AI Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_with_ai(request: ChatRequest):
    current_key = os.getenv("GEMINI_API_KEY")
    if not current_key:
        raise HTTPException(status_code=500, detail="API Key missing.")
    
    genai.configure(api_key=current_key)
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(f"Context: {request.context}\nUser: {request.message}")
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/regenerate_code")
async def regenerate_code(request: CodeRequest):
    current_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=current_key)
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(
             f"Convert this system: {request.prompt} to {request.language} code. Return ONLY code."
        )
        return {"code_snippet": response.text.replace("```",""), "code_explanation": f"Converted to {request.language}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))