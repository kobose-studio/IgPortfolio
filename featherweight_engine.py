import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

engine_script = '''<script is:inline>
(function() {
  if (window.__IMLAND_FEATHERWEIGHT_ACTIVE) return;
  window.__IMLAND_FEATHERWEIGHT_ACTIVE = true;

  const isMobile = window.innerWidth <= 768 || /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

  // 1. PIXEL RATIO SHIELD: Taglia il carico GPU fino al 70% su monitor 4K/Retina e Mobile
  const maxDPR = isMobile ? 1.0 : 1.25;
  const nativeDPR = window.devicePixelRatio || 1;
  try {
    Object.defineProperty(window, 'devicePixelRatio', {
      get: function() { return Math.min(nativeDPR, maxDPR); }
    });
  } catch (e) {}

  // 2. ASYNC IMAGE CONCURRENCY QUEUE: Evita il congelamento CPU sui 445 nodi
  const MAX_CONCURRENT = isMobile ? 4 : 8;
  let activeLoads = 0;
  const loadQueue = [];
  const rawSrcDescriptor = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, 'src');

  function pumpQueue() {
    while (activeLoads < MAX_CONCURRENT && loadQueue.length > 0) {
      const task = loadQueue.shift();
      activeLoads++;
      let released = false;

      const release = () => {
        if (released) return;
        released = true;
        activeLoads = Math.max(0, activeLoads - 1);
        setTimeout(pumpQueue, 8);
      };

      task.img.addEventListener('load', release, { once: true });
      task.img.addEventListener('error', release, { once: true });
      setTimeout(release, 4500);

      rawSrcDescriptor.set.call(task.img, task.url);
    }
  }

  if (rawSrcDescriptor && rawSrcDescriptor.set) {
    Object.defineProperty(HTMLImageElement.prototype, 'src', {
      get: rawSrcDescriptor.get,
      set: function(url) {
        this.decoding = 'async';
        if (!url || typeof url !== 'string' || url.startsWith('data:') || url.startsWith('blob:')) {
          rawSrcDescriptor.set.call(this, url);
          return;
        }
        loadQueue.push({ img: this, url: url });
        setTimeout(pumpQueue, 0);
      },
      configurable: true
    });
  }

  // 3. GPU HIBERNATION & THERMAL FRAME PACING
  const nativeRAF = window.requestAnimationFrame.bind(window);
  let lastFrameTime = 0;
  const targetInterval = isMobile ? 33 : 16; // 30 FPS su Mobile, 60 FPS su Desktop

  window.requestAnimationFrame = function(callback) {
    return nativeRAF(function(timestamp) {
      if (document.hidden) {
        setTimeout(() => nativeRAF(callback), 500);
        return;
      }

      const modalOpen = document.querySelector('#brand-modal[style*="block"], #brand-modal[style*="flex"], .brand-panel-content:not(.hidden)');
      const minDelta = modalOpen ? 250 : targetInterval;

      if (timestamp - lastFrameTime < minDelta) {
        nativeRAF(callback);
        return;
      }

      lastFrameTime = timestamp;
      callback(timestamp);
    });
  };
})();
</script>
'''

content = re.sub(r'<script is:inline>\s*\(function\(\)\s*\{\s*if\s*\(window\.__IMLAND_FEATHERWEIGHT_ACTIVE[\s\S]*?</script>', '', content)

if '---' in content:
    parts = content.split('---', 2)
    if len(parts) == 3:
        content = '---' + parts[1] + '---\n' + engine_script + parts[2]
    else:
        content = engine_script + '\n' + content
else:
    content = engine_script + '\n' + content

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("FEATHERWEIGHT ENGINE INIETTATO CON SUCCESSO.")
