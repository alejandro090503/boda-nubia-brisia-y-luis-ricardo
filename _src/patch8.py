# Parche 8: bruma viva (mesh) responsiva en todas las secciones + tintas lekshmy tricolor transparentes
import io, sys, re
P = r'C:/Users/aleja/boda-nubia-brisia-y-luis-ricardo/index.html'
s = io.open(P, encoding='utf-8').read()
def rep(o, n):
    global s
    c = s.count(o)
    if c != 1: sys.exit('ERR %d %r' % (c, o[:80]))
    s = s.replace(o, n)

LIGHT = {'hero', 'countdown', 'calendar', 'album', 'family', 'padrinos', 'weather', 'footer'}

# 1. tintas existentes -> tricolor según el tono de la sección
def sec_of(pos):
    m = None
    for mm in re.finditer(r'<(section|footer) id="([\w-]+)"', s[:pos]):
        m = mm
    return m.group(2) if m else ''
out, last = [], 0
for m in re.finditer(r"url\('ink/ink-(\w+)\.webp'\)", s):
    mode = 'light' if sec_of(m.start()) in LIGHT else 'dark'
    out.append(s[last:m.start()]); out.append("url('ink/tri-%s-%s.webp')" % (mode, m.group(1))); last = m.end()
out.append(s[last:]); s = ''.join(out)

# 2. tintas nuevas en secciones champán que no tenían
ADD = {'countdown': ('corner', 'flip'), 'calendar': ('top', ''), 'weather': ('oval', 'oval'),
       'padrinos': ('hero', 'soft flip'), 'footer': ('footer', 'soft')}
for sid, (nm, cls) in ADD.items():
    m = re.search(r'<(section|footer) id="%s"[^>]*>\n' % sid, s)
    if 'class="ink-bg' in s[m.end():m.end() + 400]: continue
    s = s[:m.end()] + '''  <div class="ink-bg %s" aria-hidden="true"><i style="background-image:url('ink/tri-light-%s.webp')"></i></div>\n''' % (cls, nm) + s[m.end():]
m = re.search(r'<section id="hero"[^>]*>\n', s)
s = s[:m.end()] + '''  <div class="ink-bg soft hz-ink" aria-hidden="true"><i style="background-image:url('ink/tri-light-hero.webp')"></i></div>\n''' + s[m.end():]

rep('.sec-light .ink-bg i{filter:grayscale(1) invert(1) sepia(.55) saturate(1.3) brightness(1.02);mix-blend-mode:multiply}\n.sec-light .ink-bg{opacity:.5}\n', '')

