#!/usr/bin/env python3
"""Yarım Asır, Bölüm 9 (Final, DEMO): Kuz İstanbul. index.html üretici.
Marka: Sandrift #B2937F, siyah #231F20, krem #F8F1E8, şeftali #FEDCC7. Başlık fontu NORD (demoda yerine açık lisanslı Krona One),
metin fontu Montserrat. Logo vektörleri Drive'daki master dosyadan (logo_yollari.py)."""
from pathlib import Path
from logo_yollari import PATHS, BOX

D = 84.8
SAND, SIYAH, KREM, SEFTALI = "#B2937F", "#231F20", "#F8F1E8", "#FEDCC7"


def fontfaces():
    out = []
    fam = [("Cormorant Garamond", "cormorant-garamond", w, st) for w, st in [(300, "normal"), (300, "italic"), (400, "italic"), (500, "italic")]]
    fam += [("Montserrat Local", "montserrat", w, "normal") for w in (300, 400, 500, 600)]
    fam += [("Nord Yerine", "krona-one", 400, "normal")]
    for name, file, w, st in fam:
        for sub, rng in [("latin", "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122"),
                         ("latin-ext", "U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1E9F,U+20A0-20C0,U+2C60-2C7F,U+A720-A7FF")]:
            out.append(f"@font-face{{font-family:'{name}';font-style:{st};font-weight:{w};font-display:block;"
                       f"src:url('assets/fonts/{file}-{sub}-{w}-{st}.woff2') format('woff2');unicode-range:{rng};}}")
    return "\n".join(out)


def logo_svg(lid, renk):
    x0, y0, x1, y1 = BOX
    g = []
    for grup, yollar in PATHS.items():
        ps = "".join(f'<path id="{lid}-{pid}" d="{d}"/>' for pid, d in yollar)
        g.append(f'<g id="{lid}-{grup}">{ps}</g>')
    return (f'<svg id="{lid}" class="logo" viewBox="{x0 - 4} {y0 - 4} {x1 - x0 + 8} {y1 - y0 + 8}" '
            f'xmlns="http://www.w3.org/2000/svg" fill="{renk}">' + "".join(g) + "</svg>")


# Montaj üzerindeki yer işaretleri (montaj 6.0 sn'de başlar)
# (parça süreleri: assets/media/montaj_parcalar.txt; "Bugün" parçaları kullanıcı isteğiyle çıkarıldı)
YERLER = [("AKSARAY", 6.1, 7.55), ("SİRKECİ", 7.7, 9.2), ("AKSARAY · BEYAZIT", 9.4, 10.55),
          ("FAHRİ KUZ OPTİK", 14.35, 15.9), ("2000 · 30. YIL", 18.15, 19.65)]


def kelimeler(metin, cls):
    return " ".join(f'<span class="{cls}">{w}</span>' for w in metin.split())


yer_html = "".join(f'<div id="yer{i}" class="clip yer" data-start="{a}" data-duration="{b - a:.2f}" data-track-index="3">'
                   f'<span class="yer-in"><span class="cizgi"></span>{ad}</span></div>' for i, (ad, a, b) in enumerate(YERLER))

