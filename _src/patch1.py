# Parche 1: datos del cliente + paleta + puntos 1, 2, 4, 10, 11, 12
import re, sys, io
P = r'C:/Users/aleja/boda-nubia-brisia-y-luis-ricardo/index.html'
s = io.open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('ERROR rep: %d apariciones de %r' % (n, old[:80]))
    s = s.replace(old, new)

def sec(id_):
    """devuelve (inicio, fin) de <section id=...>...</section> (sin anidar)"""
    a = s.find('<section id="%s"' % id_)
    if a < 0: sys.exit('no section ' + id_)
    b = s.find('</section>', a) + len('</section>')
    return a, b

def get(id_):
    a, b = sec(id_); return s[a:b]

def put(id_, html):
    global s
    a, b = sec(id_); s = s[:a] + html + s[b:]

def drop(id_):
    global s
    a, b = sec(id_)
    # quita también el comentario inmediatamente anterior
    pre = s[:a].rstrip()
    if pre.endswith('-->'):
        c = pre.rfind('<!--'); pre = pre[:c]
    s = pre.rstrip() + '\n\n' + s[b:].lstrip()

# ───────── HEAD ─────────
rep('<meta name="theme-color" content="#000000">', '<meta name="theme-color" content="#0A1430">')
rep('<title>César &amp; Neidy · 07 · XI · 2026</title>', '<title>Nubia Brisia &amp; Luis Ricardo · 05 · VI · 2027</title>')
rep('content="Invitación de boda de César y Neidy Ivonne — 7 de Noviembre de 2026 · Acolman, Estado de México"',
    'content="Invitación de boda de Nubia Brisia y Luis Ricardo — 5 de junio de 2027 · Ciudad de México"')
rep('content="Boda César & Neidy · 7 Nov 2026"', 'content="Boda Nubia Brisia & Luis Ricardo · 5 jun 2027"')
rep('content="Nos casamos — Acolman, Estado de México · 7 de noviembre de 2026"', 'content="Nos casamos — Ciudad de México · 5 de junio de 2027"')
rep('https://boda-neidy-y-cesar.vercel.app/og-image.jpg', 'https://boda-nubia-brisia-y-luis-ricardo.vercel.app/og-image.jpg')

# ───────── PALETA (negro/champán → azul noche/dorado) ─────────
pal = [
 ('rgba(212,197,178', 'rgba(212,175,55'), ('rgba(212, 197, 178', 'rgba(212,175,55'),
 ('#D4C5B2', '#D4AF37'), ('#d4c5b2', '#D4AF37'),
 ('#E9E0D4', '#F1DC8A'), ('#e9e0d4', '#F1DC8A'),
 ('#8A7A62', '#9C7A1E'), ('#8a7a62', '#9C7A1E'),
 ('#F2ECE2', '#FFF4CC'), ('#f2ece2', '#FFF4CC'),
 ('rgba(138,122,98', 'rgba(156,122,30'), ('rgba(233,224,212', 'rgba(241,220,138'),
 ('rgba(10,9,8', 'rgba(10,20,48'), ('#0A0908', '#0A1430'), ('#0a0908', '#0A1430'),
 ('#12100c', '#0E1A3C'), ('#12100C', '#0E1A3C'), ('#100e0a', '#0D1838'), ('#100E0A', '#0D1838'),
 ('rgba(34,32,24', 'rgba(19,34,74'), ('#181610', '#0F1C40'), ('#222018', '#13224A'),
 ('rgba(24,22,16', 'rgba(15,28,64'), ('#0e0d08', '#0B1634'), ('#0E0D08', '#0B1634'),
 ('#1a1710', '#0F1B3E'), ('#141209', '#0C1736'), ('#12110a', '#0D1838'),
 ('rgba(28,25,18', 'rgba(16,30,66'), ('rgba(12,11,7', 'rgba(10,20,46'),
 ('rgba(8,7,5', 'rgba(8,14,34'), ('rgba(6,5,4', 'rgba(6,11,28'),
 ('rgba(196,86,106', 'rgba(74,123,183'), ('rgba(224,121,138', 'rgba(74,123,183'),
 ('#e0798a', '#4A7BB7'), ('#E0798A', '#4A7BB7'), ('#e8a090', '#7FA6D6'), ('#E8A090', '#7FA6D6'),
 ('#f0c3cb', '#B9CFEA'), ('#F0C3CB', '#B9CFEA'), ('#2E2820', '#13224A'), ('#221E16', '#0F1C40'),
]
for a, b in pal: s = s.replace(a, b)
rep('--cream:     #FFFFFF;', '--cream:     #F7E7CE;')
rep('--gold-grad: linear-gradient(135deg,#9C7A1E 0%,#D4AF37 26%,#FFF4CC 50%,#D4AF37 74%,#9C7A1E 100%);',
    '--gold-grad: linear-gradient(135deg,#9C7A1E 0%,#D4AF37 26%,#FFF4CC 50%,#D4AF37 74%,#9C7A1E 100%);\n'
    '  --surface:#13224A; --acc-deep:#1E3A8A; --acc:#4A7BB7; --gold-deep:#9C7A1E;\n'
    '  --foil:linear-gradient(100deg,#9C7A1E 0%,#D4AF37 30%,#FFFBEA 50%,#D4AF37 70%,#9C7A1E 100%);')

