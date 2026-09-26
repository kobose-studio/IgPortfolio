import os
import json
import urllib.request
from urllib.error import URLError, HTTPError

print("⚡ Inizializzazione Data Engine...")

# 1. Estrazione variabili dal file .env
env_vars = {}
try:
    with open('.env') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                env_vars[key] = value
except FileNotFoundError:
    print("❌ ERRORE: File .env non trovato nella radice del progetto.")
    exit(1)

TOKEN = env_vars.get('IG_ACCESS_TOKEN')
if not TOKEN:
    print("❌ ERRORE CRITICO: IG_ACCESS_TOKEN mancante nel file .env.")
    exit(1)

print("🔌 Connessione alle API Graph di Instagram in corso...")

# 2. Endpoint API di Meta
url = f"https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,thumbnail_url,permalink,timestamp&access_token={TOKEN}"

try:
    # 3. Esecuzione della richiesta HTTPS
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        
    # 4. Generazione della cartella di destinazione (se mancante)
    os.makedirs('src', exist_ok=True)
    
    # 5. Scrittura fisica della cache su disco
    with open('src/portfolio_cache.json', 'w') as f:
        json.dump(data, f, indent=4)
        
    media_count = len(data.get('data', []))
    print(f"✅ VITTORIA: Estratti {media_count} nodi multimediali.")
    print("✅ CACHE GENERATA: src/portfolio_cache.json salvato con successo.")

except HTTPError as e:
    print(f"❌ ERRORE HTTP DI META: Codice {e.code}")
    print(f"Dettagli Meta: {e.read().decode()}")
except URLError as e:
    print(f"❌ ERRORE DI RETE: {e.reason}")
except Exception as e:
    print(f"❌ ERRORE IMPREVISTO SUL SERVER: {str(e)}")
