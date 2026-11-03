# Parche 7: corrige el fundido superior, cuenta regresiva y tarjetas de familia en champán
import io, sys
P = r'C:/Users/aleja/boda-nubia-brisia-y-luis-ricardo/index.html'
s = io.open(P, encoding='utf-8').read()
def rep(o, n):
    global s
    c = s.count(o)
    if c != 1: sys.exit('ERR %d %r' % (c, o[:80]))
    s = s.replace(o, n)

rep("""        st.push('rgba(' + c.join(',') + ',' + al.toFixed(3) + ') ' + (pos === 'bot' ? (t*h) : (h - t*h)).toFixed(1) + 'px');
      }
      if (pos === 'top') st.reverse();""", """        st.push('rgba(' + c.join(',') + ',' + al.toFixed(3) + ') ' + (t*h).toFixed(1) + 'px');
      }""")
rep("""      var h = diff > 200 ? 230 : 150;
      cross(A, 'bot', b, h, 0, .5);
      cross(Bs, 'top', a, h, .5, 1);""", """      var base = diff > 200 ? 260 : 160;
      var h = Math.round(Math.min(base, A.offsetHeight * .3, Bs.offsetHeight * .3));
      cross(A, 'bot', b, h, 0, .5);
      cross(Bs, 'top', a, h, .5, 1);""")

rep("#countdown.sec-light .cd-ring-item{background:radial-gradient(circle at 50% 35%,#FFFDF6,#F3E3C7)!important;box-shadow:0 10px 28px rgba(30,58,138,.14),inset 0 0 0 1px rgba(184,144,30,.35)!important}\n#countdown.sec-light .cd-ring-item *{color:#13224A}",
"""#countdown.sec-light{--cd-olive:#4A7BB7;--cd-gold:#A8811C;--cd-accent:#13224A;--cd-terra:#1E3A8A;border:none}
#countdown.sec-light .cd-wave-top,#countdown.sec-light .cd-wave-bot{display:none}
#countdown.sec-light .cd-num{text-shadow:none}
#countdown.sec-light .cd-ring-item *{text-shadow:none}""")

CSS = r'''
/* tarjetas de familia en champán */
#family.sec-light .fam-card{background:linear-gradient(180deg,#FFFBF1,#F6E9D1)!important;border:1px solid rgba(184,144,30,.55)!important;
  box-shadow:0 18px 40px rgba(30,58,138,.16),inset 0 0 0 6px rgba(255,255,255,.5)!important}
#family.sec-light .fam-card *{text-shadow:none!important}
'''
i = s.find('  </style>'); s = s[:i] + CSS + s[i:]
io.open(P, 'w', encoding='utf-8', newline='\n').write(s); print('ok')
