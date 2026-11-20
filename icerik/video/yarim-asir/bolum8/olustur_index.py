#!/usr/bin/env python3
"""Yarım Asır, Bölüm 8 (Bugün): index.html üretici. Zamanlamalar ve metin burada tek yerde durur."""
from pathlib import Path

D = 52.0

# görüntü klipleri: id, tür, kaynak, başlangıç, süre, hareket (ölçek başlangıç→bitiş, y kayması px)
SHOTS = [
    ("s-kutular", "video", "kutular.mp4", 0.0,  3.0,  (1.00, 1.06, 0)),
    ("s-magaza",  "video", "magaza.mp4",  3.0,  7.5,  (1.00, 1.08, 0)),
    ("s-bugun",   "video", "bugun.mp4",   10.4, 6.5,  (1.00, 1.05, 0)),
    ("s-el",      "video", "el.mp4",      16.8, 2.3,  (1.04, 1.00, 0)),
    ("s-figur",   "video", "figur.mp4",   19.0, 2.2,  (1.00, 1.05, 0)),
    ("s-beyaz",   "video", "beyaz.mp4",   21.5, 6.8,  (1.00, 1.05, 0)),
    ("s-genc",    "img",   "genc.jpg",    38.4, 1.75, (1.08, 1.02, 0)),
    ("s-simdi",   "video", "simdi.mp4",   40.0, 2.0,  (1.02, 1.08, 0)),
]
FADE = {"s-magaza": 0.5, "s-bugun": 0.4, "s-el": 0.35, "s-figur": 0.35, "s-beyaz": 0.35, "s-genc": 0.5, "s-simdi": 0.6}

def dagit(a, b, metin, off):
    """Kelime zamanlarını konuşma aralığına harf uzunluğuna göre dağıtır (anlatım deşifresi yerine)."""
    ws = metin.split(); n = [len(w.strip(",.:;…")) + 2 for w in ws]; tot = sum(n); t = a; out = []
    for w, k in zip(ws, n):
        out.append((w, round(t + off, 2))); t += (b - a) * k / tot
    return out

B = dagit(0.91, 4.40, "Kuz Optik'e bir damla ekledi ve yoluna kızının adıyla devam etti:", 1.46)
CAPS = [
    ("c1", dagit(0.00, 0.55, "Durmadı.", 1.5), B[0][1] - 0.14),
    ("c2", B[:5], B[5][1] - 0.14),
    ("c3", B[5:], 6.2),
    ("c3b", dagit(5.08, 6.18, "Damla Kuz Optik.", 1.17), 7.5),
    ("c4", dagit(4.18, 6.36, "Kendi adıyla ilk mağazasını açtığı yere,", 6.42), 12.81),
    ("c5", dagit(6.53, 8.82, "Ataköy Atrium AVM'ye geri dönmüştü.", 6.42), 15.4),
    ("c6", dagit(9.10, 10.16, "Bugün hâlâ orada.", 6.42), 16.8),
    ("c7", dagit(10.41, 12.48, "Her gözlük kişiye özel tasarlanıyor;", 6.59), 19.1),
    ("c8", dagit(12.65, 14.48, "her modelden yalnızca bir tane.", 6.59), 21.35),
    ("c9", dagit(14.73, 15.23, "Ve bugün,", 13.57) + dagit(15.41, 17.56, "birçok yeniliğiyle online mağazasında da.", 13.57), 33.4),
    ("c10", dagit(17.84, 18.76, "Yarım asır geçti.", 20.76), 40.3),
    ("c11", dagit(18.97, 20.57, "Tutku hâlâ ilk günkü gibi.", 20.76), 41.9),
    ("c12", dagit(20.81, 21.48, "Ve hikâye,", 21.39) + dagit(21.66, 23.41, "çok yakında yeni bir sayfa açacak.", 21.39), 45.3),
]
QUOTES = [
    ("q1", [("“On", 7.72), ("sene", 7.90), ("aradan", 8.16), ("sonra", 8.52)], 8.80),
    ("q2", [("tekrar", 8.86), ("Ataköy", 9.62), ("Atrium", 9.80), ("AVM'deyiz.”", 9.96)], 10.6),
    ("q3", [("“Beyazı", 21.70), ("daha", 22.10), ("beyaz,", 22.36)], 22.6),
    ("q4", [("siyahı", 22.68), ("daha", 22.98), ("siyah", 23.24), ("gören", 23.52)], 24.5),
    ("q5", [("dünyanın", 24.60), ("en", 24.98), ("kaliteli", 25.14)], 25.5),
    ("q6", [("güneş", 25.56), ("gözlüklerini", 25.82), ("yapıyoruz,", 26.36)], 26.75),
    ("q7", [("özel", 26.82), ("tasarım", 27.08), ("olarak.”", 27.46)], 28.0),
]
PLACES = []
MARKERS = [("m-atakoy", "Ataköy Atrium AVM", 7.6, 10.6)]


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

