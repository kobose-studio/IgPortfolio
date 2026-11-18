import re
import os

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# --- A. FIX HTML STATICO IMWEAR ---
# Sostituiamo brutalmente l'intero blocco HTML dei 3 prodotti con codice pulito, 
# forzando l'uso della classe .carousel-wrapper e i tag <img> esatti

imwear_html = '''
    <div class="grid grid-cols-1 md:grid-cols-3 gap-12 mt-12 w-full">
      
      <!-- COLONNA 1: CLASSIC HOODIE -->
      <article class="flex flex-col gap-4">
        <div class="carousel-wrapper relative w-full h-[220px] bg-neutral-100 overflow-hidden">
          <img src="/brand/hoodie-2.jpg" class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700" style="opacity:1;" />
          <img src="/brand/hoodie-3.jpg" class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700" style="opacity:0;" />
          <img src="/brand/hoodie-4.jpg" class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700" style="opacity:0;" />
          <img src="/brand/hoodie-5.jpg" class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700" style="opacity:0;" />
          <img src="/brand/hoodie-6.jpg" class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700" style="opacity:0;" />
          <img src="/brand/hoodie-7.jpg" class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700" style="opacity:0;" />
          <img src="/brand/hoodie-8.jpg" class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700" style="opacity:0;" />
          <img src="/brand/hoodie-9.jpg" class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700" style="opacity:0;" />
        </div>
        <header>
          <p class="text-[9px] uppercase tracking-widest text-[#d8a05c] mb-1 font-mono-tech">SIGNATURE COLLECTION</p>
          <p class="text-[9px] uppercase tracking-widest text-neutral-400 mb-4 font-mono-tech">UNISEX & KIDS // HEAVYWEIGHT</p>
          <h2 class="text-xl font-bold font-syne uppercase tracking-tight leading-none mb-1">IMLAND / CLASSIC HOODIE</h2>
          <p class="text-xs text-neutral-500 font-mono-tech mb-4">Cotone Organico Pesante // Vestibilità & Calore</p>
        </header>
        <p class="text-sm text-neutral-800 leading-relaxed font-inter">Il capo iconico dell'Atelier IMLAND. Una felpa ad alta grammatura, morbida, densa e calda, pensata per accompagnare il ritmo della montagna e la vita di tutti i giorni. Struttura resistente e massimo comfort.</p>
        <div class="mt-auto pt-6 text-right">
          <a href="mailto:info@imland.it?subject=Pre-Order Classic Hoodie" class="inline-block bg-black text-white text-[10px] uppercase font-mono-tech tracking-widest px-4 py-2 hover:bg-[#d8a05c] transition-colors">[ PRE-ORDER VIA EMAIL ]</a>
        </div>
      </article>

      <!-- COLONNA 2: FULL-ZIP HOODIE -->
      <article class="flex flex-col gap-4">
        <div class="carousel-wrapper relative w-full h-[220px] bg-neutral-100 overflow-hidden">
          <img src="/brand/hoodie_zip-1.jpg" class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700" style="opacity:1;" />
          <img src="/brand/hoodie_zip-2.jpg" class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700" style="opacity:0;" />
          <img src="/brand/hoodie_zip-3.jpg" class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700" style="opacity:0;" />
        </div>
        <header>
          <p class="text-[9px] uppercase tracking-widest text-[#d8a05c] mb-1 font-mono-tech">ALPINE EDITION</p>
          <p class="text-[9px] uppercase tracking-widest text-neutral-400 mb-4 font-mono-tech">UNISEX // DYNAMIC LAYER</p>
          <h2 class="text-xl font-bold font-syne uppercase tracking-tight leading-none mb-1">IMLAND / FULL-ZIP HOODIE</h2>
          <p class="text-xs text-neutral-500 font-mono-tech mb-4">Felpa con Zip // Comfort & Praticità</p>
        </header>
        <p class="text-sm text-neutral-800 leading-relaxed font-inter">Strato versatile con zip integrale a scorrimento rapido. Morbida, pratica e avvolgente, offre la giusta protezione termica durante le giornate all'aria aperta e nei cambi di temperatura.</p>
        <div class="mt-auto pt-6 text-right">
          <a href="mailto:info@imland.it?subject=Pre-Order Full-Zip Hoodie" class="inline-block bg-black text-white text-[10px] uppercase font-mono-tech tracking-widest px-4 py-2 hover:bg-[#d8a05c] transition-colors">[ PRE-ORDER VIA EMAIL ]</a>
        </div>
      </article>

      <!-- COLONNA 3: ESSENTIALS & GEAR -->
      <article class="flex flex-col gap-4">
        <div class="carousel-wrapper relative w-full h-[220px] bg-neutral-100 overflow-hidden">
          <img src="/brand/tee-1.jpg" class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700" style="opacity:1;" />
          <img src="/brand/tee-2.jpg" class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700" style="opacity:0;" />
          <img src="/brand/tee-3.jpg" class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700" style="opacity:0;" />
          <img src="/brand/tee-4.jpg" class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700" style="opacity:0;" />
          <img src="/brand/tee-5.jpg" class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700" style="opacity:0;" />
        </div>
        <header>
          <p class="text-[9px] uppercase tracking-widest text-[#d8a05c] mb-1 font-mono-tech">RAW COTTON & LIGHTWEAR</p>
          <p class="text-[9px] uppercase tracking-widest text-neutral-400 mb-4 font-mono-tech">APPAREL & ACCESSORIES</p>
          <h2 class="text-xl font-bold font-syne uppercase tracking-tight leading-none mb-1">IMLAND / ESSENTIALS & GEAR</h2>
          <p class="text-xs text-neutral-500 font-mono-tech mb-4">T-Shirt, Gerla Bag & Neck Warmer</p>
        </header>
        <p class="text-sm text-neutral-800 leading-relaxed font-inter">L'ecosistema essenziale IMLAND. La T-Shirt e la sacca 'Gerla Bag' sono realizzate in purissimo cotone organico al 100%. Il Neck Warmer è un copricollo leggerissimo e traspirante, progettato per riparare dal vento con la massima discrezione.</p>
        <div class="mt-auto pt-6 text-right">
          <a href="mailto:info@imland.it?subject=Pre-Order Essentials" class="inline-block bg-black text-white text-[10px] uppercase font-mono-tech tracking-widest px-4 py-2 hover:bg-[#d8a05c] transition-colors">[ PRE-ORDER VIA EMAIL ]</a>
        </div>
      </article>

    </div>
'''

