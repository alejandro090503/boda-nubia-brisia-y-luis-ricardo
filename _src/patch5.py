# Parche 5: sobre propio B&R (imagen + video del cliente)
import io, sys
P = r'C:/Users/aleja/boda-nubia-brisia-y-luis-ricardo/index.html'
s = io.open(P, encoding='utf-8').read()
def rep(o, n):
    global s
    c = s.count(o)
    if c != 1: sys.exit('ERR %d %r' % (c, o[:80]))
    s = s.replace(o, n)
rep('fotos-clientes/audio/boda-metzli-y-rodolfo/sobre-apertura.mp4', 'fotos-clientes/boda-nubia-brisia-luis-ricardo/video/sobre-apertura.mp4')
rep('object-position:center;z-index:2;transform:scale(1.18)}', 'object-position:center;z-index:2}')
rep('object-position:center;z-index:3;opacity:0;transform:scale(1.18)}', 'object-position:center;z-index:3;opacity:0}')
rep('''  color:rgba(212,175,55,.8);opacity:0;cursor:pointer;white-space:nowrap;z-index:10;
  text-shadow:0 1px 6px rgba(0,0,0,.5);''', '''  color:#1E3A8A;font-weight:600;opacity:0;cursor:pointer;white-space:nowrap;z-index:10;
  text-shadow:0 0 10px rgba(255,255,255,.9),0 0 3px rgba(255,255,255,.8);''')
rep('#envelope-screen{position:fixed;inset:0;z-index:10000;overflow:hidden;cursor:pointer;opacity:0;background:#000000}',
    '#envelope-screen{position:fixed;inset:0;z-index:10000;overflow:hidden;cursor:pointer;opacity:0;background:#F4EFE3}')
io.open(P, 'w', encoding='utf-8', newline='\n').write(s); print('ok')
