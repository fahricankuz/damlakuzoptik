#!/usr/bin/env python3
"""Yarım Asır, Bölüm 2 (Usta Eli): index.html üretici. Zamanlamalar ve metin burada tek yerde durur."""
from pathlib import Path

D = 41.0

# görüntü klipleri: id, tür, kaynak, başlangıç, süre, hareket (ölçek başlangıç→bitiş, y kayması px)
SHOTS = [
    ("s-acilis",  "img",   "acilis.jpg",    0.0,  2.9,  (1.00, 1.08, 0)),
    ("s-sirkeci", "video", "sirkeci.mp4",   2.8,  4.6,  (1.00, 1.06, 0)),
    ("s-roportaj","video", "roportaj.mp4",  7.3,  7.7,  (1.00, 1.05, 0)),
    ("s-olcum",   "video", "olcum.mp4",     14.8, 3.9,  (1.00, 1.05, 0)),
    ("s-goz",     "img",   "goz.jpg",       18.5, 3.9,  (1.08, 1.02, 0)),
    ("s-detay1",  "video", "detay1.mp4",    22.2, 1.6,  (1.00, 1.03, 0)),
    ("s-detay2",  "video", "detay2.mp4",    23.7, 1.55, (1.03, 1.00, 0)),
    ("s-detay3",  "video", "detay3.mp4",    25.15,1.55, (1.00, 1.03, 0)),
    ("s-detay4",  "video", "detay4.mp4",    26.6, 2.6,  (1.03, 1.00, 0)),
    ("s-bugun",   "video", "bugun.mp4",     28.9, 4.6,  (1.00, 1.04, 0)),
]
FADE = {"s-sirkeci": 0.35, "s-roportaj": 0.4, "s-olcum": 0.35, "s-goz": 0.35, "s-detay1": 0.45,
        "s-detay2": 0.4, "s-detay3": 0.4, "s-detay4": 0.4, "s-bugun": 0.5}

# altyazı grupları: id, [(kelime, zaman)], bitiş  (anlatım kelime zamanları + yerleşim farkı)
O1, O2, O3 = 3.00, 15.10 - 3.62, 29.20 - 9.18
CAPS = [
    ("c1", [("Hikâye,", 0.00+O1), ("Sirkeci'nin", 0.80+O1), ("saat", 1.44+O1), ("ve", 1.80+O1)], 4.85),
    ("c2", [("gözlük", 1.92+O1), ("çarşısında", 2.32+O1), ("başladı.", 2.88+O1)], 6.55),
    ("c3", [("Önce", 3.68+O2), ("gözü", 3.96+O2), ("ölçmeyi", 4.24+O2), ("öğrendi.", 4.64+O2)], 16.85),
    ("c4", [("Sonra", 5.44+O2), ("camı,", 5.80+O2), ("sonra", 6.40+O2), ("çerçeveyi;", 6.64+O2)], 18.95),
    ("c5", [("her", 7.60+O2), ("birini", 7.76+O2), ("bir", 8.16+O2), ("yüze", 8.36+O2), ("göre.", 8.64+O2)], 21.20),
    ("c6", [("Yarım", 9.227+O3), ("asır", 9.52+O3), ("sonra", 9.80+O3), ("bile", 10.04+O3), ("ölçü", 10.32+O3), ("aynı:", 10.64+O3)], 31.15),
    ("c7", [("önce", 11.32+O3), ("göz,", 11.64+O3), ("sonra", 12.28+O3), ("gözlük.", 12.52+O3)], 33.60),
]
# Fahri Kuz'un kendi sesi: 90'lar röportajı (kaynak − 308.7) ve tanıtım filmi (kaynak − 8.7)
R1, R2 = -308.7, 22.4 - 31.1
QUOTES = [
    ("q1", [("“Sekiz", 315.62+R1), ("yaşta", 315.88+R1), ("yetiştirildik,", 316.18+R1), ("tabirle.", 317.02+R1)], 9.60),
    ("q2", [("Küçük", 318.42+R1), ("yaşlarda", 318.58+R1), ("işe", 319.02+R1), ("başladık", 319.22+R1)], 11.45),
    ("q3", [("ve", 320.24+R1), ("zamanla", 320.36+R1), ("işi", 321.26+R1), ("çok", 321.50+R1), ("özümsedik,", 322.08+R1), ("benimsedik.”", 322.80+R1)], 15.00),
    ("q4", [("“Camının", 31.28+R2), ("bombesinden", 32.18+R2), ("rengine", 33.30+R2), ("kadar,", 33.86+R2)], 25.45),
    ("q5", [("kaplamasına", 34.28+R2), ("kadar", 34.92+R2), ("hepsini", 35.16+R2)], 26.75),
    ("q6", [("kendimiz", 35.60+R2), ("tespit", 36.66+R2), ("ediyoruz.”", 37.08+R2)], 29.00),
]
PLACES = []

