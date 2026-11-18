import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    s = f.read()

# 1. Rimuove il vecchio wrapper freccia corrotto
pfx = '((t) => { if (typeof window !== "undefined" && window.innerWidth <= 768) {'
while pfx in s:
    start = s.index(pfx)
    open_p = s.index('})(', start) + 2
    pos, depth, quote = open_p + 1, 1, None
    while pos < len(s) and depth > 0:
        ch = s[pos]
        if quote:
            if ch == '\\': pos += 2; continue
            if ch == quote: quote = None
        else:
            if ch in ('"', "'", '`'): quote = ch
            elif ch == '(': depth += 1
            elif ch == ')': depth -= 1
        pos += 1
    if depth == 0:
        s = s[:start] + s[open_p + 1 : pos - 1] + s[pos:]
    else:
        break

s = re.sub(r'(\b(?:textureLoader|TextureLoader\(\))\.load\([^;]*?\([^()]*\))\)\s*=>', r'\1 =>', s)

# 2. Bilanciatore contestuale a pila: richiude TUTTE le '(' aperte nello stesso blocco prima di ';'
def balance_all_unclosed_parens(astro_src):
    m = re.search(r'(<script(?![^>]*is:inline)[^>]*>)([\s\S]*?)(</script>)', astro_src)
    if not m:
        return astro_src
    code = m.group(2)
    out = []
    i, n = 0, len(code)
    b_d = 0
    paren_stack = []
    q, lc, bc, rx = None, False, False, False
    prev_sig = '\n'

    while i < n:
        ch = code[i]
        nxt = code[i + 1] if i + 1 < n else ''

        if lc:
            out.append(ch)
            if ch == '\n': lc = False
            i += 1; continue
        if bc:
            out.append(ch)
            if ch == '*' and nxt == '/':
                out.append(nxt); bc = False; i += 2; continue
            i += 1; continue
        if q:
            out.append(ch)
            if ch == '\\' and i + 1 < n:
                out.append(nxt); i += 2; continue
            if ch == q:
                q = None; prev_sig = ')'
            i += 1; continue
        if rx:
            out.append(ch)
            if ch == '\\' and i + 1 < n:
                out.append(nxt); i += 2; continue
            if ch == '/':
                rx = False; prev_sig = ')'
            i += 1; continue

        if ch == '/' and nxt == '/':
            out.append('//'); lc = True; i += 2; continue
        if ch == '/' and nxt == '*':
            out.append('/*'); bc = True; i += 2; continue
        if ch == '/' and prev_sig in ('(', ',', '=', ':', '[', '!', '&', '|', '?', '{', ';', '\n'):
            out.append(ch); rx = True; i += 1; continue
        if ch in ('"', "'", '`'):
            out.append(ch); q = ch; i += 1; continue

        if ch == '{':
            b_d += 1
            prev_sig = ch
            out.append(ch)
        elif ch == '}':
            b_d = max(0, b_d - 1)
            prev_sig = ch
            out.append(ch)
        elif ch == '(':
            is_for = bool(re.search(r'\bfor\s*$', ''.join(out[-12:])))
            paren_stack.append((b_d, is_for))
            prev_sig = ch
            out.append(ch)
        elif ch == ')':
            if paren_stack:
                paren_stack.pop()
            prev_sig = ch
            out.append(ch)
        elif ch == ';':
            closed_count = 0
            while paren_stack and paren_stack[-1][0] == b_d and not paren_stack[-1][1]:
                paren_stack.pop()
                closed_count += 1
            out.append(')' * closed_count + ';')
            prev_sig = ';'
        else:
            if not ch.isspace():
                prev_sig = ch
            out.append(ch)
        i += 1

    return astro_src[:m.start(2)] + ''.join(out) + astro_src[m.end(2):]

s = balance_all_unclosed_parens(s)

# 3. Pulisce vecchi patch
s = re.sub(r'<(?:script|style) id="imland-[^"]*"[\s\S]*?</(?:script|style)>', '', s)

# 4. Scudo anti-crash iOS/Android (45 nodi + DPR 1x su mobile)
s = re.sub(
    r'renderer\.setPixelRatio\([^;]+\);',
    'renderer.setPixelRatio(window.innerWidth <= 768 ? 1 : Math.min(window.devicePixelRatio, 1.5));',
    s
)
s = re.sub(r'antialias:\s*true', 'antialias: window.innerWidth > 768', s)
s = re.sub(
    r'(const\s+(?:mediaItems|allMedia|items|posts)\s*=\s*)([^;\n]+);',
    r'\1(window.innerWidth <= 768 ? (\2).slice(0, 45) : (\2));',
    s,
    count=1
)

