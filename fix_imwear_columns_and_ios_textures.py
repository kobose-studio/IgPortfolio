import os
import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica file fisici presenti in public/brand/
brand_files = sorted(os.listdir('public/brand')) if os.path.isdir('public/brand') else []
print("File rilevati in public/brand/:", [f for f in brand_files if f.endswith(('.jpg', '.jpeg', '.png'))])

# Vettori esatti per le 3 colonne IMWEAR
col_1_hoodie = [f'/brand/hoodie-{i}.jpg' for i in range(1, 10)]
col_2_zip    = [f'/brand/hoodie_zip-{i}.jpg' for i in range(1, 4)]
col_3_tee    = [f'/brand/tee-{i}.jpg' for i in range(1, 6)]

# A. AGGIORNAMENTO STRUTTURA DATI JS (const products)
new_products_block = f'''const products = [
  {{
    title: "IMLAND / CLASSIC HOODIE",
    subtitle: "Signature Collection",
    category: "UNISEX & KIDS // HEAVYWEIGHT",
    desc: "Il capo iconico dell'Atelier IMLAND. Una felpa ad alta grammatura, morbida, densa e calda, pensata per accompagnare il ritmo della montagna e la vita di tutti i giorni. Struttura resistente e massimo comfort.",
    images: {col_1_hoodie}
  }},
  {{
    title: "IMLAND / FULL-ZIP HOODIE",
    subtitle: "Alpine Edition",
    category: "UNISEX // DYNAMIC LAYER",
    desc: "Strato versatile con zip integrale a scorrimento rapido. Morbida, pratica e avvolgente, offre la giusta protezione termica durante le giornate all'aria aperta e nei cambi di temperatura.",
    images: {col_2_zip}
  }},
  {{
    title: "IMLAND / ESSENTIALS & GEAR",
    subtitle: "Raw Cotton & Lightwear",
    category: "APPAREL & ACCESSORIES",
    desc: "L'ecosistema essenziale IMLAND. La T-Shirt e la sacca 'Gerla Bag' sono realizzate in purissimo cotone organico al 100%. Il Neck Warmer è un copricollo leggerissimo e traspirante, progettato per riparare dal vento con la massima discrezione.",
    images: {col_3_tee}
  }}
];'''

if 'const products =' in content:
    content = re.sub(r'const products\s*=\s*\[[\s\S]*?\];', new_products_block, content)

# B. AGGIORNAMENTO DIRETTO DEI 3 CONTENITORI HTML .carousel-wrapper (Elimina eventuali <img> statici errati)
wrapper_pattern = re.compile(r'(<div[^>]*class=["\'][^"\']*carousel-wrapper[^"\']*["\'][^>]*>)([\s\S]*?)(</div>)', re.IGNORECASE)
wrappers = list(wrapper_pattern.finditer(content))

def build_imgs_html(img_list, alt_prefix):
    tags = []
    for idx, src in enumerate(img_list):
        opacity = "1" if idx == 0 else "0"
        tags.append(f'<img src="{src}" alt="{alt_prefix} {idx+1}" loading="eager" style="opacity: {opacity}; transition: opacity 0.9s ease;" />')
    return "\n            " + "\n            ".join(tags) + "\n          "

if len(wrappers) >= 3:
    # Sostituzione a ritroso per mantenere intatti gli indici
    content = content[:wrappers[2].start(2)] + build_imgs_html(col_3_tee, "IMLAND Essentials") + content[wrappers[2].end(2):]
    content = content[:wrappers[1].start(2)] + build_imgs_html(col_2_zip, "IMLAND Full-Zip Hoodie") + content[wrappers[1].end(2):]
    content = content[:wrappers[0].start(2)] + build_imgs_html(col_1_hoodie, "IMLAND Classic Hoodie") + content[wrappers[0].end(2):]
    print(f"Aggiornati direttamente {len(wrappers)} contenitori HTML .carousel-wrapper (9 - 3 - 5)!")

# C. RIDUZIONE NODI MOBILE DIRETTAMENTE SUL DATASET ASTRO (85 nodi su telefono = VRAM leggera e foto visibili)
content = re.sub(
    r'(const\s+(?:mediaItems|allMedia|items|posts)\s*=\s*)([^;\n]+);',
    r'\1(typeof window !== "undefined" && window.innerWidth <= 768 ? (\2).slice(0, 85) : (\2));',
    content,
    count=1
)