def fontfaces():
    out = []
    for fam, file, w, st in [
        ("Cormorant Garamond", "cormorant-garamond", 300, "normal"), ("Cormorant Garamond", "cormorant-garamond", 300, "italic"),
        ("Cormorant Garamond", "cormorant-garamond", 400, "italic"), ("Cormorant Garamond", "cormorant-garamond", 500, "italic"),
        ("Inter Local", "inter", 500, "normal"), ("Inter Local", "inter", 600, "normal")]:
        for sub, rng in [("latin", "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122"),
                         ("latin-ext", "U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1E9F,U+20A0-20C0,U+2C60-2C7F,U+A720-A7FF")]:
            out.append(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};font-display:block;"
                       f"src:url('assets/fonts/{file}-{sub}-{w}-{st}.woff2') format('woff2');unicode-range:{rng};}}")
    return "\n".join(out)

def words(ws, cls):
    return " ".join(f'<span class="{cls}">{w}</span>' for w, _ in ws)

MEDIA_START = {}
shots_html = []
for i, (sid, kind, src, st, du, _) in enumerate(SHOTS):
    z = 10 + i
    if i + 1 < len(SHOTS) and SHOTS[i+1][3] <= st + du + 0.01:
        du = max(du, SHOTS[i+1][3] - st + FADE.get(SHOTS[i+1][0], 0.25) + 0.05)
    if kind == "img":
        shots_html.append(
            f'<div id="{sid}" class="clip shot" data-start="{st}" data-duration="{du}" data-track-index="1" style="z-index:{z}">'
            f'<img id="{sid}-m" class="shot-media" src="assets/media/{src}" alt=""></div>')
    else:
        shots_html.append(
            f'<div id="{sid}-w" class="shot-wrap" style="z-index:{z}">'
            f'<video id="{sid}" class="clip shot-video" data-start="{st}" data-duration="{du}" data-track-index="2" '
            f'data-media-start="{MEDIA_START.get(sid,0)}" src="assets/media/{src}" muted playsinline></video></div>')

caps_html = []
for cid, ws, end in CAPS:
    st = ws[0][1] - 0.12
    caps_html.append(f'<p id="{cid}" class="clip cap" data-start="{st:.2f}" data-duration="{end-st:.2f}" data-track-index="4">{words(ws, "w")}</p>')
for qid, ws, end in QUOTES:
    st = ws[0][1] - 0.15
    caps_html.append(f'<p id="{qid}" class="clip quote" data-start="{st:.2f}" data-duration="{end-st:.2f}" data-track-index="4">{words(ws, "qw")}</p>')

places_html = "".join(
    f'<div id="{pid}" class="clip place" data-start="{t:.2f}" data-duration="{17.9-t:.2f}" data-track-index="3" style="top:{250+i*76}px">'
    f'<span class="place-in"><span class="rule"></span>{name}</span></div>'
    for i, (pid, name, t) in enumerate(PLACES))

tl = []
for sid, kind, src, st, du, (s0, s1, dy) in SHOTS:
    tgt = f"#{sid}-m" if kind == "img" else f"#{sid}-w"
    tl.append(f'tl.fromTo("{tgt}",{{scale:{s0},y:0}},{{scale:{s1},y:{dy},duration:{du},ease:"none"}},{st});')
    # kısa geçiş: bir sonraki klip 0.25 sn içinde opaklıkla gelir
    if st > 0:
        el = f"#{sid}"
        tl.append(f'tl.fromTo("{el}",{{opacity:0}},{{opacity:1,duration:{FADE.get(sid,0.25)},ease:"power1.inOut"}},{st});')
for cid, ws, end in CAPS:
    st = ws[0][1] - 0.12
    tl.append(f'tl.fromTo("#{cid}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{st:.2f});')
    tl.append(f'tl.to("#{cid}",{{opacity:0,duration:0.2,ease:"power1.in"}},{end-0.22:.2f});')
    for j, (_, t) in enumerate(ws):
        tl.append(f'tl.fromTo("#{cid} .w:nth-child({j+1})",{{opacity:0.32}},{{opacity:1,duration:0.18,ease:"power1.out"}},{t:.2f});')
