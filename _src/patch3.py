# Parche 3: video de intro (Jesús acompañando a los novios) entre el sobre y la invitación, con la música del reel
import io, sys
P='index.html'; s=io.open(P,encoding='utf-8').read()
def rep(o,n):
    global s
    c=s.count(o)
    if c!=1: sys.exit('ERR %d %r'%(c,o[:70]))
    s=s.replace(o,n)
SB='https://bsjoelxktbvlavfoozhk.supabase.co/storage/v1/object/public/fotos-clientes/'
rep('<div id="env-flash"></div>', '''<div id="env-flash"></div>
<audio id="introAudio" preload="auto" src="'''+SB+'''audio/boda-nubia-brisia-luis-ricardo/intro-musica.mp3"></audio>
<div id="intro-screen" aria-hidden="true">
  <video id="introVid" src="'''+SB+'''boda-nubia-brisia-luis-ricardo/video/intro.mp4" poster="fotos/intro-poster.jpg" muted playsinline webkit-playsinline preload="auto"></video>
  <button id="introSkip" type="button">Saltar</button>
</div>''')
rep('  </style>', '''#intro-screen{position:fixed;inset:0;z-index:9998;background:#0A1430;display:none;opacity:1}
#intro-screen.on{display:block}
#introVid{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
#introSkip{position:absolute;right:16px;bottom:max(18px,env(safe-area-inset-bottom));min-height:44px;padding:0 18px;border-radius:999px;
  border:1px solid rgba(212,175,55,.6);background:rgba(10,20,48,.45);color:#F7E7CE;font-family:'Jost',sans-serif;font-weight:500;
  font-size:14px;letter-spacing:.18em;text-transform:uppercase;cursor:pointer}
  </style>''')
rep('''function startMusicOnOpen() {
  var aud = document.getElementById('bgMusic');''', '''function startMusicOnOpen() {
  if (window.__introOn) return;
  var aud = document.getElementById('bgMusic');''')
rep('''  function revealInvitation() {
    prepareInvitation();
    gsap.to(envFlash, {''', '''  function revealInvitation() {
    prepareInvitation();
    playIntro();
    gsap.to(envFlash, {''')
rep('''  function openEnvelope() {
    if (opened) return;
    opened = true;''', '''  /* ── INTRO: video de los novios con Jesús; la música del reel suena desde que se toca el sobre ── */
  window.__introOn = true;
  var introDone = false;
  function finishIntro(){
    if (introDone) return; introDone = true;
    var scr = document.getElementById('intro-screen'), ia = document.getElementById('introAudio');
    gsap.to(scr, { opacity: 0, duration: 1.2, ease: 'power2.inOut', onComplete: function(){ scr.style.display = 'none'; } });
    if (ia && !ia.paused) gsap.to(ia, { volume: 0, duration: 1.4, onComplete: function(){ try{ ia.pause(); }catch(e){} } });
    window.__introOn = false;
    setTimeout(startMusicOnOpen, 600);
    setTimeout(function(){ ScrollTrigger.refresh(); }, 1300);
  }
  function playIntro(){
    var scr = document.getElementById('intro-screen'), v = document.getElementById('introVid');
    if (!scr || !v) { finishIntro(); return; }
    scr.classList.add('on');
    v.addEventListener('ended', finishIntro);
    document.getElementById('introSkip').addEventListener('click', finishIntro);
    var p; try { p = v.play(); } catch(e) { finishIntro(); return; }
    if (p && p.catch) p.catch(function(){ finishIntro(); });
    setTimeout(finishIntro, 14000);
  }
  function unlockSong(){
    /* desbloquea la canción dentro del toque para poder darle play al terminar el video */
    var bm = document.getElementById('bgMusic');
    try { bm.muted = true; var q = bm.play(); if (q && q.then) q.then(function(){ bm.pause(); bm.currentTime = 0; bm.muted = false; }).catch(function(){ bm.muted = false; }); } catch(e) { bm.muted = false; }
  }

  function openEnvelope() {
    if (opened) return;
    opened = true;
    unlockSong();''')
io.open(P,'w',encoding='utf-8',newline='\n').write(s); print('ok')
