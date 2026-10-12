import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# --- 1. FIX TYPO EMAIL (Sostituzione Globale) ---
content = content.replace('imlandmoterosa', 'imlandmonterosa')
content = content.replace('IMLANDMOTEROSA', 'IMLANDMONTEROSA')

# --- 2. FIX ELEVAZIONE MOBILE (La Spinta Gravitazionale) ---
mobile_y_offset_css = '''
  /* Y-OFFSET SHIELD FOR MOBILE IMAGES */
  @media (max-width: 768px) {
    canvas {
      transform: translateY(-22vh) !important;
      transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
  }
</style>'''

if 'Y-OFFSET SHIELD' not in content:
    content = content.replace('</style>', mobile_y_offset_css)

# --- 3. FIX VIDEO NERI (La Sentinella Asincrona) ---
video_sentinel_js = '''
<script>
  /* KINETIC VIDEO SENTINEL */
  // Questo algoritmo monitora il DOM. Quando un video appare (nei post o nei caroselli), lo forza al play.
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.tagName === 'VIDEO') {
          node.muted = true;
          node.setAttribute('playsinline', '');
          node.setAttribute('autoplay', '');
          node.setAttribute('loop', '');
          node.play().catch(e => console.log("Autoplay bypass intervenuto"));
        } else if (node.querySelectorAll) {
          node.querySelectorAll('video').forEach(vid => {
            vid.muted = true;
            vid.setAttribute('playsinline', '');
            vid.setAttribute('autoplay', '');
            vid.setAttribute('loop', '');
            vid.play().catch(e => console.log("Autoplay bypass intervenuto"));
          });
        }
      });
    });
  });
  observer.observe(document.body, { childList: true, subtree: true });

  // Fallback per video già presenti al caricamento
  window.addEventListener("DOMContentLoaded", () => {
     document.querySelectorAll('video').forEach(vid => {
        vid.muted = true;
        vid.setAttribute('playsinline', '');
        vid.setAttribute('autoplay', '');
        vid.setAttribute('loop', '');
        vid.play();
     });
  });
</script>
'''
if 'KINETIC VIDEO SENTINEL' not in content:
    content = content.replace('</body>', video_sentinel_js + '\n</body>')

# --- 4. FIX SIPARIO (The Absolute Loader) ---
loader_html = '''
<!-- THE ABSOLUTE KINETIC LOADER -->
<div id="imland-absolute-loader" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 999999; background-color: #fafafa; display: flex; flex-direction: column; align-items: center; justify-content: center; transition: opacity 1.2s ease-in-out; pointer-events: none; opacity: 1;">
  <div style="text-align: center; padding: 0 24px;">
    <h1 style="font-family: 'Syne', sans-serif; font-size: 15px; font-weight: 900; letter-spacing: 0.25em; text-transform: uppercase; color: #111111; margin-bottom: 24px; animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;">
      Loading Archive...
    </h1>
    <p style="font-family: monospace; font-size: 10px; letter-spacing: 0.15em; color: #b3a082; text-transform: uppercase; max-width: 320px; margin: 0 auto; line-height: 1.8;">
      For the deepest visual journey,<br><br>the Desktop experience is highly recommended.
    </p>
  </div>
</div>
<style>
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
</style>
<script>
  window.addEventListener('load', () => {
    // Il sipario rimane per 1.5 secondi per dare tempo al 3D di stabilizzarsi
    setTimeout(() => {
      const loader = document.getElementById('imland-absolute-loader');
      if(loader) {
        loader.style.opacity = '0';
        setTimeout(() => loader.remove(), 1200);
      }
    }, 1500);
  });
</script>
'''

if 'THE ABSOLUTE KINETIC LOADER' not in content:
    # Iniettiamo in modo insopprimibile subito dopo l'apertura del body
    content = re.sub(r'(<body[^>]*>)', r'\1\n' + loader_html, content, count=1)

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("🎯 CALIBRAZIONE FINALE COMPLETATA. Bug eradicati.")
