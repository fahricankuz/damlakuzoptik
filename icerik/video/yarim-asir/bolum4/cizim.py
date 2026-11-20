"""Bölüm 4 çizim katmanı: tasarım masasındaki eskiz kâğıtları (kurşun kalem, renkli kalem, bant, el yazısı notlar).
Hepsi koddan üretilir; dış görsel kullanılmaz. Referans: kullanıcının paylaştığı tasarımcı eskizleri (yalnızca üslup).
Çizgiler pathLength=1 + stroke-dashoffset ile 'çizilir'; notlar soldan sağa açılır."""

GRAFIT = "#3d3a36"
MAVI = "#2c4f9e"
KIRMIZI = "#b8323a"
YESIL = "#4f6b3a"
MUREKKEP = "#24335e"

W, H = 960, 740  # her kâğıdın çizim alanı


def goz(cx, cy, w, h, lift, s):
    """Kedi gözü eğilimli cam şekli. s=-1 sol cam (dış kenar solda), s=+1 sağ cam."""
    T = (cx, cy - h / 2)
    O = (cx + s * w / 2, cy - h * 0.08)
    B = (cx + s * w * 0.04, cy + h / 2)
    I = (cx - s * w / 2, cy - h * 0.02)
    f = lambda v: f"{v:.1f}"
    return (f"M{f(T[0])},{f(T[1])} "
            f"C{f(T[0] + s * w * 0.36)},{f(T[1] - lift * 0.5)} {f(O[0])},{f(O[1] - h * 0.48 - lift)} {f(O[0])},{f(O[1])} "
            f"C{f(O[0])},{f(O[1] + h * 0.36)} {f(B[0] + s * w * 0.42)},{f(B[1])} {f(B[0])},{f(B[1])} "
            f"C{f(B[0] - s * w * 0.40)},{f(B[1])} {f(I[0])},{f(I[1] + h * 0.40)} {f(I[0])},{f(I[1])} "
            f"C{f(I[0])},{f(I[1] - h * 0.42)} {f(T[0] - s * w * 0.34)},{f(T[1])} {f(T[0])},{f(T[1])} Z")


def yuvarlak(cx, cy, r):
    return f"M{cx - r},{cy} a{r},{r} 0 1,0 {2 * r},0 a{r},{r} 0 1,0 {-2 * r},0"


class Kagit:
    """Bir kâğıdın çizgilerini ve animasyon sırasını toplar."""

    def __init__(self, ad):
        self.ad, self.els, self.anim = ad, [], []
        self.n = 0

    def _id(self):
        self.n += 1
        return f"{self.ad}-{self.n}"

    def cizgi(self, d, t, dur=1.2, renk=GRAFIT, k=2.2, op=0.9, cift=True, filt="grafit", cap="round"):
        """Kurşun kalem çizgisi; cift=True ise hafif kaymış ikinci geçiş (el çizimi hissi)."""
        for j, (dx, dy, o) in enumerate([(0, 0, op)] + ([(1.6, 1.1, op * 0.45)] if cift else [])):
            i = self._id()
            tr = f' transform="translate({dx},{dy})"' if (dx or dy) else ""
            self.els.append(f'<path id="{i}" class="pc" d="{d}" pathLength="1" stroke="{renk}" stroke-width="{k}" '
                            f'stroke-linecap="{cap}" opacity="{o:.2f}" filter="url(#{filt})"{tr}/>')
            self.anim.append(f'tl.fromTo("#{i}",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{dur},ease:"power1.inOut"}},{t + j * 0.18:.2f});')

    def boya(self, d, t, dur=1.6, renk=MAVI, k=18, op=0.8):
        """Renkli kalemle kalın dolgu çizgisi."""
        self.cizgi(d, t, dur, renk, k, op, cift=False, filt="renkli")

    def not_(self, x, y, metin, t, boy=34, renk=MUREKKEP, aci=0, anchor="start", dur=0.7):
        i = self._id()
        rot = f' transform="rotate({aci} {x} {y})"' if aci else ""
        self.els.append(f'<text id="{i}" class="el" x="{x}" y="{y}" font-size="{boy}" fill="{renk}" text-anchor="{anchor}"{rot}>{metin}</text>')
        self.anim.append(f'tl.fromTo("#{i}",{{clipPath:"inset(-20% 100% -20% 0%)"}},{{clipPath:"inset(-20% 0% -20% 0%)",duration:{dur},ease:"none"}},{t:.2f});')

    def ham(self, svg, t=None, dur=0.6):
        """Animasyonsuz ya da yalnızca belirerek gelen öğe."""
        if t is None:
            self.els.append(svg)
            return
        i = self._id()
        self.els.append(f'<g id="{i}" opacity="0">{svg}</g>')
        self.anim.append(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:{dur},ease:"power1.out"}},{t:.2f});')

    def svg(self, zemin):
        return (f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">'
                f'{zemin}<g fill="none">' + "\n".join(self.els) + "</g></svg>")


