import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# A. ELEVAZIONE CAMERA 3D IN FOCUS SU MOBILE (Spinge la foto isolata verso l'alto, sopra il box bianco)
# Intercetta l'assegnazione di offsetY / targetY per activeMesh e imposta -1.12 su smartphone
content = re.sub(
    r'(const\s+offsetY\s*=\s*)[^;]+;',
    r'\1(window.innerWidth <= 768 ? -1.12 : 0.0);',
    content
)

# Se il camera target Y usa direttamente activeMesh.position.y senza offsetY, inietta la elevazione mobile
if 'offsetY' not in content:
    content = re.sub(
        r'(camera\.position\.y\s*\+=\s*\(\s*activeMesh\.position\.y)(\s*-\s*camera\.position\.y\s*\))',
        r'\1 + (window.innerWidth <= 768 ? -1.12 : 0.0)\2',
        content
    )

# Calibra la distanza Z in focus su mobile portrait per evitare che i lati della foto tocchino i bordi
content = re.sub(
    r'(FOCUS_Z\s*-\s*camera\.position\.z)',
    r'(FOCUS_Z + (window.innerWidth <= 768 ? 1.15 : 0.0) - camera.position.z)',
    content
)

# B. INIEZIONE MOTORE TATTILE & CALIBRATORE SPECULARE SUB-PIXEL
ux_script = '''<script is:inline>
(function() {
  if (window.__IMLAND_MOBILE_FRAMING_V8) return;
  window.__IMLAND_MOBILE_FRAMING_V8 = true;

  const isMobile = window.innerWidth <= 768 || /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
  if (!isMobile) return;

  // 1. ALLINEAMENTO SPECULARE A CICLO CHIUSO DEL BINARIO SINISTRO
  function syncMirrorRails() {
    let leftRail = null;
    let rightRail = null;

    const allEls = document.querySelectorAll('nav, aside, header, div');
    for (const el of allEls) {
      const txt = (el.textContent || '').trim();
      if (!leftRail && txt.includes('MANIFESTO') && txt.includes('IMWEAR') && txt.length < 130) {
        leftRail = el;
      }
      if (!rightRail && txt.includes('ARCHIVE 2026') && txt.length < 130) {
        rightRail = el;
      }
    }

    if (leftRail) {
      // Misura il margine esatto del binario destro (es. 12px) per replicarlo a sinistra
      let targetGap = 12;
      if (rightRail) {
        const rRect = rightRail.getBoundingClientRect();
        const rightMargin = window.innerWidth - rRect.right;
        if (rightMargin >= 4 && rightMargin <= 36) {
          targetGap = Math.round(rightMargin);
        }
      }

      leftRail.style.setProperty('position', 'fixed', 'important');
      leftRail.style.setProperty('top', '50%', 'important');
      leftRail.style.setProperty('right', 'auto', 'important');
      leftRail.style.setProperty('writing-mode', 'vertical-rl', 'important');
      leftRail.style.setProperty('transform', 'translateY(-50%) rotate(180deg)', 'important');
      leftRail.style.setProperty('background', 'transparent', 'important');
      leftRail.style.setProperty('backdrop-filter', 'none', 'important');
      leftRail.style.setProperty('-webkit-backdrop-filter', 'none', 'important');
      leftRail.style.setProperty('border', 'none', 'important');
      leftRail.style.setProperty('box-shadow', 'none', 'important');
      leftRail.style.setProperty('padding', '0', 'important');
      leftRail.style.setProperty('margin', '0', 'important');
      leftRail.style.setProperty('width', 'auto', 'important');
      leftRail.style.setProperty('height', 'auto', 'important');
      leftRail.style.setProperty('z-index', '40', 'important');

      // Correzione sub-pixel basata sul bounding box reale post-rotazione
      leftRail.style.setProperty('left', targetGap + 'px', 'important');
      const lRect = leftRail.getBoundingClientRect();
      if (Math.abs(lRect.left - targetGap) > 1) {
        const correctedLeft = targetGap + (targetGap - lRect.left);
        leftRail.style.setProperty('left', Math.max(4, correctedLeft) + 'px', 'important');
      }
    }

    // Rileva isolamento opera per dissolvere il menu sinistro ed evitare sovrapposizioni sulla foto
    const stage = document.getElementById('editorial-stage');
    const isIsolated = stage && (
      stage.classList.contains('is-active') ||
      (getComputedStyle(stage).opacity !== '0' && getComputedStyle(stage).pointerEvents !== 'none')
    );
    document.body.classList.toggle('mobile-artwork-isolated', Boolean(isIsolated));

    // Ancora la barra slide del carosello subito sopra il bordo del box bianco inferiore
    if (isIsolated) {
      const card = stage.querySelector('div');
      const slideBar = document.querySelector('[class*="slide"], [id*="slide"], [class*="carousel-nav"]');
      if (card && slideBar && !card.contains(slideBar)) {
        const cardRect = card.getBoundingClientRect();
        if (cardRect.top > 120) {
          slideBar.style.setProperty('position', 'fixed', 'important');
          slideBar.style.setProperty('top', 'auto', 'important');
          slideBar.style.setProperty('bottom', (window.innerHeight - cardRect.top + 8) + 'px', 'important');
          slideBar.style.setProperty('left', '50%', 'important');
          slideBar.style.setProperty('transform', 'translateX(-50%)', 'important');
          slideBar.style.setProperty('z-index', '65', 'important');
        }
      }
    }
  }

  // 2. GESTURE SWIPE ORIZZONTALE PER SFOGLIARE LE SLIDE DEL CAROSELLO CON IL POLLICE
  let swipeStartX = 0;
  let swipeStartY = 0;

  window.addEventListener('touchstart', (e) => {
    if (e.touches && e.touches.length === 1) {
      swipeStartX = e.touches[0].clientX;
      swipeStartY = e.touches[0].clientY;
    }
  }, { passive: true });

  window.addEventListener('touchend', (e) => {
    if (!document.body.classList.contains('mobile-artwork-isolated')) return;
    if (!e.changedTouches || e.changedTouches.length === 0) return;

    const dx = e.changedTouches[0].clientX - swipeStartX;
    const dy = e.changedTouches[0].clientY - swipeStartY;

    // Se il gesto è prevalentemente orizzontale (> 42px), attiva Prev o Next Slide
    if (Math.abs(dx) > 42 && Math.abs(dx) > Math.abs(dy) * 1.4) {
      const buttons = Array.from(document.querySelectorAll('button'));
      if (dx < 0) {
        const nextBtn = buttons.find(b => /NEXT\s*SLIDE/i.test(b.textContent || ''));
        if (nextBtn) nextBtn.click();
      } else {
        const prevBtn = buttons.find(b => /PREV\s*SLIDE/i.test(b.textContent || ''));
        if (prevBtn) prevBtn.click();
      }
    }
  }, { passive: true });

  window.addEventListener('DOMContentLoaded', syncMirrorRails);
  window.addEventListener('resize', syncMirrorRails);
  setInterval(syncMirrorRails, 180);
})();
</script>
'''