# ───────── SOBRE: intro de la 111 (Metzli) ─────────
rep('<img id="env-image" src="sobre.jpg" alt="Sobre invitación César &amp; Neidy" />',
    '<img id="env-image" src="sobre.jpg" alt="Sobre de la invitación de Nubia Brisia y Luis Ricardo" />')
rep('src="https://bsjoelxktbvlavfoozhk.supabase.co/storage/v1/object/public/fotos-clientes/boda-neidy-y-cesar/video/sobre-apertura.mp4"',
    'src="https://bsjoelxktbvlavfoozhk.supabase.co/storage/v1/object/public/fotos-clientes/audio/boda-metzli-y-rodolfo/sobre-apertura.mp4"')
# temporización del video de Metzli: el blanco del video se continúa al final
rep("""    if (!flashStarted && envVideo.duration && envVideo.currentTime >= envVideo.duration - 5) {
      flashStarted = true;
      gsap.to(envFlash, { opacity: 1, duration: 4.5, ease: 'none', onComplete: revealInvitation });
    }""", """    if (!flashStarted && envVideo.duration && envVideo.currentTime >= envVideo.duration - 0.45) {
      flashStarted = true;
      gsap.to(envFlash, { opacity: 1, duration: 0.45, ease: 'none', onComplete: revealInvitation });
    }""")
rep("opacity: 0, duration: 3, ease: 'power1.out',\n      onComplete: function () { envFlash.style.display = 'none'; }",
    "opacity: 0, duration: 1.4, ease: 'power1.out',\n      onComplete: function () { envFlash.style.display = 'none'; }")

# ───────── MÚSICA ─────────
rep('https://bsjoelxktbvlavfoozhk.supabase.co/storage/v1/object/public/fotos-clientes/audio/boda-neidy-y-cesar/cancion.mp3',
    'https://bsjoelxktbvlavfoozhk.supabase.co/storage/v1/object/public/fotos-clientes/audio/boda-nubia-brisia-luis-ricardo/cancion.mp3')

