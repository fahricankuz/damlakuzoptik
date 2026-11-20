#!/usr/bin/env python3
"""Bölüm 10 (DEMO 2): Kuz İstanbul açılış duyurusu. Örnek videodaki gibi aydınlık, akıcı, kinetik yazı ve yüzen arayüz.
Kurgu müziğe oturtuldu: ses/muzik.mp3 117,5 BPM (vuruş ≈ 0,51 sn), yüksek bölüm 16,23 sn'de başlar, müzik 28,5 sn'de çözülür.
Marka karoları damlakuzoptik.com/pages/markalarimiz görselleridir (değiştirilmeden). Ürün fotoğrafları siteden.
Site ekranları aynı içerikle kuruldu; yalnızca logo ve alan adı Kuz İstanbul / kuz.istanbul."""
import math
import random
from pathlib import Path
from logo_yollari import PATHS, BOX

D = 30.0
SAND, SIYAH, KREM, SEFTALI = "#B2937F", "#231F20", "#F8F1E8", "#FEDCC7"
MARKA_AD = {"ray-ban": "Ray-Ban", "tom-ford": "Tom Ford", "vogue": "Vogue", "chopard": "Chopard",
            "etnia-barcelona": "Etnia Barcelona", "porsche-design": "Porsche Design", "prada": "Prada", "persol": "Persol"}


def fontfaces():
    out = []
    for w in (300, 400, 500, 600):
        for sub, rng in [("latin", "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122"),
                         ("latin-ext", "U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1E9F,U+20A0-20C0,U+2C60-2C7F,U+A720-A7FF")]:
            out.append(f"@font-face{{font-family:'Mont';font-style:normal;font-weight:{w};font-display:block;"
                       f"src:url('assets/fonts/montserrat-{sub}-{w}-normal.woff2') format('woff2');unicode-range:{rng};}}")
    return "\n".join(out)


def logo(lid, renk):
    x0, y0, x1, y1 = BOX
    g = "".join(f'<g id="{lid}-{grup}">' + "".join(f'<path id="{lid}-{pid}" d="{d}"/>' for pid, d in yollar) + "</g>"
                for grup, yollar in PATHS.items())
    return (f'<svg id="{lid}" class="logo" viewBox="{x0 - 4} {y0 - 4} {x1 - x0 + 8} {y1 - y0 + 8}" '
            f'xmlns="http://www.w3.org/2000/svg" fill="{renk}" overflow="visible">{g}</svg>')


def isaret(lid, renk):  # yalnızca logo işareti (kart için)
    ps = "".join(f'<path d="{d}"/>' for _, d in PATHS["mark"])
    return f'<svg id="{lid}" class="logo" viewBox="190 190 214 202" xmlns="http://www.w3.org/2000/svg" fill="{renk}">{ps}</svg>'


def karo(slug, cls="karo"):
    return (f'<div class="{cls}"><div class="karo-img" style="background-image:url(\'assets/media/markalar/{slug}.jpg\')"></div>'
            f'<div class="karo-ad">{MARKA_AD[slug]}</div></div>')


def kel(parcalar):
    return " ".join(f'<span class="kl {r}">{w}</span>' for m, r in parcalar for w in m.split())


CAM = (f'<svg viewBox="0 0 200 200" width="150" height="150"><defs>'
       f'<radialGradient id="cg" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#eef3f5"/><stop offset="1" stop-color="#d5e0e5"/></radialGradient>'
       f'<linearGradient id="cr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8dcd2"/><stop offset="1" stop-color="{SAND}"/></linearGradient></defs>'
       f'<ellipse cx="100" cy="104" rx="78" ry="74" fill="url(#cg)" stroke="url(#cr)" stroke-width="5"/>'
       f'<path d="M52 74 Q70 46 104 42" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" opacity=".95"/>'
       f'<path d="M140 150 Q156 136 162 118" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".7"/></svg>')
DURUM = ('<div class="durum"><span>9:41</span><span class="ikonlar">'
         '<svg width="34" height="20" viewBox="0 0 34 20"><rect x="0" y="13" width="6" height="7" rx="1.5"/><rect x="9" y="9" width="6" height="11" rx="1.5"/>'
         '<rect x="18" y="5" width="6" height="15" rx="1.5"/><rect x="27" y="0" width="6" height="20" rx="1.5"/></svg>'
         '<svg width="28" height="20" viewBox="0 0 28 20"><path d="M14 18 l4-4 a6 6 0 0 0 -8 0z M6 10 a11.5 11.5 0 0 1 16 0 l-2.6 2.6 a8 8 0 0 0 -10.8 0z M1.5 5.6 a18 18 0 0 1 25 0 l-2.6 2.6 a14.5 14.5 0 0 0 -19.8 0z"/></svg>'
         '<svg width="46" height="22" viewBox="0 0 46 22"><rect x="1" y="1" width="38" height="20" rx="6" fill="none" stroke="#111" stroke-opacity=".45" stroke-width="2"/>'
         '<rect x="4" y="4" width="32" height="14" rx="3.5"/><rect x="41" y="7" width="3" height="8" rx="1.5" opacity=".5"/></svg></span></div>')
