import os
import re
import json

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# A. SCANSIONE REALE DELLA CARTELLA public/brand/ (Zero file fantasma)
brand_dir = 'public/brand'
all_brand_files = sorted([
    fn for fn in os.listdir(brand_dir)
    if os.path.isfile(os.path.join(brand_dir, fn))
    and fn.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
])

# Colonna 1: Tutte le felpe classiche reali (esclude zip, gear, logo)
col_classic = [
    f'/brand/{fn}' for fn in all_brand_files
    if 'hoodie' in fn.lower() and 'zip' not in fn.lower() and 'gear' not in fn.lower()
]

# Colonna 2: TUTTI i file con "zip" nel nome (hoodie_zip-1..3 + zip-hoodie.jpg)
col_zip = [
    f'/brand/{fn}' for fn in all_brand_files
    if 'zip' in fn.lower()
]

# Colonna 3: Tutte le t-shirt / essentials (tee-1..5)
col_essentials = [
    f'/brand/{fn}' for fn in all_brand_files
    if fn.lower().startswith('tee-')
]

print("Colonna 1 (Classic):", col_classic)
print("Colonna 2 (Full-Zip):", col_zip)
print("Colonna 3 (Essentials):", col_essentials)

# B. SOSTITUZIONE DI OGNI ARRAY /brand/... NEL CODICE SORGENTE ASTRO
brand_array_pattern = re.compile(r'\[[^\]]*[\'"]/brand/[^\]]*\]')
found_arrays = list(brand_array_pattern.finditer(content))

if len(found_arrays) >= 3:
    replacements = [
        json.dumps(col_classic),
        json.dumps(col_zip),
        json.dumps(col_essentials)
    ]
    # Sostituisce a ritroso i primi 3 array del catalogo IMWEAR preservando gli indici
    for idx in range(2, -1, -1):
        m = found_arrays[idx]
        content = content[:m.start()] + replacements[idx] + content[m.end():]
    print(f"Sostituiti {min(3, len(found_arrays))} array catalogo direttamente nel sorgente Astro!")

# Bonifica globale di eventuali singoli riferimenti a file rimossi
content = content.replace("'/brand/hoodie-0.jpg'", f"'{col_classic[0]}'")
content = content.replace('"/brand/hoodie-0.jpg"', f'"{col_classic[0]}"')
content = content.replace("'/brand/hoodie-10.jpg'", f"'{col_classic[-1]}'")
content = content.replace('"/brand/hoodie-10.jpg"', f'"{col_classic[-1]}"')