# ───────── MENÚ (punto 12): lista de secciones ─────────
a = s.find('<ul class="nav-lista">'); b = s.find('</ul>', a) + 5
s = s[:a] + '''<ul class="nav-lista">
    <li><a href="#invite">Nuestra invitación</a></li>
    <li><a href="#countdown">Cuenta regresiva</a></li>
    <li><a href="#location">Ceremonia y recepción</a></li>
    <li><a href="#itinerary">Itinerario</a></li>
    <li><a href="#family">Nuestras familias</a></li>
    <li><a href="#dresscode">Código de vestimenta</a></li>
    <li><a href="#sobres">Lluvia de sobres</a></li>
    <li><a href="#hospedaje">Hospedaje</a></li>
    <li><a href="#gallery">Galería</a></li>
    <li><a href="#album">Álbum de fotos</a></li>
    <li><a href="#faq">Preguntas frecuentes</a></li>
    <li><a href="#rsvp" class="nav-rsvp">Confirmar asistencia</a></li>
  </ul>
  <span class="nav-filete" aria-hidden="true"></span>''' + s[b:]

# ───────── HERO (punto 1) ─────────
rep('''  <div class="h-bg" id="heroBg">
    <video id="heroPic" src="https://bsjoelxktbvlavfoozhk.supabase.co/storage/v1/object/public/fotos-clientes/boda-neidy-y-cesar/video/hero.mp4"
           poster="hero.jpg" autoplay muted loop playsinline webkit-playsinline
           preload="auto" aria-label="César y Neidy"></video>
  </div>''', '''  <div class="h-bg hero-bg" id="heroBg" role="img" aria-label="Nubia Brisia y Luis Ricardo">
    <i class="hero-drift" style="background-image:url('fotos/foto2.jpg')"></i>
    <i class="hero-sheen" aria-hidden="true"></i>
  </div>''')
rep('<p class="h-we" id="hWe">Nos casamos</p>', '<p class="h-we" id="hWe">Nos casamos</p>')
rep('<div class="h-clip"><span class="h-name" id="hN1">Neidy</span></div>', '<div class="h-clip"><span class="h-name foil-text" id="hN1">Nubia Brisia</span></div>')
rep('<div class="h-amp-clip"><span class="h-amp" id="hAmp">&amp;</span></div>', '<div class="h-amp-clip"><span class="h-amp foil-text" id="hAmp">&amp;</span></div>')
rep('<div class="h-clip"><span class="h-name" id="hN2">César</span></div>', '<div class="h-clip"><span class="h-name foil-text" id="hN2">Luis Ricardo</span></div>')
rep('<p class="h-date">07 · Noviembre · 2026</p>\n      <p class="h-city">Acolman · Estado de México</p>',
    '<p class="h-date">05 · Junio · 2027</p>\n      <p class="h-city">Ciudad de México</p>')
# scroll: textos suben/desvanecen/blur; foto solo sube 70px
rep('''  gsap.to('#heroBg', {
    yPercent: 22, ease: 'none',
    scrollTrigger: { trigger: '#hero', start: 'top top', end: 'bottom top', scrub: true }
  });''', '''  gsap.to('#heroBg', {
    y: -70, ease: 'none',
    scrollTrigger: { trigger: '#hero', start: 'top top', end: 'bottom top', scrub: true }
  });
  if (!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    gsap.fromTo('#hCnt', { y: 0, opacity: 1, filter: 'blur(0px)' }, {
      y: -110, opacity: 0, filter: 'blur(10px)', ease: 'none', immediateRender: false,
      scrollTrigger: { trigger: '#hero', start: 'top top', end: 'bottom top', scrub: true }
    });
  }''')

# ───────── INVITACIÓN + FRASE ─────────
rep('<h2 class="heading rvc">César &amp; Neidy</h2>', '<h2 class="heading rvc foil-text">Nubia Brisia &amp; Luis Ricardo</h2>')
rep('''    Sábado, 7 de Noviembre de 2026<br>
    Acolman, Estado de México''', '''    Sábado, 5 de junio de 2027<br>
    Ciudad de México''')
