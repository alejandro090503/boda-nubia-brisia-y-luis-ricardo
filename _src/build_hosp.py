# Construye blocks/hosp.html + hosp.css (3 hoteles) a partir del parcial de boda-ana-y-miguel
import json, io, re
B = r'C:/Users/aleja/AppData/Local/Temp/claude/C--Users-aleja/61662fee-e927-4bfd-bf71-b8b93a534439/scratchpad/blocks/'
d = json.load(io.open(B + 'hoteles.json', encoding='utf-8'))
src_css = io.open(B + 'hosp_src.css', encoding='utf-8').read()
src = io.open(B + 'hosp_src.html', encoding='utf-8').read()

# ── CSS repintado ──
css = src_css
for a, b in [('rgba(227,192,143', 'rgba(212,175,55'), ('rgba(18,5,9', 'rgba(10,20,48'), ('rgba(183,110,121', 'rgba(74,123,183'),
             ('rgba(153,36,79', 'rgba(30,58,138'), ('#2a0b16', '#0A1430'), ('rgba(28,10,18', 'rgba(15,28,64'), ('#1b0b11', '#0F1C40'),
             ('rgba(74,16,40', 'rgba(19,34,74'), ('rgba(36,12,22', 'rgba(16,30,66'), ('#7a1f45', '#2B4C9A'), ('#6a1a3a', '#2B4C9A'),
             ('#3a0d1f', '#16275A')]:
    css = css.replace(a, b)
css = css.replace('.hs-map .leaflet-tile-pane{filter:sepia(.9) hue-rotate(295deg) saturate(1.9) brightness(.66) contrast(1.18)}',
                  '.hs-map .leaflet-tile-pane{filter:sepia(.55) hue-rotate(178deg) saturate(1.7) brightness(.78) contrast(1.12)}')
css = re.sub(r'<style>|</style>|<!--.*?-->', '', css, flags=re.S)
css = ('#hospedaje{--champ:#F7E7CE;--gold-lt:#F1DC8A;--metal:linear-gradient(135deg,#9C7A1E 0%,#D4AF37 30%,#FFF4CC 50%,#D4AF37 70%,#9C7A1E 100%);'
       "--sans:'Jost',sans-serif;--serif:'Playfair Display',serif;--text-soft:rgba(247,231,206,.9);--wine:#1E3A8A;--wine-deep:#0F1C40;--bg:#0A1430;--bg2:#13224A}\n"
       + css + '''
/* nubia: selector de hotel + mapa alto */
.hs-hsel{display:flex;justify-content:center;gap:10px;margin:0 0 18px}
.hs-hsel button{width:44px;height:44px;border-radius:50%;border:1px solid rgba(212,175,55,.45);background:rgba(10,20,48,.7);color:var(--champ);
  font-family:'Jost',sans-serif;font-weight:600;font-size:17px;cursor:pointer;transition:background .3s,color .3s,transform .3s}
.hs-hsel button.on{background:var(--metal);color:#0A1430;transform:scale(1.08);border-color:transparent}
.hs-hsel-cap{display:block;font-family:'Jost',sans-serif;font-weight:500;font-size:15px;color:var(--text-soft);margin:-8px 0 16px}
.hs-hotel .hs-fade{transition:opacity .3s ease}
.hs-hotel.is-swap .hs-fade{opacity:0}
#hospedaje .hs-map{height:580px}
#hospedaje .hs-frame-in{border-radius:28px}
.hs-mk-h .hs-mk-in{font-family:'Jost',sans-serif!important;font-weight:600}
''')
io.open(B + 'hosp.css', 'w', encoding='utf-8').write(css)

