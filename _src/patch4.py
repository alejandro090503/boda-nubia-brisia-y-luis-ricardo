# Parche 4: hero (novios visibles), itinerario completo "Por confirmar" + línea nueva,
# color sugerido en una sola bolita con fundido, quitar hospedaje
import io, sys, json, re
P = r'C:/Users/aleja/boda-nubia-brisia-y-luis-ricardo/index.html'
B = r'C:/Users/aleja/AppData/Local/Temp/claude/C--Users-aleja/61662fee-e927-4bfd-bf71-b8b93a534439/scratchpad/blocks/'
s = io.open(P, encoding='utf-8').read()
def rep(o, n):
    global s
    c = s.count(o)
    if c != 1: sys.exit('ERR %d %r' % (c, o[:80]))
    s = s.replace(o, n)

# ── 1. QUITAR HOSPEDAJE ──
a = s.find('<!-- 9b. HOSPEDAJE -->')
k = s.find("var root=document.getElementById('hospedaje');", a)
b = s.find('</script>', k) + len('</script>')
assert a > 0 and k > a and b > k
s = s[:a] + s[b:]
rep('    <li><a href="#hospedaje">Hospedaje</a></li>\n', '')

# ── 2. ITINERARIO ──
N = json.load(io.open(B + 'neidy_rows.json', encoding='utf-8'))
ico = {r[0]: r[2].replace('#1a1a1a', 'currentColor') for r in N}
a = s.find('<div class="timeline" id="tlWrap">'); b = s.find('<p class="tl-note">', a)
blk = s[a:b]
mine = blk.split('<div class="tl-row"')[1:]
real = {}
for p in mine:
    ev = re.search(r'tl-ev">([^<]*)', p).group(1)
    real[ev] = re.search(r'<div class="tl-ico" aria-hidden="true">(.*?)</div>\s*<p class="tl-t">', p, re.S).group(1)
PC = 'Por confirmar'
items = [
 ('11:00 AM', 'Ceremonia Religiosa', 'Templo de la Ciudad de México', real['Ceremonia Religiosa']),
 (PC, 'Sesión de Fotos', 'Los recuerdos de nuestro gran día', ico['Sesión de Fotos']),
 ('4:00 PM', 'Recepción', "Salón Jardín D'Alan", real['Recepción']),
 (PC, 'Cóctel de Bienvenida', 'Brindemos por el inicio', ico['Cocktail de Bienvenida']),
 (PC, 'Entrada de los Novios', 'Que empiece la celebración', ico['Entrada de los Novios']),
 (PC, 'Brindis', 'Por el amor y la familia', ico['Brindis']),
 (PC, 'Cena', 'La mesa nos reúne', ico['Cena']),
 (PC, 'Primer Baile', 'Nuestro primer baile como esposos', ico['Baile de los Novios']),
 (PC, 'Fiesta', '¡A celebrar juntos!', ico['Tornafiesta']),
]
rows = ''
for i, (t, ev, de, ic) in enumerate(items):
    side = 'left' if i % 2 == 0 else 'right'
    tcls = 'tl-t tl-t--pc' if t == PC else 'tl-t'
    rows += '''    <div class="tl-row" data-side="%s">
      <div class="tl-orn"></div><div class="tl-pulse"></div><div class="tl-dot"></div>
      <div class="tl-row-inner">
        <div class="tl-ico" aria-hidden="true">%s</div>
        <p class="%s">%s</p><p class="tl-ev">%s</p><p class="tl-de">%s</p>
      </div>
    </div>
''' % (side, ic.strip(), tcls, t, ev, de)
new = '''<div class="timeline" id="tlWrap">
    <svg class="tl-svg" id="tlSvg" preserveAspectRatio="none" aria-hidden="true">
      <defs>
        <linearGradient id="tlFoil" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#9C7A1E"/><stop offset=".12" stop-color="#F1DC8A"/><stop offset=".24" stop-color="#D4AF37"/>
          <stop offset=".38" stop-color="#FFF4CC"/><stop offset=".5" stop-color="#D4AF37"/><stop offset=".62" stop-color="#9C7A1E"/>
          <stop offset=".76" stop-color="#F1DC8A"/><stop offset=".88" stop-color="#D4AF37"/><stop offset="1" stop-color="#FFF4CC"/>
        </linearGradient>
        <radialGradient id="tlCometG"><stop offset="0" stop-color="#FFFBEA"/><stop offset=".35" stop-color="#F1DC8A"/><stop offset="1" stop-color="#D4AF37" stop-opacity="0"/></radialGradient>
      </defs>
      <path class="tl-svg-bg"     id="tlPathBg"/>
      <path class="tl-glow-layer" id="tlPathGlow"/>
      <path class="tl-svg-halo"   id="tlPathHalo"/>
      <path class="tl-svg-path"   id="tlPath"/>
      <g id="tlComet" class="tl-comet"><circle r="16" fill="url(#tlCometG)" opacity=".55"/><circle r="4.2" fill="#FFFBEA"/></g>
    </svg>

''' + rows + '''  </div>
  '''
s = s[:a] + new + s[b:]
rep('<p class="tl-note">Muy pronto compartiremos el itinerario completo de la celebración.</p>',
    '<p class="tl-note">Los horarios marcados como «Por confirmar» los compartiremos muy pronto.</p>')

