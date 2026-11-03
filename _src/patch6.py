# Parche 6: vinilo a la derecha, hero champán solo nombres, secciones champán,
# fundido cruzado continuo entre secciones, footer con sello, más movimiento
import io, sys, re
P = r'C:/Users/aleja/boda-nubia-brisia-y-luis-ricardo/index.html'
s = io.open(P, encoding='utf-8').read()
def rep(o, n, cnt=1):
    global s
    c = s.count(o)
    if c != cnt: sys.exit('ERR %d %r' % (c, o[:80]))
    s = s.replace(o, n)

# ── 1. VINILO A LA DERECHA ──
rep('.vinyl-btn{left:14px;right:auto;bottom:14px;width:46px;height:46px}',
    '.vinyl-btn{right:16px;left:auto;bottom:16px;width:54px;height:54px}')

# ── 2. HERO: solo nombres ──
a = s.find('<section id="hero">'); b = s.find('</section>', a) + len('</section>')
s = s[:a] + '''<section id="hero" class="hz" data-top="#F7E7CE" data-bot="#F3E3C7">
  <div class="hz-bg" aria-hidden="true"><i class="hz-glow g1"></i><i class="hz-glow g2"></i><i class="hz-glow g3"></i></div>
  <div class="h-particles" id="hPart"></div>
  <div class="hz-arch" id="heroBg" role="img" aria-label="Nubia Brisia y Luis Ricardo">
    <div class="hz-photo"><i style="background-image:url('fotos/foto2.jpg')"></i><b class="hz-sheen"></b></div>
  </div>
  <div class="h-cnt hz-cnt" id="hCnt">
    <div class="h-clip"><span class="h-name hz-name" id="hN1">Nubia Brisia</span></div>
    <div class="h-amp-clip"><span class="h-amp hz-amp" id="hAmp">&amp;</span></div>
    <div class="h-clip"><span class="h-name hz-name" id="hN2">Luis Ricardo</span></div>
  </div>
</section>''' + s[b:]
rep("  gsap.set(['#hWe','#hDiv','#hLine','#hDate','#hScroll'], { opacity: 0 });\n", "  gsap.fromTo('#heroBg', { opacity: 0, scale: .94 }, { opacity: 1, scale: 1, duration: 1.4, ease: 'power3.out' });\n")
for x in ["    .to('#hWe',    { opacity: 1, duration: .8 }, .15)\n", "    .to('#hDiv',   { opacity: 1, duration: .6 }, .35)\n",
          "    .to('#hLine',  { opacity: .7, duration: .7 }, 1.2)\n", "    .to('#hDate',  { opacity: 1, duration: .8 }, 1.35)\n"]:
    rep(x, '')
rep("    .to('#hScroll',{ opacity: 1, duration: .6 }, 1.8);", "    ;")
rep("""  gsap.to('#heroBg', {
    y: -70, ease: 'none',""", """  gsap.to('#heroBg', {
    y: -40, ease: 'none',""")

# ── 3. SECCIONES CHAMPÁN ──
LIGHT = ['countdown', 'calendar', 'album', 'family', 'padrinos', 'weather']
for sid in LIGHT:
    m = re.search(r'<section id="%s"([^>]*)>' % sid, s)
    attrs = m.group(1)
    if 'class="' in attrs:
        na = attrs.replace('class="', 'class="sec-light ', 1)
    else:
        na = attrs + ' class="sec-light"'
    s = s[:m.start()] + '<section id="%s"%s data-top="#F7E7CE" data-bot="#F3E3C7">' % (sid, na) + s[m.end():]

