import os
import json
import requests

CACHE_FILE = 'src/portfolio_cache.json'
MEDIA_DIR = 'public/archive_media'
os.makedirs(MEDIA_DIR, exist_ok=True)

TOKEN = os.getenv('IG_ACCESS_TOKEN')

# Cerca il token nella cache esistente
if not TOKEN and os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
            TOKEN = old_data.get('access_token') or old_data.get('token')
    except Exception:
        pass

if not TOKEN:
    print("\n🔑 NESSUN ACCESS TOKEN TROVATO!")
    print("Incolla qui sotto il tuo Instagram Access Token:")
    TOKEN = input("Token > ").strip()

if TOKEN:
    print(f"\n🌐 Handshake con Meta Graph API in corso...")
    graph_url = f"https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,children{{media_type,media_url,thumbnail_url}}&limit=100&access_token={TOKEN}"
    
    all_media = []
    next_url = graph_url
    
    try:
        while next_url and len(all_media) < 450:
            res = requests.get(next_url, timeout=15)
            if res.status_code == 200:
                data = res.json()
                items = data.get('data', [])
                all_media.extend(items)
                print(f"  ↳ Recuperati {len(all_media)} nodi con URL freschi da Meta...")
                next_url = data.get('paging', {}).get('next')
            else:
                print(f"❌ Errore Meta (HTTP {res.status_code}): {res.text}")
                break
        
        if all_media:
            cache_payload = {
                "access_token": TOKEN,
                "updated_at": requests.utils.default_user_agent(),
                "data": all_media
            }
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cache_payload, f, ensure_ascii=False, indent=2)
            print("✨ Cache aggiornata con URL freschi!\n")
    except Exception as e:
        print(f"⚠️ Errore connessione a Meta: {e}")

# --- FASE 2: DOWNLOAD NEL CAVEAU LOCALE ---
if not os.path.exists(CACHE_FILE):
    print("❌ Cache non trovata!")
    exit(1)

with open(CACHE_FILE, 'r', encoding='utf-8') as f:
    cache_data = json.load(f)

items = cache_data.get('data', [])
print(f"⚡ Inizio mirroring locale ({len(items)} nodi)...")

downloaded_count = 0
existing_count = 0

for idx, item in enumerate(items):
    item_id = item.get('id', f'node_{idx}')
    media_type = item.get('media_type', 'IMAGE')
    remote_url = item.get('thumbnail_url') or item.get('media_url')
    
    if not remote_url:
        continue

    ext = 'jpg'
    if media_type == 'VIDEO' and '.mp4' in remote_url.lower():
        ext = 'mp4'

    local_filename = f"{item_id}.{ext}"
    local_path = os.path.join(MEDIA_DIR, local_filename)
    relative_url = f"/archive_media/{local_filename}"

    if not os.path.exists(local_path):
        if remote_url.startswith('http'):
            try:
                res = requests.get(remote_url, timeout=10)
                if res.status_code == 200:
                    with open(local_path, 'wb') as img_file:
                        img_file.write(res.content)
                    item['media_url'] = relative_url
                    item['thumbnail_url'] = relative_url
                    downloaded_count += 1
                    print(f"[{idx+1}/{len(items)}] 💾 Scaricata: {local_filename}")
                else:
                    print(f"[{idx+1}/{len(items)}] ⚠️ Fallita HTTP {res.status_code}: {item_id}")
            except Exception as e:
                print(f"[{idx+1}/{len(items)}] ❌ Errore HTTP: {e}")
    else:
        item['media_url'] = relative_url
        item['thumbnail_url'] = relative_url
        existing_count += 1

with open(CACHE_FILE, 'w', encoding='utf-8') as f:
    json.dump(cache_data, f, ensure_ascii=False, indent=2)

print(f"\n🌲 RISULTATO FINALE:")
print(f"  • Scaricate: {downloaded_count}")
print(f"  • Locali: {existing_count}")
print(f"🎉 L'Atelier è immune ai link scaduti!")
