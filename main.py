from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURAZIONE TOKEN ---
HF_TOKEN = os.environ.get("HF_TOKEN")

if not HF_TOKEN:
    # Fallback di sicurezza se ci siamo dimenticati di settarlo
    print("⚠️ ERRORE: Token HF non trovato! Assicurati di averlo messo nelle Environment Variables di Render.")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

# --- CARICAMENTO KNOWLEDGE BASE ---
try:
    with open("knowledge.json", "r", encoding="utf-8") as f:
        KNOWLEDGE_BASE = json.load(f)
except:
    KNOWLEDGE_BASE = {}

# --- MAPPA PRODOTTI ---
PRODUCT_MAP = {
    "cognidesk": "https://synapsislab.store/cognidesk/",
    "customer": "https://synapsislab.store/cognidesk/", 
    "business plan": "https://synapsislab.store/business-plan-ai/",
    "shop": "https://synapsislab.store/smart-inteligent-shop-ai/",
    "e-commerce": "https://synapsislab.store/smart-inteligent-shop-ai/",
    "store": "https://synapsislab.store/smart-inteligent-shop-ai/",
    "ccv": "https://synapsislab.store/ccv-ai/",
    "vision": "https://synapsislab.store/ccv-ai/",
    "excel": "https://synapsislab.store/excel-rag-intelligence/",
    "spreadsheet": "https://synapsislab.store/excel-rag-intelligence/",
    "deep": "https://synapsislab.store/deep-intelligent-ai-analysis/",
    "analysis": "https://synapsislab.store/deep-intelligent-ai-analysis/",
    "email": "https://synapsislab.store/ai-intelligent-automatic-email/",
    "mail": "https://synapsislab.store/ai-intelligent-automatic-email/",
    "gmail": "https://synapsislab.store/ai-intelligent-automatic-email/",
    "about": "https://synapsislab.store/abaut-us/",
    "plugin": "https://synapsislab.store/wp-gemini-clone/",
    "gemini clone": "https://synapsislab.store/wp-gemini-clone/",
    "wp gemini": "https://synapsislab.store/wp-gemini-clone/"
}

class BotRequest(BaseModel):
    current_url: str
    user_question: str

@app.post("/ask")
def ask_ai(request: BotRequest):
    user_q_lower = request.user_question.lower()
    
    # 1. IDENTIFICAZIONE PRODOTTO
    target_url = None
    detected_product = "General Synapsis Tech"
    
    for keyword, url in PRODUCT_MAP.items():
        if keyword in user_q_lower:
            target_url = url
            detected_product = keyword.upper()
            break
    
    # 2. GESTIONE LINK E CONTESTO
    final_link_to_append = "https://synapsislab.store/servizi-soluzioni/" 
    
    if target_url and target_url in KNOWLEDGE_BASE:
        page_context = KNOWLEDGE_BASE[target_url]
        final_link_to_append = target_url
        
        # PROMPT MULTILINGUA SPECIFICO
        system_instruction = f"""
        You are the AI Sales Expert of 'Synapsis Lab'.
        TOPIC: User is asking about {detected_product}.
        
        RULES:
        1. DETECT the language of the user's question (Italian, English, Spanish, etc.).
        2. REPLY IN THE SAME LANGUAGE.
        3. Explain why {detected_product} is the best solution using the context provided.
        4. Tone: Professional, Technical, "Hacker-Chic".
        5. Do NOT include the link in the text, I will add it automatically.
        """
    else:
        page_context = KNOWLEDGE_BASE.get(request.current_url, "General info about Synapsis Lab")
        
        # PROMPT MULTILINGUA GENERICO
        system_instruction = """
        You are the AI Sales Expert of 'Synapsis Lab'.
        RULES:
        1. DETECT the language of the user's question.
        2. REPLY IN THE SAME LANGUAGE.
        3. Promote RAG systems, Databases and Automation tools personally, OCR for acquisition of large database papars,creations of systems TSS and SST for Automating calling.
        4. Tone: Professional and concise.
        """

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": f"Context:\n{page_context}\n\nQuestion:\n{request.user_question}"}
    ]

    try:
        completion = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=messages,
            max_tokens=600, # Aumentato un pelo per le traduzioni
            temperature=0.3,
        )
        
        ai_reply = completion.choices[0].message.content.strip()
        
        # Aggiungiamo il link in modo "Universale" (icona invece di testo che cambia lingua)
        final_response = f"{ai_reply}\n\n🔗 {final_link_to_append}"
        
        return {"reply": final_response}

    except Exception as e:
        print(f"❌ Error: {e}")
        return {"reply": "System Error: Neural Link unstable."}