# ── HTML ──
H = d['hoteles']; R = d['recepcion']
def esc(t): return t.replace('&', '&amp;').replace('"', '&quot;')
html = '''<section id="hospedaje">
  <span class="lbl">Si vienes de fuera</span>
  <h2 class="ttl">Hospedaje Sugerido</h2>
  <div class="gline"></div>
  <div class="hs-wrap">
    <p class="hs-why">Te compartimos algunas opciones de hotel cercanas a la recepción para que descanses cómodo.</p>

    <div class="hs-toggle" id="hsToggle" data-view="list" role="tablist" aria-label="Ver hospedaje">
      <span class="hs-ind" aria-hidden="true"></span>
      <button type="button" class="hs-tab" role="tab" aria-selected="true" data-view="list">
        <svg viewBox="0 0 24 24"><line x1="9" y1="6" x2="20" y2="6"/><line x1="9" y1="12" x2="20" y2="12"/><line x1="9" y1="18" x2="20" y2="18"/><circle cx="4.5" cy="6" r="1"/><circle cx="4.5" cy="12" r="1"/><circle cx="4.5" cy="18" r="1"/></svg>Lista
      </button>
      <button type="button" class="hs-tab" role="tab" aria-selected="false" data-view="map">
        <svg viewBox="0 0 24 24"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>Mapa
      </button>
    </div>

    <div class="hs-flip">
      <div class="hs-card" id="hsCard">
        <div class="hs-face hs-front" id="hsFront">
          <article class="hs-hotel" id="hsHotel">
            <div class="hs-hsel" id="hsHsel" role="tablist" aria-label="Elegir hotel"></div>
            <div class="hs-gal">
              <button type="button" class="hs-arrow prev" aria-label="Foto anterior"><svg viewBox="0 0 24 24"><polyline points="15 18 9 12 15 6"/></svg></button>
              <button type="button" class="hs-arrow next" aria-label="Foto siguiente"><svg viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></svg></button>
              <div class="hs-orbit">
                <div class="hs-ring">
                  <div class="hs-vp" id="hsVp"><div class="hs-track" id="hsTrack"></div></div>
                </div>
                <div class="hs-badge" aria-hidden="true"><span id="hsBadge">1</span></div>
              </div>
            </div>
            <div class="hs-dots" id="hsDots"></div>
            <div class="hs-thumbs" id="hsThumbs"></div>
            <div class="hs-fade">
              <span class="hs-type" id="hsType"></span>
              <h3 class="hs-name" id="hsName"></h3>
              <p class="hs-addr" id="hsAddr"></p>
              <div class="hs-dist">
                <span class="hs-chip"><svg viewBox="0 0 24 24"><path d="M5 17h14M7 17l1.5-5h7L17 17M6 17v2M18 17v2"/><circle cx="8" cy="14.5" r=".6"/><circle cx="16" cy="14.5" r=".6"/></svg><b id="hsMin"></b></span>
                <span class="hs-chip"><svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg><b id="hsKm"></b></span>
                <span class="hs-dist-cap">a la recepción en Salón Jardín D'Alan</span>
              </div>
              <div class="hs-btns">
                <a class="hs-btn hs-btn--pri" id="hsBook" href="#" target="_blank" rel="noopener"><svg viewBox="0 0 24 24"><rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V5a4 4 0 018 0v2"/></svg>Reservar</a>
                <a class="hs-btn hs-btn--sec" id="hsGo" href="#" target="_blank" rel="noopener"><svg viewBox="0 0 24 24"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>Cómo llegar</a>
              </div>
            </div>
          </article>
        </div>
'''
# cara B (mapa) tal cual del parcial
a = src.find('        <!-- CARA B · MAPA -->'); b = src.find('      </div>\n    </div>\n\n    <!-- Aviso de transporte -->')
html += src[a:b].replace('Mapa del hotel y la recepción', 'Mapa de hoteles y recepción') + '''      </div>
    </div>
    <p class="hs-foot">Tiempos aproximados en auto sin tráfico.</p>
  </div>
</section>
'''
hotels_js = json.dumps([{'n': str(i + 1), 'type': h['tipo'], 'name': h['nombre'], 'lat': round(h['lat'], 6), 'lng': round(h['lon'], 6),
                          'addr': h['direccion'], 'km': h['km'], 'mi': h['mi'], 'min': h['min'], 'maps': h['maps'], 'book': h['reservar'],
                          'fotos': h['fotos'], 'ruta': [[round(p[0], 5), round(p[1], 5)] for p in h['ruta']]} for i, h in enumerate(H)], ensure_ascii=False)
venue_js = json.dumps({'n': '♥', 'type': 'Recepción', 'name': R['nombre'], 'lat': R['lat'], 'lng': R['lon'], 'addr': R['direccion'],
                       'dist': 'Sábado 5 de junio · 4:00 PM', 'maps': R['maps'], 'book': ''}, ensure_ascii=False)
