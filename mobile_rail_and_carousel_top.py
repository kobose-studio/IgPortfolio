import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# Rimuove eventuali vecchie versioni del calibratore mobile V8/V9 per evitare conflitti
content = re.sub(r'<script is:inline>\s*\(function\(\)\s*\{\s*if\s*\(window\.__IMLAND_MOBILE_(?:FRAMING_V8|PRECISION_V9)[\s\S]*?</script>', '', content)
content = re.sub(r'<style id="imland-mobile-precision-css"[\s\S]*?</style>', '', content)

# Assicura un corridoio laterale simmetrico su schermi verticali (portando FOCUS_Z mobile a +1.35)
content = re.sub(
    r'FOCUS_Z\s*\+\s*\(window\.innerWidth\s*<=\s*768\s*\?\s*1\.15\s*:\s*0\.0\)',
    'FOCUS_Z + (window.innerWidth <= 768 ? 1.35 : 0.0)',
    content
)

precision_script = '''<script is:inline>
(function() {
  if (window.__IMLAND_MOBILE_PRECISION_V9) return;
  window.__IMLAND_MOBILE_PRECISION_V9 = true;

  const isMobile = window.innerWidth <= 768 || /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
  if (!isMobile) return;

  // Risale al vero contenitore posizionato (fixed/absolute) di un nodo testuale
  function getPositionedWrapper(el) {
    let curr = el;
    while (curr && curr !== document.body) {
      const pos = getComputedStyle(curr).position;
      if (pos === 'fixed' || pos === 'absolute') return curr;
      curr = curr.parentElement;
    }
    return el;
  }

  function calibrateMobileGeometry() {
    // 1. ALLINEAMENTO SPECULARE AL MILLIMETRO DEL BINARIO SINISTRO
    let leftTextNode = null;
    let rightTextNode = null;

    const nodes = document.querySelectorAll('nav, aside, header, div, span');
    for (const el of nodes) {
      const txt = (el.textContent || '').trim();
      if (!leftTextNode && txt.includes('MANIFESTO') && txt.includes('IMWEAR') && txt.length < 130) {
        leftTextNode = el;
      }
      if (!rightTextNode && txt.includes('ARCHIVE 2026') && txt.length < 130) {
        rightTextNode = el;
      }
    }

    if (leftTextNode) {
      const leftRail = getPositionedWrapper(leftTextNode);
      const rightRail = rightTextNode ? getPositionedWrapper(rightTextNode) : null;

      // Legge la distanza reale dal bordo destro di "ARCHIVE 2026" (es. 12px)
      let mirrorGap = 12;
      if (rightRail) {
        const rRect = rightRail.getBoundingClientRect();
        const rightDist = window.innerWidth - rRect.right;
        if (rightDist >= 4 && rightDist <= 32) {
          mirrorGap = Math.round(rightDist);
        }
      }

      // Ripulisce sfondi satinati e ombre sia sul contenitore che sui figli
      [leftRail, leftTextNode].forEach((targetEl) => {
        targetEl.style.setProperty('background', 'transparent', 'important');
        targetEl.style.setProperty('background-color', 'transparent', 'important');
        targetEl.style.setProperty('backdrop-filter', 'none', 'important');
        targetEl.style.setProperty('-webkit-backdrop-filter', 'none', 'important');
        targetEl.style.setProperty('box-shadow', 'none', 'important');
        targetEl.style.setProperty('border', 'none', 'important');
        targetEl.style.setProperty('padding', '0', 'important');
      });

      // Ancora il binario sinistro a filo bordo con lo stesso identico offset del destro
      leftRail.style.setProperty('position', 'fixed', 'important');
      leftRail.style.setProperty('top', '50%', 'important');
      leftRail.style.setProperty('right', 'auto', 'important');
      leftRail.style.setProperty('margin', '0', 'important');
      leftRail.style.setProperty('width', 'auto', 'important');
      leftRail.style.setProperty('height', 'auto', 'important');
      leftRail.style.setProperty('writing-mode', 'vertical-rl', 'important');
      leftRail.style.setProperty('transform', 'translateY(-50%) rotate(180deg)', 'important');
      leftRail.style.setProperty('z-index', '45', 'important');

      leftRail.style.setProperty('left', mirrorGap + 'px', 'important');
      const lRect = leftRail.getBoundingClientRect();
      if (Math.abs(lRect.left - mirrorGap) > 0.5) {
        const delta = mirrorGap - lRect.left;
        leftRail.style.setProperty('left', Math.max(4, mirrorGap + delta) + 'px', 'important');
      }
    }

    // 2. POSIZIONAMENTO BARRA CAROSELLO SOPRA LA FOTO (Sotto il logo IMLAND)
    const buttons = Array.from(document.querySelectorAll('button'));
    const prevSlideBtn = buttons.find(b => /PREV\s*SLIDE/i.test(b.textContent || ''));

    if (prevSlideBtn) {
      const carouselBar = getPositionedWrapper(prevSlideBtn) || prevSlideBtn.parentElement;
      // Calcola il margine inferiore del logo IMLAND in alto
      const logoEl = document.querySelector('header img, img[alt*="IMLAND" i], a img');
      let topAnchor = 148;
      if (logoEl) {
        const logoRect = logoEl.getBoundingClientRect();
        if (logoRect.bottom > 40 && logoRect.bottom < 190) {
          topAnchor = Math.round(logoRect.bottom + 14);
        }
      }

      if (carouselBar) {
        carouselBar.style.setProperty('position', 'fixed', 'important');
        carouselBar.style.setProperty('top', topAnchor + 'px', 'important');
        carouselBar.style.setProperty('bottom', 'auto', 'important');
        carouselBar.style.setProperty('left', '50%', 'important');
        carouselBar.style.setProperty('right', 'auto', 'important');
        carouselBar.style.setProperty('transform', 'translateX(-50%)', 'important');
        carouselBar.style.setProperty('z-index', '65', 'important');
        carouselBar.style.setProperty('display', 'inline-flex', 'important');
        carouselBar.style.setProperty('flex-direction', 'row', 'important');
        carouselBar.style.setProperty('align-items', 'center', 'important');
        carouselBar.style.setProperty('justify-content', 'center', 'important');
        carouselBar.style.setProperty('gap', '12px', 'important');
        carouselBar.style.setProperty('padding', '6px 14px', 'important');
        carouselBar.style.setProperty('white-space', 'nowrap', 'important');
        carouselBar.style.setProperty('width', 'auto', 'important');
        carouselBar.style.setProperty('max-width', '92vw', 'important');
      }
    }
  }

  window.addEventListener('DOMContentLoaded', calibrateMobileGeometry);
  window.addEventListener('resize', calibrateMobileGeometry);
  setInterval(calibrateMobileGeometry, 160);
})();
</script>
'''

precision_css = '''
<style id="imland-mobile-precision-css" is:global>
  @media (max-width: 768px) {
    /* Mantieni sempre visibili e speculari entrambi i binari verticali ai bordi */
    body.mobile-artwork-isolated nav,
    body.mobile-artwork-isolated .vertical-nav,
    body.mobile-artwork-isolated #axis-nav,
    body.mobile-artwork-isolated .sidebar-nav {
      opacity: 1 !important;
      pointer-events: auto !important;
    }

    /* Compatta i testi della barra carosello superiore su una singola riga */
    button {
      white-space: nowrap !important;
    }
  }
</style>
'''

content += "\n" + precision_script + "\n" + precision_css

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("CALIBRAZIONE SPECULARE E CAROSELLO SUPERIORE COMPLETATI.")
