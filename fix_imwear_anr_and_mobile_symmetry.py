import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# A. AGGIORNAMENTO SORGENTE ARRAY IMWEAR (Sequenza esatta verificata su GitHub)
arr_classic = "['/brand/hoodie-1.jpg', '/brand/hoodie-2.jpg', '/brand/hoodie-3.jpg', '/brand/hoodie-4.jpg', '/brand/hoodie-5.jpg', '/brand/hoodie-6.jpg', '/brand/hoodie-7.jpg', '/brand/hoodie-8.jpg', '/brand/hoodie-9.jpg']"
arr_zip     = "['/brand/hoodie_zip-1.jpg', '/brand/hoodie_zip-2.jpg', '/brand/hoodie_zip-3.jpg']"
arr_tee     = "['/brand/tee-1.jpg', '/brand/tee-2.jpg', '/brand/tee-3.jpg', '/brand/tee-4.jpg', '/brand/tee-5.jpg']"

# Sostituisce eventuali vecchi riferimenti ai file sbagliati nella seconda e terza colonna
content = content.replace("'/brand/zip-hoodie.jpg'", "'/brand/hoodie_zip-1.jpg'")
content = content.replace("'/brand/gear-beanie.jpg'", "'/brand/tee-1.jpg'")
content = content.replace("'/brand/gear-hoodie.jpg'", "'/brand/tee-2.jpg'")
content = content.replace("'/brand/gear-shell.jpg'", "'/brand/tee-3.jpg'")

# Aggiorna il blocco const products se presente
new_products_block = f'''const products = [
  {{
    title: "IMLAND / CLASSIC HOODIE",
    subtitle: "Signature Collection",
    category: "UNISEX & KIDS // HEAVYWEIGHT",
    desc: "Il capo iconico dell'Atelier IMLAND. Una felpa ad alta grammatura, morbida, densa e calda, pensata per accompagnare il ritmo della montagna e la vita di tutti i giorni. Struttura resistente e massimo comfort.",
    images: {arr_classic}
  }},
  {{
    title: "IMLAND / FULL-ZIP HOODIE",
    subtitle: "Alpine Edition",
    category: "UNISEX // DYNAMIC LAYER",
    desc: "Strato versatile con zip integrale a scorrimento rapido. Morbida, pratica e avvolgente, offre la giusta protezione termica durante le giornate all'aria aperta e nei cambi di temperatura.",
    images: {arr_zip}
  }},
  {{
    title: "IMLAND / ESSENTIALS & GEAR",
    subtitle: "Raw Cotton & Lightwear",
    category: "APPAREL & ACCESSORIES",
    desc: "L'ecosistema essenziale IMLAND. La T-Shirt e la sacca 'Gerla Bag' sono realizzate in purissimo cotone organico al 100%. Il Neck Warmer è un copricollo leggerissimo e traspirante, progettato per riparare dal vento con la massima discrezione.",
    images: {arr_tee}
  }}
];'''

if 'const products =' in content:
    content = re.sub(r'const products\s*=\s*\[[\s\S]*?\];', new_products_block, content)