js = '''<script>
(function(){
  var root=document.getElementById('hospedaje');
  if(!root||root.__hsInit)return; root.__hsInit=true;
  var RM=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var COARSE=window.matchMedia&&matchMedia('(pointer: coarse)').matches;
  function $(id){return document.getElementById(id);}
  var HOTELS=''' + hotels_js + ''';
  var VENUE=''' + venue_js + ''';
  HOTELS.forEach(function(h){h.dist=h.mi+' mi · '+h.min+' min a la recepción';});

  /* ── Lista: hotel actual + carrusel de fotos ── */
  var hi=0,pi=0,art=$('hsHotel'),track=$('hsTrack'),vp=$('hsVp'),dotsBox=$('hsDots'),thBox=$('hsThumbs'),sel=$('hsHsel');
  HOTELS.forEach(function(h,i){var b=document.createElement('button');b.type='button';b.textContent=h.n;
    b.setAttribute('aria-label','Hotel '+h.n+': '+h.name);b.addEventListener('click',function(){showHotel(i);});sel.appendChild(b);});
  function goPhoto(i){var n=track.children.length;pi=(i+n)%n;track.style.transform='translateX('+(-pi*100)+'%)';
    [].forEach.call(dotsBox.children,function(d,k){d.classList.toggle('on',k===pi);});
    [].forEach.call(thBox.children,function(d,k){d.classList.toggle('on',k===pi);});}
  function fill(h){
    track.innerHTML='';dotsBox.innerHTML='';thBox.innerHTML='';
    h.fotos.forEach(function(u,k){
      var im=document.createElement('img');im.src=u;im.alt=h.name+' · foto '+(k+1);im.width=500;im.height=500;im.decoding='async';track.appendChild(im);
      var d=document.createElement('button');d.type='button';d.setAttribute('aria-label','Foto '+(k+1));d.addEventListener('click',function(){goPhoto(k);});dotsBox.appendChild(d);
      var b=document.createElement('button');b.type='button';b.setAttribute('aria-label','Ver foto '+(k+1));
      var t=document.createElement('img');t.src=u;t.alt='';b.appendChild(t);b.addEventListener('click',function(){goPhoto(k);});thBox.appendChild(b);
    });
    $('hsBadge').textContent=h.n;$('hsType').textContent=h.type;$('hsName').textContent=h.name;$('hsAddr').textContent=h.addr;
    $('hsMin').textContent=h.min+' min';$('hsKm').textContent=h.km+' km · '+h.mi+' mi';
    $('hsBook').href=h.book;$('hsGo').href=h.maps;
    [].forEach.call(sel.children,function(b,k){b.classList.toggle('on',k===hi);b.setAttribute('aria-selected',String(k===hi));});
    goPhoto(0);
  }
  function showHotel(i){
    i=(i+HOTELS.length)%HOTELS.length; if(i===hi&&track.children.length)return; hi=i;
    if(RM||!track.children.length){fill(HOTELS[hi]);return;}
    art.classList.add('is-swap');setTimeout(function(){fill(HOTELS[hi]);art.classList.remove('is-swap');},300);
  }
  root.querySelector('.hs-arrow.prev').addEventListener('click',function(){goPhoto(pi-1);});
  root.querySelector('.hs-arrow.next').addEventListener('click',function(){goPhoto(pi+1);});
  var sx=0,sy=0;
  vp.addEventListener('touchstart',function(e){sx=e.touches[0].clientX;sy=e.touches[0].clientY;},{passive:true});
  vp.addEventListener('touchend',function(e){var dx=e.changedTouches[0].clientX-sx,dy=e.changedTouches[0].clientY-sy;
    if(Math.abs(dx)>36&&Math.abs(dx)>Math.abs(dy))goPhoto(dx<0?pi+1:pi-1);},{passive:true});
  fill(HOTELS[0]);

  /* ── Leaflet bajo demanda ── */
  var LP=null;
  function loadLeaflet(){
    if(window.L&&window.L.map)return Promise.resolve(window.L);
    if(LP)return LP;
    LP=new Promise(function(res,rej){
      var base='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/';
      if(!document.querySelector('link[data-hs-leaflet]')){
        var l=document.createElement('link');l.rel='stylesheet';l.href=base+'leaflet.min.css';l.setAttribute('data-hs-leaflet','');document.head.appendChild(l);}
      var s=document.createElement('script');s.src=base+'leaflet.min.js';s.async=true;
      s.onload=function(){res(window.L);};s.onerror=function(){LP=null;rej(new Error('leaflet'));};
      document.head.appendChild(s);
    });
    return LP;
  }

  /* ── Mapa ── */
  var map=null,bounds=null,sheet=$('hsSheet'),hint=$('hsHint');
  function fitAll(anim){
    if(!map)return;
    var o={paddingTopLeft:[46,96],paddingBottomRight:[70,120],maxZoom:15};
    if(anim&&!RM)map.flyToBounds(bounds,Object.assign({duration:.9},o));else map.fitBounds(bounds,o);
  }
  function openSheet(p){
    $('hsShNum').textContent=p.n;$('hsShType').textContent=p.type;$('hsShName').textContent=p.name;
    $('hsShAddr').textContent=p.addr;$('hsShDist').querySelector('span').textContent=p.dist;
    $('hsShMap').href=p.maps;var bk=$('hsShBook');
    if(p.book){bk.href=p.book;bk.style.display='';}else{bk.style.display='none';}
    sheet.classList.add('open');hint.classList.add('gone');
    var z=15,sh=sheet.offsetHeight||200;
    var target=map.unproject(map.project([p.lat,p.lng],z).add([0,sh/2+10]),z);
    if(RM)map.setView(target,z);else map.flyTo(target,z,{duration:1});
  }
  function closeSheet(){sheet.classList.remove('open');hint.classList.remove('gone');}
  $('hsShX').addEventListener('click',function(){closeSheet();fitAll(true);});

  function buildMap(L){
    if(map)return;
    map=L.map('hsMap',{zoomControl:false,attributionControl:true,scrollWheelZoom:false,
      dragging:!COARSE,tap:false,touchZoom:true,doubleClickZoom:true,zoomSnap:.25,minZoom:10,maxZoom:18});
    var esri='https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/';
    L.tileLayer(esri+'World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',{maxNativeZoom:16,maxZoom:18,
      attribution:'Tiles &copy; Esri — Esri, HERE, Garmin, &copy; OpenStreetMap'}).addTo(map);
    L.tileLayer(esri+'World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}',{maxNativeZoom:16,maxZoom:18}).addTo(map);
    map.attributionControl.setPrefix(false);
    bounds=L.latLngBounds([[VENUE.lat,VENUE.lng]]);
    HOTELS.forEach(function(h){
      L.polyline(h.ruta,{color:'#D4AF37',weight:9,opacity:.14,lineCap:'round',lineJoin:'round',interactive:false}).addTo(map);
      L.polyline(h.ruta,{color:'#F1DC8A',weight:3.5,opacity:.95,dashArray:'2 9',lineCap:'round',lineJoin:'round',className:'hs-route',interactive:false}).addTo(map);
      var ic=L.divIcon({className:'hs-divicon',iconSize:[46,46],iconAnchor:[23,23],
        html:'<div class="hs-mk-h" role="button" aria-label="Hotel '+h.n+': '+h.name+'"><span class="hs-pulse"></span><span class="hs-pulse b"></span><span class="hs-mk-ring"><span class="hs-mk-in">'+h.n+'</span></span></div>'});
      L.marker([h.lat,h.lng],{icon:ic,keyboard:true,zIndexOffset:500}).addTo(map).on('click',function(){openSheet(h);});
      bounds.extend([h.lat,h.lng]);h.ruta.forEach(function(p){bounds.extend(p);});
    });
    var rIcon=L.divIcon({className:'hs-divicon',iconSize:[128,38],iconAnchor:[64,46],
      html:'<div class="hs-mk-r" role="button" aria-label="Recepción: '+VENUE.name+'"><b>♥</b>Recepción</div>'});
    L.marker([VENUE.lat,VENUE.lng],{icon:rIcon,keyboard:true,zIndexOffset:900}).addTo(map).on('click',function(){openSheet(VENUE);});
    map.on('click',function(){if(sheet.classList.contains('open'))closeSheet();});
    fitAll(false);
    root.querySelectorAll('.hs-ctrl').forEach(function(b){b.addEventListener('click',function(){
      var z=b.getAttribute('data-z');
      if(z==='in')map.zoomIn(1);else if(z==='out')map.zoomOut(1);else{closeSheet();fitAll(true);}
    });});
    if(COARSE){
      var ov=$('hs2f'),tt;
      $('hsMap').addEventListener('touchmove',function(e){
        if(e.touches.length===1){ov.classList.add('on');clearTimeout(tt);tt=setTimeout(function(){ov.classList.remove('on');},1300);}
        else{ov.classList.remove('on');}
      },{passive:true});
      $('hsMap').addEventListener('touchend',function(){clearTimeout(tt);tt=setTimeout(function(){ov.classList.remove('on');},700);},{passive:true});
    }
    $('hsLoading').classList.add('gone');
  }
''' + src[src.find('  /* ── 5. Selector + giro 3D ── */'):src.find('</script>') + 9]
html += js
io.open(B + 'hosp.html', 'w', encoding='utf-8').write(html)
print('ok', len(html), len(css))