TEL = f"""<div id="tel">
  <div class="tel-kalinlik"></div>
  <i class="tus" style="left:-5px;top:250px;height:64px"></i><i class="tus" style="left:-5px;top:360px;height:110px"></i>
  <i class="tus" style="left:-5px;top:490px;height:110px"></i><i class="tus" style="right:-5px;top:400px;height:170px"></i>
  <div class="tel-cerceve"><div class="tel-ic"><div class="tel-ekran">
    {DURUM}<div class="ada"></div>
    <div class="t-ust"><div class="ham"><i></i><i></i><i></i></div><div class="t-logo">{logo("tl", SIYAH)}</div>
      <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.6"><path d="M5 8h14l-1 12H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg></div>
    <div class="t-ara"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>Ne arıyorsunuz?</div>
    <div class="t-baslik">Kategoriler</div>
    <div class="kat" id="kat1"><div class="kat-g"><img src="assets/media/kat_optik.png" alt=""></div><div><div class="kat-ad">Optik Gözlük</div><div class="kat-k">Keşfet ›</div></div></div>
    <div class="kat" id="kat2"><div class="kat-g">{CAM}</div><div><div class="kat-ad">Optik Cam</div><div class="kat-k">Keşfet ›</div></div></div>
    <div class="kat" id="kat3"><div class="kat-g"><img src="assets/media/kat_gunes.png" alt=""></div><div><div class="kat-ad">Güneş Gözlüğü</div><div class="kat-k">Keşfet ›</div></div></div>
    <div class="t-alt"><i></i></div>
    <div class="cam-parlama"></div>
  </div></div></div>
</div>"""

rnd = random.Random(7)
KONF = []
for i in range(28):
    a = rnd.uniform(0, 6.283); r = rnd.uniform(260, 540)
    KONF.append((round(math.cos(a) * r), round(math.sin(a) * r * 0.8 - 60), rnd.randint(-260, 260),
                 [SAND, SEFTALI, SIYAH, "#d9c2b1"][i % 4], rnd.choice([14, 18, 22]), rnd.choice([8, 10, 26])))
konf_html = "".join(f'<i class="kf" style="width:{w}px;height:{h}px;background:{c}"></i>' for _, _, _, c, w, h in KONF)
konf_js = "[" + ",".join(f"[{x},{y},{r}]" for x, y, r, *_ in KONF) + "]"

PENCERE = ["ray-ban", "tom-ford", "vogue", "chopard", "etnia-barcelona", "porsche-design", "prada", "persol"]
UCAN = [("ray-ban", -300, -650, -10), ("tom-ford", 300, -620, 9), ("etnia-barcelona", -370, -270, -6),
        ("porsche-design", 370, -250, 7), ("vogue", -320, 340, 8), ("chopard", 320, 370, -9)]

