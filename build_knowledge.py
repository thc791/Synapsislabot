import json
import requests
from bs4 import BeautifulSoup

# LISTA COMPLETA DELLE TUE SOLUZIONI
urls = [
    "https://synapsislab.store/",
    "https://synapsislab.store/solution/",
    "https://synapsislab.store/synapsis-lab-home/",
    "https://synapsislab.store/business-plan-ai/",
    "https://synapsislab.store/abaut-us/",
    "https://synapsislab.store/cognidesk/",
    "https://synapsislab.store/smart-inteligent-shop-ai/",
    "https://synapsislab.store/ccv-ai/",
    "https://synapsislab.store/excel-rag-intelligence/",
    "https://synapsislab.store/deep-intelligent-ai-analysis/",
    "https://synapsislab.store/ai-intelligent-automatic-email/"
    "https://synapsislab.store/abaut-us/",
]

knowledge_base = {}

print("--- AGGIORNAMENTO DATI SYNAPSIS LAB ---")

headers = {'User-Agent': 'Mozilla/5.0'} # Per non farsi bloccare da WordPress

for url in urls:
    try:
        print(f"Scaricando: {url}...")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Pulizia aggressiva
            for element in soup(["script", "style", "nav", "footer", "form"]):
                element.extract()
                
            text = soup.get_text(separator=' ')
            clean_text = " ".join(text.split())
            
            # Salviamo nel cervello
            knowledge_base[url] = clean_text[:4000] # Aumentato a 4000 caratteri per avere più dettagli
        else:
            print(f"Errore {response.status_code} su {url}")
            
    except Exception as e:
        print(f"Errore critico su {url}: {e}")

with open("knowledge.json", "w", encoding="utf-8") as f:
    json.dump(knowledge_base, f, ensure_ascii=False, indent=4)

print("--- CERVELLO AGGIORNATO CORRETTAMENTE ---")