def bant(x, y, w, h, aci):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="rgba(214,178,104,.55)" '
            f'transform="rotate({aci} {x + w / 2} {y + h / 2})"/>')


def zemin(renk, kareli=False):
    return (f'<rect width="{W}" height="{H}" fill="{renk}"/>'
            + (f'<rect width="{W}" height="{H}" fill="url(#kare)"/>' if kareli else "")
            + f'<rect width="{W}" height="{H}" fill="{renk}" filter="url(#kagitdoku)"/>')


def kagit1():
    """Ön görünüş: kutulama sistemi, kedi gözü çerçeve, lacivert renkli kalem."""
    k = Kagit("k1")
    t0 = 2.9
    k.ham(bant(40, -14, 150, 46, -8) + bant(780, -10, 150, 46, 6))
    # yapı çizgileri
    k.cizgi("M40,360 L920,360", t0, 0.9, renk="#7a8db8", k=1.2, op=0.7, cift=False)
    k.cizgi("M480,170 L480,600", t0 + 0.2, 0.7, renk="#7a8db8", k=1.2, op=0.7, cift=False)
    # kutulama dikdörtgenleri
    k.cizgi("M110,250 L440,250 L440,480 L110,480 Z", t0 + 0.4, 1.0, renk="#8a8478", k=1.1, op=0.55, cift=False)
    k.cizgi("M520,250 L850,250 L850,480 L520,480 Z", t0 + 0.6, 1.0, renk="#8a8478", k=1.1, op=0.55, cift=False)
    L = goz(275, 365, 330, 230, 34, -1)
    R = goz(685, 365, 330, 230, 34, 1)
    Li = goz(278, 368, 290, 194, 22, -1)
    Ri = goz(682, 368, 290, 194, 22, 1)
    k.ham(f'<path d="{Li} {Ri}" fill="url(#tarama)" opacity=".3" filter="url(#grafit)"/>', t0 + 3.9, 1.0)
    k.cizgi(L, t0 + 0.7, 1.5, k=2.6)
    k.cizgi(R, t0 + 1.0, 1.5, k=2.6)
    k.cizgi(Li, t0 + 1.6, 1.2, k=1.8, op=0.8)
    k.cizgi(Ri, t0 + 1.8, 1.2, k=1.8, op=0.8)
    k.cizgi("M440,330 C452,300 508,300 520,330", t0 + 2.0, 0.6, k=2.6)
    k.cizgi("M112,318 L58,312 M113,330 L60,326", t0 + 2.2, 0.5, k=2.0)
    k.cizgi("M848,318 L902,312 M847,330 L900,326", t0 + 2.3, 0.5, k=2.0)
    # lacivert renkli kalem (çerçeve gövdesi)
    k.boya(goz(276, 366, 310, 212, 28, -1), t0 + 2.6, 1.7)
    k.boya(goz(684, 366, 310, 212, 28, 1), t0 + 3.0, 1.7)
    # ölçüler
    k.cizgi("M110,520 L440,520 M110,508 L110,532 M440,508 L440,532", t0 + 1.2, 0.7, renk="#5a5550", k=1.2, cift=False)
    k.cizgi("M440,560 L520,560 M440,548 L440,572 M520,548 L520,572", t0 + 1.4, 0.6, renk="#5a5550", k=1.2, cift=False)
    k.not_(275, 555, "52", t0 + 1.6, 34, GRAFIT, anchor="middle", dur=0.3)
    k.not_(480, 600, "18", t0 + 1.8, 34, GRAFIT, anchor="middle", dur=0.3)
    # notlar
    k.not_(60, 110, "Model 04", t0 + 0.3, 58, MUREKKEP, -2)
    k.cizgi("M60,126 C140,120 220,124 270,118", t0 + 0.9, 0.5, renk=MUREKKEP, k=2.2, cift=False)
    k.not_(600, 150, "lacivert asetat", t0 + 3.2, 40, MAVI, -3)
    k.cizgi("M700,162 C690,200 650,225 618,245 M618,245 L640,240 M618,245 L626,226", t0 + 3.6, 0.6, renk=MAVI, k=2.0, cift=False)
    k.not_(540, 670, "köprü: anatomik · uç: yükseltilmiş", t0 + 4.4, 34, GRAFIT, -1)
    k.not_(70, 680, "ön görünüş", t0 + 4.0, 34, KIRMIZI, -2)
    return k


