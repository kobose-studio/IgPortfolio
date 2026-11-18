# IMLAND MATRIX — MASTER BLUEPRINT v1.1 [DEMO RELEASE CANDIDATE]

## 1. L'Architettura (Lo Stack)
* **Frontend & SSG**: Astro + Vite Rollup (compilazione statica verificata < 1.2s).
* **3D Engine & Shaders**: Three.js + Custom GLSL Liquid Distortion Shaders con riflessione inerziale al puntatore.
* **Procedural WebGL Darkroom Plates**: Generatore dinamico `THREE.CanvasTexture` (720x900, fondo ossidiana, cornice `#C89E5A`) per i Reel e le slide video privi di cover statica locale, eliminando ogni nodo fantasma.
* **Data & Assets Pipeline**: Cache Instagram locale (`src/portfolio_cache.json` + `/archive_media/`) e Lookbook IMWEAR (`/brand/`).
* **Mobile Performance Shield**: Capping automatico a **45 nodi** e `devicePixelRatio: 1.0x` su schermi mobili (`<= 768px` / iOS WebKit / Android) per zero crash di memoria.

## 2. Architettura Funzionale Consolidata (Demo v1.1)
* **Spazio 3D & Focus Mode**: Galassia orbitante con isolamento centrale dell'opera, background ghosting e controllo carosello `[ PREV SLIDE ] / [ NEXT SLIDE ]` isolato dagli eventi canvas.
* **Assi Tipografici Perimetrali**:
  * **Header / Sinistra**: Navigazione sezioni (`MANIFESTO`, `IMWEAR`, `CONTACTS`).
  * **Destra**: Colophon istituzionale fisso `ARCHIVE 2026 // © IMLAND.IT`.
* **Schede Modali Centrate**:
  * **MANIFESTO**: Testo definitivo a 3 movimenti poetici uniformati nella grana tipografica.
  * **IMWEAR (8-3-5)**: Classic Hoodie (`hoodie-2..9`), Full-Zip Hoodie (`hoodie_zip-1..3`), Essentials & Gear (`tee-1..5`).
  * **CONTACTS**: Canali diretti Atelier Alagna Valsesia.

## 3. Roadmap verso Production v1.2
* **Audio Ambientale**: Rifinitura micro-interazioni sonore (`SOUND: ON/OFF`).
* **Custom Domain**: Collegamento DNS definitivo `imland.it` su Vercel Edge.