CSS = r'''
/* ═══ BRUMA VIVA + TINTAS TRICOLOR ═══ */
.ink-bg{background:none!important}
.ink-bg i{background-color:transparent!important}
.sec-light .ink-bg{opacity:.85}
.sec-light .ink-bg.soft{opacity:.6}
#hero .hz-ink{opacity:.42;z-index:-1!important}
.fx-mesh{position:absolute;inset:0;z-index:-3;overflow:hidden;pointer-events:none}
.fx-mesh .orb{position:absolute;border-radius:50%;
  width:calc(var(--k) * clamp(300px,118vw,760px));height:calc(var(--k) * clamp(300px,118vw,760px));
  left:var(--x);top:var(--y);transform-origin:center;translate:-50% -50%;
  background:radial-gradient(circle,var(--c) 0%,var(--c2) 34%,transparent 70%);
  animation:orbDrift var(--d) ease-in-out infinite alternate;animation-delay:var(--dl,0s);will-change:transform}
.fx-mesh .orb:nth-child(even){animation-name:orbDrift2}
@keyframes orbDrift{0%{transform:translate(0,0) scale(1)}50%{transform:translate(14%,-10%) scale(1.18)}100%{transform:translate(-12%,12%) scale(.9)}}
@keyframes orbDrift2{0%{transform:translate(0,0) scale(1.08)}50%{transform:translate(-14%,9%) scale(.9)}100%{transform:translate(10%,-13%) scale(1.16)}}
.fx-mesh::after{content:'';position:absolute;top:0;bottom:0;left:-70%;width:70%;
  background:linear-gradient(100deg,transparent,var(--silk) 50%,transparent);animation:meshSheen 15s ease-in-out infinite}
@keyframes meshSheen{0%{transform:translateX(0) skewX(-14deg)}100%{transform:translateX(260%) skewX(-14deg)}}
/* azul noche: oro, champán, azul acero y sombra profunda */
.fx-d{--silk:rgba(247,231,206,.07)}
.fx-d .orb:nth-child(1){--k:.95;--x:16%;--y:20%;--c:rgba(212,175,55,.34);--c2:rgba(212,175,55,.12);--d:15s}
.fx-d .orb:nth-child(2){--k:.85;--x:88%;--y:64%;--c:rgba(247,231,206,.22);--c2:rgba(247,231,206,.08);--d:19s;--dl:-5s}
.fx-d .orb:nth-child(3){--k:1;--x:70%;--y:12%;--c:rgba(74,123,183,.40);--c2:rgba(74,123,183,.14);--d:17s;--dl:-3s}
.fx-d .orb:nth-child(4){--k:.9;--x:22%;--y:88%;--c:rgba(3,7,20,.50);--c2:rgba(3,7,20,.18);--d:21s;--dl:-8s}
.fx-d.v2 .orb:nth-child(1){--x:84%;--y:26%}.fx-d.v2 .orb:nth-child(2){--x:14%;--y:60%}.fx-d.v2 .orb:nth-child(3){--x:30%;--y:8%}.fx-d.v2 .orb:nth-child(4){--x:80%;--y:92%}
/* champán: luz blanca, oro, azul polvo y sombra arena */
.fx-l{--silk:rgba(255,255,255,.35)}
.fx-l .orb:nth-child(1){--k:1;--x:20%;--y:18%;--c:rgba(255,251,240,.85);--c2:rgba(255,251,240,.3);--d:16s}
.fx-l .orb:nth-child(2){--k:.9;--x:86%;--y:42%;--c:rgba(212,175,55,.34);--c2:rgba(212,175,55,.12);--d:19s;--dl:-4s}
.fx-l .orb:nth-child(3){--k:.85;--x:12%;--y:78%;--c:rgba(74,123,183,.24);--c2:rgba(74,123,183,.08);--d:17s;--dl:-7s}
.fx-l .orb:nth-child(4){--k:.8;--x:78%;--y:94%;--c:rgba(168,129,28,.22);--c2:rgba(168,129,28,.08);--d:22s;--dl:-2s}
.fx-l.v2 .orb:nth-child(1){--x:80%;--y:14%}.fx-l.v2 .orb:nth-child(2){--x:16%;--y:46%}.fx-l.v2 .orb:nth-child(3){--x:88%;--y:76%}.fx-l.v2 .orb:nth-child(4){--x:24%;--y:96%}
@media(prefers-reduced-motion:reduce){.fx-mesh .orb,.fx-mesh::after{animation:none}}
'''
i = s.find('  </style>'); s = s[:i] + CSS + s[i:]

JS = r'''<script>
/* bruma viva: 4 esferas por sección, paleta según el tono; se pausa fuera de pantalla */
(function(){
  function go(){
    var secs = document.querySelectorAll('#main-content > section, #main-content > footer');
    var nd = 0, nl = 0;
    secs.forEach(function(sec){
      if (sec.querySelector(':scope > .fx-mesh')) return;
      var light = sec.classList.contains('sec-light');
      var k = light ? nl++ : nd++;
      var m = document.createElement('div');
      m.className = 'fx-mesh ' + (light ? 'fx-l' : 'fx-d') + (k % 2 ? ' v2' : '');
      m.setAttribute('aria-hidden', 'true');
      m.innerHTML = '<i class="orb"></i><i class="orb"></i><i class="orb"></i><i class="orb"></i>';
      sec.insertBefore(m, sec.firstChild);
    });
    if ('IntersectionObserver' in window){
      var io = new IntersectionObserver(function(es){ es.forEach(function(e){
        e.target.querySelectorAll('.orb').forEach(function(o){ o.style.animationPlayState = e.isIntersecting ? 'running' : 'paused'; });
      }); }, { rootMargin: '200px 0px' });
      document.querySelectorAll('.fx-mesh').forEach(function(m){ io.observe(m); });
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
})();
</script>
'''
i = s.rfind('</body>'); s = s[:i] + JS + s[i:]
io.open(P, 'w', encoding='utf-8', newline='\n').write(s); print('ok')
