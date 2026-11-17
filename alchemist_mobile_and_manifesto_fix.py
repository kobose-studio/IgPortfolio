import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# A. AGGIORNAMENTO MANIFESTO: Rimozione "MONTEROSA" e innesto paragrafo poetico sulla fotografia
content = re.sub(
    r'IMLAND\s+MONTEROSA\s+nasce\s+sotto',
    'IMLAND nasce sotto',
    content,
    flags=re.IGNORECASE
)

photo_paragraph = (
    '<p style="margin-top: 1.15rem;">'
    'Questo senso di appartenenza — visivo, immersivo e profondamente romantico — trova nella '
    '<strong>fotografia</strong> il suo fulcro naturale: uno sguardo lento che custodisce il legame '
    'intimo con la valle, rivelando sfumature silenziose e messaggi nascosti a chi sa fermarsi ad '
    'ascoltare con la giusta attenzione.'
    '</p>'
)

if 'Questo senso di appartenenza' not in content:
    content = re.sub(
        r'(bussola\s+esistenziale\.\s*</p>)',
        r'\1\n          ' + photo_paragraph,
        content,
        count=1
    )

# B. TAGLIO DIRETTO A 48 NODI SU MOBILE PRIMA DEL CICLO THREE.JS (Azzera il freeze CPU/RAM su Android)
content = re.sub(
    r'(const\s+(?:mediaItems|allMedia|items|posts)\s*=\s*)([^;\n]+);',
    r'\1((typeof window !== "undefined" && (window.innerWidth <= 768 || /Android|iPhone|iPad|iPod/i.test(navigator.userAgent))) ? (\2).slice(0, 48) : (\2));',
    content,
    count=1
)

# Riduce eventuali suddivisioni pesanti delle geometrie su mobile a 1x1 (2 triangoli per piano)
content = re.sub(
    r'new THREE\.PlaneGeometry\(\s*([^,]+)\s*,\s*([^,]+)\s*,\s*\d+\s*,\s*\d+\s*\)',
    r'new THREE.PlaneGeometry(\1, \2, window.innerWidth <= 768 ? 1 : 12, window.innerWidth <= 768 ? 1 : 12)',
    content
)

# Rimuove eventuali vecchi blocchi patch per mantenere il file pulito e privo di conflitti
content = re.sub(r'<script id="imland-master-v10"[\s\S]*?</script>', '', content)
content = re.sub(r'<style id="imland-master-v10-css"[\s\S]*?</style>', '', content)