# 5. Aggiornamento Manifesto
new_manifesto = (
    "IMLAND nasce sotto l'ombra imponente della parete est del Monte Rosa. "
    "Non creiamo capi per il consumo di massa, né per la moda da passerella cittadina.</p>\n"
    '<p style="margin-top:1.1rem;max-width:680px;line-height:1.65;">'
    "Progettiamo <strong>outfit outdoor ad alte prestazioni</strong> per chi vive la montagna con "
    "rispetto, silenzio e radici profonde. In un mondo saturo di rumore digitale, Alagna e le sue "
    "valli da scoprire rimangono la nostra unica bussola esistenziale.</p>\n"
    '<p style="margin-top:1.1rem;max-width:680px;line-height:1.65;">'
    "Affiancando al rigore dell'equipaggiamento alpino la <strong>fotografia</strong> come strumento "
    "di ascolto lento, ogni immagine che ruota nel vortice smette di essere un semplice post e si "
    "trasforma in un indizio silenzioso nascosto tra le pieghe della valle.</p>"
)

s = re.sub(
    r'IMLAND(?:\s+MONTEROSA)?\s+nasce\s+sotto[\s\S]*?bussola\s+esistenziale\.\s*</p>',
    lambda _: new_manifesto,
    s,
    count=1,
    flags=re.I
)

# 6. Bonifica immagini IMWEAR & Video Stage
s = s.replace('/brand/hoodie-1.jpg', '/brand/hoodie-2.jpg')
s = s.replace('/brand/hoodie-A.jpg', '/brand/hoodie-2.jpg')
s = s.replace('/brand/zip-hoodie.jpg', '/brand/hoodie_zip-1.jpg')

new_video = '''if (data.media_type === 'VIDEO') {
  videoStage.style.cssText = 'display:flex;align-items:center;justify-content:center;' +
    'width:min(88vw,440px);min-height:280px;max-height:62vh;margin:0 auto;pointer-events:auto;';
  const v = document.createElement('video');
  v.src = data.media_url;
  v.poster = data.thumbnail_url || '';
  v.autoplay = true; v.loop = true; v.muted = true; v.controls = true; v.playsInline = true;
  v.setAttribute('playsinline', '');
  v.style.cssText = 'width:100%;height:auto;max-height:62vh;object-fit:contain;' +
    'border-radius:4px;background:#0b0b0b;pointer-events:auto;';
  v.onerror = () => {
    if (!data.thumbnail_url) return;
    videoStage.innerHTML = '<a href="' + (data.permalink || '#') + '" target="_blank" ' +
      'style="display:block;width:100%;text-align:center;text-decoration:none;">' +
      '<img src="' + data.thumbnail_url + '" style="max-height:56vh;margin:0 auto;border-radius:4px;"/>' +
      '<div style="margin-top:8px;font-family:monospace;font-size:10px;background:#111;' +
      'color:#fff;padding:6px 12px;display:inline-block;">[ GUARDA VIDEO SU INSTAGRAM ]</div></a>';
  };
  videoStage.appendChild(v);
}'''

s = re.sub(
    r'if\s*\(\s*data\.media_type\s*===\s*[\'"]VIDEO[\'"]\s*\)\s*\{[\s\S]*?videoStage\.appendChild\(video\);\s*\}',
    lambda _: new_video,
    s,
    count=1
)

