import os, re

target = 'src/components/PortfolioSceneSphere.astro'
s = open(target, encoding='utf-8').read()

# 1. Verifica che il motore 3D sia integro (nessun reset distruttivo)
for tok in ('THREE.Scene', 'THREE.PerspectiveCamera', 'THREE.WebGLRenderer', 'requestAnimationFrame'):
    assert tok in s, f"ERRORE DI SICUREZZA: token mancante {tok} - nessuna modifica applicata!"

# 2. Bonifica statica su tutti i file .astro in src/:
#    - Sostituisce /brand/hoodie-1.jpg (file inesistente) con /brand/hoodie-2.jpg direttamente nell'HTML sorgente
for root, _, files in os.walk('src'):
    for fn in files:
        if not fn.endswith('.astro'):
            continue
        fp = os.path.join(root, fn)
        txt = open(fp, encoding='utf-8').read()
        orig = txt
        txt = txt.replace('/brand/hoodie-1.jpg', '/brand/hoodie-2.jpg')
        txt = txt.replace('/brand/hoodie-A.jpg', '/brand/hoodie-2.jpg')
        if txt != orig:
            open(fp, 'w', encoding='utf-8').write(txt)

s = open(target, encoding='utf-8').read()

# Rimuove eventuali vecchi blocchi V43/V44/V45 per sostituirli con V45 pulito e unificato
s = re.sub(r'\n\s*// === V4[35] MAGNETIC MOBILE TOUCH-TO-3D ENGINE ===[\s\S]*?// === END V4[35] MAGNETIC ===\n', '\n', s)
s = re.sub(r'<(?:script|style) id="imland-v4[345]-[^"]*"[\s\S]*?</(?:script|style)>', '', s)