# C. SCRIPT RUNTIME V10: Android Time-Sliced Loader + Centratura Modali + Allineamento Binario Sinistro
master_script = '''<script id="imland-master-v10" is:inline>
(function() {
  if (window.__IMLAND_MASTER_V10) return;
  window.__IMLAND_MASTER_V10 = true;

  const isMobile = window.innerWidth <= 768 || /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

  // 1. SCUDO HARDWARE MOBILE: PixelRatio 1.0x + WebGL Low-Power + Time-Slicing TextureLoader
  if (isMobile) {
    try {
      Object.defineProperty(window, 'devicePixelRatio', { get: function() { return 1.0; } });
    } catch (e) {}

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

    // Diluisce i caricamenti delle texture nel tempo per impedire ad Android Chrome di mostrare "UI non risponde"
    const patchThreeLoader = () => {
      if (window.THREE && window.THREE.TextureLoader && !window.THREE.TextureLoader.__patchedV10) {
        window.THREE.TextureLoader.__patchedV10 = true;
        const origLoad = window.THREE.TextureLoader.prototype.load;
        let slotIndex = 0;

        window.THREE.TextureLoader.prototype.load = function(url, onLoad, onProgress, onError) {
          const tex = new window.THREE.Texture();
          tex.generateMipmaps = false;
          tex.minFilter = window.THREE.LinearFilter;
          tex.magFilter = window.THREE.LinearFilter;

          const delay = Math.floor(slotIndex / 3) * 65;
          slotIndex++;

          setTimeout(() => {
            origLoad.call(this, url, (loadedTex) => {
              tex.image = loadedTex.image;
              tex.needsUpdate = true;
              if (onLoad) onLoad(tex);
            }, onProgress, onError);
          }, delay);

          return tex;
        };
      }
    };
    patchThreeLoader();
    setInterval(patchThreeLoader, 120);
  }

  // 2. PAUSA MOTORE 3D QUANDO UNA MODALE E' APERTA (Libera 100% CPU/GPU)
  const nativeRAF = window.requestAnimationFrame.bind(window);
  let lastTick = 0;
  window.requestAnimationFrame = function(cb) {
    return nativeRAF(function(ts) {
      if (document.hidden) {
        setTimeout(() => nativeRAF(cb), 500);
        return;
      }
      const anyModalOpen = Array.from(document.querySelectorAll('#brand-modal, #contacts-modal, #manifesto-modal')).some(
        m => getComputedStyle(m).display !== 'none' && getComputedStyle(m).opacity !== '0'
      );
      if (anyModalOpen) {
        setTimeout(() => nativeRAF(cb), 350);
        return;
      }
      if (isMobile && ts - lastTick < 33) {
        nativeRAF(cb);
        return;
      }
      lastTick = ts;
      cb(ts);
    });
  };

  // 3. SINCRONIZZAZIONE TESTI MANIFESTO & CENTRATURA MATEMATICA MODALI
  function syncManifestoAndCenterModals() {
    // Assicura la rimozione di MONTEROSA e la presenza del paragrafo fotografico anche su render dinamici
    const manifestoRoot = document.getElementById('manifesto-modal') || document.body;
    const paragraphs = manifestoRoot.querySelectorAll('p');
    paragraphs.forEach((p) => {
      if (p.textContent && p.textContent.includes('IMLAND MONTEROSA nasce sotto')) {
        p.innerHTML = p.innerHTML.replace(/IMLAND\s+MONTEROSA\s+nasce\s+sotto/gi, 'IMLAND nasce sotto');
      }
      if (p.textContent && p.textContent.includes('bussola esistenziale.') && p.parentElement && !p.parentElement.textContent.includes('Questo senso di appartenenza')) {
        const extra = document.createElement('p');
        extra.style.marginTop = '1.15rem';
        extra.innerHTML = 'Questo senso di appartenenza — visivo, immersivo e profondamente romantico — trova nella <strong>fotografia</strong> il suo fulcro naturale: uno sguardo lento che custodisce il legame intimo con la valle, rivelando sfumature silenziose e messaggi nascosti a chi sa fermarsi ad ascoltare con la giusta attenzione.';
        p.parentElement.appendChild(extra);
      }
    });

    // Centra perfettamente ogni scheda modale rispetto all'intera pagina (zero slittamento a destra)
    const overlays = document.querySelectorAll('#brand-modal, #contacts-modal, #manifesto-modal');
    overlays.forEach((ov) => {
      if (getComputedStyle(ov).display === 'none') return;
      ov.style.setProperty('position', 'fixed', 'important');
      ov.style.setProperty('inset', '0', 'important');
      ov.style.setProperty('left', '0', 'important');
      ov.style.setProperty('top', '0', 'important');
      ov.style.setProperty('width', '100vw', 'important');
      ov.style.setProperty('height', '100dvh', 'important');
      ov.style.setProperty('margin', '0', 'important');
      ov.style.setProperty('padding', '16px', 'important');
      ov.style.setProperty('transform', 'none', 'important');
      ov.style.setProperty('display', 'flex', 'important');
      ov.style.setProperty('align-items', 'center', 'important');
      ov.style.setProperty('justify-content', 'center', 'important');
      ov.style.setProperty('box-sizing', 'border-box', 'important');

      const box = ov.firstElementChild;
      if (box) {
        box.style.setProperty('position', 'relative', 'important');
        box.style.setProperty('left', 'auto', 'important');
        box.style.setProperty('right', 'auto', 'important');
        box.style.setProperty('top', 'auto', 'important');
        box.style.setProperty('bottom', 'auto', 'important');
        box.style.setProperty('transform', 'none', 'important');
        box.style.setProperty('margin', '0 auto', 'important');
        box.style.setProperty('width', 'min(92vw, 880px)', 'important');
        box.style.setProperty('max-width', 'min(92vw, 880px)', 'important');
        box.style.setProperty('max-height', '85dvh', 'important');
        box.style.setProperty('overflow-y', 'auto', 'important');
        box.style.setProperty('box-sizing', 'border-box', 'important');
      }
    });

    // 4. ALLINEAMENTO A FILO BORDO SINISTRO DEL MENU MOBILE (Speculare ad ARCHIVE 2026)
    if (isMobile) {
      let leftRail = null;
      let rightRail = null;

      const allBlocks = document.querySelectorAll('nav, aside, header, div');
      for (const el of allBlocks) {
        const txt = (el.textContent || '').trim();
        if (!leftRail && txt.includes('MANIFESTO') && txt.includes('IMWEAR') && txt.length < 140) {
          leftRail = el;
        }
        if (!rightRail && txt.includes('ARCHIVE 2026') && txt.length < 140) {
          rightRail = el;
        }
      }

      if (leftRail) {
        // Risale eventuale wrapper fixed esterno per azzerarne offset e sfondo satinato
        let container = leftRail;
        while (container.parentElement && container.parentElement !== document.body) {
          const pos = getComputedStyle(container.parentElement).position;
          if (pos === 'fixed' || pos === 'absolute') {
            container = container.parentElement;
          } else {
            break;
          }
        }

        let targetLeft = 10;
        if (rightRail) {
          const rRect = rightRail.getBoundingClientRect();
          const rightMargin = window.innerWidth - rRect.right;
          if (rightMargin >= 4 && rightMargin <= 24) {
            targetLeft = Math.round(rightMargin);
          }
        }

        [container, leftRail].forEach((node) => {
          node.style.setProperty('background', 'transparent', 'important');
          node.style.setProperty('background-color', 'transparent', 'important');
          node.style.setProperty('backdrop-filter', 'none', 'important');
          node.style.setProperty('-webkit-backdrop-filter', 'none', 'important');
          node.style.setProperty('box-shadow', 'none', 'important');
          node.style.setProperty('border', 'none', 'important');
          node.style.setProperty('padding', '0', 'important');
        });

        container.style.setProperty('position', 'fixed', 'important');
        container.style.setProperty('top', '50%', 'important');
        container.style.setProperty('left', targetLeft + 'px', 'important');
        container.style.setProperty('right', 'auto', 'important');
        container.style.setProperty('margin', '0', 'important');
        container.style.setProperty('width', 'auto', 'important');
        container.style.setProperty('height', 'auto', 'important');
        container.style.setProperty('writing-mode', 'vertical-rl', 'important');
        container.style.setProperty('transform', 'translateY(-50%) rotate(180deg)', 'important');
        container.style.setProperty('z-index', '45', 'important');
      }
    }
  }

  window.addEventListener('DOMContentLoaded', syncManifestoAndCenterModals);
  window.addEventListener('resize', syncManifestoAndCenterModals);
  setInterval(syncManifestoAndCenterModals, 200);
})();
</script>
'''

# D. SCUDO CSS GLOBALE PER CENTRATURA ASSOLUTA E PULIZIA MOBILE
master_css = '''<style id="imland-master-v10-css" is:global>
  #brand-modal, #contacts-modal, #manifesto-modal {
    position: fixed !important;
    inset: 0 !important;
    width: 100vw !important;
    height: 100dvh !important;
    margin: 0 !important;
    padding: 16px !important;
    transform: none !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
  }

  .brand-panel-content, .contacts-panel-content, .manifesto-panel-content {
    position: relative !important;
    left: auto !important;
    right: auto !important;
    top: auto !important;
    bottom: auto !important;
    transform: none !important;
    margin: 0 auto !important;
    width: min(92vw, 880px) !important;
    max-width: min(92vw, 880px) !important;
    max-height: 85dvh !important;
    overflow-y: auto !important;
    box-sizing: border-box !important;
  }
</style>
'''

content += "\n" + master_script + "\n" + master_css

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("INTERVENTO V10 COMPLETATO: MANIFESTO POETICO, MODALI CENTRATE E ANDROID ZERO-ANR ATTIVI.")
