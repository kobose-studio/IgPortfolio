import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# A. FEATHERWEIGHT ENGINE V2 (Include Mobile VRAM Diet & 90-Node Cap)
engine_v2 = '''<script is:inline>
(function() {
  if (window.__IMLAND_FEATHERWEIGHT_V2) return;
  window.__IMLAND_FEATHERWEIGHT_V2 = true;

  const isMobile = window.innerWidth <= 768 || /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

  // 1. PIXEL RATIO SHIELD
  const maxDPR = isMobile ? 1.0 : 1.25;
  const nativeDPR = window.devicePixelRatio || 1;
  try {
    Object.defineProperty(window, 'devicePixelRatio', {
      get: function() { return Math.min(nativeDPR, maxDPR); }
    });
  } catch (e) {}

  // 2. DISABILITA ANTIALIASING PESANTE SU MOBILE
  if (isMobile) {
    const origGetContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function(type, attrs) {
      if (type === 'webgl' || type === 'webgl2' || type === 'experimental-webgl') {
        attrs = Object.assign({}, attrs, { antialias: false, powerPreference: 'low-power' });
      }
      return origGetContext.call(this, type, attrs);
    };
  }

  // 3. RIDUCE A 90 NODI SU MOBILE (Salva 80% di VRAM mantendo il vortice pieno)
  if (isMobile) {
    const origParse = JSON.parse;
    JSON.parse = function(text, reviver) {
      const res = origParse.call(this, text, reviver);
      if (res && Array.isArray(res.data) && res.data.length > 90) {
        res.data = res.data.slice(0, 90);
      } else if (Array.isArray(res) && res.length > 100 && res[0] && (res[0].media_url || res[0].id)) {
        return res.slice(0, 90);
      }
      return res;
    };
  }

  // 4. ASYNC QUEUE + MOBILE TEXTURE DOWNSAMPLER (Max 512px su smartphone)
  const MAX_CONCURRENT = isMobile ? 4 : 8;
  let activeLoads = 0;
  const loadQueue = [];
  const rawSrcDescriptor = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, 'src');

  function downscaleForMobile(img, url, release) {
    const proxy = new Image();
    proxy.crossOrigin = 'anonymous';
    proxy.onload = () => {
      try {
        const MAX_DIM = 512;
        let w = proxy.naturalWidth || 512;
        let h = proxy.naturalHeight || 512;
        if (w > MAX_DIM || h > MAX_DIM) {
          const ratio = Math.min(MAX_DIM / w, MAX_DIM / h);
          w = Math.round(w * ratio);
          h = Math.round(h * ratio);
        }
        const canvas = document.createElement('canvas');
        canvas.width = w;
        canvas.height = h;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(proxy, 0, 0, w, h);
        const smallDataUrl = canvas.toDataURL('image/jpeg', 0.78);
        rawSrcDescriptor.set.call(img, smallDataUrl);
      } catch (err) {
        rawSrcDescriptor.set.call(img, url);
      }
      release();
    };
    proxy.onerror = () => {
      rawSrcDescriptor.set.call(img, url);
      release();
    };
    proxy.src = url;
  }

  function pumpQueue() {
    while (activeLoads < MAX_CONCURRENT && loadQueue.length > 0) {
      const task = loadQueue.shift();
      activeLoads++;
      let released = false;

      const release = () => {
        if (released) return;
        released = true;
        activeLoads = Math.max(0, activeLoads - 1);
        setTimeout(pumpQueue, 10);
      };

      setTimeout(release, 5000);

      if (isMobile && !task.url.includes('/brand/')) {
        downscaleForMobile(task.img, task.url, release);
      } else {
        task.img.addEventListener('load', release, { once: true });
        task.img.addEventListener('error', release, { once: true });
        rawSrcDescriptor.set.call(task.img, task.url);
      }
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

  // 5. GPU HIBERNATION & THERMAL FRAME PACING
  const nativeRAF = window.requestAnimationFrame.bind(window);
  let lastFrameTime = 0;
  const targetInterval = isMobile ? 33 : 16;

  window.requestAnimationFrame = function(callback) {
    return nativeRAF(function(timestamp) {
      if (document.hidden) {
        setTimeout(() => nativeRAF(callback), 500);
        return;
      }
      const modalOpen = document.querySelector('#brand-modal[style*="block"], #brand-modal[style*="flex"], #contacts-modal[style*="block"], #contacts-modal[style*="flex"]');
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

# Rimuove v1 e v2 precedenti
content = re.sub(r'<script is:inline>\s*\(function\(\)\s*\{\s*if\s*\(window\.__IMLAND_FEATHERWEIGHT_[\s\S]*?</script>', '', content)

if '---' in content:
    parts = content.split('---', 2)
    if len(parts) == 3:
        content = '---' + parts[1] + '---\n' + engine_v2 + parts[2]
    else:
        content = engine_v2 + '\n' + content
else:
    content = engine_v2 + '\n' + content

# B. FIX DEFINITIVO MODALI (Riunisce Contatti, IMWEAR e Manifesto in una singola cornice)
clean_modal_css = '''
<style is:global>
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

  /* 2. RIUNIFICAZIONE SCHEDA CONTATTI / IMWEAR / MANIFESTO (Zero spaccature) */
  #brand-modal, #contacts-modal, #manifesto-modal {
    box-sizing: border-box !important;
    padding: 16px !important;
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
    box-sizing: border-box !important;
    background: #ffffff !important;
    border: 1px solid #111111 !important;
  }

  /* 3. PULIZIA MOBILE MENU LATERALE */
  @media (max-width: 768px) {
    .vertical-nav, #axis-nav, .sidebar-nav {
      display: none !important;
    }
    .brand-panel-content, .contacts-panel-content, .manifesto-panel-content {
      padding: 18px !important;
    }
  }
</style>
'''

content = re.sub(r'<style is:global>[\s\S]*?</style>', '', content)
content += "\n" + clean_modal_css

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("CONTATTI RIUNIFICATI E MOBILE VRAM DIET V2 ATTIVATI.")
