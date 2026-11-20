#!/usr/bin/env python3
"""Bölüm 10 (DEMO): Kuz İstanbul açılış duyurusu. Aydınlık, kinetik tipografi, yüzen arayüz kartları.
Marka görselleri damlakuzoptik.com/pages/markalarimiz sayfasındaki karolardan (değiştirilmeden) alınmıştır;
site ekranları aynı düzenle, yalnızca logo ve alan adı Kuz İstanbul / kuz.istanbul olarak kurulmuştur."""
import random
from pathlib import Path
from logo_yollari import PATHS, BOX

D = 30.0
SAND, SIYAH, KREM, SEFTALI = "#B2937F", "#231F20", "#F8F1E8", "#FEDCC7"
MARKALAR = {"armani-exchange": "Armani Exchange", "burberry": "Burberry", "bvlgari": "Bvlgari", "chloe": "Chloe",
            "chopard": "Chopard", "dolce-gabbana": "Dolce & Gabbana", "emporio-armani": "Emporio Armani",
            "ermenegildo-zegna": "Ermenegildo Zegna", "etnia-barcelona": "Etnia Barcelona", "fendi": "Fendi",
            "furla": "Furla", "giorgio-armani": "Giorgio Armani", "guess": "Guess", "jimmy-choo": "Jimmy Choo",
            "max-mara": "Max Mara", "maybach": "Maybach", "michael-kors": "Michael Kors", "miu-miu": "Miu Miu",
            "omega": "Omega", "oliver-peoples": "Oliver Peoples", "persol": "Persol", "philipp-plein": "Philipp Plein",
            "police": "Police", "porsche-design": "Porsche Design", "prada": "Prada", "ray-ban": "Ray-Ban",
            "serengeti": "Serengeti", "swarovski": "Swarovski", "tiffany-co": "Tiffany&Co", "tom-ford": "Tom Ford",
            "versace": "Versace", "vogue": "Vogue"}


def fontfaces():
    out = []
    fam = [("Mont", "montserrat", w, "normal") for w in (300, 400, 500, 600)] + [("Nord Yerine", "krona-one", 400, "normal")]
    for name, file, w, st in fam:
        for sub, rng in [("latin", "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122"),
                         ("latin-ext", "U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1E9F,U+20A0-20C0,U+2C60-2C7F,U+A720-A7FF")]:
            out.append(f"@font-face{{font-family:'{name}';font-style:{st};font-weight:{w};font-display:block;"
                       f"src:url('assets/fonts/{file}-{sub}-{w}-{st}.woff2') format('woff2');unicode-range:{rng};}}")
    return "\n".join(out)


def logo(lid, renk, sadece_isaret=False):
    x0, y0, x1, y1 = BOX
    gruplar = {"mark": PATHS["mark"]} if sadece_isaret else PATHS
    ps = "".join(f'<path d="{d}"/>' for g in gruplar.values() for _, d in g)
    if sadece_isaret:
        xs = [194, 300]  # işaret kutusu (logo_yollari BOX'ın sol kısmı)
        return (f'<svg id="{lid}" class="logo" viewBox="190 190 {(x1 - x0) * 0.36:.0f} {y1 - y0 + 8}" '
                f'xmlns="http://www.w3.org/2000/svg" fill="{renk}">{ps}</svg>')
    return (f'<svg id="{lid}" class="logo" viewBox="{x0 - 4} {y0 - 4} {x1 - x0 + 8} {y1 - y0 + 8}" '
            f'xmlns="http://www.w3.org/2000/svg" fill="{renk}">{ps}</svg>')


def karo(slug, cls="karo"):
    return (f'<div class="{cls}"><div class="karo-img" style="background-image:url(\'assets/media/markalar/{slug}.jpg\')"></div>'
            f'<div class="karo-ad">{MARKALAR[slug]}</div></div>')