# B. FEATHERWEIGHT ENGINE V6: Android ANR Shield (60 nodi drip-feed) + Guardia IMWEAR
engine_v6 = '''<script is:inline>
(function() {
  if (window.__IMLAND_FEATHERWEIGHT_V6) return;
  window.__IMLAND_FEATHERWEIGHT_V6 = true;

  const isMobile = window.innerWidth <= 768 || /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

  // 1. PIXEL RATIO SHIELD: 1.0x su Mobile (risparmia 75% RAM GPU), 1.25x su Desktop
  const maxDPR = isMobile ? 1.0 : 1.25;
  const nativeDPR = window.devicePixelRatio || 1;
  try {
    Object.defineProperty(window, 'devicePixelRatio', {
      get: function() { return Math.min(nativeDPR, maxDPR); }
    });
  } catch (e) {}

  // 2. CONTESTO WEBGL MOBILE LEGGERO (Zero blocco watchdog Android "UI non risponde")
  if (isMobile) {
    const origGetContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function(type, attrs) {
      if (type === 'webgl' || type === 'webgl2' || type === 'experimental-webgl') {
        attrs = Object.assign({}, attrs, {
          antialias: false,
          powerPreference: 'low-power',
          precision: 'mediump'
        });
      }
      return origGetContext.call(this, type, attrs);
    };

    // Limita la galassia mobile a 60 nodi per mantenere la RAM sempre leggera
    const origParse = JSON.parse;
    JSON.parse = function(text, reviver) {
      const res = origParse.call(this, text, reviver);
      if (res && Array.isArray(res.data) && res.data.length > 60) {
        res.data = res.data.slice(0, 60);
      } else if (Array.isArray(res) && res.length > 60 && res[0] && (res[0].media_url || res[0].id)) {
        return res.slice(0, 60);
      }
      return res;
    };
  }

  // 3. DRIP-FEED ASYNC QUEUE (Cede respiro al thread UI Android ogni 30ms)
  const MAX_CONCURRENT = isMobile ? 3 : 8;
  let activeLoads = 0;
  const loadQueue = [];
  const rawSrcDescriptor = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, 'src');

  function pumpQueue() {
    while (activeLoads < MAX_CONCURRENT && loadQueue.length > 0) {
      const task = loadQueue.shift();
      activeLoads++;
      let released = false;

      const release = () => {
        if (released) return;
        released = true;
        activeLoads = Math.max(0, activeLoads - 1);
        setTimeout(pumpQueue, isMobile ? 30 : 8);
      };

      task.img.addEventListener('load', release, { once: true });
      task.img.addEventListener('error', release, { once: true });
      setTimeout(release, 3500);

      rawSrcDescriptor.set.call(task.img, task.url);
    }
  }

  if (rawSrcDescriptor && rawSrcDescriptor.set) {
    Object.defineProperty(HTMLImageElement.prototype, 'src', {
      get: rawSrcDescriptor.get,
      set: function(url) {
        this.decoding = 'async';
        if (!url || typeof url !== 'string' || url.startsWith('data:') || url.startsWith('blob:') || url.includes('/brand/')) {
          rawSrcDescriptor.set.call(this, url);
          return;
        }
        loadQueue.push({ img: this, url: url });
        setTimeout(pumpQueue, 0);
      },
      configurable: true
    });
  }

  // 4. GUARDIANO CAROSELLI IMWEAR (Forza le 3 collezioni esatte 9-3-5 contro ogni sovrascrittura)
  const CATALOG_SETS = {
    classic: ['/brand/hoodie-1.jpg', '/brand/hoodie-2.jpg', '/brand/hoodie-3.jpg', '/brand/hoodie-4.jpg', '/brand/hoodie-5.jpg', '/brand/hoodie-6.jpg', '/brand/hoodie-7.jpg', '/brand/hoodie-8.jpg', '/brand/hoodie-9.jpg'],
    zip: ['/brand/hoodie_zip-1.jpg', '/brand/hoodie_zip-2.jpg', '/brand/hoodie_zip-3.jpg'],
    essentials: ['/brand/tee-1.jpg', '/brand/tee-2.jpg', '/brand/tee-3.jpg', '/brand/tee-4.jpg', '/brand/tee-5.jpg']
  };
  const slideIndexes = { classic: 0, zip: 0, essentials: 0 };

  function enforceImwearCatalog(advanceSlide) {
    const modal = document.getElementById('brand-modal') || document.querySelector('[class*="brand-panel"]');
    if (!modal) return;

    // Cerca le 3 card prodotto tramite il loro titolo
    const cards = modal.querySelectorAll('article, .product-card, [class*="card"], [class*="col"]');
    let matchedAny = false;

    cards.forEach((card) => {
      const txt = (card.textContent || '').toUpperCase();
      let key = null;
      if (txt.includes('FULL-ZIP')) key = 'zip';
      else if (txt.includes('CLASSIC HOODIE')) key = 'classic';
      else if (txt.includes('ESSENTIALS')) key = 'essentials';

      if (!key) return;
      const imgs = card.querySelectorAll('img');
      if (imgs.length === 0) return;
      matchedAny = true;

      const list = CATALOG_SETS[key];
      if (advanceSlide) {
        slideIndexes[key] = (slideIndexes[key] + 1) % list.length;
      }
      const targetSrc = list[slideIndexes[key]];

      // Se c'e' una sola <img> dinamica, aggiorna direttamente il suo src
      if (imgs.length === 1) {
        if (!imgs[0].getAttribute('src')?.endsWith(targetSrc)) {
          rawSrcDescriptor.set.call(imgs[0], targetSrc);
        }
      } else {
        // Se ci sono piu' <img> sovrapposte, allinea gli src e gestisce la dissolvenza
        imgs.forEach((imgEl, idx) => {
          const expected = list[idx % list.length];
          if (!imgEl.getAttribute('src')?.endsWith(expected)) {
            rawSrcDescriptor.set.call(imgEl, expected);
          }
          imgEl.style.opacity = (idx === slideIndexes[key]) ? '1' : '0';
          imgEl.style.transition = 'opacity 0.85s ease';
        });
      }
    });

    // Fallback posizionale sui primi 3 .carousel-wrapper se i titoli non sono nello stesso nodo
    if (!matchedAny) {
      const wrappers = modal.querySelectorAll('.carousel-wrapper');
      const keys = ['classic', 'zip', 'essentials'];
      wrappers.forEach((wrap, i) => {
        const key = keys[i];
        if (!key) return;
        const list = CATALOG_SETS[key];
        if (advanceSlide) slideIndexes[key] = (slideIndexes[key] + 1) % list.length;
        const imgs = wrap.querySelectorAll('img');
        imgs.forEach((imgEl, idx) => {
          const expected = list[idx % list.length];
          if (!imgEl.getAttribute('src')?.endsWith(expected)) {
            rawSrcDescriptor.set.call(imgEl, expected);
          }
          imgEl.style.opacity = (idx === slideIndexes[key]) ? '1' : '0';
        });
      });
    }
  }

  window.addEventListener('DOMContentLoaded', () => enforceImwearCatalog(false));
  setInterval(() => enforceImwearCatalog(true), 3200);
  document.addEventListener('click', () => setTimeout(() => enforceImwearCatalog(false), 60));

  // 5. DISCRIMINATORE TATTILE SWIPE VS TAP & STATO ISOLAMENTO MOBILE
  if (isMobile) {
    let touchStartX = 0;
    let touchStartY = 0;
    let movedBeyondThreshold = false;

    window.addEventListener('touchstart', (e) => {
      if (e.touches && e.touches.length > 0) {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
        movedBeyondThreshold = false;
      }
    }, { passive: true, capture: true });

    window.addEventListener('touchmove', (e) => {
      if (e.touches && e.touches.length > 0) {
        const dx = e.touches[0].clientX - touchStartX;
        const dy = e.touches[0].clientY - touchStartY;
        if (Math.hypot(dx, dy) > 12) {
          movedBeyondThreshold = true;
        }
      }
    }, { passive: true, capture: true });

    window.addEventListener('click', (e) => {
      if (movedBeyondThreshold && e.target && e.target.tagName === 'CANVAS') {
        e.stopImmediatePropagation();
        e.preventDefault();
        movedBeyondThreshold = false;
      }
    }, { capture: true });

    // Monitora se una foto e' isolata per nascondere il menu laterale ed evitare sovrapposizioni
    setInterval(() => {
      const stage = document.getElementById('editorial-stage');
      const isIsolated = stage && (stage.classList.contains('is-active') || getComputedStyle(stage).opacity === '1' && getComputedStyle(stage).pointerEvents !== 'none');
      document.body.classList.toggle('mobile-artwork-isolated', Boolean(isIsolated));
    }, 150);
  }

  // 6. GPU HIBERNATION & THERMAL FRAME PACING (30 FPS Mobile / Pausa a modale aperta)
  const nativeRAF = window.requestAnimationFrame.bind(window);
  let lastFrameTime = 0;
  const targetInterval = isMobile ? 33 : 16;

  window.requestAnimationFrame = function(callback) {
    return nativeRAF(function(timestamp) {
      if (document.hidden) {
        setTimeout(() => nativeRAF(callback), 500);
        return;
      }
      const modalOpen = document.querySelector('#brand-modal[style*="block"], #brand-modal[style*="flex"], #contacts-modal[style*="block"], #contacts-modal[style*="flex"], #manifesto-modal[style*="block"], #manifesto-modal[style*="flex"]');
      if (modalOpen) {
        setTimeout(() => nativeRAF(callback), 400);
        return;
      }

      if (timestamp - lastFrameTime < targetInterval) {
        nativeRAF(callback);
        return;
      }
      lastFrameTime = timestamp;
      callback(timestamp);
    });
  };
})();
</script>
'''