for qid, ws, end in QUOTES:
    st = ws[0][1] - 0.15
    tl.append(f'tl.fromTo("#{qid}",{{opacity:0,y:18}},{{opacity:1,y:0,duration:0.45,ease:"power3.out"}},{st:.2f});')
    tl.append(f'tl.to("#{qid}",{{opacity:0,duration:0.25,ease:"power1.in"}},{end-0.27:.2f});')
    for j, (_, t) in enumerate(ws):
        tl.append(f'tl.fromTo("#{qid} .qw:nth-child({j+1})",{{opacity:0.3}},{{opacity:1,duration:0.22,ease:"power1.out"}},{t:.2f});')
for pid, name, t in PLACES:
    tl.append(f'tl.fromTo("#{pid} .place-in",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},{t:.2f});')
    tl.append(f'tl.to("#{pid} .place-in",{{opacity:0,duration:0.3}},17.55);')

html = f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<style>
{fontfaces()}
:root {{ --ground:#0b0907; --paper:rgba(255,250,240,.95); --gold:#d6c29a; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:var(--ground); }}
#root {{ position:relative; width:100%; height:100%; overflow:hidden; background:var(--ground); }}
.shot, .shot-wrap {{ position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:hidden; }}
.shot-media {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; transform-origin:50% 40%; }}
.shot-wrap {{ transform-origin:50% 40%; }}
.shot-video {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
#shade {{ position:absolute; inset:0; z-index:40; pointer-events:none;
  background:linear-gradient(180deg, rgba(11,9,7,.55) 0%, rgba(11,9,7,0) 20%, rgba(11,9,7,0) 46%, rgba(11,9,7,.62) 60%, rgba(11,9,7,.86) 72%, rgba(11,9,7,.9) 100%); }}
.cap {{ position:absolute; left:90px; right:170px; top:1110px; z-index:60; font-family:'Inter Local',Inter,sans-serif; font-weight:500;
  font-size:54px; line-height:1.28; letter-spacing:-.008em; color:var(--paper); }}
.quote {{ position:absolute; left:90px; right:150px; top:1040px; z-index:60; font-family:'Cormorant Garamond',serif; font-style:italic;
  font-weight:400; font-size:86px; line-height:1.06; color:var(--paper); }}
.w, .qw {{ display:inline; }}
#who, #who2 {{ position:absolute; left:90px; top:1300px; z-index:60; }}
.label, .place-in {{ font-family:'Inter Local',Inter,sans-serif; font-weight:600; font-size:28px; letter-spacing:.38em; color:var(--gold); text-transform:uppercase; white-space:nowrap; }}
.place-in, #marker-in {{ font-size:36px; letter-spacing:.3em; color:var(--paper); text-shadow:0 2px 22px rgba(0,0,0,.9), 0 0 4px rgba(0,0,0,.7); }}
.rule {{ display:inline-block; width:56px; height:1px; background:var(--gold); vertical-align:middle; margin-right:22px; }}
.place {{ position:absolute; left:90px; z-index:60; }}
.place-in {{ display:inline-block; }}
#scrim {{ position:absolute; left:0; top:0; width:1080px; height:900px; z-index:55; background:radial-gradient(120% 90% at 0% 18%, rgba(11,9,7,.78) 0%, rgba(11,9,7,.45) 38%, rgba(11,9,7,0) 70%); }}
#marker {{ position:absolute; left:90px; top:250px; z-index:60; }}
#open {{ position:absolute; left:0; right:0; top:760px; z-index:60; text-align:center; }}
#open-h {{ font-family:'Cormorant Garamond',serif; font-weight:300; font-size:184px; line-height:1; letter-spacing:-.01em; color:var(--paper); }}
#open-s {{ margin-top:44px; font-family:'Inter Local',Inter,sans-serif; font-weight:500; font-size:28px; letter-spacing:.34em; color:rgba(255,250,240,.66); padding-left:.34em; }}
#band {{ position:absolute; inset:0; z-index:45; background:var(--ground); }}
#band-img {{ position:absolute; left:0; top:656px; width:1080px; height:608px; object-fit:cover; }}
#band-top {{ position:absolute; left:0; right:0; top:540px; text-align:center; }}
#band-bot {{ position:absolute; left:0; right:0; top:1320px; text-align:center; font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:300; font-size:58px; color:rgba(255,250,240,.82); }}
#end {{ position:absolute; inset:0; z-index:45; }}
#end-img {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
#end-t {{ position:absolute; left:0; right:0; top:720px; text-align:center; }}
#end-h {{ font-family:'Cormorant Garamond',serif; font-weight:300; font-size:176px; line-height:1; color:var(--paper); }}
#end-bar {{ width:72px; height:1px; background:var(--gold); margin:58px auto 46px; }}
#end-tag {{ font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:300; font-size:58px; color:rgba(255,250,240,.82); }}
#end-ep {{ margin-top:52px; font-family:'Inter Local',Inter,sans-serif; font-weight:500; font-size:28px; letter-spacing:.6em; padding-left:.6em; color:var(--gold); }}
#end-next {{ margin-top:120px; font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:300; font-size:44px; color:rgba(255,250,240,.58); }}
#black {{ position:absolute; inset:0; z-index:90; background:#000; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
{chr(10).join(shots_html)}
<div id="end" data-layout-allow-occlusion class="clip" data-start="33.3" data-duration="{D-33.3:.1f}" data-track-index="1">
  <img id="end-img" src="assets/media/kapanis_zemin.jpg" alt="">
  <div id="end-t" data-layout-allow-occlusion>
    <div id="end-h">Yarım Asır</div>
    <div id="end-bar"></div>
    <div id="end-tag">Usta eli</div>
    <div id="end-ep">BÖLÜM 2</div>
    <div id="end-next">Hikâye devam ediyor.</div>
  </div>