markers_html = "".join(
    f'<div id="{mid}" class="clip marker" data-start="{a:.2f}" data-duration="{b-a:.2f}" data-track-index="3"><span class="marker-in label"><span class="rule"></span>{name}</span></div>'
    for mid, name, a, b in MARKERS)
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
for mid, name, a, b in MARKERS:
    tl.append(f'tl.fromTo("#{mid} .marker-in",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.45,ease:"power3.out"}},{a+0.05:.2f});')
    tl.append(f'tl.to("#{mid} .marker-in",{{opacity:0,duration:0.3}},{b-0.35:.2f});')
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
.place-in, #marker-in, .marker-in {{ font-size:36px; letter-spacing:.3em; color:var(--paper); text-shadow:0 2px 22px rgba(0,0,0,.9), 0 0 4px rgba(0,0,0,.7); }}
.rule {{ display:inline-block; width:56px; height:1px; background:var(--gold); vertical-align:middle; margin-right:22px; }}
.place {{ position:absolute; left:90px; z-index:60; }}
.place-in {{ display:inline-block; }}
#scrim {{ position:absolute; left:0; top:0; width:1080px; height:900px; z-index:55; background:radial-gradient(120% 90% at 0% 18%, rgba(11,9,7,.78) 0%, rgba(11,9,7,.45) 38%, rgba(11,9,7,0) 70%); }}
#who, #who2 {{ position:absolute; left:90px; top:1300px; z-index:60; }}
#marker, .marker {{ position:absolute; left:90px; top:250px; z-index:60; }}
#yanil {{ position:absolute; inset:0; z-index:50; background:#050403; }}
#yanil-h {{ position:absolute; left:0; right:0; top:860px; text-align:center; font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:300; font-size:150px; color:var(--paper); }}
#open-sis {{ position:absolute; inset:0; z-index:55; background:radial-gradient(90% 45% at 50% 46%, rgba(8,6,5,.88) 0%, rgba(8,6,5,.6) 55%, rgba(8,6,5,.25) 100%); }}
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
.sahne {{ position:absolute; inset:0; z-index:25; opacity:0; background:radial-gradient(120% 70% at 50% 38%, #2a2119 0%, #15100c 55%, #0b0907 100%); }}
#duel-sol, #duel-sag {{ position:absolute; top:430px; width:540px; text-align:center; }}
#duel-sol {{ left:0; }} #duel-sag {{ left:540px; }}
.duel-n {{ font-family:'Cormorant Garamond',serif; font-weight:300; font-size:168px; line-height:1; color:var(--paper); font-variant-numeric:lining-nums; white-space:nowrap; }}
.duel-l {{ margin-top:34px; font-family:'Inter Local',Inter,sans-serif; font-weight:600; font-size:24px; letter-spacing:.32em; padding-left:.32em; color:var(--gold); }}
#duel-cizgi {{ position:absolute; left:539px; top:420px; width:1px; height:330px; background:var(--gold); opacity:.5; transform-origin:50% 0; }}
.kart {{ position:absolute; left:80px; width:920px; padding:76px 70px 60px; background:#efe7d3; box-shadow:0 30px 80px rgba(0,0,0,.65), 0 4px 12px rgba(0,0,0,.4); }}
.kart-q {{ font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:400; font-size:84px; line-height:1.08; color:#2a2420; }}
.kart-q + .kart-q {{ margin-top:26px; }}
.kart-q b {{ font-weight:500; }}
.kart-k {{ margin-top:44px; font-family:'Inter Local',Inter,sans-serif; font-weight:600; font-size:20px; letter-spacing:.14em; color:#7a6a55; white-space:nowrap; text-transform:uppercase; }}
.kart-k .rule {{ background:#a48a5e; }}
#kart1 {{ top:470px; }} #kart2 {{ top:420px; }}
#tel {{ position:absolute; left:300px; top:170px; width:480px; height:930px; border-radius:62px; background:#0d0d0d; padding:16px;
  box-shadow:0 40px 90px rgba(0,0,0,.75), inset 0 0 0 2px #2b2b2b; }}
#tel-ekran {{ position:relative; width:448px; height:898px; border-radius:48px; overflow:hidden; background:#fff; }}
.ekran {{ position:absolute; left:0; top:0; width:448px; height:auto; }}
#tel-adres {{ position:absolute; left:0; right:0; top:1040px; text-align:center; }}
#isik {{ position:absolute; left:-200px; top:200px; width:1480px; height:1100px; background:radial-gradient(closest-side, rgba(255,226,180,.30), rgba(255,226,180,.08) 55%, rgba(255,226,180,0) 100%); }}
#logo-img {{ position:absolute; left:90px; top:500px; width:900px; height:auto; filter:drop-shadow(0 18px 30px rgba(0,0,0,.7)); }}
#manset {{ position:absolute; left:90px; right:90px; top:1090px; z-index:60; }}
#manset-l {{ margin-bottom:30px; }}
#manset-h {{ font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:400; font-size:104px; line-height:1.04; color:var(--paper); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
{chr(10).join(shots_html)}
<div id="end" data-layout-allow-occlusion class="clip" data-start="45.4" data-duration="{D-45.4:.1f}" data-track-index="1">
  <img id="end-img" src="assets/media/kapanis_zemin.jpg" alt="">
  <div id="end-t" data-layout-allow-occlusion>
    <div id="end-h">Yarım Asır</div>
    <div id="end-bar"></div>
    <div id="end-tag">Bugün</div>
    <div id="end-ep">BÖLÜM 8</div>
    <div id="end-next">Hikâye devam ediyor.</div>
  </div>
</div>
<div id="online" class="clip sahne" data-layout-allow-occlusion data-start="28.1" data-duration="5.6" data-track-index="0">
  <div id="tel"><div id="tel-ekran"><img id="ek1" class="ekran" src="assets/media/asistan1.jpg" alt="Kuz AI gözlük seçim asistanı"><img id="ek2" class="ekran" src="assets/media/asistan2.jpg" alt="Yüz şekli seçimi"><img id="ek3" class="ekran" src="assets/media/asistan3.jpg" alt="Çerçeve tipi seçimi"></div></div>
</div>
<div id="alinti1" class="clip sahne" data-layout-allow-occlusion data-start="33.6" data-duration="4.9" data-track-index="0">
  <div id="kart1" class="kart"><div class="kart-q">“En büyük zenginlik ve maharet insan ilişkileridir.”</div>
  <div class="kart-k"><span class="rule"></span>Fahri Kuz · Takvim, 2009 · Savaş Ay söyleşisi</div></div>
</div>
<div id="son" class="clip sahne" data-layout-allow-occlusion data-start="41.8" data-duration="3.8" data-track-index="0"><div id="isik"></div></div>
<div id="shade"></div>
<div id="open-sis" class="clip" data-start="0" data-duration="2.4" data-track-index="2"></div>
<div id="open" class="clip" data-start="0" data-duration="2.4" data-track-index="3">
  <div id="open-h">Bugün.</div>
  <div id="open-s">YARIM ASIR · BÖLÜM 8</div>
</div>
{markers_html}
<div id="who" class="clip" data-start="7.55" data-duration="3.05" data-track-index="3"><span id="who-in" class="label"><span class="rule"></span>Fahri Kuz</span></div>
<div id="who2" class="clip" data-start="21.5" data-duration="6.55" data-track-index="3"><span id="who2-in" class="label"><span class="rule"></span>Fahri Kuz</span></div>
{places_html}
{chr(10).join(caps_html)}

<div id="black" data-layout-allow-occlusion class="clip" data-start="51.0" data-duration="1.0" data-track-index="5"></div>
<audio id="miks" class="clip" data-start="0" data-duration="{D}" data-track-index="6" data-volume="1" src="assets/audio/miks.m4a"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
// açılış
tl.fromTo("#open-h",{{opacity:0.0,y:10}},{{opacity:1,y:0,duration:0.7,ease:"power3.out"}},0);
tl.fromTo("#open-s",{{opacity:0}},{{opacity:1,duration:0.6,ease:"power2.out"}},0.5);
tl.to("#open-h,#open-s,#open-sis",{{opacity:0,duration:0.4,ease:"power1.in"}},1.95);
{chr(10).join(tl)}
// alıntı imzaları
tl.fromTo("#who-in",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.45,ease:"power3.out"}},7.6);
tl.to("#who-in",{{opacity:0,duration:0.3}},10.25);
tl.fromTo("#who2-in",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.45,ease:"power3.out"}},21.6);
tl.to("#who2-in",{{opacity:0,duration:0.3}},27.75);
// online mağaza: Kuz AI asistanı
tl.fromTo("#online",{{opacity:0}},{{opacity:1,duration:0.5}},28.1);
tl.fromTo("#tel",{{opacity:0,y:80,rotation:-3}},{{opacity:1,y:0,rotation:0,duration:1.0,ease:"power3.out"}},28.2);
tl.fromTo("#ek2",{{opacity:0,x:60}},{{opacity:1,x:0,duration:0.45,ease:"power2.out"}},30.0);
tl.fromTo("#ek3",{{opacity:0,x:60}},{{opacity:1,x:0,duration:0.45,ease:"power2.out"}},31.6);
tl.fromTo("#tel",{{scale:1}},{{scale:1.04,duration:4.3,ease:"none",immediateRender:false}},29.2);
tl.to("#online",{{opacity:0,duration:0.4,ease:"power1.in"}},33.3);
// söyleşi kartı
tl.fromTo("#alinti1",{{opacity:0}},{{opacity:1,duration:0.4}},33.6);
tl.fromTo("#kart1",{{opacity:0,y:60,rotation:2.5}},{{opacity:1,y:0,rotation:-1.2,duration:0.9,ease:"power3.out"}},33.7);
tl.fromTo("#kart1",{{scale:1}},{{scale:1.03,duration:3.8,ease:"none",immediateRender:false}},34.6);
tl.to("#alinti1",{{opacity:0,duration:0.4,ease:"power1.in"}},38.1);
// son: sıcak ışık yavaşça açılır
tl.fromTo("#son",{{opacity:0}},{{opacity:1,duration:0.6}},41.8);
tl.fromTo("#isik",{{opacity:0,scale:0.6}},{{opacity:1,scale:1.1,duration:3.4,ease:"power1.inOut"}},41.9);
// kapanış
tl.fromTo("#end",{{opacity:0}},{{opacity:1,duration:1.0,ease:"power1.inOut"}},45.4);
tl.fromTo("#end-img",{{scale:1.08}},{{scale:1.0,duration:6.6,ease:"none"}},45.4);
tl.fromTo("#end-h",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.9,ease:"power3.out"}},46.0);
tl.fromTo("#end-bar",{{scaleX:0}},{{scaleX:1,duration:0.7,ease:"power2.inOut"}},46.7);
tl.fromTo("#end-tag",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.7,ease:"power3.out"}},47.0);
tl.fromTo("#end-ep",{{opacity:0}},{{opacity:1,duration:0.6}},47.9);
tl.fromTo("#end-next",{{opacity:0}},{{opacity:1,duration:0.8}},48.8);
tl.fromTo("#black",{{opacity:0}},{{opacity:1,duration:0.9,ease:"power1.in"}},51.0);
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
Path(__file__).with_name("index.html").write_text(html, encoding="utf-8")
print("index.html yazıldı")