# Rimuove le precedenti versioni del Featherweight Engine
content = re.sub(r'<script is:inline>\s*\(function\(\)\s*\{\s*if\s*\(window\.__IMLAND_FEATHERWEIGHT_[\s\S]*?</script>', '', content)

if '---' in content:
    parts = content.split('---', 2)
    if len(parts) == 3:
        content = '---' + parts[1] + '---\n' + engine_v6 + parts[2]
    else:
        content = engine_v6 + '\n' + content
else:
    content = engine_v6 + '\n' + content

# C. SCUDO CSS GLOBALE: Simmetria Speculare Menu Sinistro + Centratura Foto Isolata Mobile
symmetry_and_polish_css = '''
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

  /* 3. SIMMETRIA SPECULARE & FIX POSIZIONAMENTO SMARTPHONE */
  @media (max-width: 768px) {
    /* Riporta il menu verticale sinistro a filo bordo, speculare a "ARCHIVE 2026" a destra */
    nav, .vertical-nav, #axis-nav, .sidebar-nav, [class*="left-nav"] {
      position: fixed !important;
      left: 10px !important;
      right: auto !important;
      top: 50% !important;
      transform: translateY(-50%) rotate(-90deg) !important;
      transform-origin: left center !important;
      margin: 0 !important;
      padding: 0 !important;
      background: transparent !important;
      backdrop-filter: none !important;
      -webkit-backdrop-filter: none !important;
      border: none !important;
      box-shadow: none !important;
      width: auto !important;
      height: auto !important;
      z-index: 40 !important;
      transition: opacity 0.25s ease !important;
    }

    /* Quando una foto e' isolata, dissolve il menu sinistro per non coprire foto e pulsanti */
    body.mobile-artwork-isolated nav,
    body.mobile-artwork-isolated .vertical-nav,
    body.mobile-artwork-isolated #axis-nav,
    body.mobile-artwork-isolated .sidebar-nav {
      opacity: 0 !important;
      pointer-events: none !important;
    }

    /* Ripristina pulsanti inline compatti su una sola riga (niente testi spezzati su 3 righe) */
    button, a {
      white-space: nowrap !important;
      touch-action: manipulation !important;
    }

    /* Centra perfettamente l'opera isolata e la scheda didattica in basso */
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
content += "\n" + symmetry_and_polish_css

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("FIX COMPLETATO: IMWEAR 9-3-5 BLINDATO, ANDROID ANR DISATTIVATO E MENU MOBILE SIMMETRICO.")
