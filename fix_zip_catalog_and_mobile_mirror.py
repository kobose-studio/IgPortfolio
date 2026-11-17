import os
import re
import json

target = 'src/components/PortfolioSceneSphere.astro'
brand_dir = 'public/brand'

with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# Funzione di controllo integrità reale dell'immagine (evita riquadri grigi/corrotti)
def is_valid_image(filepath):
    if not os.path.isfile(filepath) or os.path.getsize(filepath) < 2048:
        return False
    with open(filepath, 'rb') as img_f:
        header = img_f.read(8)
    # Verifica magic bytes JPEG (\xff\xd8) o PNG (\x89PNG)
    return header.startswith(b'\xff\xd8') or header.startswith(b'\x89PNG')

all_files = sorted(os.listdir(brand_dir)) if os.path.isdir(brand_dir) else []

# Smistamento automatico e verificato dei 3 cataloghi
col_classic = []
col_zip = []
col_tee = []

for fname in all_files:
    lower = fname.lower()
    if not lower.endswith(('.jpg', '.jpeg', '.png')):
        continue
    full_path = os.path.join(brand_dir, fname)
    if not is_valid_image(full_path):
        print(f"⚠️ Scartato file non valido o corrotto: {fname}")
        continue

    web_path = f"/brand/{fname}"
    if 'zip' in lower:
        col_zip.append(web_path)
    elif lower.startswith('hoodie-'):
        col_classic.append(web_path)
    elif lower.startswith('tee-'):
        col_tee.append(web_path)

# Ordine naturale per i file zip (hoodie_zip-1, 2, 3, zip-hoodie)
col_zip.sort()

print("✅ Colonna 1 (Classic Hoodie) verificata:", col_classic)
print("✅ Colonna 2 (Full-Zip Hoodie - tutti i *zip*) verificata:", col_zip)
print("✅ Colonna 3 (Essentials & Gear) verificata:", col_tee)

# A. AGGIORNA IL BLOCCO DATI NEL COMPONENTE ASTRO
new_products_block = f'''const products = [
  {{
    title: "IMLAND / CLASSIC HOODIE",
    subtitle: "Signature Collection",
    category: "UNISEX & KIDS // HEAVYWEIGHT",
    desc: "Il capo iconico dell'Atelier IMLAND. Una felpa ad alta grammatura, morbida, densa e calda, pensata per accompagnare il ritmo della montagna e la vita di tutti i giorni. Struttura resistente e massimo comfort.",
    images: {json.dumps(col_classic)}
  }},
  {{
    title: "IMLAND / FULL-ZIP HOODIE",
    subtitle: "Alpine Edition",
    category: "UNISEX // DYNAMIC LAYER",
    desc: "Strato versatile con zip integrale a scorrimento rapido. Morbida, pratica e avvolgente, offre la giusta protezione termica durante le giornate all'aria aperta e nei cambi di temperatura.",
    images: {json.dumps(col_zip)}
  }},
  {{
    title: "IMLAND / ESSENTIALS & GEAR",
    subtitle: "Raw Cotton & Lightwear",
    category: "APPAREL & ACCESSORIES",
    desc: "L'ecosistema essenziale IMLAND. La T-Shirt e la sacca 'Gerla Bag' sono realizzate in purissimo cotone organico al 100%. Il Neck Warmer è un copricollo leggerissimo e traspirante, progettato per riparare dal vento con la massima discrezione.",
    images: {json.dumps(col_tee)}
  }}
];'''

if 'const products =' in content:
    content = re.sub(r'const products\s*=\s*\[[\s\S]*?\];', new_products_block, content)