# 3. Motore Magnetico Touch-to-3D V45:
#    - Calcola la bounding box 2D proiettata di ogni foto 3D nel tunnel (+26px di margine per il pollice)
#    - Aggiorna istantaneamente mouse/targetMouse prima del click sintetico
magnetic_v45_ts = '''
  // === V45 MAGNETIC MOBILE TOUCH-TO-3D ENGINE ===
  let __v45TouchX = 0, __v45TouchY = 0, __v45TouchTime = 0;
  const __v45ProjVec = new THREE.Vector3();
  const __v45CornerVec = new THREE.Vector3();

  const __v45FindVortexTarget = (clientX: number, clientY: number) => {
    const rc = renderer.domElement.getBoundingClientRect();
    if (!rc.width || !rc.height) return null;

    const photoMeshes: THREE.Mesh[] = [];
    scene.traverse((obj: any) => {
      if (!obj || !obj.isMesh || !obj.visible) return;
      if (typeof activeMesh !== 'undefined' && obj === activeMesh) return;
      const mat = obj.material;
      if (mat && ((mat.uniforms && mat.uniforms.uTexture) || mat.map)) {
        photoMeshes.push(obj);
      }
    });

    // 1. Raycast diretto sul punto esatto toccato
    __pn.set(((clientX - rc.left) / rc.width) * 2 - 1, -((clientY - rc.top) / rc.height) * 2 + 1);
    __pr.setFromCamera(__pn, camera);
    const exactHits = __pr.intersectObjects(photoMeshes, false);
    if (exactHits.length > 0) {
      const hm = exactHits[0].object as THREE.Mesh;
      hm.getWorldPosition(__v45ProjVec);
      __v45ProjVec.project(camera);
      return {
        mesh: hm,
        ndcX: __v45ProjVec.x,
        ndcY: __v45ProjVec.y,
        sx: rc.left + (__v45ProjVec.x + 1) * 0.5 * rc.width,
        sy: rc.top + (-__v45ProjVec.y + 1) * 0.5 * rc.height
      };
    }

    // 2. Proiezione 2D di bounding-box + raggio magnetico 68px per tap su smartphone
    let best: { mesh: THREE.Mesh; ndcX: number; ndcY: number; sx: number; sy: number; score: number } | null = null;
    for (const m of photoMeshes) {
      m.getWorldPosition(__v45ProjVec);
      __v45ProjVec.project(camera);
      if (__v45ProjVec.z < -1 || __v45ProjVec.z > 1) continue;

      const sx = rc.left + (__v45ProjVec.x + 1) * 0.5 * rc.width;
      const sy = rc.top + (-__v45ProjVec.y + 1) * 0.5 * rc.height;

      let halfW = 34, halfH = 42;
      if (m.geometry) {
        if (!m.geometry.boundingBox) m.geometry.computeBoundingBox();
        const bb = m.geometry.boundingBox;
        if (bb) {
          __v45CornerVec.set(bb.max.x, bb.max.y, 0).applyMatrix4(m.matrixWorld).project(camera);
          const cx = rc.left + (__v45CornerVec.x + 1) * 0.5 * rc.width;
          const cy = rc.top + (-__v45CornerVec.y + 1) * 0.5 * rc.height;
          halfW = Math.max(28, Math.abs(cx - sx));
          halfH = Math.max(34, Math.abs(cy - sy));
        }
      }

      const dx = Math.max(0, Math.abs(clientX - sx) - (halfW + 26));
      const dy = Math.max(0, Math.abs(clientY - sy) - (halfH + 26));
      const edgeDist = Math.hypot(dx, dy);
      const centerDist = Math.hypot(clientX - sx, clientY - sy);

      if (edgeDist === 0 || centerDist <= 68) {
        const score = edgeDist * 2 + centerDist * 0.35 + (__v45ProjVec.z * 20);
        if (!best || score < best.score) {
          best = { mesh: m, ndcX: __v45ProjVec.x, ndcY: __v45ProjVec.y, sx, sy, score };
        }
      }
    }
    return best;
  };

  const __v45DispatchPointerAndClick = (targetHit: { ndcX: number; ndcY: number; sx: number; sy: number }) => {
    try {
      if (typeof mouse !== 'undefined' && mouse && typeof mouse.set === 'function') {
        mouse.set(targetHit.ndcX, targetHit.ndcY);
      }
    } catch (_e) {}
    try {
      if (typeof targetMouse !== 'undefined' && targetMouse && typeof targetMouse.set === 'function') {
        targetMouse.set(targetHit.ndcX, targetHit.ndcY);
      }
    } catch (_e) {}

    const evInit = {
      clientX: targetHit.sx,
      clientY: targetHit.sy,
      bubbles: true,
      cancelable: true,
      view: window
    };
    renderer.domElement.dispatchEvent(new PointerEvent('pointermove', { ...evInit, pointerType: 'mouse', isPrimary: true }));
    renderer.domElement.dispatchEvent(new MouseEvent('mousemove', evInit));
    requestAnimationFrame(() => {
      renderer.domElement.dispatchEvent(new PointerEvent('pointerdown', { ...evInit, pointerType: 'mouse', button: 0, isPrimary: true }));
      renderer.domElement.dispatchEvent(new MouseEvent('mousedown', { ...evInit, button: 0 }));
      renderer.domElement.dispatchEvent(new PointerEvent('pointerup', { ...evInit, pointerType: 'mouse', button: 0, isPrimary: true }));
      renderer.domElement.dispatchEvent(new MouseEvent('mouseup', { ...evInit, button: 0 }));
      renderer.domElement.dispatchEvent(new MouseEvent('click', { ...evInit, button: 0 }));
    });
  };

  renderer.domElement.addEventListener('touchstart', (e: TouchEvent) => {
    const t = e.touches && e.touches[0];
    if (!t) return;
    __v45TouchX = t.clientX;
    __v45TouchY = t.clientY;
    __v45TouchTime = Date.now();
    const hit = __v45FindVortexTarget(t.clientX, t.clientY);
    if (hit) {
      renderer.domElement.dispatchEvent(new MouseEvent('mousemove', { clientX: hit.sx, clientY: hit.sy, bubbles: true }));
    }
  }, { passive: true });

  renderer.domElement.addEventListener('touchend', (e: TouchEvent) => {
    const st = document.getElementById('editorial-stage');
    if (st && st.classList.contains('is-active')) return;
    const t = e.changedTouches && e.changedTouches[0];
    if (!t) return;
    const moved = Math.hypot(t.clientX - __v45TouchX, t.clientY - __v45TouchY);
    const dt = Date.now() - __v45TouchTime;
    if (moved < 22 && dt < 520) {
      const hit = __v45FindVortexTarget(t.clientX, t.clientY);
      if (hit) {
        e.preventDefault();
        __v45DispatchPointerAndClick(hit);
      }
    }
  }, { passive: false });
  // === END V45 MAGNETIC ===
'''

