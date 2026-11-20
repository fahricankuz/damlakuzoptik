#!/usr/bin/env python3
"""Yarım Asır, Bölüm 7 (Devir): index.html üretici. Zamanlamalar ve metin burada tek yerde durur."""
from pathlib import Path

D = 37.0

# görüntü klipleri: id, tür, kaynak, başlangıç, süre, hareket (ölçek başlangıç→bitiş, y kayması px)
SHOTS = [
    ("s-lazer",  "video", "lazer.mp4",  0.0,  7.2,  (1.00, 1.06, 0)),
    ("s-defile", "video", "defile.mp4", 7.0,  4.75, (1.04, 1.00, 0)),
    ("s-bugun",  "video", "bugun.mp4",  25.0, 5.9,  (1.00, 1.06, 0)),
]
FADE = {"s-defile": 0.5, "s-bugun": 0.9}

def dagit(a, b, metin, off):
    """Kelime zamanlarını konuşma aralığına harf uzunluğuna göre dağıtır (anlatım deşifresi yerine)."""
    ws = metin.split(); n = [len(w.strip(",.:;…")) + 2 for w in ws]; tot = sum(n); t = a; out = []
    for w, k in zip(ws, n):
        out.append((w, round(t + off, 2))); t += (b - a) * k / tot
    return out

B = dagit(4.23, 8.41, "Türkiye'de o güne kadar eşi benzeri görülmemiş büyüklükte bir yabancı ortaklık.", 2.77)
C = dagit(8.86, 13.11, "İki yıl süren bu ortaklığın ardından şirket, tamamen yabancı ortaklara devredildi.", 2.94)
CAPS = [
    ("c1", dagit(0.00, 3.73, "İki binli yıllarda Fahri Kuz Optik, sektörde bir ilke imza attı:", 2.8), 6.75),
    ("c2", B[:6], B[6][1] - 0.14),
    ("c3", B[6:], 11.6),
    ("c4", C[:5], C[5][1] - 0.14),
    ("c5", C[5:], 16.4),
    ("c6", dagit(13.47, 15.37, "Ertesi gün gazeteler şöyle yazdı:", 3.33), 18.95),
    ("c7", dagit(17.78, 18.92, "Bir dönem kapanmıştı.", 5.62), 25.2),
    ("c8", dagit(19.28, 21.35, "Ama Fahri Kuz için hikâye bitmemişti.", 6.32), 30.5),
]
QUOTES = []
PLACES = []
MARKERS = []

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
#logo {{ position:absolute; inset:0; z-index:25; opacity:0; background:radial-gradient(110% 70% at 50% 36%, #2a2119 0%, #15100c 55%, #0b0907 100%); }}
#logo-card {{ position:absolute; left:70px; top:330px; width:940px; padding:34px 30px 30px; background:#fbfaf6; border-radius:6px;
  box-shadow:0 30px 80px rgba(0,0,0,.7), 0 4px 12px rgba(0,0,0,.45); transform-origin:50% 50%; }}
#manset {{ position:absolute; left:90px; right:90px; top:1030px; z-index:60; }}
#manset-l {{ margin-bottom:30px; }}
#manset-h {{ font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:400; font-size:104px; line-height:1.04; color:var(--paper); }}
#logo-img {{ display:block; width:880px; height:auto; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
{chr(10).join(shots_html)}
<div id="end" data-layout-allow-occlusion class="clip" data-start="30.6" data-duration="{D-30.6:.1f}" data-track-index="1">
  <img id="end-img" src="assets/media/kapanis_zemin.jpg" alt="">
  <div id="end-t" data-layout-allow-occlusion>
    <div id="end-h">Yarım Asır</div>
    <div id="end-bar"></div>
    <div id="end-tag">Devir</div>
    <div id="end-ep">BÖLÜM 7</div>
    <div id="end-next">Hikâye devam ediyor.</div>
  </div>