# B. FEATHERWEIGHT ENGINE V7: Catalog Guard Blindato + Calibratore Speculare Mobile
engine_v7 = f'''<script is:inline>
(function() {{
  if (window.__IMLAND_FEATHERWEIGHT_V7) return;
  window.__IMLAND_FEATHERWEIGHT_V7 = true;

  const isMobile = window.innerWidth <= 768 || /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

  // 1. PIXEL RATIO SHIELD: 1.0x su Mobile (risparmia 75% RAM GPU), 1.25x su Desktop
  const maxDPR = isMobile ? 1.0 : 1.25;
  const nativeDPR = window.devicePixelRatio || 1;
  try {{
    Object.defineProperty(window, 'devicePixelRatio', {{
      get: function() {{ return Math.min(nativeDPR, maxDPR); }}
    }});
  }} catch (e) {{}}

  // 2. CONTESTO WEBGL MOBILE LEGGERO (Zero blocco watchdog Android "UI non risponde")
  if (isMobile) {{
    const origGetContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function(type, attrs) {{
      if (type === 'webgl' || type === 'webgl2' || type === 'experimental-webgl') {{
        attrs = Object.assign({{}}, attrs, {{
          antialias: false,
          powerPreference: 'low-power',
          precision: 'mediump'
        }});
      }}
      return origGetContext.call(this, type, attrs);
    }};

    const origParse = JSON.parse;
    JSON.parse = function(text, reviver) {{
      const res = origParse.call(this, text, reviver);
      if (res && Array.isArray(res.data) && res.data.length > 60) {{
        res.data = res.data.slice(0, 60);
      }} else if (Array.isArray(res) && res.length > 60 && res[0] && (res[0].media_url || res[0].id)) {{
        return res.slice(0, 60);
      }}
      return res;
    }};
  }}

  // 3. DRIP-FEED ASYNC QUEUE (Cede respiro al thread UI Android)
  const MAX_CONCURRENT = isMobile ? 3 : 8;
  let activeLoads = 0;
  const loadQueue = [];
  const rawSrcDescriptor = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, 'src');

  function pumpQueue() {{
    while (activeLoads < MAX_CONCURRENT && loadQueue.length > 0) {{
      const task = loadQueue.shift();
      activeLoads++;
      let released = false;

      const release = () => {{
        if (released) return;
        released = true;
        activeLoads = Math.max(0, activeLoads - 1);
        setTimeout(pumpQueue, isMobile ? 30 : 8);
      }};

      task.img.addEventListener('load', release, {{ once: true }});
      task.img.addEventListener('error', release, {{ once: true }});
      setTimeout(release, 3500);

      rawSrcDescriptor.set.call(task.img, task.url);
    }}
  }}

  if (rawSrcDescriptor && rawSrcDescriptor.set) {{
    Object.defineProperty(HTMLImageElement.prototype, 'src', {{
      get: rawSrcDescriptor.get,
      set: function(url) {{
        this.decoding = 'async';
        if (!url || typeof url !== 'string' || url.startsWith('data:') || url.startsWith('blob:') || url.includes('/brand/')) {{
          rawSrcDescriptor.set.call(this, url);
          return;
        }}
        loadQueue.push({{ img: this, url: url }});
        setTimeout(pumpQueue, 0);
      }},
      configurable: true
    }});
  }}

  // 4. MOTORE CAROSELLI IMWEAR BLINDATO (Con *zip* nella colonna 2 e self-healing su errore)
  const CATALOG_SETS = {{
    classic: {json.dumps(col_classic)},
    zip: {json.dumps(col_zip)},
    essentials: {json.dumps(col_tee)}
  }};
  const slideIndexes = {{ classic: 0, zip: 0, essentials: 0 }};

  function enforceImwearCatalog(advanceSlide) {{
    const modal = document.getElementById('brand-modal') || document.querySelector('[class*="brand-panel"]');
    if (!modal) return;

    // Individua solo le 3 card foglia (che contengono 1 solo titolo H2/H3 ciascuna)
    const headings = modal.querySelectorAll('h2, h3, h4');
    headings.forEach((h) => {{
      const titleTxt = (h.textContent || '').toUpperCase();
      let key = null;
      if (titleTxt.includes('FULL-ZIP')) key = 'zip';
      else if (titleTxt.includes('CLASSIC HOODIE')) key = 'classic';
      else if (titleTxt.includes('ESSENTIALS')) key = 'essentials';
      if (!key) return;

      // Risale al contenitore della singola colonna (che non contiene altri titoli)
      let card = h.parentElement;
      while (card && card !== modal && card.querySelectorAll('h2, h3, h4').length === 1 && card.querySelectorAll('img').length === 0) {{
        card = card.parentElement;
      }}
      if (!card || card === modal) return;

      const list = CATALOG_SETS[key];
      if (!list || list.length === 0) return;

      if (advanceSlide) {{
        slideIndexes[key] = (slideIndexes[key] + 1) % list.length;
      }}
      const targetSrc = list[slideIndexes[key]];

      const imgs = card.querySelectorAll('img');
      imgs.forEach((imgEl, idx) => {{
        const desired = imgs.length === 1 ? targetSrc : list[idx % list.length];
        const currentAttr = imgEl.getAttribute('src') || '';
        if (currentAttr !== desired) {{
          rawSrcDescriptor.set.call(imgEl, desired);
        }}
        // Auto-guarigione: se un'immagine fallisce, passa subito alla successiva
        imgEl.onerror = function() {{
          slideIndexes[key] = (slideIndexes[key] + 1) % list.length;
          rawSrcDescriptor.set.call(this, list[slideIndexes[key]]);
        }};
        if (imgs.length > 1) {{
          imgEl.style.opacity = (idx === slideIndexes[key]) ? '1' : '0';
          imgEl.style.transition = 'opacity 0.85s ease';
        }} else {{
          imgEl.style.opacity = '1';
        }}
      }});
    }});
  }}

  window.addEventListener('DOMContentLoaded', () => enforceImwearCatalog(false));
  setInterval(() => enforceImwearCatalog(true), 3000);
  document.addEventListener('click', () => setTimeout(() => enforceImwearCatalog(false), 50));

  // 5. CALIBRATORE GEOMETRICO SPECULARE MOBILE + GUARDIA SWIPE/TAP
  if (isMobile) {{
    let touchStartX = 0;
    let touchStartY = 0;
    let movedBeyondThreshold = false;

    window.addEventListener('touchstart', (e) => {{
      if (e.touches && e.touches.length > 0) {{
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
        movedBeyondThreshold = false;
      }}
    }}, {{ passive: true, capture: true }});

    window.addEventListener('touchmove', (e) => {{
      if (e.touches && e.touches.length > 0) {{
        const dx = e.touches[0].clientX - touchStartX;
        const dy = e.touches[0].clientY - touchStartY;
        if (Math.hypot(dx, dy) > 12) {{
          movedBeyondThreshold = true;
        }}
      }}
    }}, {{ passive: true, capture: true }});

    window.addEventListener('click', (e) => {{
      if (movedBeyondThreshold && e.target && e.target.tagName === 'CANVAS') {{
        e.stopImmediatePropagation();
        e.preventDefault();
        movedBeyondThreshold = false;
      }}
    }}, {{ capture: true }});

    function alignMobileSymmetricRails() {{
      // Trova il binario sinistro (MANIFESTO / IMWEAR) e il binario destro (ARCHIVE 2026)
      let leftRail = null;
      let rightRail = null;
      const candidates = document.querySelectorAll('nav, aside, header, div');
      for (const el of candidates) {{
        const txt = (el.textContent || '').trim();
        if (!leftRail && txt.includes('MANIFESTO') && txt.includes('IMWEAR') && txt.length < 120) {{
          leftRail = el;
        }}
        if (!rightRail && txt.includes('ARCHIVE 2026') && txt.length < 120) {{
          rightRail = el;
        }}
      }}

      if (leftRail) {{
        // Calcola l'offset esatto dal bordo destro (es. 14px) per replicarlo a sinistra al sub-pixel
        let targetMargin = 14;
        if (rightRail) {{
          const rRect = rightRail.getBoundingClientRect();
          const rightGap = window.innerWidth - rRect.right;
          if (rightGap >= 6 && rightGap <= 40) {{
            targetMargin = Math.round(rightGap);
          }}
        }}

        leftRail.style.setProperty('position', 'fixed', 'important');
        leftRail.style.setProperty('top', '50%', 'important');
        leftRail.style.setProperty('left', targetMargin + 'px', 'important');
        leftRail.style.setProperty('right', 'auto', 'important');
        leftRail.style.setProperty('transform-origin', 'left top', 'important');
        leftRail.style.setProperty('transform', 'rotate(-90deg) translateX(-50%)', 'important');
        leftRail.style.setProperty('background', 'transparent', 'important');
        leftRail.style.setProperty('backdrop-filter', 'none', 'important');
        leftRail.style.setProperty('-webkit-backdrop-filter', 'none', 'important');
        leftRail.style.setProperty('box-shadow', 'none', 'important');
        leftRail.style.setProperty('border', 'none', 'important');
        leftRail.style.setProperty('padding', '0', 'important');
        leftRail.style.setProperty('margin', '0', 'important');
        leftRail.style.setProperty('width', 'max-content', 'important');
        leftRail.style.setProperty('z-index', '40', 'important');
      }}

      // Nasconde la barra sinistra quando un'opera è isolata
      const stage = document.getElementById('editorial-stage');
      const isIsolated = stage && (stage.classList.contains('is-active') || (getComputedStyle(stage).opacity === '1' && getComputedStyle(stage).pointerEvents !== 'none'));
      document.body.classList.toggle('mobile-artwork-isolated', Boolean(isIsolated));
    }}

    window.addEventListener('DOMContentLoaded', alignMobileSymmetricRails);
    window.addEventListener('resize', alignMobileSymmetricRails);
    setInterval(alignMobileSymmetricRails, 250);
  }}

  // 6. GPU HIBERNATION & THERMAL FRAME PACING
  const nativeRAF = window.requestAnimationFrame.bind(window);
  let lastFrameTime = 0;
  const targetInterval = isMobile ? 33 : 16;

  window.requestAnimationFrame = function(callback) {{
    return nativeRAF(function(timestamp) {{
      if (document.hidden) {{
        setTimeout(() => nativeRAF(callback), 500);
        return;
      }}
      const modalOpen = document.querySelector('#brand-modal[style*="block"], #brand-modal[style*="flex"], #contacts-modal[style*="block"], #contacts-modal[style*="flex"], #manifesto-modal[style*="block"], #manifesto-modal[style*="flex"]');
      if (modalOpen) {{
        setTimeout(() => nativeRAF(callback), 400);
        return;
      }}
      if (timestamp - lastFrameTime < targetInterval) {{
        nativeRAF(callback);
        return;
      }}
      lastFrameTime = timestamp;
      callback(timestamp);
    }});
  }};
}})();
</script>
'''