def kagit2():
    """Yan görünüş, menteşe detayı ve üç katmanlı asetat kesiti."""
    k = Kagit("k2")
    t0 = 11.4
    k.ham(bant(380, -16, 170, 46, 3))
    # çerçeve ön kesiti (sol) ve sap
    k.cizgi("M92,330 C88,380 90,470 100,560 L138,560 C132,470 130,380 134,330 Z", t0, 1.0, k=2.6)
    k.cizgi("M138,420 L780,412 C840,410 880,440 905,520", t0 + 0.4, 1.6, k=2.6)
    k.cizgi("M138,450 L780,442 C830,440 862,466 884,530", t0 + 0.6, 1.6, k=2.0, op=0.8)
    k.ham('<path d="M150,456 L770,448 C820,446 850,470 870,520 L862,524 C840,478 812,460 770,462 L150,470 Z" '
          'fill="url(#tarama)" opacity=".5" filter="url(#grafit)"/>', t0 + 2.0, 0.9)
    # menteşe
    k.cizgi("M138,404 L188,404 L188,466 L138,466", t0 + 1.0, 0.6, k=2.2)
    k.cizgi(yuvarlak(163, 435, 8), t0 + 1.3, 0.4, k=1.8)
    # büyüteç ve detay
    k.cizgi(yuvarlak(720, 200, 130), t0 + 1.6, 1.0, k=2.0)
    k.cizgi("M600,252 L196,420", t0 + 1.9, 0.7, renk="#5a5550", k=1.2, cift=False)
    for j in range(5):
        y = 120 + j * 32
        k.cizgi(f"M672,{y} L768,{y} L768,{y + 24} L672,{y + 24} Z", t0 + 2.2 + j * 0.12, 0.4, k=1.8)
    k.cizgi("M720,112 L720,288", t0 + 2.9, 0.5, renk=KIRMIZI, k=1.6, cift=False)
    k.not_(590, 372, "menteşe · 5 boğum", t0 + 3.0, 38, MUREKKEP, -2)
    # üç katmanlı kesit
    k.ham('<rect x="120" y="600" width="70" height="90" fill="#1d1b1a" opacity=".85" filter="url(#renkli)"/>'
          '<rect x="190" y="600" width="70" height="90" fill="#9a5a24" opacity=".85" filter="url(#renkli)"/>'
          '<rect x="260" y="600" width="70" height="90" fill="#9fb4bf" opacity=".8" filter="url(#renkli)"/>', t0 + 3.4, 0.8)
    k.cizgi("M120,600 L330,600 L330,690 L120,690 Z M190,600 L190,690 M260,600 L260,690", t0 + 3.2, 0.9, k=1.8)
    k.not_(360, 640, "üç katman asetat", t0 + 4.0, 38, MUREKKEP, -1)
    k.not_(360, 682, "siyah · kaplumbağa · kristal", t0 + 4.5, 30, GRAFIT, -1)
    k.cizgi("M560,520 C600,560 640,560 690,540 M690,540 L672,532 M690,540 L676,556", t0 + 3.6, 0.6, renk=MUREKKEP, k=2.0, cift=False)
    k.not_(700, 560, "sap eğimi 8°", t0 + 3.9, 36, MUREKKEP, -3)
    k.not_(60, 90, "yan görünüş", t0 + 0.6, 40, KIRMIZI, -2)
    return k