rep('<p class="qt-txt">Más valen dos que uno, porque obtienen más fruto de su esfuerzo. Si caen, el uno levanta al otro. ¡Ay del que cae y no tiene quien lo levante! Si dos se acuestan juntos, entrarán en calor; uno solo ¿cómo va a calentarse? Uno solo puede ser vencido, pero dos pueden resistir. ¡La cuerda de tres hilos no se rompe fácilmente!</p>\n    <span class="qt-sig">Eclesiastés 4:9-12</span>',
    '<p class="qt-txt">«Existe una influencia celestial sobre todas las cosas. A menudo, cuando suceden las cosas, no es por accidente. Un día, cuando miremos atrás a aquello que pareció coincidencia en nuestra vida, nos daremos cuenta de que quizás, después de todo, tal vez no haya sido así»… Dios no hace las cosas por «coincidencia», sino… por «DESIGNIO DIVINO».</p>\n    <span class="qt-sig">Thomas S. Monson / Ronald A. Rasband</span>')

# ───────── QUITAR secciones sin datos del cliente ─────────
for x in ['story', 'bridesmaids', 'godparents', 'songs', 'wishes', 'contact', 'surprise', 'spoiler']:
    drop(x)
# modal de la caja de regalo (la sustituye la lluvia de sobres)
a = s.find('<div class="gift-backdrop" id="gift-backdrop"'); b = s.find('<!-- 8. ÁLBUM COMPARTIDO -->')
assert a > 0 and b > a
s = s[:a] + s[b:]
put('gifts', '<!--@@SOBRES@@-->')

# ───────── COUNTDOWN ─────────
rep("const WED = new Date('2026-11-07T16:00:00');", "const WED = new Date('2027-06-05T11:00:00-06:00');")

# ───────── UBICACIONES ─────────
TEMPLE_ICO = ''
put('location', '''<section id="location">
  <!--@@INK:location@@-->
  <span class="lbl">¿Dónde y cuándo?</span>
  <h2 class="ttl">La Celebración</h2>
  <div class="gline"></div>

  <div class="loc-card">
    <p class="loc-type" style="text-align:center">✦  Ceremonia Religiosa</p>
    <h3 class="loc-name" style="text-align:center">Templo de la Ciudad de México</h3>
    <p class="loc-sub">La Iglesia de Jesucristo de los Santos de los Últimos Días</p>
    <div class="loc-time" style="text-align:center">11:00 <em>AM</em></div>
    <p class="loc-addr" style="text-align:center">@@CER_ADDR@@</p>
    <a href="https://www.google.com/maps/place/Mexico+City+Mexico+Temple/@19.4658419,-99.089404,17z/data=!3m1!4b1!4m6!3m5!1s0x85d1fbc4648b0ee7:0x61382b34e9618369!8m2!3d19.4658369!4d-99.0868291"
       target="_blank" rel="noopener" class="btn" style="max-width:310px;margin:0 auto">
      <svg class="loc-pin" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
      Ver en Google Maps
    </a>
  </div>

  <div class="loc-card">
    <p class="loc-type" style="text-align:center">✦  Recepción</p>
    <h3 class="loc-name" style="text-align:center">Salón Jardín D'Alan</h3>
    <div class="loc-time" style="text-align:center">4:00 <em>PM</em></div>
    <p class="loc-addr" style="text-align:center">@@REC_ADDR@@</p>
    <a href="https://www.google.com/maps/place/SALON+JARDIN+D+ALAN/@19.3383456,-99.0566118,17z/data=!3m1!4b1!4m6!3m5!1s0x85ce0281215de89d:0x3eec0be007e32e0c!8m2!3d19.3383406!4d-99.0540369"
       target="_blank" rel="noopener" class="btn" style="max-width:310px;margin:0 auto">
      <svg class="loc-pin" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
      Ver en Google Maps
    </a>
  </div>
</section>''')

