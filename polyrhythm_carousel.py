import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# Trova il blocco del carosello e sostituiscilo con la nuova logica matematica sfalsata
new_react_carousel = '''{prod.images ? (
  <div class="carousel-wrapper">
    {prod.images.map((img, i) => {
      /* 
       * LA MATEMATICA DEL CAOS ORGANICO:
       * Invece di 6 secondi fissi, creiamo un moltiplicatore basato sull'id della colonna.
       * Colonna 1 (7 img) = ~5.5s per foto
       * Colonna 2 (5 img) = ~6.8s per foto 
       * Colonna 3 (4 img) = ~6.1s per foto
       */
      const baseTime = 5.5 + (prod.title.length % 3) * 0.65;
      const totalDur = prod.images.length * baseTime;
      
      /* Calcoliamo il delay negativo per partire senza frame grigi */
      let dly = (i * baseTime) + ((prod.title.length % 5) * 1.5);
      while (dly > 0) dly -= totalDur;
      
      return <img src={img} alt={prod.title} class={`product-img kburns-${prod.images.length}`} style={`animation-duration: ${totalDur}s; animation-delay: ${dly}s;`} />;
    })}
  </div>
) : ('''

# Sostituzione mirata
content = re.sub(r'\{prod\.images \? \(\s*<div class="carousel-wrapper">.*?</div>\s*\)\s*:\s*\(', new_react_carousel, content, flags=re.DOTALL)

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("🎵 POLIRITMIA INIETTATA: Caroselli asincroni attivati con successo.")