assert '// Mobile Touch-to-Raycast Bridge:' in s, "Anchor bridge non trovato!"
s = s.replace('// Mobile Touch-to-Raycast Bridge:', magnetic_v45_ts + '\n  // Mobile Touch-to-Raycast Bridge:', 1)

# 4. CSS + Controller V45:
#    - Eclissa TOTALMENTE logo IMLAND (img[src*="logo-imland"]) e menu quando IMWEAR / MANIFESTO / CONTACTS sono aperti
#    - Porta le modali a z-index: 99999 !important direttamente su document.body
#    - Blindatura IMWEAR 8-3-5 su MutationObserver + error fallback
v45_ui_block = '''
<style id="imland-v45-css" is:global>
  #brand-modal,
  #contacts-modal,
  #manifesto-modal {
    position: fixed !important;
    inset: 0 !important;
    width: 100vw !important;
    height: 100dvh !important;
    z-index: 99999 !important;
    background: rgba(246, 245, 242, 0.86) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
  }
  #brand-modal > div,
  #contacts-modal > div,
  #manifesto-modal > div,
  .brand-panel-content,
  .contacts-panel-content,
  .manifesto-panel-content {
    position: relative !important;
    z-index: 100000 !important;
    background: #ffffff !important;
  }

  body.imland-modal-open [data-imland-nav="1"],
  body.imland-modal-open [data-imland-logo="1"],
  body.imland-modal-open img[src*="logo-imland"],
  body.imland-modal-open header:not(#brand-modal header):not(#contacts-modal header):not(#manifesto-modal header),
  body.imland-modal-open nav:not(#brand-modal nav):not(#contacts-modal nav):not(#manifesto-modal nav) {
    display: none !important;
    opacity: 0 !important;
    visibility: hidden !important;
    pointer-events: none !important;
  }
</style>
<script id="imland-v45-controller" is:inline>
(function(){
  if (window.__V45_UI) return;
  window.__V45_UI = 1;

  document.addEventListener('error', (e) => {
    const img = e.target;
    if (img && img.tagName === 'IMG') {
      const src = img.getAttribute('src') || '';
      if (src.includes('hoodie-1') || src.includes('hoodie-A')) {
        img.setAttribute('src', '/brand/hoodie-2.jpg');
      }
    }
  }, true);

  const isModalOpen = (el) => {
    if (!el) return false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0') return false;
    const r = el.getBoundingClientRect();
    return r.width > 40 && r.height > 40;
  };

  const enforceModalOcclusion = () => {
    const modalIds = ['brand-modal', 'contacts-modal', 'manifesto-modal'];
    let anyOpen = false;
    for (const id of modalIds) {
      const m = document.getElementById(id);
      if (m) {
        if (m.parentElement !== document.body) document.body.appendChild(m);
        if (isModalOpen(m)) anyOpen = true;
      }
    }
    document.body.classList.toggle('imland-modal-open', anyOpen);

    document.querySelectorAll('img[src*="logo-imland"]').forEach((img) => {
      const wrap = img.closest('div, header, a') || img.parentElement;
      if (wrap && !wrap.querySelector('[data-imland-nav="1"]')) {
        wrap.setAttribute('data-imland-logo', '1');
      }
    });
  };

  const CAT = {
    c1: ['/brand/hoodie-2.jpg','/brand/hoodie-3.jpg','/brand/hoodie-4.jpg','/brand/hoodie-5.jpg','/brand/hoodie-6.jpg','/brand/hoodie-7.jpg','/brand/hoodie-8.jpg','/brand/hoodie-9.jpg'],
    c2: ['/brand/hoodie_zip-1.jpg','/brand/hoodie_zip-2.jpg','/brand/hoodie_zip-3.jpg'],
    c3: ['/brand/tee-1.jpg','/brand/tee-2.jpg','/brand/tee-3.jpg','/brand/tee-4.jpg','/brand/tee-5.jpg']
  };
  const idx = { c1: 0, c2: 0, c3: 0 };

  function lockImwearColumns() {
    const bm = document.getElementById('brand-modal');
    if (!bm) return;

    const headings = Array.from(bm.querySelectorAll('h1, h2, h3, h4, p, span, div')).filter((el) => {
      if (el.children.length > 0) return false;
      const tx = (el.textContent || '').trim().toUpperCase();
      return tx.includes('CLASSIC HOODIE') || tx.includes('FULL-ZIP') || tx.includes('ESSENTIALS');
    });

    const cards = { c1: null, c2: null, c3: null };
    for (const h of headings) {
      const tx = (h.textContent || '').trim().toUpperCase();
      const key = tx.includes('FULL-ZIP') ? 'c2' : (tx.includes('CLASSIC HOODIE') ? 'c1' : 'c3');
      let card = h.parentElement;
      while (card && card !== bm) {
        const u = (card.textContent || '').toUpperCase();
        const countTitles = (u.includes('CLASSIC HOODIE') ? 1 : 0) + (u.includes('FULL-ZIP') ? 1 : 0) + (u.includes('ESSENTIALS') ? 1 : 0);
        if (countTitles === 1 && card.querySelector('img')) {
          cards[key] = card;
        } else if (countTitles > 1) {
          break;
        }
        card = card.parentElement;
      }
    }

    ['c1', 'c2', 'c3'].forEach((k) => {
      const card = cards[k];
      if (!card) return;
      const imgs = Array.from(card.querySelectorAll('img:not(.imwear-dissolve)'));
      if (!imgs.length) return;
      for (let i = 1; i < imgs.length; i++) imgs[i].remove();
      const curSrc = imgs[0].getAttribute('src') || '';
      if (!CAT[k].includes(curSrc)) {
        imgs[0].setAttribute('src', CAT[k][idx[k]]);
      }
    });
  }

  const bootV45 = () => {
    enforceModalOcclusion();
    lockImwearColumns();

    ['brand-modal', 'contacts-modal', 'manifesto-modal'].forEach((id) => {
      const el = document.getElementById(id);
      if (el) {
        new MutationObserver(() => {
          enforceModalOcclusion();
          if (id === 'brand-modal') lockImwearColumns();
        }).observe(el, { attributes: true, subtree: true, attributeFilter: ['style', 'class', 'src', 'hidden'] });
      }
    });
  };

  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', bootV45) : bootV45();
  document.addEventListener('click', () => {
    enforceModalOcclusion();
    lockImwearColumns();
    setTimeout(() => { enforceModalOcclusion(); lockImwearColumns(); }, 40);
    setTimeout(() => { enforceModalOcclusion(); lockImwearColumns(); }, 200);
  }, { capture: true });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      setTimeout(enforceModalOcclusion, 25);
      setTimeout(enforceModalOcclusion, 160);
    }
  });
})();
</script>
'''

s = s.rstrip() + '\n' + v45_ui_block + '\n'
open(target, 'w', encoding='utf-8').write(s)
print("OK_V45_INCREMENTAL_ALL_FIXES_READY")
