#!/usr/bin/env python3
"""Yarım Asır, Bölüm 1: index.html üretici. Zamanlamalar ve metin burada tek yerde durur."""
from pathlib import Path

D = 44.0

# görüntü klipleri: id, tür, kaynak, başlangıç, süre, hareket (ölçek başlangıç→bitiş, y kayması px)
SHOTS = [
    ("s-kapi",     "img",   "kapi.jpg",       0.0,  3.8,  (1.00, 1.07, 0)),
    ("s-kapiyakin","img",   "kapi_yakin.jpg", 3.8,  2.8,  (1.10, 1.03, 0)),
    ("s-muayene",  "img",   "muayene.jpg",    6.6,  2.4,  (1.02, 1.08, -20)),
    ("s-el",       "img",   "muayene_el.jpg", 9.0,  2.6,  (1.08, 1.02, 0)),
    ("s-grup",     "img",   "grup.jpg",       11.6, 1.8,  (1.00, 1.06, 0)),
    ("s-doksan",   "video", "doksanlar.mp4",  13.4, 4.8,  (1.00, 1.05, 0)),
    ("s-bugun",    "video", "bugun.mp4",      18.2, 4.1,  (1.00, 1.04, 0)),
    ("s-alinti",   "video", "alinti.mp4",     26.6, 8.6,  (1.00, 1.03, 0)),
]

# altyazı grupları: id, [(kelime, zaman)], bitiş
O1, O2, O3, O4 = 2.40, 2.92, 3.36, 6.20
CAPS = [
    ("c1", [("Yarım", .10+O1), ("asır", .34+O1), ("önce,", .60+O1), ("Aksaray'da", 1.20+O1)], 4.16),
    ("c2", [("küçük", 1.80+O1), ("bir", 2.10+O1), ("gözlükçü", 2.28+O1), ("dükkânı", 2.70+O1), ("açıldı.", 3.08+O1)], 6.20),
    ("c3", [("Gözler", 3.90+O2), ("ölçüldü,", 4.28+O2), ("camlar", 5.00+O2), ("kesildi,", 5.42+O2)], 9.10),
    ("c4", [("her", 6.22+O2), ("çerçeve", 6.46+O2), ("bir", 7.00+O2), ("yüze", 7.20+O2), ("göre", 7.44+O2), ("ayarlandı.", 7.66+O2)], 11.50),
    ("c5", [("Yıllar", 8.58+O3), ("içinde", 8.86+O3), ("o", 9.22+O3), ("dükkân,", 9.32+O3)], 13.30),
    ("c6", [("İstanbul'un", 9.92+O3), ("dört", 10.52+O3), ("bir", 10.76+O3), ("yanına", 10.94+O3), ("yayılan", 11.26+O3)], 14.98),
    ("c7", [("bir", 11.66+O3), ("zincire", 11.86+O3), ("dönüştü.", 12.24+O3)], 16.60),
    ("c8", [("Ve", 13.06+O4), ("o", 13.26+O4), ("usta,", 13.40+O4), ("Fahri", 13.96+O4), ("Kuz,", 14.30+O4)], 20.94),
    ("c9", [("bugün", 14.78+O4), ("hâlâ", 15.10+O4), ("aynı", 15.62+O4), ("tutkuyla", 15.86+O4)], 22.44),
    ("c10", [("gözlük", 16.30+O4), ("tasarlıyor.", 16.62+O4)], 23.30),
]
OQ = 26.6 - 73.0
QUOTES = [
    ("q1", [("“Biz", 73.40+OQ), ("önce", 73.68+OQ), ("bir", 73.96+OQ), ("optisyeniz,", 74.20+OQ)], 28.94),
    ("q2", [("sonra", 75.38+OQ), ("gözlük", 75.68+OQ), ("konusunda", 76.00+OQ), ("bir", 76.42+OQ), ("danışmanız,", 76.58+OQ)], 31.24),
    ("q3", [("ne", 77.68+OQ), ("tip", 77.88+OQ), ("yüze", 78.10+OQ), ("ne", 78.38+OQ), ("tip", 78.52+OQ), ("gözlük", 78.74+OQ), ("uyacağı", 79.12+OQ)], 33.12),
    ("q4", [("konusunda", 79.56+OQ), ("bir", 80.00+OQ), ("estetisyeniz.”", 80.26+OQ)], 35.10),
]
PLACES = [("p-aksaray", "Aksaray", 13.55), ("p-beyazit", "Beyazıt", 14.05), ("p-akmerkez", "Akmerkez", 14.55), ("p-atakoy", "Ataköy", 15.05)]

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

MEDIA_START = {'s-bugun': 0.9}
shots_html = []
for i, (sid, kind, src, st, du, _) in enumerate(SHOTS):
    z = 10 + i
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
    f'<div id="{pid}" class="clip place" data-start="{t:.2f}" data-duration="{17.9-t:.2f}" data-track-index="3" style="top:{250+i*64}px">'
    f'<span class="place-in"><span class="rule"></span>{name}</span></div>'
    for i, (pid, name, t) in enumerate(PLACES))

