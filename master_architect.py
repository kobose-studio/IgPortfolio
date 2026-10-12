import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# --- A. SIPARIO DI CARICAMENTO (LOADING SCREEN & DESKTOP WARNING) ---
loader_curtain = '''
<!-- IMLAND FULLSCREEN LOADING CURTAIN -->
<div id="imland-loader" style="position: fixed; inset: 0; width: 100vw; height: 100vh; z-index: 999999; background-color: #fafafa; display: flex; flex-direction: column; align-items: center; justify-content: center; transition: opacity 1.5s cubic-bezier(0.16, 1, 0.3, 1); pointer-events: auto;">
  <div style="text-align: center; padding: 0 24px; max-width: 400px;">
    <h1 style="font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 800; letter-spacing: 0.25em; text-transform: uppercase; color: #111111; margin-bottom: 20px; animation: loaderPulse 2s infinite;">
      MATERIALIZING ARCHIVE...
    </h1>
    <p style="font-family: monospace; font-size: 10px; letter-spacing: 0.15em; color: #b3a082; text-transform: uppercase; line-height: 1.8; margin: 0;">
      For the deepest visual journey,<br><br>the Desktop experience is highly recommended.
    </p>
  </div>
</div>

<style>
  @keyframes loaderPulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
</style>

<script>
  window.addEventListener('load', () => {
    // Garantisce che il 3D sia completamente renderizzato prima di sollevare il sipario
    setTimeout(() => {
      const loader = document.getElementById('imland-loader');
      if (loader) {
        loader.style.opacity = '0';
        loader.style.pointerEvents = 'none';
        setTimeout(() => loader.remove(), 1500);
      }
    }, 2000);
  });
</script>
'''

if 'imland-loader' not in content:
    idx_body = content.find('<body')
    if idx_body != -1:
        idx_close = content.find('>', idx_body)
        content = content[:idx_close+1] + '\n' + loader_curtain + content[idx_close+1:]
    else:
        content = loader_curtain + content

# --- B. MENU RESPONSIVE MOBILE BRUTALISTA (/ / /) ---
burger_menu_html = '''
<!-- IMLAND BRUTALIST MOBILE HAMBURGER -->
<div id="mobile-burger" class="md:hidden" style="position: fixed; top: 20px; right: 20px; z-index: 99999; cursor: pointer; font-family: monospace; font-size: 11px; letter-spacing: 0.2em; color: #111111; background: rgba(250, 250, 250, 0.9); backdrop-filter: blur(8px); padding: 8px 14px; border: 1px solid #eeeeee; transition: all 0.3s ease;">
  / / /
</div>

<div id="mobile-nav-overlay" class="md:hidden" style="position: fixed; inset: 0; width: 100vw; height: 100vh; background: rgba(250, 250, 250, 0.96); backdrop-filter: blur(16px); z-index: 99998; display: flex; flex-direction: column; align-items: center; justify-content: center; opacity: 0; pointer-events: none; transition: opacity 0.4s ease;">
  <a href="#" class="mobile-nav-link" data-target="MANIFESTO" style="font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 900; text-transform: uppercase; color: #111111; text-decoration: none; margin-bottom: 2rem; letter-spacing: -0.03em;">MANIFESTO</a>
  <a href="#" class="mobile-nav-link" data-target="IMWEAR" style="font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 900; text-transform: uppercase; color: #111111; text-decoration: none; margin-bottom: 2rem; letter-spacing: -0.03em;">IMWEAR</a>
  <a href="#" class="mobile-nav-link" data-target="CONTACTS" style="font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 900; text-transform: uppercase; color: #111111; text-decoration: none; margin-bottom: 3rem; letter-spacing: -0.03em;">CONTACTS</a>
  
  <a href="#" class="mobile-nav-link" data-target="SOUND" style="font-family: monospace; font-size: 10px; letter-spacing: 0.2em; color: #555555; text-decoration: none; border: 1px solid #cccccc; padding: 10px 20px;">SOUND : TOGGLE</a>
</div>

<script>
  document.addEventListener("DOMContentLoaded", () => {
    const burger = document.getElementById('mobile-burger');
    const overlay = document.getElementById('mobile-nav-overlay');
    let isOpen = false;

    if (burger && overlay) {
      burger.addEventListener('click', () => {
        isOpen = !isOpen;
        if (isOpen) {
          overlay.style.opacity = '1';
          overlay.style.pointerEvents = 'auto';
          burger.innerText = '[ X ]';
          burger.style.background = '#111111';
          burger.style.color = '#fafafa';
        } else {
          overlay.style.opacity = '0';
          overlay.style.pointerEvents = 'none';
          burger.innerText = '/ / /';
          burger.style.background = 'rgba(250, 250, 250, 0.9)';
          burger.style.color = '#111111';
        }
      });

      document.querySelectorAll('.mobile-nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
          e.preventDefault();
          const target = link.getAttribute('data-target');
          burger.click(); // Chiude il sipario

          const allLinks = document.querySelectorAll('a, button, span');
          allLinks.forEach(el => {
            if (el.innerText && el.innerText.toUpperCase().includes(target) && el !== link) {
              el.click();
            }
          });
        });
      });
    }
  });
</script>
'''