</div>
<div id="shade"></div>
<div id="open" class="clip" data-start="0" data-duration="3.0" data-track-index="3">
  <div id="open-h">Sekiz yaşında.</div>
  <div id="open-s">YARIM ASIR · BÖLÜM 2</div>
</div>
<div id="marker" class="clip" data-start="2.95" data-duration="4.5" data-track-index="3"><span id="marker-in" class="label"><span class="rule"></span>Sirkeci</span></div>
{places_html}
{chr(10).join(caps_html)}
<div id="who" class="clip" data-start="6.7" data-duration="8.4" data-track-index="3"><span id="who-in" class="label"><span class="rule"></span>Fahri Kuz</span></div>
<div id="who2" class="clip" data-start="22.5" data-duration="6.6" data-track-index="3"><span id="who2-in" class="label"><span class="rule"></span>Fahri Kuz</span></div>
<div id="black" data-layout-allow-occlusion class="clip" data-start="40.0" data-duration="1.0" data-track-index="5"></div>
<audio id="miks" class="clip" data-start="0" data-duration="{D}" data-track-index="6" data-volume="1" src="assets/audio/miks.m4a"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
// açılış
tl.fromTo("#open-h",{{opacity:0.0,y:10}},{{opacity:1,y:0,duration:0.7,ease:"power3.out"}},0);
tl.fromTo("#open-s",{{opacity:0}},{{opacity:1,duration:0.6,ease:"power2.out"}},0.5);
tl.to("#open-h,#open-s",{{opacity:0,duration:0.4,ease:"power1.in"}},2.55);
tl.fromTo("#marker-in",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.45,ease:"power3.out"}},3.0);
tl.to("#marker-in",{{opacity:0,duration:0.3}},7.1);
{chr(10).join(tl)}
// alıntı imzaları
tl.fromTo("#who-in",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.45,ease:"power3.out"}},6.8);
tl.to("#who-in",{{opacity:0,duration:0.3}},14.75);
tl.fromTo("#who2-in",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.45,ease:"power3.out"}},22.6);
tl.to("#who2-in",{{opacity:0,duration:0.3}},28.75);
// kapanış
tl.fromTo("#end",{{opacity:0}},{{opacity:1,duration:1.0,ease:"power1.inOut"}},33.3);
tl.fromTo("#end-img",{{scale:1.08}},{{scale:1.0,duration:7.7,ease:"none"}},33.3);
tl.fromTo("#end-h",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.9,ease:"power3.out"}},33.9);
tl.fromTo("#end-bar",{{scaleX:0}},{{scaleX:1,duration:0.7,ease:"power2.inOut"}},34.6);
tl.fromTo("#end-tag",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.7,ease:"power3.out"}},34.95);
tl.fromTo("#end-ep",{{opacity:0}},{{opacity:1,duration:0.6}},36.0);
tl.fromTo("#end-next",{{opacity:0}},{{opacity:1,duration:0.8}},37.0);
tl.fromTo("#black",{{opacity:0}},{{opacity:1,duration:0.9,ease:"power1.in"}},40.0);
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
Path(__file__).with_name("index.html").write_text(html, encoding="utf-8")
print("index.html yazıldı")
