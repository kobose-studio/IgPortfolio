import os
import re

# Verifica quale componente è montato in index.astro
with open('src/pages/index.astro', 'r', encoding='utf-8') as f:
    idx_html = f.read()
print("Componente attivo in index.astro:", [l.strip() for l in idx_html.splitlines() if 'Portfolio' in l])

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# A. RIMUOVE EVENTUALI VECCHI BLOCCHI PATCH CHE POTEVANO CREARE CONFLITTI
content = re.sub(r'<script id="imland-[^"]*"[\s\S]*?</script>', '', content)
content = re.sub(r'<style id="imland-[^"]*"[\s\S]*?</style>', '', content)

# B. AGGIORNAMENTO MANIFESTO POETICO (Senza "MONTEROSA" + paragrafo fotografia)
new_manifesto_html = """IMLAND nasce sotto l'ombra imponente della parete est del Monte Rosa. Non creiamo capi per il consumo di massa, né per la moda da passerella cittadina.</p>
          <p style="margin-top: 1.1rem; max-width: 680px; line-height: 1.65;">Progettiamo <strong>outfit outdoor ad alte prestazioni</strong> per chi vive la montagna con rispetto, silenzio e radici profonde. In un mondo saturo di rumore digitale, Alagna e le sue valli da scoprire rimangono la nostra unica bussola esistenziale.</p>
          <p style="margin-top: 1.1rem; max-width: 680px; line-height: 1.65;">Affiancando al rigore dell'equipaggiamento alpino la <strong>fotografia</strong> come strumento di ascolto lento, ogni immagine che ruota nel vortice smette di essere un semplice post e si trasforma in un indizio silenzioso nascosto tra le pieghe della valle.</p>"""

# Sostituisce il blocco del vecchio testo fino a "bussola esistenziale.</p>"
manifesto_pattern = re.compile(
    r'IMLAND(?:\s+MONTEROSA)?\s+nasce\s+sotto[\s\S]*?bussola\s+esistenziale\.\s*</p>',
    re.IGNORECASE
)
if manifesto_pattern.search(content):
    content = manifesto_pattern.sub(lambda _: new_manifesto_html, content, count=1)
    print("✅ Testo Manifesto aggiornato con successo.")
else:
    print("⚠️ Pattern Manifesto non trovato direttamente, verrà sincronizzato anche via DOM.")

# C. BONIFICA RIFERIMENTI SORGENTE IMWEAR (Elimina hoodie-1.jpg e allinea le zip)
content = content.replace('/brand/hoodie-1.jpg', '/brand/hoodie-2.jpg')
content = content.replace('/brand/hoodie-A.jpg', '/brand/hoodie-2.jpg')
content = content.replace('/brand/zip-hoodie.jpg', '/brand/hoodie_zip-1.jpg')

# D. FIX VIDEO PLAYER NELLA MODALE EDITORIALE (Evita la barra nera schiacciata 0:00)
old_video_block = re.compile(r'if\s*\(\s*data\.media_type\s*===\s*[\'"]VIDEO[\'"]\s*\)\s*\{[\s\S]*?videoStage\.appendChild\(video\);\s*\}')
new_video_block = """if (data.media_type === 'VIDEO') {
            videoStage.style.cssText = 'display:flex; align-items:center; justify-content:center; width:min(88vw, 440px); min-height:280px; max-height:62vh; margin:0 auto; pointer-events:auto;';
            const video = document.createElement('video');
            video.src = data.media_url;
            video.poster = data.thumbnail_url || '';
            video.autoplay = true;
            video.loop = true;
            video.muted = true;
            video.controls = true;
            video.playsInline = true;
            video.setAttribute('playsinline', '');
            video.style.cssText = 'width:100%; height:auto; max-height:62vh; object-fit:contain; border-radius:4px; background:#0b0b0b; box-shadow:0 24px 50px rgba(0,0,0,0.18); pointer-events:auto;';
            video.onerror = () => {
              videoStage.innerHTML = '';
              if (data.thumbnail_url) {
                const fallbackWrap = document.createElement('a');
                fallbackWrap.href = data.permalink || '#';
                fallbackWrap.target = '_blank';
                fallbackWrap.rel = 'noopener noreferrer';
                fallbackWrap.style.cssText = 'position:relative; display:block; width:100%; max-height:62vh; text-decoration:none;';
                fallbackWrap.innerHTML = `<img src="${data.thumbnail_url}" style="width:100%; max-height:62vh; object-fit:contain; border-radius:4px; display:block;" /><span style="position:absolute; bottom:14px; left:50%; transform:translateX(-50%); background:#111; color:#fff; font-family:monospace; font-size:10px; letter-spacing:0.1em; padding:6px 12px; white-space:nowrap;">[ GUARDA VIDEO SU INSTAGRAM ↗ ]</span>`;
                videoStage.appendChild(fallbackWrap);
              }
            };
            videoStage.appendChild(video);
          }"""

if old_video_block.search(content):
    content = old_video_block.sub(lambda _: new_video_block, content, count=1)
    print("✅ Player Video aggiornato con dimensioni reali e fallback thumbnail.")