def kelimeler(parcalar, cls):
    # parcalar: [(metin, renk_sinifi)]
    return " ".join(f'<span class="{cls} {r}">{w}</span>' for m, r in parcalar for w in m.split())


def telefon(pid, sluglar):
    return (f'<div class="tel" id="{pid}"><div class="tel-ekran">'
            f'<div class="tel-ust"><div class="ham"><i></i><i></i><i></i></div>{logo(pid + "-lg", SIYAH)}<div class="canta"></div></div>'
            f'<div class="tel-baslik">Markalarımız</div>'
            f'<div class="tel-grid">{"".join(karo(s, "karo kucuk") for s in sluglar)}</div>'
            f'</div></div>')


IKON_PIN = (f'<svg viewBox="0 0 48 48" width="64" height="64"><path d="M24 4c-8 0-14 6-14 14 0 10 14 26 14 26s14-16 14-26c0-8-6-14-14-14z" fill="{SAND}"/>'
            f'<circle cx="24" cy="18" r="5.5" fill="{KREM}"/></svg>')
IMLEC = ('<svg viewBox="0 0 28 36" width="46" height="59"><path d="M2 2 L2 28 L9 21 L14 33 L19 31 L14 19 L24 19 Z" '
         'fill="#111" stroke="#fff" stroke-width="2.2" stroke-linejoin="round"/></svg>')
YILDIZ = (f'<svg viewBox="-50 -50 100 100" width="100%" height="100%"><path d="M0,-48 C4,-12 12,-4 48,0 C12,4 4,12 0,48 C-4,12 -12,4 -48,0 C-12,-4 -4,-12 0,-48 Z" fill="url(#yg)"/>'
          f'<defs><linearGradient id="yg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{SEFTALI}"/><stop offset="1" stop-color="{SAND}"/></linearGradient></defs></svg>')

# konfeti: sabit tohumla, her render aynı
rnd = random.Random(7)
KONF = []
for i in range(26):
    a = rnd.uniform(0, 6.283)
    r = rnd.uniform(260, 520)
    import math
    KONF.append(dict(x=round(math.cos(a) * r), y=round(math.sin(a) * r * 0.8 - 60), rot=rnd.randint(-260, 260),
                     renk=[SAND, SEFTALI, SIYAH, "#d9c2b1"][i % 4], w=rnd.choice([14, 18, 22]), h=rnd.choice([8, 10, 26])))
konf_html = "".join(f'<i class="kf" style="width:{k["w"]}px;height:{k["h"]}px;background:{k["renk"]}"></i>' for k in KONF)
konf_js = "[" + ",".join(f'[{k["x"]},{k["y"]},{k["rot"]}]' for k in KONF) + "]"