if 'IMLAND BRUTALIST MOBILE HAMBURGER' not in content:
    content = content.replace('</body>', burger_menu_html + '\n</body>')

# --- C. ELEVAZIONE IMMAGINE 3D SU MOBILE & PREVENZIONE CRASH VIDEO ---
master_responsive_css = '''
  /* RESPONSIVE ELEVATION & VIDEO MEMORY SHIELD */
  @media (max-width: 768px) {
    /* Nascondiamo il menu desktop laterale per attivare il panino /// */
    .vertical-nav, #axis-nav, [class*="nav-container"] {
      display: none !important;
    }

    /* Solleviamo il Canvas WebGL mantenendo il logo IMLAND in alto totalmente libero */
    canvas {
      transform: translateY(-18vh) scale(0.88) !important;
      transform-origin: center top !important;
      transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    /* Compatta la scheda informativa in basso */
    #image-info-panel, .info-panel {
      max-height: 35vh !important;
      bottom: 12px !important;
      left: 4vw !important;
      right: 4vw !important;
      width: 92vw !important;
      overflow-y: auto !important;
    }
  }

  /* VIDEO PREVENT BLACK BOX */
  video {
    object-fit: cover !important;
    background-color: #000000;
  }
</style>'''

idx_s = content.rfind('</style>')
if idx_s != -1:
    content = content[:idx_s] + master_responsive_css + content[idx_s+8:]

# --- D. SENTINELLA VIDEO ANTI-CRASH (AUTOPLAY SAFE) ---
video_safe_script = '''
<script>
  /* SAFE VIDEO DECODER FOR MOBILE CHROME */
  document.addEventListener("DOMContentLoaded", () => {
    const processVideos = () => {
      document.querySelectorAll('video').forEach(vid => {
        vid.muted = true;
        vid.defaultMuted = true;
        vid.setAttribute('playsinline', '');
        vid.setAttribute('webkit-playsinline', '');
        vid.setAttribute('preload', 'metadata');
        
        if (vid.paused) {
          let p = vid.play();
          if (p !== undefined) {
            p.catch(() => {
              // Fallback per blocchi browser severi
              vid.muted = true;
            });
          }
        }
      });
    };

    processVideos();
    // Osserva eventuali nuovi video caricati dinamicamente nei caroselli
    const obs = new MutationObserver(processVideos);
    obs.observe(document.body, { childList: true, subtree: true });
  });
</script>
'''

if 'SAFE VIDEO DECODER' not in content:
    content = content.replace('</body>', video_safe_script + '\n</body>')

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("🚀 MASTER ARCHITECT COMPLETATO: Loader, Burger ///, Viewport Shift e Video Shield installati.")