def hurda(k, x, y, w, h, aci, zem, t, icerik_svg, bantlar=""):
    """Kâğıt parçası (kolaj): yerine düşerek gelir."""
    i = k._id()
    z = (f'<rect width="{w}" height="{h}" fill="#f2ecdc"/><rect width="{w}" height="{h}" fill="url(#kare)"/>' if zem == "kare"
         else f'<rect width="{w}" height="{h}" fill="#f5f2ea"/>')
    k.els.append(f'<g transform="translate({x},{y}) rotate({aci} {w / 2} {h / 2})"><g id="{i}" opacity="0">'
                 f'<rect x="4" y="8" width="{w}" height="{h}" fill="rgba(0,0,0,.22)" filter="url(#golge)"/>'
                 f'{z}{icerik_svg}{bantlar}</g></g>')
    k.anim.append(f'tl.fromTo("#{i}",{{opacity:0,y:-26}},{{opacity:1,y:0,duration:0.55,ease:"power2.out"}},{t:.2f});')


def kagit3():
    """Kolaj: renk ve form denemeleri, asetat numunesi."""
    k = Kagit("k3")
    t0 = 17.7
    # a) kedi gözü, lacivert
    sa = (f'<path d="{goz(201, 129, 254, 136, 40, -1)}" stroke="{MAVI}" stroke-width="15" fill="none" opacity=".8" filter="url(#renkli)"/>'
          f'<path d="{goz(200, 128, 270, 150, 46, -1)}" stroke="{GRAFIT}" stroke-width="2.4" fill="none" filter="url(#grafit)"/>'
          f'<path d="{goz(203, 131, 236, 120, 32, -1)}" stroke="{GRAFIT}" stroke-width="1.6" fill="none" filter="url(#grafit)"/>'
          f'<path d="M336,108 L392,104 M336,118 L392,116" stroke="{GRAFIT}" stroke-width="2" filter="url(#grafit)"/>'
          f'<path d="M50,128 L380,128" stroke="#7a8db8" stroke-width="1" opacity=".6"/>'
          f'<text class="el" x="30" y="236" font-size="32" fill="{KIRMIZI}" transform="rotate(-2 30 236)">H 41 mm</text>')
    hurda(k, 30, 40, 420, 260, -3, "kare", t0, sa, bant(160, -14, 110, 34, -4))
    # b) yuvarlak, kurşun kalem
    sb = (f'<path d="{yuvarlak(120, 120, 78)} {yuvarlak(290, 120, 78)}" stroke="{GRAFIT}" stroke-width="2.6" fill="none" filter="url(#grafit)"/>'
          f'<path d="{yuvarlak(120, 120, 66)} {yuvarlak(290, 120, 66)}" stroke="{GRAFIT}" stroke-width="1.4" fill="none" opacity=".7" filter="url(#grafit)"/>'
          f'<path d="M198,108 C210,92 200,92 212,108" stroke="{GRAFIT}" stroke-width="2.4" fill="none" filter="url(#grafit)"/>'
          f'<path d="{yuvarlak(120, 120, 64)}" fill="url(#tarama)" opacity=".3" filter="url(#grafit)"/>'
          f'<text class="el" x="40" y="236" font-size="36" fill="{MUREKKEP}" transform="rotate(-1 40 236)">pantos · ince</text>')
    hurda(k, 510, 30, 410, 260, 2.5, "beyaz", t0 + 0.8, sb, bant(300, -12, 100, 32, 8))
    # c) benekli varyasyon
    c = goz(190, 120, 260, 150, 40, -1)
    noktalar = "".join(f'<circle cx="{110 + (j % 7) * 26 + (j // 7) * 12}" cy="{68 + (j // 7) * 18}" r="5.5" fill="{KIRMIZI}" opacity=".8" filter="url(#renkli)"/>' for j in range(17))
    sc = (f'<path d="{c}" stroke="#8d8a85" stroke-width="13" fill="none" opacity=".55" filter="url(#renkli)"/>'
          f'<path d="{c}" stroke="{GRAFIT}" stroke-width="2.2" fill="none" filter="url(#grafit)"/>{noktalar}'
          f'<text class="el" x="30" y="232" font-size="34" fill="{MUREKKEP}" transform="rotate(-2 30 232)">benekli · bordo</text>')
    hurda(k, 40, 330, 400, 250, 1.5, "beyaz", t0 + 1.6, sc)
    # d) asetat numunesi
    sd = ('<rect x="20" y="20" width="200" height="130" rx="16" fill="#3a2414"/>'
          '<rect x="20" y="20" width="200" height="130" rx="16" fill="#c8913f" filter="url(#kaplumbaga)"/>'
          f'<text class="el" x="20" y="186" font-size="34" fill="{MUREKKEP}">kaplumbağa</text>')
    hurda(k, 540, 318, 240, 200, -4, "beyaz", t0 + 2.4, sd, bant(70, -12, 100, 30, -6))
    # e) yan profil, yeşil
    se = (f'<path d="M30,90 L380,82 C430,80 460,100 480,150" stroke="{YESIL}" stroke-width="16" fill="none" opacity=".75" filter="url(#renkli)"/>'
          f'<path d="M30,78 L380,70 C440,68 470,96 490,152 M30,100 L380,94 C424,92 452,110 470,156" stroke="{GRAFIT}" stroke-width="2.2" fill="none" filter="url(#grafit)"/>'
          f'<path d="M30,60 L30,120" stroke="{GRAFIT}" stroke-width="2.6" filter="url(#grafit)"/>'
          f'<text class="el" x="40" y="178" font-size="34" fill="{MUREKKEP}" transform="rotate(-1 40 178)">yeşil · mat · sap</text>')
    hurda(k, 400, 536, 520, 200, -1.5, "kare", t0 + 3.2, se, bant(-20, 70, 80, 30, -70))
    k.not_(780, 470, "seçilen: 04", t0 + 4.2, 42, KIRMIZI, -6)
    return k