# ── 4. FUNDIDO CRUZADO CONTINUO ──
a = s.find('    for (var i = 0; i < secs.length - 1; i++){\n      var A = secs[i], Bs = secs[i+1], a = edge(A,\'bot\')')
b = s.find('  /* brillos desfasados */', a)
assert a > 0 and b > a
s = s[:a] + '''    /* una sola curva smoothstep repartida entre el final de A y el inicio de B:
       A recibe el color de B con alfa s(u), B recibe el de A con alfa 1-s(u); en la frontera ambos valen 50% */
    function cross(sec, pos, c, h, from, to){
      var st = [], N = 16;
      for (var k = 0; k <= N; k++){
        var t = k / N, u = from + (to - from) * t, sm = u*u*(3-2*u);
        var al = pos === 'bot' ? sm : 1 - sm;
        st.push('rgba(' + c.join(',') + ',' + al.toFixed(3) + ') ' + (pos === 'bot' ? (t*h) : (h - t*h)).toFixed(1) + 'px');
      }
      if (pos === 'top') st.reverse();
      var el = document.createElement('div');
      el.className = 'sf sf-' + pos; el.setAttribute('aria-hidden','true');
      el.style.height = h + 'px';
      el.style.background = 'linear-gradient(to bottom,' + st.join(',') + ')';
      sec.appendChild(el);
    }
    for (var i = 0; i < secs.length - 1; i++){
      var A = secs[i], Bs = secs[i+1], a = edge(A,'bot'), b = edge(Bs,'top');
      var diff = Math.abs(a[0]-b[0]) + Math.abs(a[1]-b[1]) + Math.abs(a[2]-b[2]);
      var h = diff > 200 ? 230 : 150;
      cross(A, 'bot', b, h, 0, .5);
      cross(Bs, 'top', a, h, .5, 1);
    }
  }
''' + s[b:]

# ── 5. FOOTER CON SELLO ──
a = s.find('<footer id="footer">'); b = s.find('<div class="el-sep"></div>', a)
s = s[:a] + '''<footer id="footer" class="sec-light ft2" data-top="#F7E7CE" data-bot="#F3E3C7">
  <div class="ft2-halo" aria-hidden="true"></div>
  <img class="ft2-seal" src="sello.webp" alt="Sello B&amp;R" width="220" height="220" loading="eager">
  <p class="ft2-eyebrow">Con amor</p>
  <div class="ft-nms ft2-nms">Nubia Brisia<span>&amp;</span>Luis Ricardo</div>
  <div class="ft2-rule" aria-hidden="true"><i></i><b>✦</b><i></i></div>
  <p class="ft-dt">05 · Junio · 2027</p>
  <p class="ft-note">Ciudad de México</p>
  <p class="ft2-thanks">Gracias por ser parte de nuestra historia</p>

  ''' + s[b:]

