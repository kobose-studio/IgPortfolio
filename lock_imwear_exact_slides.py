import os
import re
import json

brand_dir = 'public/brand'

# Verifica i byte reali dei file per scartare immagini corrotte o HEIC rinominati (es. hoodie-1.jpg)
def is_browser_decodable(filepath):
    if not os.path.isfile(filepath) or os.path.getsize(filepath) < 2048:
        return False
    with open(filepath, 'rb') as f:
        head = f.read(12)
    is_jpeg = head.startswith(b'\xff\xd8\xff')
    is_png  = head.startswith(b'\x89PNG\r\n\x1a\n')
    is_webp = head[:4] == b'RIFF' and head[8:12] == b'WEBP'
    return is_jpeg or is_png or is_webp

all_brand = sorted(os.listdir(brand_dir)) if os.path.isdir(brand_dir) else []

valid_classic = []
valid_zip = []
valid_tee = []

print("\n--- CONTROLLO INTEGRITÀ FILE IN public/brand/ ---")
for fname in all_brand:
    low = fname.lower()
    if not low.endswith(('.jpg', '.jpeg', '.png', '.webp')):
        continue
    full = os.path.join(brand_dir, fname)
    if not is_browser_decodable(full):
        print(f"[SCARTATO - FILE CORROTTO/ILLEGGIBILE]: {fname}")
        continue
    # Esclude esplicitamente hoodie-1.jpg e hoodie-A.jpg dalla colonna 1
    if low in ('hoodie-1.jpg', 'hoodie-a.jpg'):
        print(f"[ESCLUSO COME RICHIESTO]: {fname}")
        continue

    url = f"/brand/{fname}"
    if fname in ('hoodie_zip-1.jpg', 'hoodie_zip-2.jpg', 'hoodie_zip-3.jpg'):
        valid_zip.append(url)
    elif low.startswith('hoodie-') and 'zip' not in low:
        valid_classic.append(url)
    elif low.startswith('tee-'):
        valid_tee.append(url)

valid_zip.sort()
print("Colonna 1 (Classic):", valid_classic)
print("Colonna 2 (Full-Zip):", valid_zip)
print("Colonna 3 (Essentials):", valid_tee)

# Trova esattamente in quali file di src/ si trovano le righe del catalogo IMWEAR
print("\n--- DOVE SI TROVANO NEL CODICE SORGENTE ---")
target_files = []
for root, _, files in os.walk('src'):
    for fn in files:
        if fn.endswith(('.astro', '.js', '.ts')):
            p = os.path.join(root, fn)
            with open(p, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            matched_lines = [i+1 for i, l in enumerate(lines) if '/brand/' in l or 'FULL-ZIP' in l.upper()]
            if matched_lines:
                print(f"File: {p} -> Righe: {matched_lines}")
                target_files.append(p)

# Controller autonomo e blindato per i 3 caroselli IMWEAR
imwear_controller = f'''<script id="imland-imwear-exact-lock" is:inline>
(function() {{
  if (window.__IMLAND_IMWEAR_EXACT_LOCK) return;
  window.__IMLAND_IMWEAR_EXACT_LOCK = true;

  const SLIDES = {{
    col1: {json.dumps(valid_classic)},
    col2: {json.dumps(valid_zip)},
    col3: {json.dumps(valid_tee)}
  }};

  const idx = {{ col1: 0, col2: 0, col3: 0 }};

  function getColumns(modal) {{
    // Cerca le 3 card tramite i titoli specifici
    const map = {{ col1: null, col2: null, col3: null }};
    const blocks = modal.querySelectorAll('div, article, section');

    for (const el of blocks) {{
      const txt = (el.textContent || '').toUpperCase();
      const imgs = el.querySelectorAll('img');
      if (imgs.length === 0) continue;

      const hasClassic = txt.includes('CLASSIC HOODIE');
      const hasZip     = txt.includes('FULL-ZIP');
      const hasEss     = txt.includes('ESSENTIALS');

      // Deve contenere SOLO il titolo di quella singola colonna
      if (hasClassic && !hasZip && !hasEss) map.col1 = el;
      if (hasZip && !hasClassic && !hasEss) map.col2 = el;
      if (hasEss && !hasClassic && !hasZip) map.col3 = el;
    }}

    // Fallback posizionale sui 3 wrapper se la struttura DOM è annidata diversamente
    if (!map.col1 || !map.col2 || !map.col3) {{
      const wrappers = modal.querySelectorAll('.carousel-wrapper');
      if (wrappers.length >= 3) {{
        map.col1 = map.col1 || wrappers[0];
        map.col2 = map.col2 || wrappers[1];
        map.col3 = map.col3 || wrappers[2];
      }}
    }}
    return map;
  }}

  function renderImwearLookbook(step) {{
    const modal = document.getElementById('brand-modal') || document.querySelector('[class*="brand-panel"]');
    if (!modal) return;

    const cols = getColumns(modal);
    (['col1', 'col2', 'col3']).forEach((key) => {{
      const container = cols[key];
      const list = SLIDES[key];
      if (!container || !list || list.length === 0) return;

      if (step) {{
        idx[key] = (idx[key] + 1) % list.length;
      }}
      const activeSrc = list[idx[key]];

      // Individua il box immagine della colonna e sostituisce eventuali <img> multiple o rotte con un singolo nodo pulito
      const imgs = Array.from(container.querySelectorAll('img'));
      if (imgs.length === 0) return;

      const primaryImg = imgs[0];
      // Rimuove eventuali <img> duplicate sovrapposte dal vecchio carosello che potevano mostrare foto sbagliate
      for (let i = 1; i < imgs.length; i++) {{
        imgs[i].remove();
      }}

      if (primaryImg.getAttribute('src') !== activeSrc) {{
        primaryImg.style.opacity = '0.25';
        primaryImg.setAttribute('src', activeSrc);
        primaryImg.onload = () => {{ primaryImg.style.opacity = '1'; }};
        setTimeout(() => {{ primaryImg.style.opacity = '1'; }}, 120);
      }} else {{
        primaryImg.style.opacity = '1';
      }}

      primaryImg.style.setProperty('position', 'relative', 'important');
      primaryImg.style.setProperty('width', '100%', 'important');
      primaryImg.style.setProperty('height', '100%', 'important');
      primaryImg.style.setProperty('object-fit', 'cover', 'important');
      primaryImg.style.setProperty('display', 'block', 'important');
      primaryImg.style.setProperty('transition', 'opacity 0.55s ease, transform 4s ease', 'important');
    }});
  }}

  window.addEventListener('DOMContentLoaded', () => renderImwearLookbook(false));
  document.addEventListener('click', () => setTimeout(() => renderImwearLookbook(false), 40));
  setInterval(() => renderImwearLookbook(true), 2800);
}})();
</script>
'''

for p in target_files:
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()

    # Sostituisce subito nel sorgente ogni riferimento al file rotto hoodie-1.jpg
    c = c.replace('/brand/hoodie-1.jpg', '/brand/hoodie-2.jpg')
    c = c.replace('/brand/hoodie-A.jpg', '/brand/hoodie-2.jpg')

    # Rimuove vecchi lock per non duplicarli
    c = re.sub(r'<script id="imland-imwear-exact-lock"[\s\S]*?</script>', '', c)
    c += "\n" + imwear_controller

    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)

print("\nLOCK IMWEAR COMPLETATO SU TUTTI I FILE TARGET.")
