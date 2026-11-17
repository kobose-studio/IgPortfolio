import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# A. PULIZIA SORGENTE: Forza l'array della seconda colonna esclusivamente sui 3 file zip richiesti
exact_zip_array = "['/brand/hoodie_zip-1.jpg', '/brand/hoodie_zip-2.jpg', '/brand/hoodie_zip-3.jpg']"
content = re.sub(
    r"\[[^\]]*hoodie_zip[^\]]*\]",
    exact_zip_array,
    content
)

# Rimuove eventuali vecchi patch script di questo fix per evitare duplicazioni
content = re.sub(r'<script id="imland-center-zip-fix"[\s\S]*?</script>', '', content)
content = re.sub(r'<style id="imland-center-zip-css"[\s\S]*?</style>', '', content)

# B. SCRIPT RUNTIME: Blocco assoluto su hoodie_zip-1/2/3.jpg + Centratura geometrica modali
fix_script = '''<script id="imland-center-zip-fix" is:inline>
(function() {
  if (window.__IMLAND_CENTER_ZIP_ACTIVE) return;
  window.__IMLAND_CENTER_ZIP_ACTIVE = true;

  const ZIP_SLIDES = [
    '/brand/hoodie_zip-1.jpg',
    '/brand/hoodie_zip-2.jpg',
    '/brand/hoodie_zip-3.jpg'
  ];
  let zipIndex = 0;

  // 1. CENTRATURA MATEMATICA DEL BOX MODALE (Desktop & Smartphone)
  function centerActiveModals() {
    const markers = [
      'IMWEAR: EQUIPAGGIAMENTO MINERALE',
      "CONNETTITI CON L'ARCHIVIO",
      'DOVE L’UNICA RISPOSTA',
      "DOVE L'UNICA RISPOSTA"
    ];

    const allNodes = document.querySelectorAll('div, section, article');
    for (const el of allNodes) {
      const txt = el.textContent || '';
      if (!markers.some(m => txt.includes(m))) continue;

      // Risale fino al foglio bianco principale (quello dentro l'overlay full-screen)
      let card = el;
      while (card.parentElement && card.parentElement !== document.body) {
        const parentRect = card.parentElement.getBoundingClientRect();
        // Se il padre copre l'intera viewport, 'card' è il box della modale
        if (parentRect.width >= window.innerWidth * 0.96 && parentRect.height >= window.innerHeight * 0.90) {
          break;
        }
        card = card.parentElement;
      }

      if (card && card !== document.body) {
        card.style.setProperty('position', 'fixed', 'important');
        card.style.setProperty('top', '50%', 'important');
        card.style.setProperty('left', '50%', 'important');
        card.style.setProperty('right', 'auto', 'important');
        card.style.setProperty('bottom', 'auto', 'important');
        card.style.setProperty('transform', 'translate(-50%, -50%)', 'important');
        card.style.setProperty('margin', '0', 'important');
        card.style.setProperty('width', 'min(92vw, 880px)', 'important');
        card.style.setProperty('max-width', 'min(92vw, 880px)', 'important');
        card.style.setProperty('max-height', '85dvh', 'important');
        card.style.setProperty('overflow-y', 'auto', 'important');
        card.style.setProperty('overflow-x', 'hidden', 'important');
        card.style.setProperty('box-sizing', 'border-box', 'important');
      }
    }
  }

  // 2. LOCK ESCLUSIVO SULLA COLONNA CENTRALE (FULL-ZIP HOODIE -> hoodie_zip-1, 2, 3)
  function lockFullZipColumn(advance) {
    const modal = document.getElementById('brand-modal') || document.body;
    // Individua il contenitore della seconda colonna tramite il testo FULL-ZIP (qualsiasi tag HTML)
    let zipCard = null;
    const candidates = modal.querySelectorAll('div, article, section');
    for (const el of candidates) {
      const t = (el.textContent || '').toUpperCase();
      if (t.includes('FULL-ZIP') && !t.includes('CLASSIC HOODIE') && !t.includes('ESSENTIALS') && el.querySelectorAll('img').length > 0) {
        zipCard = el;
        break;
      }
    }

    // Fallback posizionale: il secondo contenitore immagine dentro la modale IMWEAR
    if (!zipCard) {
      const wrappers = modal.querySelectorAll('.carousel-wrapper');
      if (wrappers.length >= 2) zipCard = wrappers[1];
    }

    if (!zipCard) return;

    if (advance) {
      zipIndex = (zipIndex + 1) % ZIP_SLIDES.length;
    }

    const currentZipSrc = ZIP_SLIDES[zipIndex];
    const imgs = zipCard.querySelectorAll('img');

    imgs.forEach((img, idx) => {
      const targetSrc = imgs.length === 1 ? currentZipSrc : ZIP_SLIDES[idx % ZIP_SLIDES.length];
      if (!img.getAttribute('src') || !img.getAttribute('src').endsWith(targetSrc)) {
        img.setAttribute('src', targetSrc);
      }
      if (imgs.length > 1) {
        img.style.setProperty('opacity', idx === zipIndex ? '1' : '0', 'important');
        img.style.setProperty('transition', 'opacity 0.75s ease', 'important');
      } else {
        img.style.setProperty('opacity', '1', 'important');
      }
    });
  }

  // Avvio immediato, ciclo fluido ogni 2.8s per le 3 zip e ascolto mutazioni DOM
  window.addEventListener('DOMContentLoaded', () => {
    centerActiveModals();
    lockFullZipColumn(false);
  });

  setInterval(() => {
    centerActiveModals();
    lockFullZipColumn(true);
  }, 2800);

  const observer = new MutationObserver(() => {
    centerActiveModals();
    lockFullZipColumn(false);
  });
  observer.observe(document.documentElement, { childList: true, subtree: true, attributes: true, attributeFilter: ['style', 'class', 'src'] });
})();
</script>
'''

# C. SCUDO CSS RESPONSIVE: Centratura perfetta e impilamento pulito delle 3 colonne su Smartphone
fix_css = '''<style id="imland-center-zip-css" is:global>
  .brand-panel-content, .contacts-panel-content, .manifesto-panel-content {
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    right: auto !important;
    bottom: auto !important;
    transform: translate(-50%, -50%) !important;
    margin: 0 !important;
    width: min(92vw, 880px) !important;
    max-width: min(92vw, 880px) !important;
    max-height: 85dvh !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    box-sizing: border-box !important;
  }

  /* Su smartphone impila le 3 colonne IMWEAR in verticale dentro il box centrato (zero tagli a destra) */
  @media (max-width: 768px) {
    .brand-panel-content .grid,
    #brand-modal .grid,
    [class*="brand-panel"] [class*="grid"] {
      display: grid !important;
      grid-template-columns: 1fr !important;
      gap: 24px !important;
      width: 100% !important;
    }
  }
</style>
'''

content += "\n" + fix_script + "\n" + fix_css

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("CENTRATURA BOX MODALE E LOCK COLONNA FULL-ZIP (1-2-3) COMPLETATI.")