# cometa que sigue la punta de la línea
rep("""      const off = len * (1 - self.progress);
      capas.forEach(function(el){ el.style.strokeDashoffset = off; });""",
"""      const off = len * (1 - self.progress);
      capas.forEach(function(el){ el.style.strokeDashoffset = off; });
      const cm = document.getElementById('tlComet');
      if (cm) { const pt = data.path.getPointAtLength(len * self.progress); cm.setAttribute('transform', 'translate(' + pt.x + ',' + pt.y + ')'); cm.style.opacity = self.progress > .002 && self.progress < .998 ? 1 : 0; }""")

# ── 3. COLOR SUGERIDO: una sola bolita que funde ──
a = s.find('<div class="dcx-palette" data-dcx-swap>'); b = s.find('</div>\n  </div>', a)
cols = re.findall(r'background:(#[0-9A-Fa-f]{6})"></span><span class="dcx-name">([^<]+)<', s[a:b])
assert len(cols) == 6, cols
s = s[:a] + '''<div class="dcx-one" data-colors='%s'>
      <span class="dcx-dot dcx-ball"><i class="dcx-l on" style="background:%s"></i><i class="dcx-l"></i></span>
      <span class="dcx-name dcx-onename" aria-live="polite">%s</span>
    </div>''' % (json.dumps(cols, ensure_ascii=False), cols[0][0], cols[0][1]) + s[b:]

# ── CSS ──
CSS = r'''
/* ═══ ronda 2 ═══ */
/* HERO: la foto ocupa la parte de arriba completa y los textos van debajo, sin tapar a los novios */
#hero{background:#0A1430}
#hero .h-bg{top:-5%;bottom:34%}
.hero-drift{background-position:center bottom;transform-origin:50% 88%}
#hero .h-ov{background:linear-gradient(to bottom,rgba(10,20,48,.25) 0%,rgba(10,20,48,0) 14%,rgba(10,20,48,0) 50%,rgba(10,20,48,.55) 58%,rgba(10,20,48,.92) 64%,#0A1430 70%,#0A1430 100%)}
#hero .h-cnt{padding-bottom:64px}
#hero .h-div{margin:12px 0 2px}
#hero .h-name{font-size:clamp(44px,12.4vw,58px)}
#hero .h-amp{font-size:clamp(34px,9.6vw,44px)}
#hero .h-date-wrap{margin-top:16px}
#hero .h-frame{bottom:22px}

/* ITINERARIO: línea dorada metálica, sin filtros pesados, con cometa en la punta */
#itinerary .tl-svg-bg{stroke:rgba(212,175,55,.38);stroke-width:1.6;stroke-dasharray:1 7;stroke-linecap:round}
#itinerary .tl-svg-path{stroke:url(#tlFoil);stroke-width:2.6;filter:none;animation:none}
#itinerary .tl-glow-layer{stroke:#D4AF37;stroke-width:12;opacity:.14;filter:none;animation:none}
#itinerary .tl-svg-halo{stroke:#F1DC8A;stroke-width:5;opacity:.28;filter:none;animation:tlHalo2 3.4s ease-in-out infinite}
@keyframes tlHalo2{0%,100%{opacity:.18}50%{opacity:.4}}
.tl-comet{opacity:0;transition:opacity .3s}
.tl-comet circle:first-child{animation:tlComet 1.6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes tlComet{0%,100%{transform:scale(.8)}50%{transform:scale(1.25)}}
#itinerary .tl-t--pc{font-family:'Jost',sans-serif;font-style:italic;font-weight:500;letter-spacing:.06em;text-transform:none;opacity:.9}
#itinerary .tl-ico svg{color:#D4AF37}
@media(prefers-reduced-motion:reduce){#itinerary .tl-svg-halo,.tl-comet circle:first-child{animation:none}}

/* VESTIMENTA: una sola bolita que cambia de color con fundido */
#dresscode .dcx-one{display:flex;flex-direction:column;align-items:center;margin-top:6px}
#dresscode .dcx-ball{width:84px;height:84px}
#dresscode .dcx-l{position:absolute;inset:0;border-radius:50%;opacity:0;transition:opacity 1.4s ease}
#dresscode .dcx-l.on{opacity:1}
#dresscode .dcx-ball::before{z-index:2}
#dresscode .dcx-onename{margin-top:12px;font-size:17px;transition:opacity .7s ease}
#dresscode .dcx-onename.out{opacity:0}
'''
i = s.find('  </style>'); s = s[:i] + CSS + s[i:]

JS = r'''<script>
/* Vestimenta: una sola bolita que funde entre los colores sugeridos */
(function(){
  function go(){
    var g = document.querySelector('#dresscode .dcx-one'); if (!g || g.__on) return; g.__on = 1;
    var cols = JSON.parse(g.getAttribute('data-colors')), L = g.querySelectorAll('.dcx-l'), nm = g.querySelector('.dcx-onename');
    var i = 0, front = 0;
    setInterval(function(){
      if (document.hidden) return;
      i = (i + 1) % cols.length; var nx = 1 - front;
      L[nx].style.background = cols[i][0]; L[nx].classList.add('on'); L[front].classList.remove('on'); front = nx;
      nm.classList.add('out'); setTimeout(function(){ nm.textContent = cols[i][1]; nm.classList.remove('out'); }, 700);
    }, 2800);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
})();
</script>
'''
i = s.rfind('</body>'); s = s[:i] + JS + s[i:]
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('ok', len(s))