tl = []
for sid, kind, src, st, du, (s0, s1, dy) in SHOTS:
    tgt = f"#{sid}-m" if kind == "img" else f"#{sid}-w"
    tl.append(f'tl.fromTo("{tgt}",{{scale:{s0},y:0}},{{scale:{s1},y:{dy},duration:{du},ease:"none"}},{st});')
    # kısa geçiş: bir sonraki klip 0.25 sn içinde opaklıkla gelir
    if st > 0:
        el = f"#{sid}"
        tl.append(f'tl.fromTo("{el}",{{opacity:0}},{{opacity:1,duration:0.25,ease:"power1.out"}},{st});')
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
#who {{ position:absolute; left:90px; top:1300px; z-index:60; }}
.label, .place-in {{ font-family:'Inter Local',Inter,sans-serif; font-weight:600; font-size:28px; letter-spacing:.38em; color:var(--gold); text-transform:uppercase; white-space:nowrap; }}
.rule {{ display:inline-block; width:56px; height:1px; background:var(--gold); vertical-align:middle; margin-right:22px; }}
.place {{ position:absolute; left:90px; z-index:60; }}
.place-in {{ display:inline-block; text-shadow:0 1px 18px rgba(0,0,0,.85), 0 0 3px rgba(0,0,0,.6); }}
#c10 {{ top:1300px; }}
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
<div id="band" class="clip" data-start="22.3" data-duration="4.3" data-track-index="1">
  <img id="band-img" src="assets/media/imza.jpg" alt="">
  <div id="band-top" class="label">Kişiye özel tasarım</div>
  <div id="band-bot">Her gözlükten yalnızca bir tane.</div>
</div>
<div id="end" data-layout-allow-occlusion class="clip" data-start="35.1" data-duration="{D-35.1:.1f}" data-track-index="1">
  <img id="end-img" src="assets/media/kapanis_zemin.jpg" alt="">
  <div id="end-t" data-layout-allow-occlusion>
    <div id="end-h">Yarım Asır</div>
    <div id="end-bar"></div>
    <div id="end-tag">Bir gözlükçünün hikâyesi</div>
    <div id="end-ep">BÖLÜM 1</div>
    <div id="end-next">Hikâye devam ediyor.</div>
  </div>
</div>
<div id="shade"></div>
<div id="open" class="clip" data-start="0" data-duration="3.0" data-track-index="3">
  <div id="open-h">Yarım asır.</div>
  <div id="open-s">BİR GÖZLÜKÇÜNÜN HİKÂYESİ</div>
</div>
<div id="marker" class="clip" data-start="3.5" data-duration="7.9" data-track-index="3"><span id="marker-in" class="label"><span class="rule"></span>Aksaray</span></div>
{places_html}
{chr(10).join(caps_html)}
<div id="who" class="clip" data-start="26.9" data-duration="8.2" data-track-index="3"><span id="who-in" class="label"><span class="rule"></span>Fahri Kuz</span></div>
<div id="black" data-layout-allow-occlusion class="clip" data-start="43.0" data-duration="1.0" data-track-index="5"></div>
<audio id="miks" class="clip" data-start="0" data-duration="{D}" data-track-index="6" data-volume="1" src="assets/audio/miks.m4a"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
// açılış
tl.fromTo("#open-h",{{opacity:0.0,y:10}},{{opacity:1,y:0,duration:0.7,ease:"power3.out"}},0);
tl.fromTo("#open-s",{{opacity:0}},{{opacity:1,duration:0.6,ease:"power2.out"}},0.5);
tl.to("#open-h,#open-s",{{opacity:0,duration:0.4,ease:"power1.in"}},2.55);
tl.fromTo("#marker-in",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.45,ease:"power3.out"}},3.55);
tl.to("#marker-in",{{opacity:0,duration:0.3}},11.0);
{chr(10).join(tl)}
// imza şeridi
tl.fromTo("#band",{{opacity:0}},{{opacity:1,duration:0.3}},22.3);
tl.fromTo("#band-img",{{scale:1.06}},{{scale:1.0,duration:4.3,ease:"power1.out"}},22.3);
tl.fromTo("#band-top",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},22.55);
tl.fromTo("#band-bot",{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.6,ease:"power3.out"}},23.6);
// alıntı imzası
tl.fromTo("#who-in",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.45,ease:"power3.out"}},27.0);
tl.to("#who-in",{{opacity:0,duration:0.3}},34.75);
// kapanış
tl.fromTo("#end",{{opacity:0}},{{opacity:1,duration:0.7,ease:"power1.inOut"}},35.1);
tl.fromTo("#end-img",{{scale:1.08}},{{scale:1.0,duration:8.9,ease:"none"}},35.1);
tl.fromTo("#end-h",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.9,ease:"power3.out"}},36.3);
tl.fromTo("#end-bar",{{scaleX:0}},{{scaleX:1,duration:0.7,ease:"power2.inOut"}},37.0);
tl.fromTo("#end-tag",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.7,ease:"power3.out"}},37.35);
tl.fromTo("#end-ep",{{opacity:0}},{{opacity:1,duration:0.6}},38.6);
tl.fromTo("#end-next",{{opacity:0}},{{opacity:1,duration:0.8}},39.6);
tl.fromTo("#black",{{opacity:0}},{{opacity:1,duration:0.9,ease:"power1.in"}},43.0);
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
Path(__file__).with_name("index.html").write_text(html, encoding="utf-8")
print("index.html yazıldı")