# ── CSS ──
CSS = r'''
/* ═══ ronda 3 ═══ */
/* HERO champán: foto completa en arco, solo nombres */
#hero.hz{min-height:100svh;display:flex;flex-direction:column;align-items:center;justify-content:center;
  padding:76px 18px 64px;background:#F7E7CE;overflow:hidden;isolation:isolate}
.hz-bg{position:absolute;inset:0;z-index:-1;pointer-events:none;
  background:radial-gradient(ellipse 80% 55% at 50% 38%,#FFF8EA 0%,#F7E7CE 55%,#EFDDBC 100%)}
.hz-glow{position:absolute;border-radius:50%;filter:blur(40px);opacity:.55;animation:hzGlow 14s ease-in-out infinite alternate}
.hz-glow.g1{width:300px;height:300px;left:-90px;top:8%;background:radial-gradient(circle,rgba(212,175,55,.45),transparent 70%)}
.hz-glow.g2{width:260px;height:260px;right:-80px;top:44%;background:radial-gradient(circle,rgba(74,123,183,.28),transparent 70%);animation-duration:17s}
.hz-glow.g3{width:240px;height:240px;left:20%;bottom:-90px;background:radial-gradient(circle,rgba(212,175,55,.35),transparent 70%);animation-duration:12s}
@keyframes hzGlow{from{transform:translate(0,0) scale(1)}to{transform:translate(30px,-26px) scale(1.18)}}
.hz-arch{position:relative;width:min(76vw,330px);aspect-ratio:624/874;z-index:1;flex:none}
.hz-arch::before,.hz-arch::after{content:'';position:absolute;border-radius:999px 999px 6px 6px;pointer-events:none}
.hz-arch::before{inset:-9px;border:1.5px solid #C9A030;box-shadow:0 18px 50px rgba(30,58,138,.22)}
.hz-arch::after{inset:-17px;border:1px solid rgba(201,160,48,.5)}
.hz-photo{position:absolute;inset:0;border-radius:999px 999px 4px 4px;overflow:hidden;background:#EAD8B6}
.hz-photo i{position:absolute;inset:0;background:center/100% 100% no-repeat;transform-origin:50% 100%;
  animation:hzKen 16s ease-in-out infinite alternate}
@keyframes hzKen{from{transform:scale(1)}to{transform:scale(1.035)}}
.hz-sheen{position:absolute;inset:0;background:linear-gradient(115deg,transparent 35%,rgba(255,250,235,.35) 50%,transparent 65%);
  background-size:260% 100%;animation:hzSheen 7s ease-in-out infinite;mix-blend-mode:soft-light}
@keyframes hzSheen{0%,100%{background-position:120% 0}50%{background-position:-20% 0}}
#hero .hz-cnt{position:relative;z-index:2;margin-top:30px;padding:0;text-align:center}
#hero .hz-name{font-size:clamp(46px,13vw,60px);filter:none;text-shadow:none;
  background:linear-gradient(100deg,#0A1430 0%,#1E3A8A 30%,#4A7BB7 48%,#1E3A8A 66%,#0A1430 100%);background-size:240% 100%;
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;
  animation:goldSweep 8s ease-in-out infinite;padding:.2em .45em;margin:-.2em -.45em}
#hero .hz-amp{font-size:clamp(32px,9vw,42px);filter:none;color:#B8901E;-webkit-text-fill-color:#B8901E;margin:-4px 0}
#hero .h-particles .h-star{filter:hue-rotate(0) brightness(.8)}
@media(prefers-reduced-motion:reduce){.hz-glow,.hz-photo i,.hz-sheen,#hero .hz-name{animation:none}}

/* SECCIONES CHAMPÁN (contraste con el azul) */
.sec-light{--cream:#13224A;--gold:#A8811C;--gold-deep:#7A5A12;
  --foil:linear-gradient(100deg,#6E5010 0%,#A8811C 22%,#D4AF37 40%,#8A6A14 58%,#B8901E 78%,#6E5010 100%);
  background:radial-gradient(ellipse 90% 60% at 50% 30%,#FBF0DC 0%,#F7E7CE 55%,#F3E3C7 100%)!important;color:#13224A}
.sec-light .heading,.sec-light .heading-sm,.sec-light .data-crit,.sec-light p,.sec-light .eyebrow{text-shadow:none!important}
.sec-light .bg-orb{mix-blend-mode:multiply;opacity:.7}
.sec-light .orn-line{background:linear-gradient(90deg,transparent,#B8901E,transparent)!important}
.sec-light .orn-diamond,.sec-light .orn-diamond-sm{border-color:#B8901E!important;background:transparent}
.sec-light .gline{background:linear-gradient(90deg,transparent,#B8901E,transparent)!important}
.sec-light .ink-bg i{filter:grayscale(1) invert(1) sepia(.55) saturate(1.3) brightness(1.02);mix-blend-mode:multiply}
.sec-light .ink-bg{opacity:.5}
'''
CSS2 = r'''
/* cuenta regresiva en champán */
#countdown.sec-light .cd-ring-item{background:radial-gradient(circle at 50% 35%,#FFFDF6,#F3E3C7)!important;box-shadow:0 10px 28px rgba(30,58,138,.14),inset 0 0 0 1px rgba(184,144,30,.35)!important}
#countdown.sec-light .cd-ring-item *{color:#13224A}
/* padrinos: tarjeta navy sobre champán */
#padrinos.sec-light .pad-solo{background:linear-gradient(180deg,#13224A,#0A1430)!important;--cream:#F7E7CE;--gold:#D4AF37;color:#F7E7CE}
#padrinos.sec-light .pad-solo *{color:inherit}
#padrinos.sec-light .pad-solo [class*="ttl"],#padrinos.sec-light .pad-solo h3{color:#F1DC8A}
/* clima */
#weather.sec-light svg circle{stroke-opacity:1}

/* FOOTER con sello */
#footer.ft2{padding:84px 22px 40px;position:relative;isolation:isolate;border-top:none}
.ft2-halo{position:absolute;left:50%;top:40px;width:340px;height:340px;transform:translateX(-50%);z-index:-1;border-radius:50%;
  background:radial-gradient(circle,rgba(212,175,55,.32),rgba(212,175,55,0) 65%);animation:ft2Halo 6s ease-in-out infinite}
@keyframes ft2Halo{0%,100%{transform:translateX(-50%) scale(.92);opacity:.7}50%{transform:translateX(-50%) scale(1.08);opacity:1}}
.ft2-seal{display:block;width:132px;height:132px;margin:0 auto 26px;border-radius:50%;
  filter:drop-shadow(0 14px 22px rgba(10,20,48,.35));animation:ft2Seal 6.5s ease-in-out infinite}
@keyframes ft2Seal{0%,100%{translate:0 0;rotate:-3deg}50%{translate:0 -10px;rotate:3deg}}
.ft2-eyebrow{font-family:'Cinzel',serif;font-size:13px;font-weight:600;letter-spacing:.42em;text-transform:uppercase;color:#A8811C;margin-bottom:6px}
#footer .ft2-nms{font-family:'Great Vibes',cursive;font-size:clamp(44px,12.6vw,58px);line-height:1.18;filter:none;
  background:linear-gradient(100deg,#0A1430 0%,#1E3A8A 30%,#4A7BB7 48%,#1E3A8A 66%,#0A1430 100%);background-size:240% 100%;
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
#footer .ft2-nms span{display:block;font-size:.62em;-webkit-text-fill-color:#B8901E;margin:-.1em 0}
.ft2-rule{display:flex;align-items:center;justify-content:center;gap:12px;margin:22px auto 4px;color:#B8901E}
.ft2-rule i{width:70px;height:1px;background:linear-gradient(90deg,transparent,#B8901E)}
.ft2-rule i:last-child{transform:scaleX(-1)}
.ft2-rule b{font-weight:400;font-size:14px;animation:ft2Twinkle 3s ease-in-out infinite}
@keyframes ft2Twinkle{0%,100%{opacity:.5;transform:scale(.85) rotate(0)}50%{opacity:1;transform:scale(1.15) rotate(90deg)}}
#footer.ft2 .ft-dt{color:#13224A;opacity:1;font-family:'Cinzel',serif;font-size:17px;letter-spacing:.24em;margin-top:14px}
#footer.ft2 .ft-note{color:#13224A;opacity:.85!important;font-size:15px;margin-top:6px;letter-spacing:.12em}
.ft2-thanks{font-family:'Playfair Display',serif;font-style:italic;font-size:16px;color:#13224A;opacity:.85;margin:20px auto 0;max-width:280px;line-height:1.5}
#footer.ft2 .el-sep{background:linear-gradient(90deg,transparent,rgba(168,129,28,.5),transparent)!important;opacity:1}
#footer.ft2 .el-credit,#footer.ft2 .el-credit span{color:#13224A!important;opacity:.8}
@media(prefers-reduced-motion:reduce){.ft2-halo,.ft2-seal,.ft2-rule b{animation:none}}

/* MÁS MOVIMIENTO */
@keyframes inkDrift{
  0%  {transform:translate3d(-5%,-3%,0) scale(1.02) rotate(-1.4deg)}
  50% {transform:translate3d(3%,4%,0)   scale(1.12) rotate(.8deg)}
  100%{transform:translate3d(5%,-2%,0)  scale(1.18) rotate(1.6deg)}
}
@keyframes inkDriftFlip{
  0%  {transform:scaleX(-1) translate3d(-5%,-3%,0) scale(1.02) rotate(-1.4deg)}
  50% {transform:scaleX(-1) translate3d(3%,4%,0)   scale(1.12) rotate(.8deg)}
  100%{transform:scaleX(-1) translate3d(5%,-2%,0)  scale(1.18) rotate(1.6deg)}
}
.ink-bg i{animation-duration:16s!important}
@keyframes levitate2{0%,100%{translate:0 0;rotate:0deg}25%{rotate:1.2deg}50%{translate:0 -13px}75%{rotate:-1.2deg}}
.loc-card,.fam-card,.pad-solo{animation:levitate2 5.5s ease-in-out infinite}
.tl-ico,.cd-ring-item,.song-vinyl,#dresscode .dcx-look,#dresscode .dcx-ball,#album img,.cal-ico,.wx-ring,.faq-ico{animation:levitate2 4.8s ease-in-out infinite}
.cd-ring-grid > :nth-child(2n){animation-delay:-1.6s}.cd-ring-grid > :nth-child(3){animation-delay:-3.1s}
.tl-row:nth-child(2n) .tl-ico{animation-delay:-2.2s}
.orn-diamond{animation:ornSpin 6s ease-in-out infinite}
@keyframes ornSpin{0%,100%{transform:rotate(45deg) scale(1)}50%{transform:rotate(225deg) scale(1.2)}}
.bg-orb{animation-duration:9s!important}
@media(prefers-reduced-motion:reduce){.loc-card,.fam-card,.pad-solo,.tl-ico,.cd-ring-item,.song-vinyl,#dresscode .dcx-look,#dresscode .dcx-ball,#album img,.orn-diamond{animation:none!important}}
'''
i = s.find('  </style>'); s = s[:i] + CSS + CSS2 + s[i:]
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('ok', len(s))
