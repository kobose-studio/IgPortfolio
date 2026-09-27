# 📜 IMLAND® MATRIX — MASTER BLUEPRINT v1.5

## 🏛️ 1. L'Architettura Globale (Lo Stack)
* **Core Framework**: Astro.js (SSG per massima velocità e SEO).
* **3D Engine**: Three.js + WebGL nativo.
* **Alchemical VFX**: Custom GLSL Shaders (Vertex & Fragment).
* **Data Pipeline**: Node.js Script (Instagram Graph API con paginazione ricorsiva).
* **Identity & Aesthetics**: Fashion Brutalism / Swiss Typography.
  * **Palette**: Mineral White (`#f2f2f0`), Onyx Black (`#0d0d0d`), Laser Emerald (`#00e676`).
  * **Typeface**: Syne Extra Bold (Display), Space Mono (HUD/Tech), Inter (Copy).

---

## 🟢 2. Fasi Completate & Collaudate

### Fase 1: Data Engine & Cache Pipeline
* **Paginazione Ricorsiva**: Script `update_cache.js` che supera il limite di 25 media di Meta e scarica fino a 200 nodi unici.
* **Filtro Anti-Materia (Video Bypass)**: Gestione condizionale dei file `.mp4`. Estrazione automatica del `thumbnail_url` per evitare piani neri in GPU.
* **State Generation**: Caching in `src/portfolio_cache.json`.

### Fase 2 & 3: WebGL Core & Liquid Shaders
* **Matrice Infinito-Inerziale**: Loop di posizionamento continuo (*Wrap-Around Modulo*).
* **Velocity Bending**: Inclinazione dinamica $3D$ della griglia in base alla velocità di scroll (`uVelocity`).
* **Liquid Distortion**: Shader GLSL per la rifrazione fluida durante la navigazione.

### Fase 4: Precision Interaction & Raycasting
* **World Matrix Sync**: Raycaster sincronizzato sulle matrici assolute (`updateMatrixWorld`) con calcolo dei limiti del canvas (`getBoundingClientRect`).
* **Inquadratura Camera Centrata**: Regia della lente al centro esatto dell'opera selezionata ($Z = 4.0$).

### Fase 5: Editorial UX & The Alchemist's Polish
* **Corner-Anchored Plaque**: Scheda editoriale ancorata in basso a destra (`bottom: 36px; right: 36px;`), isolata tramite Scoped CSS. Rimosso ogni residuo grafico in stato di navigazione (*Zero Stale UI*).
* **Ghosting Background**: Velo opaco al 4% (`uOpacity = 0.04`) sulle tessere non selezionate.
* **Cyberpunk Laser Brackets**: Mirino a 4 parentesi d'angolo `#00e676` svincolato dal *Frustum Culling* (`frustumCulled = false`) per funzionare su tutte le colonne.
* **Radial 3D Anaglyph Fringing**: Shader con maschera radiale. Il centro della foto isolata è nitido al 100%, mentre i bordi sfumano in un'aberrazione cromatica stereo-3D (Rosso/Ciano).

---

## 🔮 3. Prossime Mappe Tattiche
* **Fase 6**: Mobile Optimization & Touch Physics (Ricalibrazione colonna 2xN/3xN per smartphone).
* **Fase 7**: Micro-interazioni, Media Playback per i Video Fullscreen & Loading States.
* **Fase 8**: Build di produzione e Deployment (Vercel / Netlify).