html = f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<style>
{fontfaces()}
:root {{ --sand:{SAND}; --siyah:{SIYAH}; --krem:{KREM}; --seftali:{SEFTALI}; --kagit:rgba(255,250,240,.95); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:100%; height:100%; overflow:hidden; background:#000; }}
.tam {{ position:absolute; inset:0; }}
.serif {{ font-family:'Cormorant Garamond',serif; }}
.nord {{ font-family:'Nord Yerine','Montserrat Local',sans-serif; text-transform:uppercase; }}
.mont {{ font-family:'Montserrat Local',sans-serif; }}
/* açılış */
#acilis-y {{ position:absolute; left:110px; right:110px; top:820px; text-align:center; font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:300; font-size:78px; line-height:1.15; color:var(--kagit); }}
.w {{ opacity:0; }}
#acilis-s {{ position:absolute; left:0; right:0; top:1150px; text-align:center; font-family:'Montserrat Local',sans-serif; font-weight:500; font-size:28px; letter-spacing:.34em; color:rgba(255,250,240,.66); padding-left:.34em; }}
/* montaj */
#montaj-w {{ position:absolute; inset:0; overflow:hidden; }}
#montaj {{ position:absolute; inset:0; width:1080px; height:1920px; object-fit:cover; }}
#golge {{ position:absolute; inset:0; z-index:20; pointer-events:none; background:linear-gradient(180deg, rgba(0,0,0,.55) 0%, rgba(0,0,0,0) 22%, rgba(0,0,0,0) 70%, rgba(0,0,0,.55) 100%); }}
.yer {{ position:absolute; left:90px; top:250px; z-index:30; }}
.yer-in {{ display:inline-block; font-family:'Montserrat Local',sans-serif; font-weight:600; font-size:30px; letter-spacing:.34em; color:#fff; text-shadow:0 2px 18px rgba(0,0,0,.9); white-space:nowrap; }}
.cizgi {{ display:inline-block; width:56px; height:1px; background:var(--sand); vertical-align:middle; margin-right:22px; }}
/* söyleşi */
#soylesi {{ background:#000; }}
.s-q {{ position:absolute; left:110px; right:110px; font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:300; font-size:82px; line-height:1.12; color:var(--kagit); }}
#sq1 {{ top:700px; color:rgba(255,250,240,.7); }} #sq2 {{ top:930px; font-weight:400; }}
#sk {{ position:absolute; left:110px; top:1180px; font-family:'Montserrat Local',sans-serif; font-weight:500; font-size:24px; letter-spacing:.24em; color:var(--sand); }}
/* damla ve doğuş */
#dogus {{ background:#000; }}
#krem {{ position:absolute; inset:0; background:var(--krem); }}
#desen {{ position:absolute; left:-300px; top:-200px; width:3002px; height:2400px; opacity:0; background:url('assets/media/desen.png') repeat; background-size:1501px 751px; }}
#damla-svg {{ position:absolute; left:0; top:0; width:1080px; height:1920px; }}
#logo-w {{ position:absolute; left:140px; top:728px; width:800px; }}
.logo {{ display:block; width:100%; height:auto; overflow:visible; }}
#tag1 {{ position:absolute; left:0; right:0; top:1150px; text-align:center; font-size:34px; letter-spacing:.12em; color:var(--sand); }}
#tag2 {{ position:absolute; left:0; right:0; top:1225px; text-align:center; font-weight:400; font-size:34px; color:var(--siyah); }}
/* marka dünyası */
.sahne {{ position:absolute; inset:0; overflow:hidden; }}
.etiket {{ font-family:'Montserrat Local',sans-serif; font-weight:600; font-size:26px; letter-spacing:.34em; }}
.buyuk {{ font-family:'Nord Yerine',sans-serif; text-transform:uppercase; font-size:92px; line-height:1.08; letter-spacing:.01em; }}
.alt {{ font-family:'Montserrat Local',sans-serif; font-weight:400; font-size:38px; line-height:1.35; }}
.blok {{ position:absolute; left:100px; right:100px; }}
#sA {{ background:var(--sand); }} #sB {{ background:var(--krem); }} #sC {{ background:#000; }}
.desen-a {{ position:absolute; left:-200px; top:-160px; width:3002px; height:2320px; background-repeat:repeat; background-size:1501px 751px; opacity:.12; }}
#sayi26 {{ font-family:'Nord Yerine',sans-serif; font-size:250px; line-height:1; color:#fff; }}
#fkvid {{ position:absolute; inset:0; width:1080px; height:1920px; object-fit:cover; }}
#sC-perde {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(0,0,0,.35) 0%, rgba(0,0,0,.15) 40%, rgba(0,0,0,.85) 70%, rgba(0,0,0,.95) 100%); }}
/* duyuru: krem, ince kesik köşeli çerçeve, bol boşluk */
#duyuru {{ background:var(--krem); }}
#dy-cer {{ position:absolute; left:90px; top:430px; width:900px; height:1110px; }}
#dy-tarih {{ position:absolute; left:0; right:0; top:560px; text-align:center; font-family:'Montserrat Local',sans-serif; font-weight:500; font-size:24px; letter-spacing:.52em; color:var(--sand); padding-left:.52em; }}
#dy-tarih .ck {{ display:inline-block; width:64px; height:1px; background:var(--sand); vertical-align:middle; margin:0 28px; opacity:.7; }}
#logo2-w {{ position:absolute; left:215px; top:660px; width:650px; }}
#dy-cizgi {{ position:absolute; left:500px; top:960px; width:80px; height:1px; background:var(--sand); }}
#dy-adres {{ position:absolute; left:0; right:0; top:1000px; text-align:center; font-family:'Montserrat Local',sans-serif; font-weight:300; font-size:46px; letter-spacing:.06em; color:var(--siyah); }}
#dy-yer {{ position:absolute; left:0; right:0; top:1078px; text-align:center; font-family:'Montserrat Local',sans-serif; font-weight:500; font-size:20px; letter-spacing:.42em; color:#8c7b6e; padding-left:.42em; }}
#dy-soz {{ position:absolute; left:150px; right:150px; top:1210px; text-align:center; font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:400; font-size:54px; line-height:1.18; color:#4a3d34; }}
#dy-imza {{ position:absolute; left:0; right:0; top:1365px; text-align:center; font-family:'Montserrat Local',sans-serif; font-weight:500; font-size:20px; letter-spacing:.42em; color:var(--sand); padding-left:.42em; }}
#dy-demo {{ position:absolute; left:0; right:0; top:1590px; text-align:center; font-family:'Montserrat Local',sans-serif; font-weight:400; font-size:21px; letter-spacing:.16em; color:#9d8f83; }}
/* son */
#son {{ background:var(--sand); }}
#logo3-w {{ position:absolute; left:190px; top:800px; width:700px; }}
#son-adres {{ position:absolute; left:0; right:0; top:1120px; text-align:center; font-family:'Montserrat Local',sans-serif; font-weight:500; font-size:30px; letter-spacing:.3em; color:#fff; }}
#karart {{ position:absolute; inset:0; z-index:95; background:#000; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">

<div id="acilis" class="clip tam" data-start="0" data-duration="6.1" data-track-index="0">
  <div id="acilis-y">{kelimeler("Yarım asır önce, Aksaray'da küçük bir dükkân.", "w")}</div>
  <div id="acilis-s">YARIM ASIR · BÖLÜM 9 · FİNAL</div>
</div>

<div id="montaj-w" class="clip" data-start="6.0" data-duration="16.2" data-track-index="1">
  <video id="montaj" class="clip" data-start="6.0" data-duration="16.2" data-track-index="2" src="assets/media/montaj.mp4" muted playsinline></video>
</div>
<div id="golge" class="clip" data-start="6.0" data-duration="16.2" data-track-index="2"></div>
{yer_html}

<div id="soylesi" class="clip tam" data-layout-allow-occlusion data-start="23.6" data-duration="7.2" data-track-index="0">
  <div id="sq1" class="s-q">— Rahat durabilir mi o Bozkırlı çocuk?</div>
  <div id="sq2" class="s-q">— Durmaz. Durmadı da zaten.</div>
  <div id="sk"><span class="cizgi"></span>TAKVİM, 2009 · SAVAŞ AY SÖYLEŞİSİ</div>
</div>

<div id="dogus" class="clip tam" data-layout-allow-occlusion data-start="30.6" data-duration="21.1" data-track-index="0">
  <div id="krem"></div>
  <div id="desen"></div>
  <svg id="damla-svg" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">
    <defs><radialGradient id="dg" cx="38%" cy="62%" r="70%"><stop offset="0" stop-color="#E7D3C3"/><stop offset=".55" stop-color="{SAND}"/><stop offset="1" stop-color="#7d624f"/></radialGradient></defs>
    <path id="damla" d="M540,0 C540,0 500,58 500,92 C500,116 518,132 540,132 C562,132 580,116 580,92 C580,58 540,0 540,0 Z" fill="url(#dg)"/>
    <circle id="parlama" cx="540" cy="860" r="40" fill="#F3E4D6"/>
    <ellipse id="h1" cx="540" cy="860" rx="10" ry="3" fill="none" stroke="{SAND}" stroke-width="3"/>
    <ellipse id="h2" cx="540" cy="860" rx="10" ry="3" fill="none" stroke="{SAND}" stroke-width="2"/>
    <ellipse id="h3" cx="540" cy="860" rx="10" ry="3" fill="none" stroke="{SAND}" stroke-width="1.5"/>
  </svg>
  <div id="logo-w">{logo_svg("lg", SAND)}</div>
  <div id="tag1" class="nord">Miras, modern lüksle buluşuyor.</div>
  <div id="tag2" class="mont">Yarım asırlık hikâye, özüne dönüyor.</div>
</div>

<div id="sA" class="clip sahne" data-layout-allow-occlusion data-start="51.4" data-duration="5.4" data-track-index="0">
  <div class="desen-a" style="background-image:url('assets/media/desen_beyaz.png')"></div>
  <div class="blok" style="top:560px"><div id="sayi26">26</div><div class="etiket" style="color:#fff;margin-top:10px">MAĞAZA</div></div>
  <div class="blok buyuk" style="top:900px;color:#fff">Türkiye'nin ilk optik zinciri.</div>
</div>
<div id="sB" class="clip sahne" data-layout-allow-occlusion data-start="56.6" data-duration="5.5" data-track-index="0">
  <div class="desen-a" style="background-image:url('assets/media/desen.png');opacity:.10"></div>
  <div class="blok" style="top:520px"><div class="etiket" style="color:var(--sand)">YENİLİK</div></div>
  <div class="blok buyuk" style="top:600px;color:var(--sand)">Titanyum çerçeve. Çok odaklı cam.</div>
  <div class="blok alt" style="top:1010px;color:var(--siyah)">Türkiye'ye ilk getiren isim.</div>
</div>
<div id="sC" class="clip sahne" data-layout-allow-occlusion data-start="61.9" data-duration="5.4" data-track-index="0">
  <video id="fkvid" class="clip" data-start="61.9" data-duration="5.4" data-track-index="2" src="assets/media/fk_bugun.mp4" muted playsinline></video>
  <div id="sC-perde"></div>
  <div class="blok" style="top:1000px"><div class="etiket" style="color:var(--sand)">USTALIK</div></div>
  <div class="blok buyuk" style="top:1060px;color:#fff">Her çerçevede zarafet.</div>
</div>

<div id="duyuru" class="clip sahne" data-layout-allow-occlusion data-start="67.2" data-duration="10.2" data-track-index="0">
  <div class="desen-a" style="background-image:url('assets/media/desen.png');opacity:.045"></div>
  <svg id="dy-cer" viewBox="0 0 900 1110" xmlns="http://www.w3.org/2000/svg"><path id="dy-yol" d="M70,1 L899,1 L899,1040 L830,1109 L1,1109 L1,70 Z" fill="none" stroke="{SAND}" stroke-width="1.5" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>
  <div id="dy-tarih"><span class="ck"></span>1 ŞUBAT 2027<span class="ck"></span></div>
  <div id="logo2-w">{logo_svg("lg2", SIYAH)}</div>
  <div id="dy-cizgi"></div>
  <div id="dy-adres">kuz.istanbul</div>
  <div id="dy-yer">ATAKÖY ATRIUM AVM</div>
  <div id="dy-soz">“Yarım asırdır, aynı heyecanla.”</div>
  <div id="dy-imza">FAHRİ KUZ</div>
  <div id="dy-demo">demo · geçici ses · Fahri Kuz'un kendi kaydı eklenecek</div>
</div>

<div id="son" class="clip sahne" data-layout-allow-occlusion data-start="77.2" data-duration="7.6" data-track-index="0">
  <div class="desen-a" style="background-image:url('assets/media/desen_beyaz.png');opacity:.08"></div>
  <div id="logo3-w">{logo_svg("lg3", "#ffffff")}</div>
  <div id="son-adres">KUZ.ISTANBUL</div>
</div>

<div id="karart" data-layout-allow-occlusion class="clip" data-start="83.8" data-duration="1.0" data-track-index="5"></div>
<audio id="miks" class="clip" data-start="0" data-duration="{D}" data-track-index="6" data-volume="1" src="assets/audio/miks.m4a"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
// açılış: kelimeler anlatıcıyla birlikte
const aw = gsap.utils.toArray("#acilis-y .w");
aw.forEach((el, i) => tl.fromTo(el, {{opacity:0, y:12, filter:"blur(6px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.7, ease:"power2.out"}}, 1.15 + i*0.28));
tl.fromTo("#acilis-s", {{opacity:0}}, {{opacity:1, duration:0.8}}, 3.4);
tl.to("#acilis-y,#acilis-s", {{opacity:0, duration:0.6, ease:"power1.in"}}, 5.3);
// montaj
tl.fromTo("#montaj-w", {{opacity:0}}, {{opacity:1, duration:0.35}}, 6.0);
tl.fromTo("#montaj", {{scale:1.0}}, {{scale:1.06, duration:16.2, ease:"none"}}, 6.0);
tl.to("#montaj-w", {{opacity:0, duration:0.25, ease:"power1.in"}}, 21.9);
document.querySelectorAll(".yer").forEach((el) => {{
  const a = parseFloat(el.dataset.start), d = parseFloat(el.dataset.duration);
  tl.fromTo(el.querySelector(".yer-in"), {{opacity:0, x:-14}}, {{opacity:1, x:0, duration:0.3, ease:"power3.out"}}, a + 0.05);
  tl.to(el.querySelector(".yer-in"), {{opacity:0, duration:0.2}}, a + d - 0.22);
}});
// söyleşi
tl.fromTo("#sq1", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:0.9, ease:"power2.out"}}, 24.2);
tl.fromTo("#sq2", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:0.9, ease:"power2.out"}}, 26.3);
tl.fromTo("#sk", {{opacity:0}}, {{opacity:1, duration:0.8}}, 27.4);
tl.to("#sq1,#sq2,#sk", {{opacity:0, duration:0.7, ease:"power1.in"}}, 29.7);
// damla
tl.set("#krem", {{clipPath:"inset(100% 0% 0% 0%)"}}, 30.6);
tl.set("#parlama,#h1,#h2,#h3", {{opacity:0}}, 30.6);
tl.set("#logo-w", {{opacity:0}}, 30.6);
tl.fromTo("#damla", {{y:-160, scaleY:1.0, opacity:1}}, {{y:728, scaleY:1.35, duration:1.4, ease:"power2.in", svgOrigin:"540 66"}}, 31.6);
tl.to("#damla", {{opacity:0, duration:0.05}}, 33.0);
tl.fromTo("#parlama", {{opacity:0.95, attr:{{r:8}}}}, {{opacity:0, attr:{{r:70}}, duration:0.5, ease:"power2.out"}}, 33.0);
[["#h1",33.0,520,150,3.2],["#h2",33.35,420,120,3.0],["#h3",33.7,330,95,2.8]].forEach(([s,t,rx,ry,d]) =>
  tl.fromTo(s, {{opacity:0.95, attr:{{rx:10, ry:3}}}}, {{opacity:0, attr:{{rx:rx, ry:ry}}, duration:d, ease:"power2.out"}}, t));
// logo işareti: önce ortada tek başına, ışıkla çizilir
tl.set("#logo-w", {{opacity:1, x:257, scale:1.35, transformOrigin:"50% 50%"}}, 34.4);
tl.set("#lg-kuz path,#lg-ist path", {{opacity:0}}, 34.4);
tl.fromTo("#lg-lm-bar", {{clipPath:"inset(100% 0% 0% 0%)"}}, {{clipPath:"inset(0% 0% 0% 0%)", duration:0.6, ease:"power3.out"}}, 34.5);
tl.fromTo("#lg-lm-ok", {{opacity:0, x:60}}, {{opacity:1, x:0, duration:0.7, ease:"power3.out"}}, 35.0);
tl.fromTo("#lg-lm-uc", {{opacity:0}}, {{opacity:1, duration:0.6, ease:"power2.out"}}, 35.55);
tl.to("#logo-w", {{x:0, scale:1, duration:1.3, ease:"power3.inOut"}}, 36.3);
gsap.utils.toArray("#lg-kuz path").forEach((p, i) => tl.fromTo(p, {{opacity:0, y:26}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 36.9 + i*0.14));
gsap.utils.toArray("#lg-ist path").forEach((p, i) => tl.fromTo(p, {{opacity:0, x:-10}}, {{opacity:1, x:0, duration:0.4, ease:"power2.out"}}, 37.9 + i*0.07));
// krem zemin açılır (müziğin ritmi başlar)
tl.to("#krem", {{clipPath:"inset(0% 0% 0% 0%)", duration:0.9, ease:"power3.inOut"}}, 40.6);
tl.to("#desen", {{opacity:0.07, duration:1.2}}, 41.4);
tl.fromTo("#desen", {{x:0}}, {{x:-260, duration:10, ease:"none"}}, 41.4);
tl.to("#logo-w", {{y:-120, scale:0.86, duration:1.2, ease:"power3.inOut"}}, 43.6);
tl.fromTo("#tag1", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.8, ease:"power3.out"}}, 44.6);
tl.fromTo("#tag2", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.8, ease:"power3.out"}}, 46.0);
tl.to("#dogus", {{opacity:0, duration:0.3}}, 51.3);
// marka dünyası: 4 sahne, müziğin vurgularıyla
function sahne(id, t, ici) {{
  tl.fromTo(id, {{clipPath:"inset(0% 0% 100% 0%)"}}, {{clipPath:"inset(0% 0% 0% 0%)", duration:0.55, ease:"power3.inOut"}}, t);
  tl.fromTo(id + " .desen-a", {{x:0}}, {{x:-180, duration:5.4, ease:"none"}}, t);
  ici.forEach(([sel, dt]) => tl.fromTo(id + " " + sel, {{opacity:0, y:24}}, {{opacity:1, y:0, duration:0.7, ease:"power3.out"}}, t + dt));
}}
sahne("#sA", 51.4, [[".blok:nth-of-type(2)", 0.4], ["#sayi26", 0.6], [".buyuk", 1.4]]);
const s26 = {{v:1}};
tl.fromTo(s26, {{v:1}}, {{v:26, duration:1.2, ease:"power2.out", onUpdate:() => {{ document.getElementById("sayi26").textContent = Math.round(s26.v); }}}}, 51.9);
sahne("#sB", 56.6, [[".blok:nth-of-type(2)", 0.35], [".buyuk", 0.6], [".alt", 1.5]]);
sahne("#sC", 61.9, [[".blok:nth-of-type(3)", 0.6], [".buyuk", 0.9]]);
tl.fromTo("#fkvid", {{scale:1.04}}, {{scale:1.0, duration:5.4, ease:"none"}}, 61.9);
// duyuru
tl.fromTo("#duyuru", {{opacity:0}}, {{opacity:1, duration:0.7}}, 67.2);
tl.to("#dy-yol", {{strokeDashoffset:0, duration:1.8, ease:"power2.inOut"}}, 67.4);
tl.fromTo("#dy-tarih", {{opacity:0, y:10}}, {{opacity:1, y:0, duration:1.0, ease:"power2.out"}}, 67.8);
tl.set("#lg2-kuz path,#lg2-ist path,#lg2-mark path", {{opacity:0}}, 67.2);
tl.fromTo("#lg2-mark path", {{opacity:0, y:18}}, {{opacity:1, y:0, duration:0.6, stagger:0.09, ease:"power3.out"}}, 68.6);
tl.fromTo("#lg2-kuz path", {{opacity:0, y:18}}, {{opacity:1, y:0, duration:0.6, stagger:0.09, ease:"power3.out"}}, 68.9);
tl.fromTo("#lg2-ist path", {{opacity:0}}, {{opacity:1, duration:0.45, stagger:0.05}}, 69.4);
tl.fromTo("#dy-cizgi", {{scaleX:0}}, {{scaleX:1, duration:0.7, ease:"power3.inOut"}}, 70.2);
tl.fromTo("#dy-adres", {{opacity:0, y:12}}, {{opacity:1, y:0, duration:0.8, ease:"power3.out"}}, 70.5);
tl.fromTo("#dy-yer", {{opacity:0}}, {{opacity:1, duration:0.8}}, 71.0);
tl.fromTo("#dy-soz", {{opacity:0, y:12, filter:"blur(4px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:1.0, ease:"power2.out"}}, 73.1);
tl.fromTo("#dy-imza", {{opacity:0}}, {{opacity:1, duration:0.8}}, 74.4);
tl.fromTo("#dy-demo", {{opacity:0}}, {{opacity:1, duration:0.6}}, 74.8);
tl.fromTo("#duyuru .desen-a", {{x:0}}, {{x:-140, duration:10.2, ease:"none"}}, 67.2);
tl.to("#duyuru", {{opacity:0, duration:0.5}}, 77.0);
// son
tl.fromTo("#son", {{opacity:0}}, {{opacity:1, duration:0.6}}, 77.2);
tl.fromTo("#logo3-w", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:1.6, ease:"power3.out"}}, 77.5);
tl.fromTo("#son-adres", {{opacity:0, y:10}}, {{opacity:1, y:0, duration:0.8}}, 79.0);
tl.fromTo("#son .desen-a", {{x:0}}, {{x:-120, duration:7.6, ease:"none"}}, 77.2);
tl.fromTo("#karart", {{opacity:0}}, {{opacity:1, duration:1.0, ease:"power1.in"}}, 83.8);
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
Path(__file__).with_name("index.html").write_text(html, encoding="utf-8")
print("index.html yazıldı")