DEFS = """<svg width="0" height="0" style="position:absolute"><defs>
  <pattern id="kare" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24,0 L0,0 0,24" fill="none" stroke="rgba(70,110,170,.22)" stroke-width="1"/></pattern>
  <pattern id="tarama" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(38)"><line x1="0" y1="0" x2="0" y2="9" stroke="#3d3a36" stroke-width="1.3"/></pattern>
  <filter id="grafit" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  2.4 0 0 0 -0.45" result="m"/>
    <feComposite in="SourceGraphic" in2="m" operator="in" result="g"/>
    <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="9" result="w"/>
    <feDisplacementMap in="g" in2="w" scale="3.5" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="renkli" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.55 0.11" numOctaves="3" seed="12" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  3.2 0 0 0 -0.95" result="m"/>
    <feComposite in="SourceGraphic" in2="m" operator="in" result="g"/>
    <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="5" result="w"/>
    <feDisplacementMap in="g" in2="w" scale="5" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="kagitdoku" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" seed="2" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.40  0 0 0 0 0.32  0 0 0 0.35 -0.12"/>
  </filter>
  <filter id="golge" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="kaplumbaga" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.02 0.05" numOctaves="4" seed="7"/>
    <feColorMatrix type="matrix" values="0 0 0 0 0.18  0 0 0 0 0.10  0 0 0 0 0.05  0 0 0 2.6 -1.05"/>
    <feComposite in2="SourceGraphic" operator="in"/>
  </filter>
</defs></svg>"""