# Rimuove le precedenti versioni del Featherweight Engine
content = re.sub(r'<script is:inline>\s*\(function\(\)\s*\{\s*if\s*\(window\.__IMLAND_FEATHERWEIGHT_[\s\S]*?</script>', '', content)

if '---' in content:
    parts = content.split('---', 2)
    if len(parts) == 3:
        content = '---' + parts[1] + '---\n' + engine_v7 + parts[2]
    else:
        content = engine_v7 + '\n' + content
else:
    content = engine_v7 + '\n' + content

# C. SCUDO CSS GLOBALE: Preserva Desktop + Simmetria Assoluta Mobile
mirror_css = '''
<style is:global>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&display=swap');

  html, body {
    overscroll-behavior: none !important;
    -webkit-tap-highlight-color: transparent !important;
  }

  canvas {
    touch-action: none !important;
    user-select: none !important;
    -webkit-user-select: none !important;
  }

  /* 1. CAROUSEL STACKING */
  .carousel-wrapper {
    position: relative !important;
    width: 100% !important;
    height: 220px !important;
    overflow: hidden !important;
    display: block !important;
  }
  .carousel-wrapper img, .carousel-wrapper video {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
  }

  /* 2. FOGLIO MODALE PURO SENZA FRAME NERO */
  #brand-modal, #contacts-modal, #manifesto-modal {
    box-sizing: border-box !important;
  }

  .brand-panel-content, .contacts-panel-content, .manifesto-panel-content {
    position: relative !important;
    top: auto !important;
    left: auto !important;
    right: auto !important;
    bottom: auto !important;
    transform: none !important;
    margin: auto !important;
    width: min(92vw, 880px) !important;
    max-width: min(92vw, 880px) !important;
    max-height: 85vh !important;
    overflow-y: auto !important;
    -webkit-overflow-scrolling: touch !important;
    background: #ffffff !important;
    border: none !important;
    outline: none !important;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.06) !important;
    padding: 36px !important;
  }

  .brand-panel-content h1, .brand-panel-content h2,
  .contacts-panel-content h1, .contacts-panel-content h2,
  .manifesto-panel-content h1, .manifesto-panel-content h2,
  #contacts-modal h1, #contacts-modal h2 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: -0.02em !important;
    line-height: 1.05 !important;
  }

  .brand-panel-content p, .contacts-panel-content p, .manifesto-panel-content p,
  .brand-panel-content div, .contacts-panel-content div, .manifesto-panel-content div {
    max-width: 680px !important;
    margin-left: 0 !important;
    margin-right: auto !important;
    line-height: 1.6 !important;
  }

  .brand-panel-content header, .contacts-panel-content header, .manifesto-panel-content header {
    max-width: 100% !important;
  }

  /* 3. SIMMETRIA SPECULARE & PULIZIA MOBILE */
  @media (max-width: 768px) {
    body.mobile-artwork-isolated nav,
    body.mobile-artwork-isolated .vertical-nav,
    body.mobile-artwork-isolated #axis-nav,
    body.mobile-artwork-isolated .sidebar-nav {
      opacity: 0 !important;
      pointer-events: none !important;
    }

    button, a {
      white-space: nowrap !important;
      touch-action: manipulation !important;
    }

    #editorial-stage > div, [class*="editorial-card"], [class*="info-card"] {
      position: fixed !important;
      left: 4vw !important;
      right: 4vw !important;
      width: 92vw !important;
      max-width: 92vw !important;
      bottom: max(14px, env(safe-area-inset-bottom)) !important;
      margin: 0 !important;
      max-height: 38vh !important;
      overflow-y: auto !important;
      -webkit-overflow-scrolling: touch !important;
      z-index: 60 !important;
    }

    .brand-panel-content, .contacts-panel-content, .manifesto-panel-content {
      width: 94vw !important;
      max-width: 94vw !important;
      max-height: 82vh !important;
      padding: 22px 18px !important;
    }
  }
</style>
'''

content = re.sub(r'<style is:global>[\s\S]*?</style>', '', content)
content += "\n" + mirror_css

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("FIX COMPLETATO: CATALOGO *ZIP* VERIFICATO E BINARI MOBILI SPECULARI AL MILLIMETRO.")
