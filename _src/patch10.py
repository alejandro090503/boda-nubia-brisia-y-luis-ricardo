# Parche 10: correcciones del cliente (7-nov)
import io, sys, re
P = r'C:/Users/aleja/boda-nubia-brisia-y-luis-ricardo/index.html'
s = io.open(P, encoding='utf-8').read()
def rep(o, n, cnt=1):
    global s
    c = s.count(o)
    if c != cnt: sys.exit('ERR %d %r' % (c, o[:90]))
    s = s.replace(o, n)

# 1. video de la caminata más largo
rep('video/intro.mp4"', 'video/intro-v2.mp4"')
rep('setTimeout(finishIntro, 14000);', 'setTimeout(finishIntro, 18000);')

# 2. ceremonia 10:00 AM
rep('<div class="loc-time" style="text-align:center">11:00 <em>AM</em></div>', '<div class="loc-time" style="text-align:center">10:00 <em>AM</em></div>')
rep('<p class="tl-t">11:00 AM</p>', '<p class="tl-t">10:00 AM</p>')
rep('20270605T110000', '20270605T100000')
rep("const WED = new Date('2027-06-05T11:00:00-06:00');", "const WED = new Date('2027-06-05T10:00:00-06:00');")
s = s.replace('Ceremonia+religiosa+11:00+AM', 'Ceremonia+religiosa+10:00+AM')
rep('que inicia a las 11:00 AM', 'que inicia a las 10:00 AM')
if '11:00' in s: sys.exit('queda 11:00')

# 3. itinerario
rep('<p class="tl-t tl-t--pc">Por confirmar</p><p class="tl-ev">Entrada de los Novios</p>', '<p class="tl-t">5:00 PM</p><p class="tl-ev">Entrada de los Novios</p>')
rep('<p class="tl-t tl-t--pc">Por confirmar</p><p class="tl-ev">Cena</p>', '<p class="tl-t">6:00 PM</p><p class="tl-ev">Cena</p>')
rep('<p class="tl-t tl-t--pc">Por confirmar</p><p class="tl-ev">Fiesta</p>', '<p class="tl-t">7:00 PM</p><p class="tl-ev">Fiesta</p>')
s = re.sub(r'\s*<p class="tl-note">Los horarios marcados como «Por confirmar» los compartiremos muy pronto\.</p>', '', s, count=1)

# 4. código de vestimenta: colores para damas + 3 diseños más
rep('''  <div class="dcx-group dcx-avoid">''', '''  <div class="dcx-group">
    <p class="dcx-gttl">Para damas</p>
    <div class="dcx-palette">
      <div class="dcx-item"><span class="dcx-dot" style="background:#B3122B"></span><span class="dcx-name">Rojo</span></div>
      <div class="dcx-item"><span class="dcx-dot" style="background:#E89AB4"></span><span class="dcx-name">Rosa</span></div>
      <div class="dcx-item"><span class="dcx-dot" style="background:#141414"></span><span class="dcx-name">Negro</span></div>
    </div>
  </div>

  <div class="dcx-group dcx-avoid">''')
rep("""      {src:'dresscode/dama-3.png', cap:'Vestido largo champán'}]}""",
"""      {src:'dresscode/dama-3.png', cap:'Vestido largo champán'},
      {src:'dresscode/dama-boceto.png', cap:'Vestido de gala con drapeado'},
      {src:'dresscode/dama-negro.png', cap:'Vestido negro clásico'},
      {src:'dresscode/dama-jumpsuit.png', cap:'Jumpsuit elegante'}]}""")

# 5. regalos: leyenda del cliente (sin mesa de regalos ni sobres)
rep('<section id="sobres" aria-label="Lluvia de sobres" class="has-ink">', '<section id="sobres" aria-label="Regalos" class="has-ink">')
rep('''    <span class="lbl">Celebra con nosotros</span>
    <h2 class="ttl">Lluvia de Sobres</h2>''', '''    <span class="lbl">Celebra con nosotros</span>
    <h2 class="ttl">Regalos</h2>''')