def svg():
    k1, k2, k3 = kagit1(), kagit2(), kagit3()
    html = (DEFS
            + '<div id="masa"></div>'
            + f'<div id="sh1" class="sheet">{k1.svg(zemin("#efe7d3", True))}</div>'
            + f'<div id="sh2" class="sheet">{k2.svg(zemin("#f3efe6"))}</div>'
            + f'<div id="sh3" class="sheet">{k3.svg(zemin("#e6dbc0"))}</div>'
            + '<div id="cz-imza">Tasarım · Fahri Kuz</div>')
    return [k1, k2, k3], html


CSS = """
@font-face { font-family:'Caveat Local'; font-weight:500; src:url('assets/fonts/caveat-latin-500-normal.woff2') format('woff2'); unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD; }
@font-face { font-family:'Caveat Local'; font-weight:500; src:url('assets/fonts/caveat-latin-ext-500-normal.woff2') format('woff2'); unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF; }
#cizim { position:absolute; inset:0; z-index:5; overflow:hidden; }
#masa { position:absolute; inset:0; background:radial-gradient(120% 70% at 50% 38%, #2a2119 0%, #15100c 55%, #0b0907 100%); }
.sheet { position:absolute; left:60px; top:290px; width:960px; height:740px; box-shadow:0 28px 70px rgba(0,0,0,.65), 0 4px 10px rgba(0,0,0,.4); opacity:0; }
.sheet svg { display:block; }
.sheet .pc { stroke-dasharray:1; stroke-dashoffset:1; stroke-linejoin:round; }
.sheet .el { font-family:'Caveat Local',cursive; font-weight:500; }
.sheet text[id] { clip-path:inset(-20% 100% -20% 0%); }
#cz-imza { position:absolute; left:90px; top:212px; font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:400; font-size:58px; color:#d6c29a; opacity:0; }
"""


def timeline(kagitlar):
    out = []
    for k in kagitlar:
        out.extend(k.anim)
    out += [
        # kâğıt 1: başlıktan sonra masaya gelir
        'tl.fromTo("#sh1",{opacity:0,y:260,rotation:4,scale:0.92},{opacity:1,y:0,rotation:-1.5,scale:0.92,duration:1.1,ease:"power3.out"},2.35);',
        'tl.to("#sh1",{opacity:0,scale:0.95,duration:0.35,ease:"power1.in"},7.7);',
        'tl.fromTo("#sh1",{scale:0.92},{scale:0.95,duration:4.25,ease:"none",immediateRender:false},3.45);',
        # kâğıt 2: sağdan, öncekinin üstüne
        'tl.fromTo("#sh2",{opacity:0,x:700,rotation:9,scale:0.92},{opacity:1,x:0,rotation:1.8,scale:0.92,duration:0.9,ease:"power3.out"},10.85);',
        'tl.fromTo("#sh2",{scale:0.92},{scale:0.955,duration:6.2,ease:"none",immediateRender:false},11.75);',
                # kâğıt 3: soldan
        'tl.fromTo("#sh3",{opacity:0,x:-700,rotation:-8,scale:0.92},{opacity:1,x:0,rotation:-1.0,scale:0.92,duration:0.9,ease:"power3.out"},17.3);',
        'tl.fromTo("#sh3",{scale:0.92},{scale:0.96,duration:6.2,ease:"none",immediateRender:false},18.2);',
        'tl.to("#sh2",{opacity:0,duration:0.2},18.3);',
        # final: ilk eskiz geri gelir, imza
        'tl.set("#sh3",{opacity:0},29.0);',
        'tl.set("#sh1",{opacity:1,y:0,x:0,rotation:-1.5,scale:0.92},29.0);',
        'tl.fromTo("#sh1",{scale:0.92},{scale:0.97,duration:3.6,ease:"none",immediateRender:false},29.0);',
        'tl.fromTo("#cz-imza",{opacity:0,y:10},{opacity:1,y:0,duration:1.0,ease:"power2.out"},29.6);',
    ]
    return "\n".join(out)