content = re.sub(r'<script is:inline>\s*\(function\(\)\s*\{\s*if\s*\(window\.__IMLAND_MOBILE_FRAMING_V8[\s\S]*?</script>', '', content)
content += "\n" + ux_script

# C. SCUDO CSS MOBILE: Barra Carosello Editoriale su Singola Riga & Zero Sovrapposizioni
mobile_polish_css = '''
<style is:global>
  @media (max-width: 768px) {
    /* Dissolve il menu laterale sinistro quando una foto è aperta in primo piano */
    body.mobile-artwork-isolated nav,
    body.mobile-artwork-isolated .vertical-nav,
    body.mobile-artwork-isolated #axis-nav,
    body.mobile-artwork-isolated .sidebar-nav {
      opacity: 0 !important;
      pointer-events: none !important;
      transition: opacity 0.2s ease !important;
    }

    /* Ridisegna la pillola del carosello in una lama tipografica compatta su una sola riga */
    [class*="slide-controls"], [class*="carousel-controls"], [id*="carousel-controls"],
    div:has(> button):has([class*="slide"]) {
      display: inline-flex !important;
      flex-direction: row !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 14px !important;
      padding: 6px 14px !important;
      background: rgba(255, 255, 255, 0.94) !important;
      color: #111111 !important;
      border: 1px solid #111111 !important;
      border-radius: 2px !important;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08) !important;
      backdrop-filter: blur(8px) !important;
      -webkit-backdrop-filter: blur(8px) !important;
      white-space: nowrap !important;
      width: auto !important;
      max-width: 92vw !important;
    }

    [class*="slide-controls"] button,
    [class*="carousel-controls"] button,
    [id*="carousel-controls"] button {
      white-space: nowrap !important;
      font-size: 10px !important;
      letter-spacing: 0.08em !important;
      padding: 4px 6px !important;
      min-height: 28px !important;
      color: #111111 !important;
      background: transparent !important;
    }

    /* Scheda bianca inferiore compatta per lasciare ampio respiro alla foto sopra */
    #editorial-stage > div {
      left: 3.5vw !important;
      right: 3.5vw !important;
      width: 93vw !important;
      max-width: 93vw !important;
      bottom: max(10px, env(safe-area-inset-bottom)) !important;
      padding: 14px 16px !important;
      max-height: 31vh !important;
      overflow-y: auto !important;
    }
  }
</style>
'''

content += "\n" + mobile_polish_css

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("FASE 6.2 COMPLETATA: FOTO ELEVATA, BINARIO SINISTRO SPECULARE E CAROSELLO THUMB-DOCK ATTIVI.")