</div>
<div id="logo" class="clip" data-layout-allow-occlusion data-start="11.5" data-duration="13.8" data-track-index="0"><div id="logo-card"><img id="logo-img" src="assets/media/papagan_logo.png" alt="Fahri Kuz Optik papağan logosu"></div></div>
<div id="shade"></div>
<div id="open" class="clip" data-start="0" data-duration="3.0" data-track-index="3">
  <div id="open-h">Devir.</div>
  <div id="open-s">YARIM ASIR · BÖLÜM 7</div>
</div>
{markers_html}
<div id="manset" class="clip" data-start="19.0" data-duration="4.4" data-track-index="4"><div id="manset-l" class="label"><span class="rule"></span>Basında, ertesi gün</div><div id="manset-h">“Güle güle gözlüklü papağan.”</div></div>
{places_html}
{chr(10).join(caps_html)}

<div id="black" data-layout-allow-occlusion class="clip" data-start="36.0" data-duration="1.0" data-track-index="5"></div>
<audio id="miks" class="clip" data-start="0" data-duration="{D}" data-track-index="6" data-volume="1" src="assets/audio/miks.m4a"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
// açılış
tl.fromTo("#open-h",{{opacity:0.0,y:10}},{{opacity:1,y:0,duration:0.7,ease:"power3.out"}},0);
tl.fromTo("#open-s",{{opacity:0}},{{opacity:1,duration:0.6,ease:"power2.out"}},0.5);
tl.to("#open-h,#open-s",{{opacity:0,duration:0.4,ease:"power1.in"}},2.55);
{chr(10).join(tl)}
// papağan logosu: renkli gelir, yavaşça solar ve kararır
tl.fromTo("#logo",{{opacity:0}},{{opacity:1,duration:0.6,ease:"power1.inOut"}},11.5);
tl.fromTo("#logo-card",{{opacity:0,y:30,scale:0.95}},{{opacity:1,y:0,scale:1,duration:1.0,ease:"power3.out"}},11.6);
tl.fromTo("#logo-card",{{filter:"grayscale(0) brightness(1)"}},{{filter:"grayscale(1) brightness(0.55)",duration:9.0,ease:"power1.inOut",immediateRender:false}},13.4);
tl.fromTo("#logo-card",{{scale:1}},{{scale:0.97,duration:10,ease:"none",immediateRender:false}},12.6);
tl.to("#logo-card",{{opacity:0,duration:1.2,ease:"power1.in"}},22.0);
tl.to("#logo",{{opacity:0,duration:0.4}},24.9);
// gazete başlığı (yalnızca yazı)
tl.fromTo("#manset-l",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.5,ease:"power3.out"}},19.05);
tl.fromTo("#manset-h",{{opacity:0,y:18}},{{opacity:1,y:0,duration:0.8,ease:"power3.out"}},19.2);
tl.to("#manset",{{opacity:0,duration:0.5,ease:"power1.in"}},22.85);
// bugün: renk geri gelir
tl.fromTo("#s-bugun",{{filter:"grayscale(1) brightness(0.7)"}},{{filter:"grayscale(0) brightness(1)",duration:3.0,ease:"power1.inOut",immediateRender:false}},25.6);
// kapanış
tl.fromTo("#end",{{opacity:0}},{{opacity:1,duration:1.0,ease:"power1.inOut"}},30.6);
tl.fromTo("#end-img",{{scale:1.08}},{{scale:1.0,duration:6.4,ease:"none"}},30.6);
tl.fromTo("#end-h",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.9,ease:"power3.out"}},31.2);
tl.fromTo("#end-bar",{{scaleX:0}},{{scaleX:1,duration:0.7,ease:"power2.inOut"}},31.9);
tl.fromTo("#end-tag",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.7,ease:"power3.out"}},32.2);
tl.fromTo("#end-ep",{{opacity:0}},{{opacity:1,duration:0.6}},33.0);
tl.fromTo("#end-next",{{opacity:0}},{{opacity:1,duration:0.8}},33.9);
tl.fromTo("#black",{{opacity:0}},{{opacity:1,duration:0.9,ease:"power1.in"}},36.0);
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
Path(__file__).with_name("index.html").write_text(html, encoding="utf-8")
print("index.html yazıldı")