# 7. CSS & Controller V14
ui_patch = '''
<style id="imland-v14-css" is:global>
  #brand-modal, #contacts-modal, #manifesto-modal {
    position: fixed !important;
    inset: 0 !important;
    width: 100vw !important;
    height: 100dvh !important;
    margin: 0 !important;
    padding: 16px !important;
    transform: none !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
  }
  .brand-panel-content, .contacts-panel-content, .manifesto-panel-content {
    position: relative !important;
    inset: auto !important;
    transform: none !important;
    margin: 0 auto !important;
    width: min(92vw, 880px) !important;
    max-width: min(92vw, 880px) !important;
    max-height: 85dvh !important;
    padding: 36px !important;
    overflow-y: auto !important;
    background: #ffffff !important;
    border: none !important;
    box-shadow: 0 24px 60px rgba(0,0,0,0.06) !important;
    box-sizing: border-box !important;
  }
  @media (max-width: 768px) {
    .brand-panel-content, .contacts-panel-content, .manifesto-panel-content {
      width: 94vw !important;
      padding: 24px !important;
    }
    .brand-panel-content .grid, #brand-modal .grid {
      display: grid !important;
      grid-template-columns: 1fr !important;
      gap: 24px !important;
    }
  }
</style>
<script id="imland-v14-js" is:inline>
(function() {
  if (window.__V14) return;
  window.__V14 = 1;
  const isMob = window.innerWidth <= 768;
  const CAT = {
    c1: [
      '/brand/hoodie-2.jpg', '/brand/hoodie-3.jpg', '/brand/hoodie-4.jpg', '/brand/hoodie-5.jpg',
      '/brand/hoodie-6.jpg', '/brand/hoodie-7.jpg', '/brand/hoodie-8.jpg', '/brand/hoodie-9.jpg'
    ],
    c2: ['/brand/hoodie_zip-1.jpg', '/brand/hoodie_zip-2.jpg', '/brand/hoodie_zip-3.jpg'],
    c3: ['/brand/tee-1.jpg', '/brand/tee-2.jpg', '/brand/tee-3.jpg', '/brand/tee-4.jpg', '/brand/tee-5.jpg']
  };
  const idx = { c1: 0, c2: 0, c3: 0 };

  function syncUI(adv) {
    const m = document.getElementById('brand-modal') || document.body;
    const t = { c1: null, c2: null, c3: null };
    m.querySelectorAll('article, div, section').forEach((el) => {
      if (!el.querySelector('img')) return;
      const u = (el.textContent || '').toUpperCase();
      const a = u.includes('CLASSIC HOODIE');
      const b = u.includes('FULL-ZIP');
      const c = u.includes('ESSENTIALS');
      if (a && !b && !c) t.c1 = el;
      if (b && !a && !c) t.c2 = el;
      if (c && !a && !b) t.c3 = el;
    });
    ['c1', 'c2', 'c3'].forEach((k) => {
      if (!t[k]) return;
      if (adv) idx[k] = (idx[k] + 1) % CAT[k].length;
      const imgs = Array.from(t[k].querySelectorAll('img'));
      if (!imgs.length) return;
      for (let i = 1; i < imgs.length; i++) imgs[i].remove();
      if (imgs[0].getAttribute('src') !== CAT[k][idx[k]]) {
        imgs[0].setAttribute('src', CAT[k][idx[k]]);
      }
      imgs[0].style.cssText = 'opacity:1!important;position:relative!important;' +
        'width:100%!important;height:100%!important;object-fit:cover!important;display:block!important;';
    });
    ['#brand-modal', '#contacts-modal', '#manifesto-modal'].forEach((q) => {
      const o = document.querySelector(q);
      if (o && getComputedStyle(o).display !== 'none') {
        o.style.display = 'flex';
        o.style.alignItems = 'center';
        o.style.justifyContent = 'center';
      }
    });
    if (isMob) {
      let l = null, r = null;
      document.querySelectorAll('nav, aside, header, div').forEach((el) => {
        const tx = (el.textContent || '').trim();
        if (!l && tx.includes('MANIFESTO') && tx.includes('IMWEAR') && tx.length < 140) l = el;
        if (!r && tx.includes('ARCHIVE 2026') && tx.length < 140) r = el;
      });
      if (l) {
        let b = l;
        while (b.parentElement && b.parentElement !== document.body &&
               ['fixed', 'absolute'].includes(getComputedStyle(b.parentElement).position)) {
          b = b.parentElement;
        }
        let g = 10;
        if (r) {
          const d = window.innerWidth - r.getBoundingClientRect().right;
          if (d >= 4 && d <= 28) g = Math.round(d);
        }
        [b, l].forEach((n) => {
          n.style.background = 'transparent';
          n.style.backdropFilter = 'none';
          n.style.webkitBackdropFilter = 'none';
          n.style.boxShadow = 'none';
          n.style.border = 'none';
          n.style.padding = '0';
        });
        b.style.position = 'fixed';
        b.style.top = '50%';
        b.style.left = g + 'px';
        b.style.right = 'auto';
        b.style.writingMode = 'vertical-rl';
        b.style.transform = 'translateY(-50%) rotate(180deg)';
        b.style.zIndex = '45';
      }
    }
  }

  window.addEventListener('DOMContentLoaded', () => syncUI(false));
  document.addEventListener('click', () => setTimeout(() => syncUI(false), 30));
  setInterval(() => syncUI(true), 2800);
})();
</script>
'''

s += '\n' + ui_patch
with open(target, 'w', encoding='utf-8') as f:
    f.write(s)
print('OK_V14_READY')