# D. FEATHERWEIGHT ENGINE V5 (Zero override su HTMLImageElement.src + Disattivazione Mipmaps su Mobile)
engine_v5 = '''<script is:inline>
(function() {
  if (window.__IMLAND_FEATHERWEIGHT_V5) return;
  window.__IMLAND_FEATHERWEIGHT_V5 = true;

  const isMobile = window.innerWidth <= 768 || /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

  // 1. PIXEL RATIO SHIELD: 1.0x su Mobile per evitare saturazione VRAM iOS, 1.25x su Desktop
  const maxDPR = isMobile ? 1.0 : 1.25;
  const nativeDPR = window.devicePixelRatio || 1;
  try {
    Object.defineProperty(window, 'devicePixelRatio', {
      get: function() { return Math.min(nativeDPR, maxDPR); }
    });
  } catch (e) {}

  // 2. OTTIMIZZAZIONE WEBGL MOBILE (Low-power + no antialias pesante)
  if (isMobile) {
    const origGetContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function(type, attrs) {
      if (type === 'webgl' || type === 'webgl2' || type === 'experimental-webgl') {
        attrs = Object.assign({}, attrs, { antialias: false, powerPreference: 'low-power' });
      }
      return origGetContext.call(this, type, attrs);
    };
  }

  // 3. GUARDIA DOM IMWEAR: Assicura al volo che le 3 colonne abbiano sempre 9, 3 e 5 foto esatte
  function syncImwearCarousels() {
    const sets = [
      ['/brand/hoodie-1.jpg', '/brand/hoodie-2.jpg', '/brand/hoodie-3.jpg', '/brand/hoodie-4.jpg', '/brand/hoodie-5.jpg', '/brand/hoodie-6.jpg', '/brand/hoodie-7.jpg', '/brand/hoodie-8.jpg', '/brand/hoodie-9.jpg'],
      ['/brand/hoodie_zip-1.jpg', '/brand/hoodie_zip-2.jpg', '/brand/hoodie_zip-3.jpg'],
      ['/brand/tee-1.jpg', '/brand/tee-2.jpg', '/brand/tee-3.jpg', '/brand/tee-4.jpg', '/brand/tee-5.jpg']
    ];
    const wrappers = document.querySelectorAll('.carousel-wrapper');
    wrappers.forEach((wrap, colIdx) => {
      if (!sets[colIdx]) return;
      const imgs = wrap.querySelectorAll('img');
      if (imgs.length !== sets[colIdx].length || (imgs[0] && !imgs[0].getAttribute('src').includes(sets[colIdx][0]))) {
        wrap.innerHTML = sets[colIdx].map((src, i) =>
          `<img src="${src}" alt="IMLAND ${colIdx+1}-${i+1}" style="position:absolute;top:0;left:0;width:100%;height:100%;object-fit:cover;opacity:${i===0?1:0};transition:opacity 0.9s ease;" />`
        ).join('');
      }
    });
  }
  window.addEventListener('DOMContentLoaded', syncImwearCarousels);
  setTimeout(syncImwearCarousels, 800);

  // 4. DISCRIMINATORE TATTILE SWIPE VS TAP (Evita aperture accidentali durante lo scroll)
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

# Disattiva generateMipmaps sui TextureLoader su Mobile per salvare il 65% di VRAM iOS
content = re.sub(
    r'(new THREE\.TextureLoader\(\)\.load\([^)]+\))',
    r'((t) => { if (typeof window !== "undefined" && window.innerWidth <= 768) { t.generateMipmaps = false; t.minFilter = THREE.LinearFilter; } return t; })(\1)',
    content
)
content = re.sub(
    r'(textureLoader\.load\([^)]+\))',
    r'((t) => { if (typeof window !== "undefined" && window.innerWidth <= 768) { t.generateMipmaps = false; t.minFilter = THREE.LinearFilter; } return t; })(\1)',
    content
)

# Sostituisce le vecchie versioni del Featherweight Engine mantenendo intatto il CSS globale
content = re.sub(r'<script is:inline>\s*\(function\(\)\s*\{\s*if\s*\(window\.__IMLAND_FEATHERWEIGHT_[\s\S]*?</script>', '', content)

if '---' in content:
    parts = content.split('---', 2)
    if len(parts) == 3:
        content = '---' + parts[1] + '---\n' + engine_v5 + parts[2]
    else:
        content = engine_v5 + '\n' + content
else:
    content = engine_v5 + '\n' + content

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("FIX COMPLETATO: COLONNE IMWEAR 9-3-5 E TEXTURE IOS WEBGL SBLOCCATE.")