# ───────── CALENDARIO ─────────
a = s.find('<a href="https://calendar.google.com/calendar/render?'); b = s.find('"', s.find('href="', a) + 6)
s = s[:a] + '<a href="https://calendar.google.com/calendar/render?action=TEMPLATE&text=Boda+de+Nubia+Brisia+%26+Luis+Ricardo&dates=20270605T110000/20270606T010000&ctz=America/Mexico_City&details=Ceremonia+religiosa+11:00+AM+-+Templo+de+la+Ciudad+de+M%C3%A9xico+%7C+Recepci%C3%B3n+4:00+PM+-+Sal%C3%B3n+Jard%C3%ADn+D%27Alan&location=Ciudad+de+M%C3%A9xico' + s[b:]

# ───────── ITINERARIO (solo lo confirmado) ─────────
it = get('itinerary')
r0 = it.find('<div class="tl-row"'); r1 = it.rfind('</div>\n  </div>\n</section>')
TEMPLE = '''<svg viewBox="0 0 64 64">
          <line x1="32" y1="2" x2="32" y2="12"/>
          <path d="M28 20 L32 10 L36 20 Z"/>
          <rect x="26" y="20" width="12" height="12"/>
          <rect x="12" y="32" width="40" height="26"/>
          <rect x="17" y="38" width="5" height="9" opacity=".7"/><rect x="42" y="38" width="5" height="9" opacity=".7"/>
          <path d="M28 58 V46 Q32 41 36 46 V58"/>
        </svg>'''
DOOR = it[it.find('<!-- Marco puerta doble -->') - 60: it.find('</svg></div>', it.find('<!-- Marco puerta doble -->')) + 6]
rows = '''<div class="tl-row" data-side="left">
      <div class="tl-orn"></div><div class="tl-pulse"></div><div class="tl-dot"></div>
      <div class="tl-row-inner">
        <div class="tl-ico" aria-hidden="true">''' + TEMPLE + '''</div>
        <p class="tl-t">11:00 AM</p><p class="tl-ev">Ceremonia Religiosa</p><p class="tl-de">Templo de la Ciudad de México</p>
      </div>
    </div>
    <div class="tl-row" data-side="right">
      <div class="tl-orn"></div><div class="tl-pulse"></div><div class="tl-dot"></div>
      <div class="tl-row-inner">
        <div class="tl-ico" aria-hidden="true"><svg viewBox="0 0 64 64">
          <rect x="10" y="10" width="44" height="50" rx="2"/>
          <line x1="32" y1="10" x2="32" y2="60"/>
          <circle cx="28" cy="36" r="1.6" fill="currentColor" stroke="none"/>
          <circle cx="36" cy="36" r="1.6" fill="currentColor" stroke="none"/>
          <path d="M10 18 Q32 6 54 18"/>
        </svg></div>
        <p class="tl-t">4:00 PM</p><p class="tl-ev">Recepción</p><p class="tl-de">Salón Jardín D'Alan</p>
      </div>
    </div>
  '''
it = it[:r0] + rows + it[r1:]
it = it.replace('</div>\n</section>', '</div>\n  <p class="tl-note">Muy pronto compartiremos el itinerario completo de la celebración.</p>\n</section>', 1) if it.count('</div>\n</section>') == 1 else it
it = it.replace('<section id="itinerary">', '<section id="itinerary">\n  <!--@@INK:itinerary@@-->', 1)
put('itinerary', it)

# ───────── DRESS CODE (lo llena el agente C) ─────────
put('dresscode', '<!--@@DRESSCODE@@-->')

# ───────── HOSPEDAJE (se construye con datos de hoteles) ─────────
put('lodging', '<!--@@HOSPEDAJE@@-->')