TELLER = [("telA", ["ray-ban", "tom-ford", "vogue", "chopard", "prada", "persol"]),
          ("telB", ["etnia-barcelona", "porsche-design", "versace", "burberry", "bvlgari", "chloe"]),
          ("telC", ["tom-ford", "jimmy-choo", "max-mara", "maybach", "fendi", "furla"]),
          ("telD", ["chopard", "ray-ban", "oliver-peoples", "swarovski", "miu-miu", "omega"])]
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
:root {{ --sand:{SAND}; --siyah:{SIYAH}; --krem:{KREM}; --seftali:{SEFTALI}; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:var(--krem); }}
#root {{ position:relative; width:100%; height:100%; overflow:hidden; background:var(--krem); font-family:'Mont',sans-serif; }}
.tam {{ position:absolute; inset:0; }}
.logo {{ display:block; width:100%; height:auto; }}
/* zemin ışıkları */
#isik1 {{ position:absolute; left:-260px; top:-200px; width:1100px; height:1100px; border-radius:50%; background:radial-gradient(circle, rgba(254,220,199,.75) 0%, rgba(254,220,199,0) 65%); }}
#isik2 {{ position:absolute; left:300px; top:1000px; width:1100px; height:1100px; border-radius:50%; background:radial-gradient(circle, rgba(178,147,127,.28) 0%, rgba(178,147,127,0) 65%); }}
/* kinetik yazı */
.kl {{ display:inline-block; opacity:0; }}
.s {{ color:var(--sand); }} .k {{ color:var(--siyah); }}
#s1-y {{ position:absolute; left:80px; right:80px; top:900px; text-align:center; font-weight:500; font-size:82px; line-height:1.2; letter-spacing:-.01em; }}
#s1-kart {{ position:absolute; left:440px; top:640px; width:200px; height:200px; border-radius:46px; background:linear-gradient(145deg,#fff, #f3e7dc); box-shadow:0 30px 60px rgba(120,90,70,.22), inset 0 2px 0 #fff, inset 0 -6px 14px rgba(178,147,127,.18); display:flex; align-items:center; justify-content:center; }}
#s1-kart .logo {{ width:96px; }}
/* telefonlar */
#s2 {{ perspective:1500px; }}
#tel-sahne {{ position:absolute; left:0; top:0; width:1080px; height:1920px; transform-style:preserve-3d; }}
.tel {{ position:absolute; width:400px; height:840px; border-radius:62px; background:#151313; padding:14px; box-shadow:0 40px 80px rgba(60,40,30,.28); }}
.tel-ekran {{ width:100%; height:100%; border-radius:50px; background:#fff; overflow:hidden; padding:58px 18px 0; }}
.tel-ust {{ display:flex; align-items:center; justify-content:space-between; height:52px; padding:0 8px; }}
.tel-ust .logo {{ width:120px; }}
.ham i {{ display:block; width:26px; height:2.5px; background:#222; margin:5px 0; }}
.canta {{ width:24px; height:24px; border:2.5px solid #222; border-radius:4px; }}
.tel-baslik {{ margin:22px 0 14px; text-align:center; font-weight:600; font-size:22px; color:#111; }}
.tel-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
.karo-img {{ width:100%; aspect-ratio:1; border-radius:8px; background-size:cover; background-position:center; }}
.karo-ad {{ margin-top:6px; text-align:center; font-weight:500; color:#222; }}
.kucuk .karo-ad {{ font-size:13px; }}
#telA {{ left:-70px; top:230px; transform:rotateY(58deg) rotateZ(-6deg); }}
#telB {{ left:750px; top:860px; transform:rotateY(-58deg) rotateZ(-6deg); }}
#telC {{ left:520px; top:-330px; transform:rotateX(-62deg) rotateZ(16deg); }}
#telD {{ left:160px; top:1400px; transform:rotateX(62deg) rotateZ(16deg); }}
#s2-perde {{ position:absolute; left:20px; right:20px; top:760px; height:380px; background:radial-gradient(ellipse at center, rgba(248,241,232,.97) 42%, rgba(248,241,232,0) 70%); }}
#s2-y {{ position:absolute; left:120px; right:120px; top:880px; text-align:center; font-weight:500; font-size:66px; line-height:1.2; }}
#s2-y2 {{ position:absolute; left:120px; right:120px; top:920px; text-align:center; font-weight:500; font-size:66px; line-height:1.2; }}
/* yükleme */
#s3-etiket {{ position:absolute; left:160px; top:860px; font-weight:500; font-size:30px; color:#8c7b6e; letter-spacing:.02em; }}
#s3-sayi {{ position:absolute; right:160px; top:800px; font-weight:500; font-size:92px; color:var(--sand); line-height:1; }}
#s3-sayi span {{ color:#d8c8bb; font-weight:400; }}
#s3-bar {{ position:absolute; left:160px; top:930px; width:760px; height:66px; border-radius:33px; background:#efe4da; box-shadow:inset 0 2px 6px rgba(120,90,70,.12); overflow:hidden; }}
#s3-dolu {{ position:absolute; left:0; top:0; height:100%; width:100%; border-radius:33px; background:linear-gradient(90deg, #8f705c, {SAND} 55%, {SEFTALI}); transform-origin:0 50%; box-shadow:0 10px 40px rgba(178,147,127,.45); }}
#s3-tamam {{ position:absolute; left:0; right:0; top:760px; text-align:center; font-weight:500; font-size:84px; color:var(--sand); }}
#s3-tik {{ position:absolute; left:430px; top:900px; width:220px; height:220px; border-radius:50%; background:linear-gradient(145deg,#fff,#f4e9df); box-shadow:0 26px 60px rgba(120,90,70,.25), inset 0 2px 0 #fff; }}
#s3-tik svg {{ position:absolute; inset:0; }}
#konf {{ position:absolute; left:540px; top:1010px; }}
.kf {{ position:absolute; left:0; top:0; border-radius:3px; opacity:0; }}
/* tarayıcı penceresi */
#s4 {{ perspective:1700px; }}
#pencere {{ position:absolute; left:60px; top:520px; width:960px; height:860px; border-radius:30px; background:#fff; box-shadow:0 50px 100px rgba(90,65,50,.25), 0 0 0 1px rgba(178,147,127,.25); overflow:hidden; transform-origin:50% 60%; }}
#p-bar {{ height:64px; background:#f6f1ec; display:flex; align-items:center; padding:0 24px; gap:10px; border-bottom:1px solid #eadfd5; }}
#p-bar i {{ width:14px; height:14px; border-radius:50%; background:#e0d3c8; display:block; }}
#p-url {{ margin-left:24px; flex:1; height:38px; border-radius:19px; background:#fff; display:flex; align-items:center; padding:0 20px; font-size:20px; font-weight:500; color:#555; border:1px solid #eadfd5; }}
#p-url b {{ color:#111; font-weight:600; }}
#p-ust {{ display:flex; align-items:center; justify-content:space-between; padding:22px 40px; border-bottom:1px solid #f0e8e1; }}
#p-ust .logo {{ width:170px; }}
#p-menu {{ display:flex; gap:28px; font-size:17px; font-weight:500; color:#333; }}
#p-baslik {{ text-align:center; margin-top:26px; font-weight:600; font-size:30px; color:#111; }}
#p-ara {{ margin:16px auto 0; width:420px; height:44px; border-radius:22px; border:1px solid #e6dbd1; font-size:17px; color:#999; display:flex; align-items:center; padding:0 20px; }}
#p-grid {{ display:grid; grid-template-columns:repeat(4, 1fr); gap:18px; padding:24px 40px; }}
#p-grid .karo-ad {{ font-size:15px; }}
#imlec {{ position:absolute; left:0; top:0; z-index:40; opacity:0; }}
.ucan {{ position:absolute; left:400px; top:780px; width:280px; padding:12px 12px 14px; background:#fff; border-radius:22px; box-shadow:0 30px 70px rgba(90,65,50,.25); opacity:0; }}
.ucan .karo-img {{ border-radius:14px; }}
.ucan .karo-ad {{ font-size:22px; margin-top:10px; font-weight:600; }}
#s4-y {{ position:absolute; left:110px; right:110px; top:880px; text-align:center; font-weight:500; font-size:64px; line-height:1.2; }}
/* mağaza */
#s5-ust {{ position:absolute; left:0; right:0; top:700px; text-align:center; font-weight:600; font-size:24px; letter-spacing:.38em; color:var(--sand); padding-left:.38em; }}
#satir {{ position:absolute; left:90px; top:820px; width:900px; height:190px; border-radius:30px; background:#fff; box-shadow:0 30px 70px rgba(90,65,50,.18); display:flex; align-items:center; padding:0 34px; gap:28px; }}
#satir-ik {{ width:122px; height:122px; border-radius:24px; background:linear-gradient(145deg,{SEFTALI},#f6e6da); display:flex; align-items:center; justify-content:center; }}
#satir-b {{ font-weight:600; font-size:42px; color:#111; }}
#satir-a {{ margin-top:8px; font-weight:400; font-size:26px; color:#8c7b6e; }}
#dugme {{ position:absolute; left:320px; top:1060px; width:440px; height:94px; border-radius:20px; background:#111; color:#fff; font-weight:600; font-size:30px; display:flex; align-items:center; justify-content:center; box-shadow:0 20px 40px rgba(0,0,0,.25); opacity:0; }}
#hap {{ position:absolute; left:290px; top:1060px; width:500px; height:110px; border-radius:55px; background:linear-gradient(90deg,{SAND},#c9ab96); color:#fff; font-weight:600; font-size:36px; display:flex; align-items:center; justify-content:center; box-shadow:0 24px 60px rgba(178,147,127,.45); opacity:0; }}
/* Fahri Kuz */
#s6 {{ perspective:1600px; }}
#fk-kart {{ position:absolute; left:210px; top:300px; width:660px; height:825px; border-radius:40px; overflow:hidden; background:#ddd; box-shadow:0 50px 100px rgba(90,65,50,.3), 0 0 0 10px #fff; }}
#fk-vid {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
#fk-ad {{ position:absolute; left:0; right:0; top:1210px; text-align:center; font-weight:600; font-size:28px; letter-spacing:.42em; color:var(--sand); padding-left:.42em; }}
#s6-y {{ position:absolute; left:80px; right:80px; top:1275px; text-align:center; font-weight:500; font-size:64px; line-height:1.2; }}
/* kapanış */
#yildiz {{ position:absolute; left:440px; top:860px; width:200px; height:200px; }}
#son-logo {{ position:absolute; left:210px; top:780px; width:660px; }}
#son-adres {{ position:absolute; left:0; right:0; top:1100px; text-align:center; font-weight:400; font-size:44px; color:var(--siyah); letter-spacing:.04em; }}
#son-alt {{ position:absolute; left:0; right:0; top:1180px; text-align:center; font-weight:600; font-size:22px; letter-spacing:.36em; color:var(--sand); padding-left:.36em; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
<div id="zemin" class="clip tam" data-start="0" data-duration="{D}" data-track-index="0"><div id="isik1"></div><div id="isik2"></div></div>

<div id="s1" class="clip tam" data-layout-allow-occlusion data-start="0" data-duration="4.4" data-track-index="1">
  <div id="s1-kart">{logo("s1-lg", SAND, sadece_isaret=True)}</div>
  <div id="s1-y">{kelimeler([("Yarım asırlık", "s"), ("hikâye,", "k")], "kl")}<br>{kelimeler([("özüne", "s"), ("dönüyor.", "k")], "kl")}</div>
</div>

<div id="s2" class="clip tam" data-layout-allow-occlusion data-start="4.2" data-duration="4.6" data-track-index="1">
  <div id="tel-sahne">{"".join(telefon(p, s) for p, s in TELLER)}</div>
  <div id="s2-perde"></div>
  <div id="s2-y">{kelimeler([("Ray-Ban.", "s"), ("Tom Ford.", "k"), ("Vogue.", "s")], "kl")}</div>
  <div id="s2-y2">{kelimeler([("Hepsi", "k"), ("tek adreste.", "s")], "kl")}</div>
</div>

<div id="s3" class="clip tam" data-layout-allow-occlusion data-start="8.6" data-duration="3.7" data-track-index="1">
  <div id="s3-etiket">kuz.istanbul hazırlanıyor</div>
  <div id="s3-sayi"><b id="s3-n">63</b><span>/100</span></div>
  <div id="s3-bar"><div id="s3-dolu"></div></div>
  <div id="s3-tamam">Hazır</div>
  <div id="konf">{konf_html}</div>
  <div id="s3-tik"><svg viewBox="0 0 220 220"><path id="tik-yol" d="M70 112 L100 140 L152 84" fill="none" stroke="{SAND}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg></div>
</div>

<div id="s4" class="clip tam" data-layout-allow-occlusion data-start="12.2" data-duration="5.3" data-track-index="1">
  <div id="pencere">
    <div id="p-bar"><i></i><i></i><i></i><div id="p-url"><b>kuz.istanbul</b>/markalarimiz</div></div>
    <div id="p-ust">{logo("p-lg", SIYAH)}<div id="p-menu"><span>Güneş Gözlüğü</span><span>Optik</span><span>Markalar</span><span>Mağaza</span></div></div>
    <div id="p-baslik">Markalarımız</div>
    <div id="p-ara">Marka ara…</div>
    <div id="p-grid">{"".join(karo(s) for s in PENCERE)}</div>
  </div>
  {"".join(f'<div class="ucan" id="u-{s}">{karo(s, "ic")}</div>' for s, *_ in UCAN)}
  <div id="s4-y">{kelimeler([("Chopard.", "s"), ("Etnia Barcelona.", "k"), ("Porsche Design.", "s")], "kl")}</div>
</div>

<div id="s5" class="clip tam" data-layout-allow-occlusion data-start="17.4" data-duration="4.3" data-track-index="1">
  <div id="s5-ust">AYNI ADRES · YENİ İSİM</div>
  <div id="satir"><div id="satir-ik">{IKON_PIN}</div><div><div id="satir-b">Ataköy Atrium AVM</div><div id="satir-a">Kuz İstanbul mağazası · İstanbul</div></div></div>
  <div id="dugme">Mağazaya gel</div>
  <div id="hap">Sizi bekliyoruz</div>
</div>

<div id="s6" class="clip tam" data-layout-allow-occlusion data-start="21.6" data-duration="4.2" data-track-index="1">
  <div id="fk-kart"><video id="fk-vid" class="clip" data-start="21.6" data-duration="4.2" data-track-index="2" src="assets/media/fk_kart.mp4" muted playsinline></video></div>
  <div id="fk-ad">FAHRİ KUZ</div>
  <div id="s6-y">{kelimeler([("Yarım asırlık", "s"), ("hikâye,", "k")], "kl")}<br>{kelimeler([("özüne", "s"), ("dönüyor.", "k")], "kl")}</div>
</div>

<div id="s7" class="clip tam" data-layout-allow-occlusion data-start="25.7" data-duration="4.3" data-track-index="1">
  <div id="yildiz">{YILDIZ}</div>
  <div id="son-logo">{logo("son-lg", SIYAH)}</div>
  <div id="son-adres">kuz.istanbul</div>
  <div id="son-alt">1 ŞUBAT 2027 · ATAKÖY ATRIUM AVM</div>
</div>

<div id="imlec" class="clip" data-layout-allow-occlusion data-start="12.2" data-duration="9.5" data-track-index="3">{IMLEC}</div>
<audio id="miks" class="clip" data-start="0" data-duration="{D}" data-track-index="6" data-volume="1" src="assets/audio/miks.m4a"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
const giris = (sel, t, aralik) => gsap.utils.toArray(sel).forEach((el, i) =>
  tl.fromTo(el, {{opacity:0, y:22, filter:"blur(14px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.55, ease:"power3.out"}}, t + i*aralik));
const cikis = (sel, t) => tl.to(sel, {{opacity:0, filter:"blur(12px)", y:-14, duration:0.35, ease:"power2.in"}}, t);
// zemin ışıkları yavaşça kayar
tl.fromTo("#isik1", {{x:0, y:0}}, {{x:220, y:260, duration:{D}, ease:"none"}}, 0);
tl.fromTo("#isik2", {{x:0, y:0}}, {{x:-260, y:-300, duration:{D}, ease:"none"}}, 0);
// 1: Yarım asırlık hikâye, özüne dönüyor.
giris("#s1-y .kl", 0.25, 0.32);
tl.fromTo("#s1-kart", {{opacity:0, scale:0.4, rotation:-12, y:40}}, {{opacity:1, scale:1, rotation:0, y:0, duration:0.7, ease:"back.out(1.8)"}}, 1.9);
tl.to("#s1-kart", {{y:-14, duration:1.2, ease:"sine.inOut"}}, 2.6);
cikis("#s1-y .kl", 3.85);
tl.to("#s1-kart", {{scale:3.2, opacity:0, rotation:8, duration:0.5, ease:"power2.in"}}, 3.85);
// 2: telefon tüneli
tl.fromTo("#tel-sahne", {{scale:1.35, rotation:-6, opacity:0}}, {{scale:1, rotation:4, opacity:1, duration:4.6, ease:"power2.out"}}, 4.2);
tl.to("#tel-sahne", {{opacity:1, duration:0.01}}, 4.6);
giris("#s2-y .kl", 4.6, 0.38);
cikis("#s2-y .kl", 6.6);
giris("#s2-y2 .kl", 6.9, 0.3);
tl.to("#tel-sahne", {{scale:1.6, opacity:0, duration:0.45, ease:"power2.in"}}, 8.3);
cikis("#s2-y2 .kl", 8.3);
// 3: yükleme ve "Hazır"
tl.fromTo("#s3-etiket,#s3-sayi,#s3-bar", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.45, stagger:0.06, ease:"power3.out"}}, 8.65);
tl.fromTo("#s3-dolu", {{scaleX:0.63}}, {{scaleX:1, duration:1.6, ease:"power2.inOut"}}, 8.9);
const sy = {{v:63}};
tl.fromTo(sy, {{v:63}}, {{v:100, duration:1.6, ease:"power2.inOut", onUpdate:() => {{ document.getElementById("s3-n").textContent = Math.round(sy.v); }}}}, 8.9);
tl.to("#s3-etiket,#s3-sayi,#s3-bar", {{opacity:0, y:-20, filter:"blur(8px)", duration:0.35, ease:"power2.in"}}, 10.6);
tl.set("#s3-tamam,#s3-tik", {{opacity:0}}, 8.6);
tl.fromTo("#s3-tik", {{opacity:0, scale:0.3}}, {{opacity:1, scale:1, duration:0.55, ease:"back.out(2)"}}, 10.85);
tl.to("#tik-yol", {{strokeDashoffset:0, duration:0.45, ease:"power2.out"}}, 11.15);
tl.fromTo("#s3-tamam", {{opacity:0, y:20, filter:"blur(10px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.5, ease:"power3.out"}}, 11.0);
{konf_js}.forEach(([x, y, r], i) => {{
  const el = document.querySelectorAll("#konf .kf")[i];
  tl.fromTo(el, {{x:0, y:0, rotation:0, opacity:1}}, {{x:x, y:y, rotation:r, duration:0.9, ease:"power3.out"}}, 11.05);
  tl.to(el, {{y:y + 160, opacity:0, duration:0.6, ease:"power1.in"}}, 11.95);
}});
tl.to("#s3-tamam,#s3-tik", {{opacity:0, scale:0.9, duration:0.3}}, 12.0);
// 4: kuz.istanbul pencere, imleç, uçuşan markalar
tl.fromTo("#pencere", {{opacity:0, rotationX:38, rotationZ:-8, y:240, scale:0.86}}, {{opacity:1, rotationX:0, rotationZ:0, y:0, scale:1, duration:1.3, ease:"power3.out"}}, 12.2);
tl.fromTo("#imlec", {{opacity:0, x:900, y:1500}}, {{opacity:1, x:900, y:1500, duration:0.2}}, 13.2);
tl.to("#imlec", {{x:770, y:1030, duration:0.9, ease:"power2.inOut"}}, 13.3);
tl.to("#p-grid .karo:nth-child(4)", {{scale:1.06, duration:0.25, ease:"power2.out"}}, 14.1);
tl.to("#imlec", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, 14.35);
tl.to("#imlec", {{opacity:0, duration:0.2}}, 14.75);
tl.to("#pencere", {{opacity:0, scale:0.9, filter:"blur(10px)", duration:0.45, ease:"power2.in"}}, 14.6);
{[ [x, y, r] for _, x, y, r in UCAN ]}.forEach(([x, y, r], i) => {{
  const el = document.querySelectorAll(".ucan")[i];
  tl.fromTo(el, {{opacity:0, x:0, y:0, scale:0.5, rotation:0}}, {{opacity:1, x:x, y:y, scale:1, rotation:r, duration:0.8, ease:"power3.out"}}, 14.75 + i*0.05);
  tl.to(el, {{y:y - 40, rotation:r*0.6, duration:2.0, ease:"none"}}, 15.6);
  tl.to(el, {{opacity:0, scale:0.85, duration:0.35, ease:"power2.in"}}, 17.1);
}});
giris("#s4-y .kl", 15.2, 0.32);
cikis("#s4-y .kl", 17.05);
// 5: Ataköy Atrium AVM
tl.fromTo("#s5-ust", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.5}}, 17.5);
tl.fromTo("#satir", {{opacity:0, y:40, scale:0.94}}, {{opacity:1, y:0, scale:1, duration:0.6, ease:"power3.out"}}, 17.6);
tl.fromTo("#dugme", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, 18.7);
tl.fromTo("#imlec", {{opacity:0, x:980, y:1250}}, {{opacity:1, x:980, y:1250, duration:0.2}}, 18.9);
tl.to("#imlec", {{x:600, y:1110, duration:0.7, ease:"power2.inOut"}}, 19.0);
tl.to("#imlec", {{scale:0.85, duration:0.08, yoyo:true, repeat:1}}, 19.75);
tl.to("#dugme", {{scale:0.95, duration:0.08, yoyo:true, repeat:1}}, 19.75);
tl.to("#imlec", {{opacity:0, duration:0.2}}, 20.1);
tl.to("#dugme", {{opacity:0, scale:0.9, duration:0.25}}, 20.0);
tl.fromTo("#hap", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.5, ease:"back.out(1.7)"}}, 20.2);
tl.to("#s5-ust,#satir,#hap", {{opacity:0, filter:"blur(10px)", duration:0.35}}, 21.3);
// 6: Fahri Kuz
tl.fromTo("#fk-kart", {{opacity:0, rotationY:-28, rotationX:8, y:80, scale:0.9}}, {{opacity:1, rotationY:0, rotationX:0, y:0, scale:1, duration:1.1, ease:"power3.out"}}, 21.6);
tl.to("#fk-kart", {{rotationY:5, duration:3.0, ease:"sine.inOut"}}, 22.7);
tl.fromTo("#fk-ad", {{opacity:0}}, {{opacity:1, duration:0.6}}, 22.2);
giris("#s6-y .kl", 22.5, 0.3);
tl.to("#fk-kart,#fk-ad,#s6-y .kl", {{opacity:0, filter:"blur(12px)", duration:0.4, ease:"power2.in"}}, 25.35);
// 7: yıldız ve logo
tl.fromTo("#yildiz", {{opacity:0, scale:0.2, rotation:-90}}, {{opacity:1, scale:1, rotation:0, duration:0.6, ease:"back.out(2)"}}, 25.75);
tl.to("#yildiz", {{rotation:180, scale:5, opacity:0, duration:0.55, ease:"power2.in"}}, 26.45);
tl.fromTo("#son-logo", {{opacity:0, scale:0.9, filter:"blur(14px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:0.8, ease:"power3.out"}}, 26.7);
tl.fromTo("#son-adres", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 27.3);
tl.fromTo("#son-alt", {{opacity:0}}, {{opacity:1, duration:0.7}}, 27.7);
tl.to("#son-logo", {{scale:1.03, duration:3.3, ease:"none"}}, 26.7);
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
Path(__file__).with_name("index.html").write_text(html, encoding="utf-8")
print("index.html yazıldı")