rep('<span class="sbx-desc">Si deseas obsequiarnos algo, el día de la boda habrá un buzón para recibir tu sobre con mucho cariño.</span>',
    '<span class="sbx-desc">"Lo más importante para nosotros es tenerte ese día compartiendo nuestra alegría. No tendremos mesa de regalos ni habrá sobres; si de corazón nace tener un detalle con nosotros, ¡lo que decidas y te nazca estará perfecto!"</span>')
rep('<li><a href="#sobres">Lluvia de sobres</a></li>', '<li><a href="#sobres">Regalos</a></li>')

# 6. galería: foto e imagen intercaladas
G = [  # (archivo, ancho, alto, alt, foco)
 ('foto1.jpg', 714, 953, 'Nubia y Luis Ricardo frente al templo', '50% 50%'),
 ('g-decirte.jpg', 451, 877, 'Decirte que eres el amor de mi vida es poco', '50% 30%'),
 ('g-templo-escalera.jpg', 649, 764, 'Nubia y Luis Ricardo subiendo al templo', '50% 50%'),
 ('g-columpio.jpg', 720, 987, 'Ilustración de una pareja en columpios', '50% 50%'),
 ('g-templo-fuente.jpg', 760, 1013, 'Nubia y Luis Ricardo junto a la fuente del templo', '50% 60%'),
 ('g-deseo.jpg', 512, 391, 'Mi único deseo es estar con Dios y contigo toda la vida', '50% 50%'),
 ('g-selfie.jpg', 673, 636, 'Nubia y Luis Ricardo sonriendo', '50% 40%'),
 ('g-casualidades.jpg', 720, 828, 'No sé cuántas casualidades tuvieron que ocurrir para coincidir contigo', '50% 50%'),
 ('foto2.jpg', 624, 874, 'Nubia y Luis Ricardo vestidos de novios frente al templo', '50% 0%'),
 ('g-caricatura.jpg', 610, 760, 'Caricatura de Nubia y Luis Ricardo', '50% 50%'),
 ('foto3.jpg', 609, 475, 'Nubia y Luis Ricardo sonriendo juntos', '50% 50%'),
 ('g-abrazo.jpg', 720, 932, 'Ilustración de una pareja abrazada', '50% 50%'),
]
N = len(G)
cards = []
for i, (f, w, h, alt, op) in enumerate(G):
    land = ' g3-land' if w > h * 1.1 else ''
    cards.append(f'''      <button class="g3-card{land}" type="button" data-i="{i}" style="--ar:{w}/{h}" aria-label="Ver foto {i+1} de {N}">
        <span class="g3-frame"><img src="fotos/{f}" alt="{alt}" width="{w}" height="{h}" decoding="async" style="object-position:{op}"></span>
        <span class="g3-mirror" aria-hidden="true"><img src="fotos/{f}" alt="" width="{w}" height="{h}" decoding="async" style="object-position:{op}"></span>
      </button>''')
a = s.index('    <div class="g3-track" id="g3-track">\n') + len('    <div class="g3-track" id="g3-track">\n')
b = s.index('    </div>\n  </div>\n\n  <div class="g3-dots"', a)
assert b > a
s = s[:a] + '\n'.join(cards) + '\n' + s[b:]
rep('<div class="g3-dots" id="g3-dots" aria-hidden="true"><i></i><i></i><i></i></div>', '<div class="g3-dots" id="g3-dots" aria-hidden="true">' + '<i></i>' * N + '</div>')
rep('<figcaption id="g3-lb-count">1 / 3</figcaption>', '<figcaption id="g3-lb-count">1 / %d</figcaption>' % N)

io.open(P, 'w', encoding='utf-8', newline='\n').write(s); print('ok')