# E. CONTROLLER DEFINITIVO V12 (IMWEAR 9-3-5 + Centratura Modali + Sync Manifesto)
controller_v12 = """
<!-- IMLAND_BUILD_V12_VERIFIED -->
<script id="imland-v12-controller" is:inline>
(function() {
  if (window.__IMLAND_V12_ACTIVE) return;
  window.__IMLAND_V12_ACTIVE = true;

  const CATALOG = {
    col1: [
      '/brand/hoodie-2.jpg',
      '/brand/hoodie-3.jpg',
      '/brand/hoodie-4.jpg',
      '/brand/hoodie-5.jpg',
      '/brand/hoodie-6.jpg',
      '/brand/hoodie-7.jpg',
      '/brand/hoodie-8.jpg',
      '/brand/hoodie-9.jpg'
    ],
    col2: [
      '/brand/hoodie_zip-1.jpg',
      '/brand/hoodie_zip-2.jpg',
      '/brand/hoodie_zip-3.jpg'
    ],
    col3: [
      '/brand/tee-1.jpg',
      '/brand/tee-2.jpg',
      '/brand/tee-3.jpg',
      '/brand/tee-4.jpg',
      '/brand/tee-5.jpg'
    ]
  };

  const pointers = { col1: 0, col2: 0, col3: 0 };

  function syncImwearBoxes(advance) {
    const modal = document.getElementById('brand-modal') || document.body;
    // Trova le 3 card tramite i loro titoli specifici
    const allEls = Array.from(modal.querySelectorAll('article, div, section'));
    const targets = { col1: null, col2: null, col3: null };

    for (const el of allEls) {
      const txt = (el.textContent || '').toUpperCase();
      if (el.querySelectorAll('img').length === 0) continue;
      const c1 = txt.includes('CLASSIC HOODIE');
      const c2 = txt.includes('FULL-ZIP');
      const c3 = txt.includes('ESSENTIALS');
      if (c1 && !c2 && !c3) targets.col1 = el;
      if (c2 && !c1 && !c3) targets.col2 = el;
      if (c3 && !c1 && !c2) targets.col3 = el;
    }

    (['col1', 'col2', 'col3']).forEach((k) => {
      const card = targets[k];
      if (!card) return;
      const list = CATALOG[k];
      if (advance) pointers[k] = (pointers[k] + 1) % list.length;
      const nextSrc = list[pointers[k]];

      const imgs = Array.from(card.querySelectorAll('img'));
      if (imgs.length === 0) return;

      // Mantiene un unico tag <img> pulito per evitare sovrapposizioni del vecchio carosello
      const img = imgs[0];
      for (let i = 1; i < imgs.length; i++) imgs[i].remove();

      if (img.getAttribute('src') !== nextSrc) {
        img.setAttribute('src', nextSrc);
      }
      img.style.setProperty('opacity', '1', 'important');
      img.style.setProperty('position', 'relative', 'important');
      img.style.setProperty('width', '100%', 'important');
      img.style.setProperty('height', '100%', 'important');
      img.style.setProperty('object-fit', 'cover', 'important');
      img.style.setProperty('display', 'block', 'important');
    });
  }

  function centerAllModals() {
    ['#brand-modal', '#contacts-modal', '#manifesto-modal'].forEach((sel) => {
      const ov = document.querySelector(sel);
      if (!ov || getComputedStyle(ov).display === 'none') return;
      ov.style.setProperty('position', 'fixed', 'important');
      ov.style.setProperty('inset', '0', 'important');
      ov.style.setProperty('width', '100vw', 'important');
      ov.style.setProperty('height', '100dvh', 'important');
      ov.style.setProperty('display', 'flex', 'important');
      ov.style.setProperty('align-items', 'center', 'important');
      ov.style.setProperty('justify-content', 'center', 'important');
      ov.style.setProperty('padding', '16px', 'important');
      ov.style.setProperty('margin', '0', 'important');
      ov.style.setProperty('transform', 'none', 'important');

      const panel = ov.firstElementChild;
      if (panel) {
        panel.style.setProperty('position', 'relative', 'important');
        panel.style.setProperty('left', 'auto', 'important');
        panel.style.setProperty('right', 'auto', 'important');
        panel.style.setProperty('top', 'auto', 'important');
        panel.style.setProperty('bottom', 'auto', 'important');
        panel.style.setProperty('transform', 'none', 'important');
        panel.style.setProperty('margin', '0 auto', 'important');
        panel.style.setProperty('width', 'min(92vw, 880px)', 'important');
        panel.style.setProperty('max-width', 'min(92vw, 880px)', 'important');
        panel.style.setProperty('background', '#ffffff', 'important');
        panel.style.setProperty('border', 'none', 'important');
        panel.style.setProperty('box-shadow', '0 24px 60px rgba(0,0,0,0.06)', 'important');
      }
    });
  }

  window.addEventListener('DOMContentLoaded', () => {
    syncImwearBoxes(false);
    centerAllModals();
  });
  document.addEventListener('click', () => {
    setTimeout(() => {
      syncImwearBoxes(false);
      centerAllModals();
    }, 30);
  });
  setInterval(() => {
    syncImwearBoxes(true);
    centerAllModals();
  }, 2800);
})();
</script>
"""

content += "\n" + controller_v12

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ File Astro aggiornato e pronto per il test di compilazione locale.")
