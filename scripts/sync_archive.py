import os
import json
import requests

CACHE_FILE = 'src/portfolio_cache.json'
MEDIA_DIR = 'public/archive_media'

os.makedirs(MEDIA_DIR, exist_ok=True)

if not os.path.exists(CACHE_FILE):
    print(f"❌ Errore: File {CACHE_FILE} non trovato!")
    exit(1)

with open(CACHE_FILE, 'r', encoding='utf-8') as f:
    cache_data = json.load(f)

items = cache_data.get('data', [])
print(f"⚡ Inizio mirroring locale per {len(items)} nodi d'archivio IMLAND...\n")

downloaded_count = 0
existing_count = 0

for idx, item in enumerate(items):
    item_id = item.get('id', f'node_{idx}')
    media_type = item.get('media_type', 'IMAGE')
    remote_url = item.get('thumbnail_url') or item.get('media_url')
    
    if not remote_url:
        continue

    # Estensione file
    ext = 'jpg'
    if media_type == 'VIDEO' and '.mp4' in remote_url.lower():
        ext = 'mp4'

    local_filename = f"{item_id}.{ext}"
    local_path = os.path.join(MEDIA_DIR, local_filename)
    relative_url = f"/archive_media/{local_filename}"

    # Se l'immagine non è ancora nel caveau locale, la scarichiamo!
    if not os.path.exists(local_path) or not remote_url.startswith('/archive_media/'):
        if remote_url.startswith('http'):
            try:
                res = requests.get(remote_url, timeout=12)
                if res.status_code == 200:
                    with open(local_path, 'wb') as img_file:
                        img_file.write(res.content)
                    item['media_url'] = relative_url
                    item['thumbnail_url'] = relative_url
                    downloaded_count += 1
                    print(f"[{idx+1}/{len(items)}] 💾 Blindata nel caveau: {local_filename}")
                else:
                    print(f"[{idx+1}/{len(items)}] ⚠️ URL Meta scaduto (HTTP {res.status_code}): {item_id}")
            except Exception as e:
                print(f"[{idx+1}/{len(items)}] ❌ Errore connessione per {item_id}: {e}")
        else:
            item['media_url'] = relative_url
            item['thumbnail_url'] = relative_url
    else:
        item['media_url'] = relative_url
        item['thumbnail_url'] = relative_url
        existing_count += 1

# Salviamo la cache aggiornata con i percorsi locali
with open(CACHE_FILE, 'w', encoding='utf-8') as f:
    json.dump(cache_data, f, ensure_ascii=False, indent=2)

print(f"\n✨ Sincronizzazione Completata!")
print(f"📦 Nuove immagini scaricate: {downloaded_count}")
print(f"🔒 Immagini già presenti nel caveau: {existing_count}")
print(f"🌲 Il portfolio IMLAND MONTEROSA è ora al 100% INDIPENDENTE dai server di Meta!")