# ───────── FAMILIA ─────────
put('family', '''<section id="family" style="text-align:center">
  <!--@@INK:family@@-->
  <span class="eyebrow">Con la bendición de</span>
  <h2 class="heading-sm foil-text">Nuestras Familias</h2>
  <div class="fam-rings">
    <svg viewBox="0 0 62 26" width="62" height="26" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <circle cx="20" cy="13" r="11" fill="none" stroke="#D4AF37" stroke-width="1.3" opacity=".8"/>
      <circle cx="20" cy="13" r="7.5" fill="none" stroke="#D4AF37" stroke-width=".5" opacity=".38"/>
      <circle cx="42" cy="13" r="11" fill="none" stroke="#D4AF37" stroke-width="1.3" opacity=".8"/>
      <circle cx="42" cy="13" r="7.5" fill="none" stroke="#D4AF37" stroke-width=".5" opacity=".38"/>
      <polygon points="31,8.5 33.2,13 31,17.5 28.8,13" fill="#D4AF37" opacity=".6"/>
    </svg>
  </div>
  <div class="orn" style="margin-top:8px"><div class="orn-line"></div><div class="orn-diamond-sm"></div><div class="orn-diamond"></div><div class="orn-diamond-sm"></div><div class="orn-line"></div></div>

  <div class="fam-card" style="max-width:340px;margin:28px auto 0">
    <span class="fam-role-lbl">Padres de la Novia</span>
    <span class="fam-name">Aurelia<br>Benítez</span>
    <div class="fam-and"><div class="fam-and-line"></div><span class="fam-and-txt">&amp;</span><div class="fam-and-line"></div></div>
    <span class="fam-name">Ángel<br>Jaramillo <span class="fam-cross" aria-label="finado">†</span></span>

    <div class="fam-rule"></div>

    <span class="fam-role-lbl">Padres del Novio</span>
    <span class="fam-name">José Luis<br>González</span>
    <div class="fam-and"><div class="fam-and-line"></div><span class="fam-and-txt">&amp;</span><div class="fam-and-line"></div></div>
    <span class="fam-name">María Luisa<br>Ramírez</span>
  </div>
</section>''')

# ───────── PADRINOS: por confirmar ─────────
put('padrinos', '''<section id="padrinos">
  <span class="lbl">Nuestros</span>
  <h2 class="ttl">Padrinos</h2>
  <div class="gline"></div>
  <div class="pad-solo">
    <img class="pad-ic" src="icons/padrinos/anillos.svg" alt="" width="54" height="54" aria-hidden="true">
    <p class="pad-role">Por confirmar</p>
    <p class="pad-names">Muy pronto les presentaremos a nuestros padrinos.</p>
  </div>
</section>''')

# ───────── GALERÍA (la llena el agente D) ─────────
put('gallery', '<!--@@GALLERY@@-->')

# ───────── ÁLBUM ─────────
rep('<!-- Álbum de Elysium: el QR abre /album → panel-invitados.vercel.app/subir/boda-neidy-y-cesar -->',
    '<!-- Álbum de Elysium: el QR abre /album → panel-invitados.vercel.app/subir/boda-nubia-brisia-y-luis-ricardo -->')
rep('<div class="album-qr" data-fecha="2026-11-07">', '<div class="album-qr" data-fecha="2027-06-05">')
rep('<section id="album">', '<section id="album">\n  <!--@@INK:album@@-->')

# ───────── CLIMA (junio en CDMX) ─────────
rep('<div class="wx-pct">10<span>%</span></div>', '<div class="wx-pct">60<span>%</span></div>')
rep('<div class="wx-val">23°<span>C</span></div>', '<div class="wx-val">25°<span>C</span></div>')
rep('<div class="wx-val">8°<span>C</span></div>', '<div class="wx-val">13°<span>C</span></div>')
rep('<p class="wx-note">Noviembre en Acolman es seco y fresco — la noche baja bastante</p>',
    '<p class="wx-note">Junio es temporada de lluvias en la Ciudad de México</p>')
