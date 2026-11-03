# Parche 2: integrar bloques (tintas, dress code, sobres, hospedaje, galería, RSVP) + CSS/JS de puntos 1,2,4,10,11,12
import re, sys, io, json
P = r'C:/Users/aleja/boda-nubia-brisia-y-luis-ricardo/index.html'
B = r'C:/Users/aleja/AppData/Local/Temp/claude/C--Users-aleja/61662fee-e927-4bfd-bf71-b8b93a534439/scratchpad/blocks/'
s = io.open(P, encoding='utf-8').read()
def rd(f): return io.open(B + f, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit('ERROR rep: %d apariciones de %r' % (n, old[:90]))
    s = s.replace(old, new)
def cut(a_mark, b_mark, incl_b=True):
    """borra desde a_mark hasta b_mark (único)"""
    global s
    a = s.find(a_mark); assert a >= 0 and s.count(a_mark) == 1, a_mark[:60]
    b = s.find(b_mark, a); assert b > a, b_mark[:60]
    s = s[:a] + s[b + (len(b_mark) if incl_b else 0):]

d = json.load(io.open(B + 'hoteles.json', encoding='utf-8'))
# ── direcciones ──
rep('@@CER_ADDR@@', 'Av. 510 No. 90, Col. San Juan de Aragón, Gustavo A. Madero, CDMX')
rep('@@REC_ADDR@@', 'Av. Insurgentes 69, Col. La Era, Iztapalapa, CDMX')
rep('@@DIST_SEDES@@', 'Entre ambas hay unos 21 km, de 25 a 50 minutos en auto según el tráfico.')

# ── bloques HTML ──
rep('<!--@@SOBRES@@-->', rd('sobres.html'))
rep('<!--@@DRESSCODE@@-->', rd('dresscode.html'))
rep('<!--@@HOSPEDAJE@@-->', rd('hosp.html'))
rep('<!--@@GALLERY@@-->', rd('gallery.html'))
rep('<!--@@RSVP@@-->', rd('rsvp.html'))

# ── tintas ──
INK = {
 'invite':   ('ink-top', ''), 'family': ('ink-hero', ' soft'), 'location': ('ink-corner', ' oval'),
 'itinerary':('ink-top', ' flip'), 'dresscode': ('ink-oval', ' oval flip'), 'sobres': ('ink-hero', ' soft flip'),
 'album':    ('ink-oval', ' oval'), 'rsvp': ('ink-footer', ' soft'),
}
for sid, (img, cls) in INK.items():
    layer = '<div class="ink-bg%s" aria-hidden="true"><i style="background-image:url(\'ink/%s.webp\')"></i></div>' % (cls, img)
    mark = '<!--@@INK:%s@@-->' % sid
    if mark in s:
        rep(mark, layer)
    else:
        m = re.search(r'<section id="%s"[^>]*>' % sid, s)
        assert m, sid
        s = s[:m.end()] + '\n  ' + layer + s[m.end():]
    # clase has-ink en la sección
    m = re.search(r'<section id="%s"([^>]*)>' % sid, s)
    tag = m.group(0)
    if 'class="' in tag: new = tag.replace('class="', 'class="has-ink ', 1)
    else: new = tag[:-1] + ' class="has-ink">'
    s = s[:m.start()] + new + s[m.end():]

# ── menú en el orden real de la página ──
order = [x for x in re.findall(r'<section id="([a-z]+)"', s)]
names = {'invite': 'Nuestra invitación', 'countdown': 'Cuenta regresiva', 'location': 'Ceremonia y recepción', 'itinerary': 'Itinerario',
         'sobres': 'Lluvia de sobres', 'album': 'Álbum de fotos', 'dresscode': 'Código de vestimenta', 'hospedaje': 'Hospedaje',
         'family': 'Nuestras familias', 'padrinos': 'Padrinos', 'gallery': 'Galería', 'weather': 'El clima', 'faq': 'Preguntas frecuentes', 'rsvp': 'Confirmar asistencia'}
lis = '\n'.join('    <li><a href="#%s"%s>%s</a></li>' % (x, ' class="nav-rsvp"' if x == 'rsvp' else '', names[x]) for x in order if x in names)
a = s.find('<ul class="nav-lista">'); b = s.find('</ul>', a)
s = s[:a] + '<ul class="nav-lista">\n' + lis + '\n  ' + s[b:]
print('orden:', order)

# ── CSS viejo de galería y RSVP ──
cut('#gallery{', '.rsvp-editar-btn:disabled{opacity:.45;cursor:not-allowed}')
# ── JS viejo ──
rep('  initRSVP();\n', '  if (window.initRSVP2) initRSVP2();\n  if (window.initGallery3D) initGallery3D();\n')
a = s.find("trigger: '#gallery', start: 'top 82%', once: true,")
a = s.rfind('\n', 0, s.rfind('ScrollTrigger.create', 0, a)) ; b = s.find('});', s.find("trigger: '#gallery', start: 'top 82%'")) + 3
s = s[:a] + s[b:]
a = s.find("  gsap.fromTo('.rsvp-card'"); b = s.find('\n', s.find("gsap.fromTo(['.rsvp-ornament'"))
s = s[:a] + s[b + 1:]
cut('function initRSVP(){', '\nfunction initWheel() {', incl_b=False)
a = s.find('function initWheel() {')
# fin de initWheel: siguiente "\n}\n" al nivel 0
b = s.find('\n}\n', a) + 3
s = s[:a] + s[b:]

# ── CSS nuevo ──
CSS = rd('ink.css') + rd('dresscode.css') + rd('sobres.css') + rd('hosp.css') + rd('gallery.css') + rd('rsvp.css') + r'''
/* ═══════════ NUBIA & LUIS · paquete de efectos ═══════════ */
/* 1 · HERO */
#hero{justify-content:flex-end;padding:48px 24px 0}
#hero .h-cnt{padding-bottom:110px}
#hero .h-bg{top:-12%;bottom:-12%;left:0;right:0;overflow:hidden;will-change:transform}
.hero-drift{position:absolute;inset:0;background:center 22%/cover no-repeat;animation:heroDrift 26s ease-in-out infinite alternate}
@keyframes heroDrift{0%{transform:translate3d(-1%,-1%,0) scale(1.02)}100%{transform:translate3d(1.2%,1.6%,0) scale(1.10)}}
.hero-sheen{position:absolute;inset:0;mix-blend-mode:soft-light;pointer-events:none;
  background:linear-gradient(115deg,transparent 30%,rgba(255,244,214,.6) 47%,rgba(255,250,232,.75) 50%,rgba(255,244,214,.6) 53%,transparent 70%);
  background-size:260% 100%;animation:heroSheen 9s ease-in-out infinite}
@keyframes heroSheen{0%,100%{background-position:110% 0}50%{background-position:-10% 0}}
#hero .h-ov{background:linear-gradient(to bottom,rgba(10,20,48,0) 0%,rgba(10,20,48,0) 42%,rgba(10,20,48,.5) 62%,rgba(10,20,48,.86) 82%,rgba(10,20,48,.94) 100%)}
#hero .h-name{font-size:clamp(46px,13.6vw,64px);filter:drop-shadow(0 2px 10px rgba(0,0,0,.55))}
#hero .h-amp{font-size:clamp(38px,11vw,52px)}
#hero .h-date{color:#F7E7CE}
@media(prefers-reduced-motion:reduce){.hero-drift,.hero-sheen{animation:none}}

/* 2 · FUNDIDOS ENTRE SECCIONES */
#main-content > section,#main-content > footer{isolation:isolate}
.sf{position:absolute;left:0;right:0;z-index:-1;pointer-events:none}
.sf-top{top:0}.sf-bot{bottom:0}
.sf-hero{z-index:2}

/* 4 · LEVITAR (translate/rotate individuales: no chocan con GSAP) */
@keyframes levitate{0%,100%{translate:0 0;rotate:0deg}25%{rotate:.6deg}50%{translate:0 -9px}75%{rotate:-.6deg}}
.loc-card,.fam-card,.pad-solo{animation:levitate 6.5s ease-in-out infinite}
.loc-card + .loc-card{animation-delay:-2.2s}
.pad-solo{animation-delay:-4.1s}
@media(prefers-reduced-motion:reduce){.loc-card,.fam-card,.pad-solo{animation:none}}
.loc-card.lift{box-shadow:0 34px 70px rgba(0,0,0,.6),0 0 0 1px rgba(212,175,55,.35)}
.loc-pin{animation:pinBeat 1.8s ease-in-out infinite}
@keyframes pinBeat{0%,100%{transform:scale(1)}50%{transform:scale(1.25)}}

/* 10 + 11 · TÍTULOS CON BRILLO METÁLICO (sin cortar la script) */
.ttl,.heading,.heading-sm,.foil-text{
  background:var(--foil);background-size:220% 100%;
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:var(--gold-deep);
  animation:goldSweep 7s ease-in-out infinite;text-shadow:none;
  padding:.22em .45em;margin-left:-.45em;margin-right:-.45em;margin-top:-.22em;margin-bottom:-.22em;
  line-height:1.25;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.ttl{display:block;margin-top:calc(16px - .22em)}
.heading,.heading-sm,.ft-nms{display:block}
.h-amp.foil-text{filter:drop-shadow(0 2px 8px rgba(0,0,0,.45))}
@keyframes goldSweep{0%,100%{background-position:0% 0}50%{background-position:100% 0}}
@media(prefers-reduced-motion:reduce){.ttl,.heading,.heading-sm,.foil-text{animation:none;background-position:50% 0}}
.h-amp-clip{overflow:visible}

/* ubicación: nombre del lugar en serif legible */
.loc-name{font-family:'Playfair Display',serif!important;font-weight:600;font-size:clamp(23px,6.4vw,27px)!important;color:#F7E7CE;line-height:1.3}
.loc-sub{font-family:'Jost',sans-serif;font-weight:500;font-size:16px;line-height:1.5;color:rgba(247,231,206,.88);text-align:center;margin:8px 0 2px}
.loc-addr{font-family:'Jost',sans-serif;font-weight:500;font-size:16px!important;opacity:.9!important;line-height:1.6}
.fam-cross{font-family:'Playfair Display',serif;font-size:.6em;vertical-align:.35em;color:var(--gold)}
.pad-solo{max-width:320px;margin:26px auto 0;padding:30px 22px;text-align:center;border:1px solid rgba(212,175,55,.3);border-radius:6px;
  background:linear-gradient(180deg,rgba(19,34,74,.75),rgba(10,20,48,.6));box-shadow:0 18px 50px rgba(0,0,0,.45)}
.pad-solo .pad-ic{display:block;margin:0 auto 12px}
.pad-solo .pad-role{font-family:'Playfair Display',serif;font-weight:600;font-size:22px;color:var(--gold)}
.pad-solo .pad-names{font-family:'Jost',sans-serif;font-weight:500;font-size:16px;line-height:1.5;color:#F7E7CE;margin-top:8px}
.tl-note{font-family:'Jost',sans-serif;font-weight:500;font-size:16px;line-height:1.5;color:rgba(247,231,206,.88);text-align:center;margin:26px auto 0;max-width:320px}
.hs-foot{font-family:'Jost',sans-serif;font-weight:500;font-size:14px;color:rgba(247,231,206,.75);margin-top:14px}

/* 12 · MENÚ MINIMALISTA */
.nav-btn{top:14px;right:14px;width:44px;height:44px;gap:5px;background:rgba(19,34,74,.55);
  backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border:1px solid rgba(212,175,55,.6);
  box-shadow:0 6px 18px rgba(0,0,0,.35)}
.nav-btn i{width:18px;height:1.2px;background:#F1DC8A}
.nav-btn.abierto i:nth-child(1){transform:translateY(6.2px) rotate(45deg)}
.nav-btn.abierto i:nth-child(3){transform:translateY(-6.2px) rotate(-45deg)}
#nav-panel{flex-direction:column;background:linear-gradient(180deg,rgba(10,20,48,.985),rgba(15,28,64,.985));
  backdrop-filter:none;-webkit-backdrop-filter:none;transition:opacity .45s ease}
#nav-panel::before{display:none}
.nav-lista li + li{border-top:none}
.nav-lista a{font-weight:500;font-size:clamp(20px,5.4vw,24px);padding:11px 10px;letter-spacing:.01em}
.nav-filete{display:block;width:96px;height:1px;margin:10px auto 0;background:linear-gradient(90deg,transparent,#D4AF37,#FFF4CC,#D4AF37,transparent)}
.vinyl-btn{left:14px;right:auto;bottom:14px;width:46px;height:46px}
.vinyl-btn::before{inset:-5px}
'''
i = s.find('  </style>')
s = s[:i] + CSS + '\n' + s[i:]

# ── JS nuevo (después de GSAP) ──
JS = '<script>\n' + rd('dresscode.js') + '\n' + rd('sobres.js') + '\n' + rd('gallery.js') + '\n' + rd('rsvp.js') + r'''
/* ═══ NUBIA & LUIS · fundidos, brillo y tarjetas ═══ */
(function(){
  /* Fundido uniforme entre secciones: color medio en cada frontera, curva smoothstep de 9 paradas */
  function initSectionFades(){
    var secs = [].slice.call(document.querySelectorAll('#main-content > section, #main-content > footer'));
    if (!secs.length || secs[0].querySelector('.sf')) return;
    var PAGE = [10, 20, 48];
    function hex(h){ h = h.replace('#',''); return [0,2,4].map(function(k){ return parseInt(h.substr(k,2),16); }); }
    function parse(c){ var m = (c||'').match(/[\d.]+/g); if (!m || (m.length > 3 && +m[3] === 0)) return null; return [+m[0],+m[1],+m[2]]; }
    function grads(sec){ var bi = getComputedStyle(sec).backgroundImage, m = bi && bi.match(/rgba?\([^)]+\)|#[0-9a-f]{6}/gi); return m || null; }
    function edge(sec, which){
      var dsv = sec.dataset[which]; if (dsv) return hex(dsv);
      var g = grads(sec);
      if (g && g.length >= 2){ var c = parse(which === 'top' ? g[0] : g[g.length-1]) || (/^#/.test(g[0]) ? hex(which==='top'?g[0]:g[g.length-1]) : null); if (c) return c; }
      return parse(getComputedStyle(sec).backgroundColor) || PAGE;
    }
    function grad(dir, c, h){
      var st = [];
      for (var i = 0; i <= 8; i++){ var t = i/8, a = 1 - t*t*(3-2*t);
        st.push('rgba(' + c.join(',') + ',' + a.toFixed(3) + ') ' + (t*h).toFixed(1) + 'px'); }
      return 'linear-gradient(' + dir + ',' + st.join(',') + ')';
    }
    function layer(sec, pos, c, h){
      var el = document.createElement('div');
      el.className = 'sf sf-' + pos + (sec.id === 'hero' ? ' sf-hero' : ''); el.setAttribute('aria-hidden','true');
      el.style.height = h + 'px'; el.style.background = grad(pos === 'top' ? 'to bottom' : 'to top', c, h);
      sec.appendChild(el);
    }
    for (var i = 0; i < secs.length - 1; i++){
      var A = secs[i], Bs = secs[i+1], a = edge(A,'bot'), b = edge(Bs,'top');
      var mid = [0,1,2].map(function(k){ return Math.round((a[k] + b[k]) / 2); });
      var h = A.id === 'hero' ? 90 : 170;
      layer(A, 'bot', A.id === 'hero' ? [10,20,48] : mid, h);
      layer(Bs, 'top', A.id === 'hero' ? [10,20,48] : mid, h);
    }
  }
  /* brillos desfasados */
  function staggerFoil(){
    document.querySelectorAll('.ttl,.heading,.heading-sm,.foil-text').forEach(function(t, i){
      t.style.animationDelay = (-(i * 1.37) % 7).toFixed(2) + 's';
    });
  }
  /* ubicación: al tocar se eleva */
  function lift(){
    document.querySelectorAll('.loc-card').forEach(function(c){
      c.addEventListener('click', function(e){ if (e.target.closest('a')) return; c.classList.toggle('lift'); });
    });
  }
  function go(){ initSectionFades(); staggerFoil(); lift(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
})();
</script>
'''
i = s.find('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>')
i = s.find('\n', i) + 1
s = s[:i] + JS + s[i:]

io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('ok', len(s))