# C. FEATHERWEIGHT ENGINE V6.1 + GUARDIANO IMWEAR + ALLINEAMENTO SPECULARE MENU MOBILE
engine_v6_1 = f'''<script is:inline>
(function() {{
  if (window.__IMLAND_FEATHERWEIGHT_V61) return;
  window.__IMLAND_FEATHERWEIGHT_V61 = true;

  const isMobile = window.innerWidth <= 768 || /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

  // 1. PIXEL RATIO SHIELD
  const maxDPR = isMobile ? 1.0 : 1.25;
  const nativeDPR = window.devicePixelRatio || 1;
  try {{
    Object.defineProperty(window, 'devicePixelRatio', {{
      get: function() {{ return Math.min(nativeDPR, maxDPR); }}
    }});
  }} catch (e) {{}}

  // 2. OTTIMIZZAZIONE WEBGL MOBILE & CAP A 60 NODI (Previene "UI non risponde" su Android)
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

  // 3. DRIP-FEED ASYNC QUEUE
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

  // 4. GUARDIANO CAROSELLI IMWEAR (Colonna 1: Classic | Colonna 2: Tutti i ZIP | Colonna 3: Essentials)
  const CATALOG_SETS = {{
    classic: {json.dumps(col_classic)},
    zip: {json.dumps(col_zip)},
    essentials: {json.dumps(col_essentials)}
  }};
  const slideIndexes = {{ classic: 0, zip: 0, essentials: 0 }};

  function enforceImwearCatalog(advanceSlide) {{
    const modal = document.getElementById('brand-modal') || document.querySelector('[class*="brand-panel"]');
    if (!modal) return;

    const wrappers = modal.querySelectorAll('.carousel-wrapper');
    const keys = ['classic', 'zip', 'essentials'];

    wrappers.forEach((wrap, i) => {{
      const key = keys[i];
      if (!key || !CATALOG_SETS[key] || CATALOG_SETS[key].length === 0) return;
      const list = CATALOG_SETS[key];

      if (advanceSlide) {{
        slideIndexes[key] = (slideIndexes[key] + 1) % list.length;
      }}

      let imgs = wrap.querySelectorAll('img');
      if (imgs.length !== list.length) {{
        wrap.innerHTML = list.map((src, idx) =>
          `<img src="${{src}}" alt="" onerror="this.src='${{list[0]}}'" style="position:absolute;top:0;left:0;width:100%;height:100%;object-fit:cover;opacity:${{idx === slideIndexes[key] ? 1 : 0}};transition:opacity 0.85s ease;" />`
        ).join('');
      }} else {{
        imgs.forEach((imgEl, idx) => {{
          const expected = list[idx];
          if (!imgEl.getAttribute('src')?.endsWith(expected)) {{
            rawSrcDescriptor.set.call(imgEl, expected);
          }}
          imgEl.onerror = () => {{ rawSrcDescriptor.set.call(imgEl, list[0]); }};
          imgEl.style.opacity = (idx === slideIndexes[key]) ? '1' : '0';
          imgEl.style.transition = 'opacity 0.85s ease';
        }});
      }}
    }});
  }}

  window.addEventListener('DOMContentLoaded', () => enforceImwearCatalog(false));
  setInterval(() => enforceImwearCatalog(true), 3200);
  document.addEventListener('click', () => setTimeout(() => enforceImwearCatalog(false), 50));

  // 5. SPECULARITA' MILLIMETRICA MENU SINISTRO MOBILE & SWIPE GUARD
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

    // Calibra al pixel l'offset sinistro del menu per renderlo identico al margine destro di ARCHIVE 2026
    function alignMobileRailsSymmetry() {{
      const candidates = Array.from(document.querySelectorAll('nav, div, aside, ul'));
      const leftRail = candidates.find(el =>
        el.children.length > 0 &&
        /MANIFESTO/i.test(el.textContent || '') &&
        /IMWEAR/i.test(el.textContent || '') &&
        !/ARCHIVE 2026/i.test(el.textContent || '')
      );
      const rightRail = candidates.find(el =>
        /ARCHIVE 2026/i.test(el.textContent || '') &&
        !/MANIFESTO/i.test(el.textContent || '')
      );

      if (!leftRail) return;
      leftRail.setAttribute('data-imland-left-rail', 'true');

      // Target di margine dal bordo sinistro identico al binario destro (circa 12-16px)
      let targetEdgeGap = 14;
      if (rightRail) {{
        const rRect = rightRail.getBoundingClientRect();
        const rightGap = Math.max(8, Math.min(28, window.innerWidth - rRect.right));
        targetEdgeGap = rightGap;
      }}

      const lRect = leftRail.getBoundingClientRect();
      const deltaX = targetEdgeGap - lRect.left;
      if (Math.abs(deltaX) > 1.5) {{
        const currentShift = parseFloat(leftRail.getAttribute('data-shift-x') || '0');
        const nextShift = currentShift + deltaX;
        leftRail.setAttribute('data-shift-x', String(nextShift));
        leftRail.style.setProperty('margin-left', `${{nextShift}}px`, 'important');
      }}

      // Nasconde il menu sinistro quando un'opera e' isolata al centro
      const stage = document.getElementById('editorial-stage');
      const isIsolated = stage && (stage.classList.contains('is-active') || (getComputedStyle(stage).opacity === '1' && getComputedStyle(stage).pointerEvents !== 'none'));
      document.body.classList.toggle('mobile-artwork-isolated', Boolean(isIsolated));
    }}

    window.addEventListener('DOMContentLoaded', alignMobileRailsSymmetry);
    window.addEventListener('resize', alignMobileRailsSymmetry);
    setInterval(alignMobileRailsSymmetry, 250);
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
        content = '---' + parts[1] + '---\n' + engine_v6_1 + parts[2]
    else:
        content = engine_v6_1 + '\n' + content
else:
    content = engine_v6_1 + '\n' + content

# D. SCUDO CSS GLOBALE: Preserva Desktop + Specularità Rail Mobile Senza Sfondo Opaco
final_css = '''
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

  /* 2. FOGLIO MODALE PURO SENZA FRAME NERO (IMWEAR, CONTACTS, MANIFESTO) */
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

  /* 3. SPECULARITA' BINARIO SINISTRO MOBILE */
  @media (max-width: 768px) {
    [data-imland-left-rail="true"],
    [data-imland-left-rail="true"] * {
      background: transparent !important;
      background-color: transparent !important;
      backdrop-filter: none !important;
      -webkit-backdrop-filter: none !important;
      border: none !important;
      box-shadow: none !important;
    }

    body.mobile-artwork-isolated [data-imland-left-rail="true"] {
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
content += "\n" + final_css

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("COMPILAZIONE RIUSCITA: ZIP CATALOGO AGGIORNATO E MENU MOBILE SPECULARE.")