rep('<p class="wx-text">La tarde será templada y agradable, pero al caer la noche la temperatura desciende. Te recomendamos traer un abrigo, saco o chal elegante para disfrutar la fiesta con toda comodidad.</p>',
    '<p class="wx-text">Las mañanas suelen ser soleadas y agradables, pero por la tarde es común que caiga un chubasco y la noche refresca. Te recomendamos traer un paraguas y un saco o chal elegante.</p>')
rep('href="https://www.google.com/search?q=clima+Acolman+7+noviembre+2026"', 'href="https://www.google.com/search?q=clima+Ciudad+de+M%C3%A9xico+5+junio+2027"')
s = re.sub(r'(<script>[^<]*?initWeather[^<]*?)', r'\1', s)

# ───────── FAQ ─────────
a = s.find('<div class="faq-list" id="faqList">'); b = s.find('</section>', a)
faq = [
 ('¿A qué hora debo llegar?', 'Te pedimos llegar entre 15 y 20 minutos antes de la ceremonia, que inicia a las 11:00 AM en el Templo de la Ciudad de México. La recepción comienza a las 4:00 PM en el Salón Jardín D\'Alan.'),
 ('¿Puedo llevar acompañantes extras?', 'Con mucho cariño, hemos reservado este día especialmente para las personas indicadas en esta invitación. Agradecemos su comprensión al no añadir invitados adicionales.'),
 ('¿Pueden asistir niños?', 'Para permitir a todos nuestros invitados una velada de celebración, la asistencia es únicamente de adultos.'),
 ('¿Cuál es el código de vestimenta?', 'Formal. Esta es una noche para brillar juntos: vístete como te sientas cómodo y espectacular. Te pedimos evitar el color blanco, reservado para la novia.'),
 ('¿Las dos sedes están en el mismo lugar?', 'No. La ceremonia es en el Templo de la Ciudad de México y la recepción en el Salón Jardín D\'Alan. @@DIST_SEDES@@ Considera el traslado entre la ceremonia y la recepción.'),
 ('¿Qué clima hará?', 'Junio es temporada de lluvias en la Ciudad de México: mañanas soleadas y posibles chubascos por la tarde. Un paraguas y un saco o chal no sobran.'),
 ('¿Puedo tomar fotos?', 'Claro que sí. Solo te pedimos que durante la ceremonia guardes el teléfono para vivirla con nosotros. Después, todas las fotos que quieras, y súbelas a nuestro álbum de fotos.'),
]
items = '\n'.join('''    <div class="faq-item">
      <button class="faq-q" type="button" aria-expanded="false" aria-controls="faq-a%d">%s<span class="faq-ic" aria-hidden="true"></span></button>
      <div class="faq-a" id="faq-a%d"><p>%s</p></div>
    </div>''' % (i, q, i, t) for i, (q, t) in enumerate(faq))
s = s[:a] + '<div class="faq-list" id="faqList">\n' + items + '\n  </div>\n' + s[b:]

# ───────── RSVP (lo llena el agente D) ─────────
put('rsvp', '<!--@@RSVP@@-->')

# ───────── FOOTER ─────────
rep('<div class="ft-nms">César &amp; Neidy</div>', '<div class="ft-nms foil-text">Nubia Brisia &amp; Luis Ricardo</div>')
rep('<p class="ft-dt">07 · Noviembre · 2026</p>\n  <p class="ft-note">Acolman · Estado de México<br>Con amor, los novios</p>',
    '<p class="ft-dt">05 · Junio · 2027</p>\n  <p class="ft-note">Ciudad de México<br>Con amor, los novios</p>')

# ───────── JS: quitar inits de secciones eliminadas ─────────
for x in ["    initPadrinos();\n", "    initOneByOne('bridesmaids', 'dhFrame', 'dhDots');\n",
          "    initOneByOne('godparents', 'bmFrame', 'bmDots');\n", "    initRevealCards();\n",
          "    initLodging();\n", "    initTrays();\n", "    initGiftBox();\n"]:
    rep(x, '')

io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('ok', len(s))