html = f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<style>
{fontfaces()}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:{KREM}; }}
#root {{ position:relative; width:100%; height:100%; overflow:hidden; background:{KREM}; font-family:'Mont',sans-serif; }}
.tam {{ position:absolute; inset:0; }}
.logo {{ display:block; width:100%; height:auto; }}
#isik1 {{ position:absolute; left:-260px; top:-200px; width:1100px; height:1100px; border-radius:50%; background:radial-gradient(circle, rgba(254,220,199,.8) 0%, rgba(254,220,199,0) 65%); }}
#isik2 {{ position:absolute; left:300px; top:1000px; width:1100px; height:1100px; border-radius:50%; background:radial-gradient(circle, rgba(178,147,127,.26) 0%, rgba(178,147,127,0) 65%); }}
.kl {{ display:inline-block; opacity:0; }}
.s {{ color:{SAND}; }} .k {{ color:{SIYAH}; }}
.buyuk {{ position:absolute; left:70px; right:70px; text-align:center; font-weight:500; font-size:84px; line-height:1.18; letter-spacing:-.015em; }}
/* 1 */
#s1-y {{ top:900px; }}
#s1-kart {{ position:absolute; left:450px; top:650px; width:180px; height:180px; border-radius:44px; background:linear-gradient(145deg,#fff,#f3e7dc); box-shadow:0 30px 60px rgba(120,90,70,.22), inset 0 2px 0 #fff, inset 0 -6px 14px rgba(178,147,127,.18); display:flex; align-items:center; justify-content:center; }}
#s1-kart .logo {{ width:84px; }}
/* 2: telefon */
#s2 {{ perspective:2200px; }}
#tel {{ position:absolute; left:270px; top:560px; width:540px; height:1110px; transform-style:preserve-3d; }}
.tel-kalinlik {{ position:absolute; inset:0; border-radius:88px; background:linear-gradient(90deg,#2a2826,#5b5752 50%,#2a2826); transform:translateZ(-22px); }}
.tus {{ position:absolute; width:6px; border-radius:3px; background:linear-gradient(90deg,#3d3a37,#8f8a84,#3d3a37); transform:translateZ(-11px); }}
.tel-cerceve {{ position:absolute; inset:0; border-radius:88px; padding:6px; background:linear-gradient(135deg,#c9c3bb 0%,#6d6863 14%,#3a3734 45%,#5e5a55 80%,#cfc8c0 100%); box-shadow:0 70px 140px -30px rgba(70,45,30,.5), 0 30px 50px -25px rgba(70,45,30,.45); }}
.tel-ic {{ width:100%; height:100%; border-radius:82px; background:#060606; padding:15px; }}
.tel-ekran {{ position:relative; width:100%; height:100%; border-radius:68px; overflow:hidden; background:#fff; padding-top:96px; }}
.durum {{ position:absolute; left:0; right:0; top:22px; height:44px; display:flex; justify-content:space-between; align-items:center; padding:0 40px 0 58px; font-weight:600; font-size:27px; color:#111; z-index:4; }}
.ikonlar {{ display:flex; gap:9px; align-items:center; fill:#111; }}
.ada {{ position:absolute; top:20px; left:50%; width:150px; height:46px; margin-left:-75px; background:#000; border-radius:23px; z-index:5; }}
.t-ust {{ display:flex; align-items:center; justify-content:space-between; padding:6px 30px; }}
.t-logo {{ width:150px; }}
.ham i {{ display:block; width:30px; height:2.5px; background:#111; margin:6px 0; border-radius:2px; }}
.t-ara {{ margin:18px 26px 0; height:58px; border-radius:29px; background:#f5f1ed; display:flex; align-items:center; gap:12px; padding:0 22px; font-size:21px; color:#999; }}
.t-baslik {{ margin:28px 30px 12px; font-weight:600; font-size:28px; color:#111; }}
.kat {{ margin:14px 24px 0; height:196px; border-radius:30px; background:#f8f4f0; display:flex; align-items:center; gap:22px; padding:0 22px; border:2px solid rgba(0,0,0,0); }}
.kat-g {{ width:190px; height:150px; border-radius:22px; background:#fff; display:flex; align-items:center; justify-content:center; overflow:hidden; flex:none; }}
.kat-g img {{ width:180px; height:auto; }}
.kat-ad {{ font-weight:600; font-size:30px; color:#111; }}
.kat-k {{ margin-top:8px; font-weight:500; font-size:21px; color:{SAND}; }}
.t-alt {{ position:absolute; left:0; right:0; bottom:16px; display:flex; justify-content:center; }}
.t-alt i {{ width:170px; height:7px; border-radius:4px; background:#111; }}
.cam-parlama {{ position:absolute; inset:0; background:linear-gradient(118deg, rgba(255,255,255,.35) 0%, rgba(255,255,255,.08) 26%, rgba(255,255,255,0) 38%); pointer-events:none; z-index:6; }}
#s2-a, #s2-y2 {{ top:250px; }}
#suzme {{ position:absolute; left:-1400px; top:500px; width:1500px; height:900px; border-radius:50%; background:radial-gradient(ellipse at 60% 50%, {SAND} 0%, #c9a994 35%, rgba(254,220,199,.85) 60%, rgba(254,220,199,0) 75%); transform:rotate(-24deg); opacity:0; filter:blur(46px); }}
/* 3 */
#s3-etiket {{ position:absolute; left:160px; top:860px; font-weight:500; font-size:30px; color:#8c7b6e; }}
#s3-sayi {{ position:absolute; right:160px; top:800px; font-weight:500; font-size:92px; color:{SAND}; line-height:1; }}
#s3-sayi span {{ color:#d8c8bb; font-weight:400; }}
#s3-bar {{ position:absolute; left:160px; top:930px; width:760px; height:66px; border-radius:33px; background:#efe4da; box-shadow:inset 0 2px 6px rgba(120,90,70,.12); overflow:hidden; }}
#s3-dolu {{ position:absolute; inset:0; border-radius:33px; background:linear-gradient(90deg,#8f705c,{SAND} 55%,{SEFTALI}); transform-origin:0 50%; }}
#s3-tamam {{ position:absolute; left:0; right:0; top:760px; text-align:center; font-weight:500; font-size:84px; color:{SAND}; }}
#s3-tik {{ position:absolute; left:430px; top:900px; width:220px; height:220px; border-radius:110px; background:linear-gradient(145deg,#fff,#f4e9df); box-shadow:0 26px 60px rgba(120,90,70,.25), inset 0 2px 0 #fff; }}
#s3-tik svg {{ position:absolute; inset:0; }}
#konf {{ position:absolute; left:540px; top:1010px; }}
.kf {{ position:absolute; left:0; top:0; border-radius:3px; opacity:0; }}
/* 4 */
#s4 {{ perspective:1800px; }}
#pencere {{ position:absolute; left:60px; top:520px; width:960px; height:860px; border-radius:30px; background:#fff; box-shadow:0 50px 100px rgba(90,65,50,.25), 0 0 0 1px rgba(178,147,127,.25); overflow:hidden; transform-origin:50% 60%; }}
#p-bar {{ height:64px; background:#f6f1ec; display:flex; align-items:center; padding:0 24px; gap:10px; border-bottom:1px solid #eadfd5; }}
#p-bar i {{ width:14px; height:14px; border-radius:50%; background:#e0d3c8; display:block; }}
#p-url {{ margin-left:24px; flex:1; height:38px; border-radius:19px; background:#fff; display:flex; align-items:center; padding:0 20px; font-size:20px; font-weight:500; color:#555; border:1px solid #eadfd5; }}
#p-url b {{ color:#111; font-weight:600; }}
#p-ust {{ display:flex; align-items:center; justify-content:space-between; padding:22px 40px; border-bottom:1px solid #f0e8e1; }}
#p-ust .logo {{ width:170px; }}
#p-menu {{ display:flex; gap:26px; font-size:17px; font-weight:500; color:#333; }}
#p-baslik {{ text-align:center; margin-top:26px; font-weight:600; font-size:30px; color:#111; }}
#p-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:18px; padding:28px 40px; }}
.karo-img {{ width:100%; aspect-ratio:1; border-radius:8px; background-size:cover; background-position:center; }}
.karo-ad {{ margin-top:6px; text-align:center; font-weight:500; color:#222; font-size:15px; }}
#imlec {{ position:absolute; left:0; top:0; z-index:40; opacity:0; }}
.ucan {{ position:absolute; left:400px; top:780px; width:280px; padding:12px 12px 14px; background:#fff; border-radius:22px; box-shadow:0 30px 70px rgba(90,65,50,.25); opacity:0; }}
.ucan .karo-img {{ border-radius:14px; }}
.ucan .karo-ad {{ font-size:22px; margin-top:10px; font-weight:600; }}
#s4-y {{ top:860px; font-size:70px; }}
#s4-y2 {{ top:900px; font-size:62px; }}
/* 5 */
#s5-ust {{ position:absolute; left:0; right:0; top:700px; text-align:center; font-weight:600; font-size:24px; letter-spacing:.38em; color:{SAND}; padding-left:.38em; }}
#satir {{ position:absolute; left:90px; top:820px; width:900px; height:190px; border-radius:30px; background:#fff; box-shadow:0 30px 70px rgba(90,65,50,.18); display:flex; align-items:center; padding:0 34px; gap:28px; }}
#satir-ik {{ width:122px; height:122px; border-radius:24px; background:linear-gradient(145deg,{SEFTALI},#f6e6da); display:flex; align-items:center; justify-content:center; }}
#satir-b {{ font-weight:600; font-size:42px; color:#111; }}
#satir-a {{ margin-top:8px; font-weight:400; font-size:26px; color:#8c7b6e; }}
#dugme {{ position:absolute; left:320px; top:1060px; width:440px; height:94px; border-radius:20px; background:#111; color:#fff; font-weight:600; font-size:30px; display:flex; align-items:center; justify-content:center; box-shadow:0 20px 40px rgba(0,0,0,.25); opacity:0; }}
#hap {{ position:absolute; left:290px; top:1060px; width:500px; height:110px; border-radius:55px; background:linear-gradient(90deg,{SAND},#c9ab96); color:#fff; font-weight:600; font-size:36px; display:flex; align-items:center; justify-content:center; box-shadow:0 24px 60px rgba(178,147,127,.45); opacity:0; }}
/* 6 */
#s6 {{ perspective:1600px; }}
#fk-kart {{ position:absolute; left:210px; top:300px; width:660px; height:825px; border-radius:40px; overflow:hidden; background:#ddd; box-shadow:0 50px 100px rgba(90,65,50,.3), 0 0 0 10px #fff; }}
#fk-vid {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
#fk-ad {{ position:absolute; left:0; right:0; top:1210px; text-align:center; font-weight:600; font-size:28px; letter-spacing:.42em; color:{SAND}; padding-left:.42em; }}
#s6-y {{ top:1275px; font-size:66px; }}
/* 7 */
#son-logo {{ position:absolute; left:210px; top:800px; width:660px; }}
#son-adres {{ position:absolute; left:0; right:0; top:1100px; text-align:center; font-weight:400; font-size:46px; color:{SIYAH}; letter-spacing:.04em; }}
#son-alt {{ position:absolute; left:0; right:0; top:1182px; text-align:center; font-weight:600; font-size:22px; letter-spacing:.36em; color:{SAND}; padding-left:.36em; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
<div id="zemin" class="clip tam" data-start="0" data-duration="{D}" data-track-index="0"><div id="isik1"></div><div id="isik2"></div></div>

<div id="s1" class="clip tam" data-layout-allow-occlusion data-start="0" data-duration="4.3" data-track-index="1">
  <div id="s1-kart">{isaret("s1-lg", SAND)}</div>
  <div id="s1-y" class="buyuk">{kel([("Yarım asırlık", "s"), ("hikâye,", "k")])}<br>{kel([("özüne", "s"), ("dönüyor.", "k")])}</div>
</div>

<div id="s2" class="clip tam" data-layout-allow-occlusion data-start="4.0" data-duration="6.6" data-track-index="1">
  {TEL}
  <div id="s2-a" class="buyuk">{kel([("Optik", "s"), ("gözlük.", "k")])}</div>
  <div id="s2-b" class="buyuk" style="top:250px">{kel([("Optik", "s"), ("cam.", "k")])}</div>
  <div id="s2-c" class="buyuk" style="top:250px">{kel([("Güneş", "s"), ("gözlüğü.", "k")])}</div>
  <div id="s2-y2" class="buyuk">{kel([("Yarım asırdır,", "s")])}<br>{kel([("tek adreste.", "k")])}</div>
  <div id="suzme"></div>
</div>

<div id="s3" class="clip tam" data-layout-allow-occlusion data-start="10.2" data-duration="4.3" data-track-index="1">
  <div id="s3-etiket">kuz.istanbul hazırlanıyor</div>
  <div id="s3-sayi"><b id="s3-n">63</b><span>/100</span></div>
  <div id="s3-bar"><div id="s3-dolu"></div></div>
  <div id="s3-tamam">Hazır</div>
  <div id="konf">{konf_html}</div>
  <div id="s3-tik"><svg viewBox="0 0 220 220"><path id="tik-yol" d="M70 112 L100 140 L152 84" fill="none" stroke="{SAND}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg></div>
</div>

<div id="s4" class="clip tam" data-layout-allow-occlusion data-start="14.1" data-duration="5.2" data-track-index="1">
  <div id="pencere">
    <div id="p-bar"><i></i><i></i><i></i><div id="p-url"><b>kuz.istanbul</b>/markalarimiz</div></div>
    <div id="p-ust">{logo("p-lg", SIYAH)}<div id="p-menu"><span>Optik Gözlük</span><span>Optik Cam</span><span>Güneş Gözlüğü</span><span>Markalar</span></div></div>
    <div id="p-baslik">Markalarımız</div>
    <div id="p-grid">{"".join(karo(s) for s in PENCERE)}</div>
  </div>
  {"".join(f'<div class="ucan">{karo(s, "ic")}</div>' for s, *_ in UCAN)}
  <div id="s4-y" class="buyuk">{kel([("Ray-Ban.", "s"), ("Tom Ford.", "k")])}<br>{kel([("Chopard.", "s")])}</div>
  <div id="s4-y2" class="buyuk">{kel([("Dünya markaları,", "k")])}<br>{kel([("Kuz İstanbul'da.", "s")])}</div>
</div>

<div id="s5" class="clip tam" data-layout-allow-occlusion data-start="19.2" data-duration="3.2" data-track-index="1">
  <div id="s5-ust">AYNI ADRES · YENİ İSİM</div>
  <div id="satir"><div id="satir-ik"><svg viewBox="0 0 48 48" width="64" height="64"><path d="M24 4c-8 0-14 6-14 14 0 10 14 26 14 26s14-16 14-26c0-8-6-14-14-14z" fill="{SAND}"/><circle cx="24" cy="18" r="5.5" fill="{KREM}"/></svg></div>
    <div><div id="satir-b">Ataköy Atrium AVM</div><div id="satir-a">Kuz İstanbul mağazası · İstanbul</div></div></div>
  <div id="dugme">Mağazaya gel</div>
  <div id="hap">Sizi bekliyoruz</div>
</div>

<div id="s6" class="clip tam" data-layout-allow-occlusion data-start="22.3" data-duration="3.6" data-track-index="1">
  <div id="fk-kart"><video id="fk-vid" class="clip" data-start="22.3" data-duration="3.6" data-track-index="2" src="assets/media/fk_kart.mp4" muted playsinline></video></div>
  <div id="fk-ad">FAHRİ KUZ</div>
  <div id="s6-y" class="buyuk">{kel([("Yarım asırlık", "s"), ("hikâye,", "k")])}<br>{kel([("özüne", "s"), ("dönüyor.", "k")])}</div>
</div>

<div id="s7" class="clip tam" data-layout-allow-occlusion data-start="25.8" data-duration="4.2" data-track-index="1">
  <div id="son-logo">{logo("sl", SIYAH)}</div>
  <div id="son-adres">kuz.istanbul</div>
  <div id="son-alt">1 ŞUBAT 2027 · ATAKÖY ATRIUM AVM</div>
</div>

<div id="imlec" class="clip" data-layout-allow-occlusion data-start="14.1" data-duration="8.2" data-track-index="3"><svg viewBox="0 0 28 36" width="46" height="59"><path d="M2 2 L2 28 L9 21 L14 33 L19 31 L14 19 L24 19 Z" fill="#111" stroke="#fff" stroke-width="2.2" stroke-linejoin="round"/></svg></div>
<audio id="miks" class="clip" data-start="0" data-duration="{D}" data-track-index="6" data-volume="1" src="assets/audio/miks.m4a"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
const B = 0.5106;                       // bir vuruş
const giris = (sel, t, a) => gsap.utils.toArray(sel).forEach((el, i) =>
  tl.fromTo(el, {{opacity:0, y:26, filter:"blur(16px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.55, ease:"power3.out"}}, t + i*a));
const cikis = (sel, t) => tl.to(sel, {{opacity:0, y:-18, filter:"blur(14px)", duration:0.32, ease:"power2.in"}}, t);
tl.fromTo("#isik1", {{x:0, y:0}}, {{x:220, y:260, duration:{D}, ease:"none"}}, 0);
tl.fromTo("#isik2", {{x:0, y:0}}, {{x:-260, y:-300, duration:{D}, ease:"none"}}, 0);

// 1 · sakin giriş
giris("#s1-y .kl", 0.25, B);
tl.fromTo("#s1-kart", {{opacity:0, scale:0.4, rotation:-12, y:30}}, {{opacity:1, scale:1, rotation:0, y:0, duration:0.7, ease:"back.out(1.8)"}}, 0.25 + 5*B);
tl.to("#s1-kart", {{y:-12, duration:1.0, ease:"sine.inOut"}}, 3.0);
cikis("#s1-y .kl", 3.8);
tl.to("#s1-kart", {{y:600, scale:0.5, opacity:0, duration:0.5, ease:"power2.in"}}, 3.8);

// 2 · gerçekçi telefon: kategoriler
tl.fromTo("#tel", {{y:1300, rotationX:38, rotationY:-24, rotationZ:6}}, {{y:0, rotationX:10, rotationY:-16, rotationZ:0, duration:1.2, ease:"power3.out"}}, 4.0);
tl.to("#tel", {{rotationX:4, rotationY:14, duration:5.0, ease:"sine.inOut"}}, 5.2);
const kat = (sel, metin, t) => {{
  giris(metin + " .kl", t, 0.16);
  tl.to(sel, {{scale:1.04, borderColor:"{SAND}", backgroundColor:"#ffffff", boxShadow:"0 18px 40px rgba(178,147,127,.35)", duration:0.35, ease:"power2.out"}}, t);
  tl.to(sel, {{scale:1, borderColor:"rgba(0,0,0,0)", backgroundColor:"#f8f4f0", boxShadow:"0 0 0 rgba(0,0,0,0)", duration:0.3}}, t + 2*B - 0.12);
  cikis(metin + " .kl", t + 2*B - 0.2);
}};
kat("#kat1", "#s2-a", 4.25 + 2*B);
kat("#kat2", "#s2-b", 4.25 + 4*B);
kat("#kat3", "#s2-c", 4.25 + 6*B);
giris("#s2-y2 .kl", 4.25 + 8*B, 0.3);
tl.fromTo("#suzme", {{x:0, y:300, opacity:1}}, {{x:2700, y:-500, duration:0.8, ease:"power2.inOut", immediateRender:false}}, 9.75);
tl.to("#tel", {{x:-900, rotationY:-30, opacity:0, duration:0.55, ease:"power2.in"}}, 9.9);
cikis("#s2-y2 .kl", 9.95);

// 3 · yükleme, "Hazır"
tl.fromTo("#s3-etiket,#s3-sayi,#s3-bar", {{opacity:0, y:22}}, {{opacity:1, y:0, duration:0.45, stagger:0.06, ease:"power3.out"}}, 10.25);
tl.fromTo("#s3-dolu", {{scaleX:0.63}}, {{scaleX:1, duration:1.6, ease:"power2.inOut"}}, 10.5);
const sy = {{v:63}};
tl.fromTo(sy, {{v:63}}, {{v:100, duration:1.6, ease:"power2.inOut", onUpdate:() => {{ document.getElementById("s3-n").textContent = Math.round(sy.v); }}}}, 10.5);
tl.to("#s3-etiket,#s3-sayi,#s3-bar", {{opacity:0, y:-20, filter:"blur(8px)", duration:0.3, ease:"power2.in"}}, 12.0);
tl.set("#s3-tamam,#s3-tik", {{opacity:0}}, 10.2);
tl.fromTo("#s3-tik", {{opacity:0, scale:0.3}}, {{opacity:1, scale:1, duration:0.55, ease:"back.out(2)"}}, 12.25);
tl.to("#tik-yol", {{strokeDashoffset:0, duration:0.4, ease:"power2.out"}}, 12.5);
tl.fromTo("#s3-tamam", {{opacity:0, y:20, filter:"blur(10px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.5, ease:"power3.out"}}, 12.35);
{konf_js}.forEach(([x, y, r], i) => {{
  const el = document.querySelectorAll("#konf .kf")[i];
  tl.fromTo(el, {{x:0, y:0, rotation:0, opacity:1}}, {{x:x, y:y, rotation:r, duration:0.9, ease:"power3.out"}}, 12.35);
  tl.to(el, {{y:y + 160, opacity:0, duration:0.6, ease:"power1.in"}}, 13.2);
}});
tl.to("#s3-tamam", {{opacity:0, filter:"blur(10px)", duration:0.3}}, 13.3);
// onay dairesi yuvarlak kareye döner ve büyüyerek pencereye geçer
tl.to("#tik-yol", {{opacity:0, duration:0.2}}, 13.35);
tl.to("#s3-tik", {{borderRadius:52, duration:0.45, ease:"power2.inOut"}}, 13.4);
tl.to("#s3-tik", {{scale:4.4, opacity:0, duration:0.45, ease:"power2.in"}}, 13.95);

// 4 · kuz.istanbul/markalarimiz: imleç tıklar, vuruşta (16,23) markalar dağılır
tl.fromTo("#pencere", {{opacity:0, rotationX:34, y:200, scale:0.8}}, {{opacity:1, rotationX:0, y:0, scale:1, duration:1.1, ease:"power3.out"}}, 14.15);
tl.to("#pencere", {{scale:1.04, duration:1.0, ease:"sine.inOut"}}, 15.2);
tl.fromTo("#imlec", {{opacity:0, x:960, y:1500}}, {{opacity:1, x:960, y:1500, duration:0.2}}, 15.1);
tl.to("#imlec", {{x:780, y:1030, duration:0.8, ease:"power2.inOut"}}, 15.2);
tl.to("#p-grid .karo:nth-child(4)", {{scale:1.07, duration:0.25, ease:"power2.out"}}, 15.85);
tl.to("#imlec", {{scale:0.85, duration:0.07, yoyo:true, repeat:1}}, 16.1);
tl.to("#imlec", {{opacity:0, duration:0.15}}, 16.3);
tl.to("#pencere", {{opacity:0, scale:0.86, filter:"blur(12px)", duration:0.35, ease:"power2.in"}}, 16.2);
{[[x, y, r] for _, x, y, r in UCAN]}.forEach(([x, y, r], i) => {{
  const el = document.querySelectorAll(".ucan")[i];
  tl.fromTo(el, {{opacity:0, x:0, y:0, scale:0.5, rotation:0}}, {{opacity:1, x:x, y:y, scale:1, rotation:r, duration:0.75, ease:"expo.out"}}, 16.23 + i*0.035);
  tl.to(el, {{y:y - 46, rotation:r*0.6, duration:2.4, ease:"none"}}, 17.0);
  tl.to(el, {{opacity:0, scale:0.85, filter:"blur(8px)", duration:0.3, ease:"power2.in"}}, 18.9);
}});
giris("#s4-y .kl", 16.4, B/2);
cikis("#s4-y .kl", 17.75);
giris("#s4-y2 .kl", 18.0, 0.22);
cikis("#s4-y2 .kl", 18.9);

// 5 · Ataköy Atrium AVM
tl.fromTo("#s5-ust", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.5}}, 19.3);
tl.fromTo("#satir", {{opacity:0, y:40, scale:0.94}}, {{opacity:1, y:0, scale:1, duration:0.6, ease:"power3.out"}}, 19.3);
tl.fromTo("#dugme", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, 20.3);
tl.fromTo("#imlec", {{opacity:0, x:900, y:1400}}, {{opacity:1, x:900, y:1400, duration:0.2}}, 20.3);
tl.to("#imlec", {{x:600, y:1110, duration:0.7, ease:"power2.inOut"}}, 20.45);
tl.to("#imlec", {{scale:0.85, duration:0.07, yoyo:true, repeat:1}}, 21.25);
tl.to("#dugme", {{scale:0.95, duration:0.07, yoyo:true, repeat:1}}, 21.25);
tl.to("#imlec", {{opacity:0, duration:0.15}}, 21.5);
tl.to("#dugme", {{opacity:0, scale:0.9, duration:0.2}}, 21.4);
tl.fromTo("#hap", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.7)"}}, 21.45);
tl.to("#s5-ust,#satir,#hap", {{opacity:0, filter:"blur(10px)", duration:0.3}}, 22.1);

// 6 · Fahri Kuz
tl.fromTo("#fk-kart", {{opacity:0, rotationY:-28, rotationX:8, y:80, scale:0.9}}, {{opacity:1, rotationY:0, rotationX:0, y:0, scale:1, duration:1.0, ease:"power3.out"}}, 22.3);
tl.to("#fk-kart", {{rotationY:5, duration:2.6, ease:"sine.inOut"}}, 23.3);
tl.fromTo("#fk-ad", {{opacity:0}}, {{opacity:1, duration:0.5}}, 22.85);
giris("#s6-y .kl", 23.35, B/2);
tl.to("#fk-kart,#fk-ad,#s6-y .kl", {{opacity:0, filter:"blur(12px)", duration:0.35, ease:"power2.in"}}, 25.45);

// 7 · logo işareti vuruşlarla kurulur, sonra KUZ İSTANBUL açılır
tl.set("#sl-kuz path,#sl-ist path,#sl-mark path", {{opacity:0}}, 25.8);
tl.set("#son-logo", {{x:274, scale:1.3, transformOrigin:"50% 50%"}}, 25.8);
tl.fromTo("#sl-lm-bar", {{opacity:1, clipPath:"inset(100% 0% 0% 0%)"}}, {{clipPath:"inset(0% 0% 0% 0%)", duration:0.4, ease:"power3.out"}}, 25.89);
tl.fromTo("#sl-lm-ok", {{opacity:0, x:70}}, {{opacity:1, x:0, duration:0.45, ease:"expo.out"}}, 25.89 + B);
tl.fromTo("#sl-lm-uc", {{opacity:0}}, {{opacity:1, duration:0.35, ease:"power2.out"}}, 25.89 + 2*B);
tl.to("#son-logo", {{x:0, scale:1, duration:0.6, ease:"power3.inOut"}}, 26.85);
gsap.utils.toArray("#sl-kuz path").forEach((p, i) => tl.fromTo(p, {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, 27.2 + i*0.08));
gsap.utils.toArray("#sl-ist path").forEach((p, i) => tl.fromTo(p, {{opacity:0, x:-10}}, {{opacity:1, x:0, duration:0.35, ease:"power2.out"}}, 27.5 + i*0.04));
tl.fromTo("#son-adres", {{opacity:0, y:14, filter:"blur(8px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.5, ease:"power3.out"}}, 27.85);
tl.fromTo("#son-alt", {{opacity:0}}, {{opacity:1, duration:0.6}}, 28.15);
tl.to("#son-logo", {{scale:1.025, duration:2.0, ease:"none"}}, 28.0);
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
Path(__file__).with_name("index.html").write_text(html, encoding="utf-8")
print("index.html yazıldı")
