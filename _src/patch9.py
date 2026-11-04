# Parche 9: nombres del hero sin background-clip (iPhone los ocultaba), carrusel con giro más visible,
# secciones azules sin tintas: solo degradado en movimiento
import io, sys, re
P = r'C:/Users/aleja/boda-nubia-brisia-y-luis-ricardo/index.html'
s = io.open(P, encoding='utf-8').read()
def rep(o, n):
    global s
    c = s.count(o)
    if c != 1: sys.exit('ERR %d %r' % (c, o[:80]))
    s = s.replace(o, n)

# 1. nombres: color sólido navy (background-clip:text + transform + blur desaparece en Safari iOS)
rep("""  background:linear-gradient(100deg,#0A1430 0%,#1E3A8A 30%,#4A7BB7 48%,#1E3A8A 66%,#0A1430 100%);background-size:240% 100%;
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;
  animation:goldSweep 8s ease-in-out infinite;padding:.2em .45em;margin:-.2em -.45em}""",
"""  color:#1E3A8A;-webkit-text-fill-color:#1E3A8A;background:none;animation:none;padding:.2em .45em;margin:-.2em -.45em}""")
# el desvanecido al hacer scroll sin blur (filter + texto en iOS)
rep("""    gsap.fromTo('#hCnt', { y: 0, opacity: 1, filter: 'blur(0px)' }, {
      y: -110, opacity: 0, filter: 'blur(10px)', ease: 'none', immediateRender: false,""",
"""    gsap.fromTo('#hCnt', { y: 0, opacity: 1 }, {
      y: -110, opacity: 0, ease: 'none', immediateRender: false,""")

# 2. carrusel: giro más notorio y el arrastre nunca se queda trabado
rep("var AUTO = 0.3;", "var AUTO = 0.42;")
rep("var DWELL = 0.75;", "var DWELL = 0.45;")
rep("""    stage.addEventListener('pointercancel', function(e){ endDrag(e, true); });""",
"""    stage.addEventListener('pointercancel', function(e){ endDrag(e, true); });
    window.addEventListener('pointerup', function(e){ endDrag(e, false); });
    window.addEventListener('pointercancel', function(e){ endDrag(e, true); });
    setInterval(function(){ if(onScreen && !lbOpen && !pageHidden && !running) start(); }, 1500);""")

# 3. secciones azules: fuera las tintas, solo degradado en movimiento
n0 = len(re.findall(r"  <div class=\"ink-bg[^\"]*\" aria-hidden=\"true\"><i style=\"background-image:url\('ink/tri-dark-\w+\.webp'\)\"></i></div>\n", s))
s = re.sub(r"  <div class=\"ink-bg[^\"]*\" aria-hidden=\"true\"><i style=\"background-image:url\('ink/tri-dark-\w+\.webp'\)\"></i></div>\n", '', s)
print('tintas azules quitadas:', n0)
CSS = r'''
/* azul: degradado vivo sin assets */
#main-content > section:not(.sec-light){background:linear-gradient(160deg,#0A1430 0%,#13224A 28%,#1E3A8A 52%,#152B63 74%,#0A1430 100%)!important;
  background-size:100% 260%!important;animation:navyFlow 18s ease-in-out infinite alternate}
@keyframes navyFlow{0%{background-position:50% 0%}100%{background-position:50% 100%}}
@media(prefers-reduced-motion:reduce){#main-content > section:not(.sec-light){animation:none}}
'''
i = s.find('  </style>'); s = s[:i] + CSS + s[i:]
io.open(P, 'w', encoding='utf-8', newline='\n').write(s); print('ok')
