import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# A. FEATHERWEIGHT ENGINE V4: Streaming nativo immagini + Discriminatore Swipe/Tap
engine_v4 = '''<script is:inline>
(function() {
  if (window.__IMLAND_FEATHERWEIGHT_V4) return;
  window.__IMLAND_FEATHERWEIGHT_V4 = true;

  const isMobile = window.innerWidth <= 768 || /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

  // 1. PIXEL RATIO SHIELD: 1.0x su Mobile per zero crash VRAM, 1.25x su Desktop 4K/Retina
  const maxDPR = isMobile ? 1.0 : 1.25;
  const nativeDPR = window.devicePixelRatio || 1;
  try {
    Object.defineProperty(window, 'devicePixelRatio', {
      get: function() { return Math.min(nativeDPR, maxDPR); }
    });
  } catch (e) {}

  // 2. OTTIMIZZAZIONE CONTESTO WEBGL MOBILE (Preserva tutte le texture senza antialiasing pesante)
  if (isMobile) {
    const origGetContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function(type, attrs) {
      if (type === 'webgl' || type === 'webgl2' || type === 'experimental-webgl') {
        attrs = Object.assign({}, attrs, { antialias: false, powerPreference: 'low-power' });
      }
      return origGetContext.call(this, type, attrs);
    };
  }

  // 3. CALIBRAZIONE ORBITA MOBILE A 120 NODI (Fluida, densa, sotto la soglia critica iOS)
  if (isMobile) {
    const origParse = JSON.parse;
    JSON.parse = function(text, reviver) {
      const res = origParse.call(this, text, reviver);
      if (res && Array.isArray(res.data) && res.data.length > 120) {
        res.data = res.data.slice(0, 120);
      } else if (Array.isArray(res) && res.length > 120 && res[0] && (res[0].media_url || res[0].id)) {
        return res.slice(0, 120);
      }
      return res;
    };
  }

  // 4. DIRECT NATIVE ASYNC QUEUE (Zero Canvas 2D offscreen -> Texture sempre visibili su Safari)
  const MAX_CONCURRENT = isMobile ? 4 : 8;
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
        setTimeout(pumpQueue, 12);
      };

      task.img.addEventListener('load', release, { once: true });
      task.img.addEventListener('error', release, { once: true });
      setTimeout(release, 4000);

      rawSrcDescriptor.set.call(task.img, task.url);
    }
  }

  if (rawSrcDescriptor && rawSrcDescriptor.set) {
    Object.defineProperty(HTMLImageElement.prototype, 'src', {
      get: rawSrcDescriptor.get,
      set: function(url) {
        this.decoding = 'async';
        if (!url || typeof url !== 'string' || url.startsWith('data:') || url.startsWith('blob:')) {
          rawSrcDescriptor.set.call(this, url);
          return;
        }
        loadQueue.push({ img: this, url: url });
        setTimeout(pumpQueue, 0);
      },
      configurable: true
    });
  }

  // 5. DISCRIMINATORE TATTILE SWIPE VS TAP (Evita aperture accidentali durante lo scroll su telefono)
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
  }

  // 6. GPU HIBERNATION & THERMAL FRAME PACING
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
      const minDelta = modalOpen ? 250 : targetInterval;

      if (timestamp - lastFrameTime < minDelta) {
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
        content = '---' + parts[1] + '---\n' + engine_v4 + parts[2]
    else:
        content = engine_v4 + '\n' + content
else:
    content = engine_v4 + '\n' + content

# B. SCUDO CSS GLOBALE: Preserva Desktop 1.0 + Ergonomia Touch & Thumb-Zone Mobile
mobile_ergonomic_css = '''
<style is:global>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&display=swap');

  /* 1. BLOCCO RIMBALZO ELASTICO E PULL-TO-REFRESH SU TELA 3D */
  html, body {
    overscroll-behavior: none !important;
    -webkit-tap-highlight-color: transparent !important;
  }

  canvas {
    touch-action: none !important;
    user-select: none !important;
    -webkit-user-select: none !important;
  }

  /* 2. CAROUSEL STACKING: Sovrappone le immagini IMWEAR nello stesso riquadro */
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

  /* 3. FOGLIO MODALE PURO SENZA FRAME NERO (IMWEAR, CONTACTS, MANIFESTO) */
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

  /* 4. TITOLI MONUMENTALI IN SYNE EXTRABOLD SU TUTTE LE SCHEDE */
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

  /* 5. GABBIA EDITORIALE COERENTE PER TESTI E RIGHE */
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

  /* 6. ERGONOMIA THUMB-ZONE & SAFE-AREA PER SMARTPHONE */
  @media (max-width: 768px) {
    .vertical-nav, #axis-nav, .sidebar-nav {
      display: none !important;
    }

    /* Barra superiore con Safe-Area Notch e target tattili ampi */
    nav, header, [class*="top-nav"], [class*="hud-top"] {
      padding-top: max(12px, env(safe-area-inset-top)) !important;
      padding-left: 12px !important;
      padding-right: 12px !important;
    }

    nav button, nav a, header button, header a {
      min-height: 40px !important;
      padding: 8px 10px !important;
      font-size: 11px !important;
      touch-action: manipulation !important;
    }

    /* Pulsanti chiusura e controllo slide dimensionati per il pollice (44px standard) */
    button, [role="button"], [class*="close"], [id*="close"] {
      min-height: 44px !important;
      min-width: 44px !important;
      touch-action: manipulation !important;
    }

    /* Modali più compatte e scorrevoli su schermo verticale */
    .brand-panel-content, .contacts-panel-content, .manifesto-panel-content {
      width: 94vw !important;
      max-width: 94vw !important;
      max-height: 82vh !important;
      padding: 22px 18px !important;
    }

    /* Scheda opera isolata ancorata in basso senza invadere la foto */
    #editorial-stage > div, [class*="editorial-card"], [class*="info-card"] {
      width: 92vw !important;
      max-width: 92vw !important;
      left: 4vw !important;
      right: 4vw !important;
      bottom: max(14px, env(safe-area-inset-bottom)) !important;
      max-height: 40vh !important;
      overflow-y: auto !important;
      -webkit-overflow-scrolling: touch !important;
    }
  }
</style>
'''

content = re.sub(r'<style is:global>[\s\S]*?</style>', '', content)
content += "\n" + mobile_ergonomic_css

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("FASE 6 COMPILATA: STREAMING NATIVO IMMAGINI + FISICA TOUCH MOBILE ATTIVI.")