# Cerchiamo il blocco grid delle tre colonne e lo sostituiamo
grid_regex = r'<div class="grid grid-cols-1 md:grid-cols-3 gap-12 mt-12 w-full">[\s\S]*?(?=</div>\s*</div>\s*</div>\s*<!-- \/ BRAND MODAL)'
if re.search(grid_regex, content):
    content = re.sub(grid_regex, imwear_html, content, count=1)
else:
    print("ATTENZIONE: Griglia IMWEAR non trovata con la regex principale. Tentativo alternativo.")
    # Fallback: cerca dal primo articolo IMWEAR fino alla fine dei 3 articoli
    alt_regex = r'<div class="grid grid-cols-1 md:grid-cols-3 gap-12 mt-12 w-full">[\s\S]*?</article>\s*</article>\s*</article>\s*</div>'
    if re.search(alt_regex, content):
        content = re.sub(alt_regex, imwear_html, content, count=1)

# --- B. FIX PLAYER VIDEO ---
# Assicuriamoci che il tag <video> iniettti correttamente data.media_url invece di restare vuoto.
video_fix_regex = r'(if\s*\(data\.media_type\s*===\s*[\'"]VIDEO[\'"]\)\s*\{[\s\S]*?video\.src\s*=)[\s\S]*?;'
if re.search(video_fix_regex, content):
    content = re.sub(video_fix_regex, r'\1 data.media_url;', content)

# Aggiungiamo attributi essenziali per i video su Safari/iOS (playsinline, muted, etc)
video_attr_regex = r'(video\.autoplay\s*=\s*true;\s*video\.loop\s*=\s*true;\s*video\.controls\s*=\s*true;\s*video\.playsInline\s*=\s*true;)'
content = re.sub(video_attr_regex, r'\1 video.muted = true; video.setAttribute("playsinline", "");', content)

# --- C. SCRIPT ROTAZIONE CAROSELLO RINNOVATO ---
# Il vecchio script 'imland-imwear-exact-lock' è rotto, lo sostituiamo con uno semplice basato sulla classe .carousel-wrapper
content = re.sub(r'<script id="imland-imwear-exact-lock"[\s\S]*?</script>', '', content)

new_carousel_script = '''
<script id="imland-simple-carousel" is:inline>
(function() {
  if (window.__IMLAND_CAROUSEL_INIT) return;
  window.__IMLAND_CAROUSEL_INIT = true;

  function rotateCarousels() {
    const wrappers = document.querySelectorAll('.carousel-wrapper');
    wrappers.forEach(wrapper => {
      const imgs = wrapper.querySelectorAll('img');
      if (imgs.length <= 1) return;
      
      // Trova l'immagine attualmente visibile (opacity = 1)
      let activeIdx = -1;
      imgs.forEach((img, idx) => {
        if (img.style.opacity === '1' || img.style.opacity === 1) {
          activeIdx = idx;
        }
      });
      
      if (activeIdx === -1) activeIdx = 0;
      
      // Calcola la prossima immagine
      const nextIdx = (activeIdx + 1) % imgs.length;
      
      // Applica la transizione
      imgs[activeIdx].style.opacity = '0';
      imgs[nextIdx].style.opacity = '1';
    });
  }

  // Ruota ogni 3 secondi
  setInterval(rotateCarousels, 3000);
})();
</script>
'''
content += "\n" + new_carousel_script

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("FIX DEFINITIVO HTML IMWEAR E VIDEO PLAYER COMPLETATO.")
