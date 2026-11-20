"""Bölüm 4 teknik çizim katmanı: mimari proje çizimi tarzında gözlük taslağı (SVG) ve GSAP animasyonları.
Tamamen koddan üretilir; dış görsel kullanılmaz. Çizgiler pathLength=1 + stroke-dashoffset ile 'çizilir'."""

GOLD = "#d6c29a"
INK = "rgba(214,194,154,.55)"


def lens(cx, cy, w, h, r):
    """Yuvarlatılmış dikdörtgen cam (alt köşeler daha yumuşak)."""
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    rb = r * 1.6
    return (f"M{x0 + r},{y0} L{x1 - r},{y0} Q{x1},{y0} {x1},{y0 + r} L{x1},{y1 - rb} "
            f"Q{x1},{y1} {x1 - rb},{y1} L{x0 + rb},{y1} Q{x0},{y1} {x0},{y1 - rb} L{x0},{y0 + r} Q{x0},{y0} {x0 + r},{y0} Z")


def svg():
    p = []  # (id, d, sınıf, gecikme grubu)
    # --- Ön görünüş (y 360–700) ---
    L = lens(305, 520, 360, 280, 46)
    R = lens(775, 520, 360, 280, 46)
    p.append(("cz-lensL", L, "ln", "a"))
    p.append(("cz-lensR", R, "ln", "a"))
    p.append(("cz-bridge", "M485,440 C510,400 570,400 595,440", "ln", "a"))
    p.append(("cz-endL", "M125,430 L88,420 L80,432", "ln", "a"))
    p.append(("cz-endR", "M955,430 L992,420 L1000,432", "ln", "a"))
    # iç cam çizgisi (asetat kalınlığı)
    p.append(("cz-inL", lens(305, 520, 326, 246, 36), "thin", "b"))
    p.append(("cz-inR", lens(775, 520, 326, 246, 36), "thin", "b"))
    # ölçü çizgileri
    p.append(("cz-dimA", "M125,330 L485,330 M125,318 L125,342 M485,318 L485,342", "dim", "b"))
    p.append(("cz-dimB", "M485,370 L595,370 M485,358 L485,382 M595,358 L595,382", "dim", "b"))
    p.append(("cz-dimC", "M80,730 L1000,730 M80,718 L80,742 M1000,718 L1000,742", "dim", "b"))
    p.append(("cz-axis", "M540,300 L540,760", "axis", "b"))
    # --- Yan görünüş: sap ve menteşe (y 800–880) ---
    p.append(("cz-temple", "M120,830 L860,830 C905,830 935,845 950,880", "ln", "c"))
    p.append(("cz-temple2", "M120,846 L860,846 C900,846 925,858 938,884", "thin", "c"))
    p.append(("cz-hinge", "M112,822 L112,854 M100,822 L124,822 M100,854 L124,854", "ln", "c"))
    p.append(("cz-screw", "M162,838 m-9,0 a9,9 0 1,0 18,0 a9,9 0 1,0 -18,0", "ln", "c"))
    # --- Cam eğrisi (y 920–1060, sol) ---
    p.append(("cz-curve", "M110,1040 Q300,920 490,1040", "ln", "d"))
    p.append(("cz-radius", "M300,1040 L300,960 M300,1040 L190,995", "dim", "d"))
    # --- Antet bloğu (sağ, y 920–1060) ---
    p.append(("cz-block", "M600,925 L1000,925 L1000,1060 L600,1060 Z M600,970 L1000,970 M600,1015 L1000,1015 M800,1015 L800,1060", "thin", "d"))

    paths = "\n".join(f'<path id="{i}" class="{c}" d="{d}" pathLength="1"/>' for i, d, c, _ in p)
    labels = """
<text class="lbl" x="305" y="312" text-anchor="middle">52</text>
<text class="lbl" x="540" y="356" text-anchor="middle">18</text>
<text class="lbl" x="540" y="772" text-anchor="middle">145</text>
<text class="note" x="120" y="804">SAP · YAN GÖRÜNÜŞ</text>
<text class="note" x="180" y="900">MENTEŞE · 5 BOĞUM</text>
<text class="note" x="110" y="1082">BAZ EĞRİSİ 6.00</text>
<text class="tb" x="616" y="956">YARIM ASIR · ÇİZİM NO. 04</text>
<text class="tb" x="616" y="1001">MALZEME · ASETAT</text>
<text class="tb" x="616" y="1046">İSTANBUL</text>
<text class="tb" x="816" y="1046">ÖLÇEK 1:1</text>
"""
    return p, f"""<svg id="cizim-svg" viewBox="0 0 1080 1920" width="1080" height="1920" xmlns="http://www.w3.org/2000/svg">
<defs>
  <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36,0 L0,0 0,36" fill="none" stroke="rgba(214,194,154,.07)" stroke-width="1"/></pattern>
  <pattern id="grid5" width="180" height="180" patternUnits="userSpaceOnUse"><path d="M180,0 L0,0 0,180" fill="none" stroke="rgba(214,194,154,.12)" stroke-width="1"/></pattern>
  <filter id="kaplumbaga" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.012 0.03" numOctaves="4" seed="7"/>
    <feColorMatrix type="matrix" values="0 0 0 0 0.62  0 0 0 0 0.36  0 0 0 0 0.14  0 0 0 2.6 -1.05"/>
    <feComposite in2="SourceGraphic" operator="in"/>
  </filter>
</defs>
<rect width="1080" height="1920" fill="#100d0a"/>
<rect width="1080" height="1920" fill="url(#grid)"/>
<rect width="1080" height="1920" fill="url(#grid5)"/>
<g id="cz-asetat" opacity="0">
  <rect x="126" y="1330" width="828" height="230" rx="10" fill="#3a2414"/>
  <rect x="126" y="1330" width="828" height="230" rx="10" fill="#c8913f" filter="url(#kaplumbaga)"/>
  <path d="{lens(345, 1445, 280, 170, 34)} {lens(735, 1445, 280, 170, 34)}" fill="none" stroke="{GOLD}" stroke-width="2" stroke-dasharray="10 8"/>
  <text class="note" x="126" y="1312">ASETAT LEVHA · KESİM ŞABLONU</text>
</g>
<g id="cz-draw" transform="translate(54,90) scale(0.9)">
<g id="cz-lines" fill="none">
{paths}
</g>
<g id="cz-labels">{labels}</g>
</g>
<text id="cz-imza" class="imza" x="90" y="268" opacity="0">Tasarım · Fahri Kuz</text>
</svg>"""


CSS = f"""
#cizim {{ position:absolute; inset:0; z-index:5; }}
#cizim-svg {{ position:absolute; left:0; top:0; }}
#cizim-svg .ln {{ stroke:{GOLD}; stroke-width:3; stroke-dasharray:1; stroke-dashoffset:1; stroke-linecap:round; stroke-linejoin:round; }}
#cizim-svg .thin {{ stroke:{INK}; stroke-width:1.5; stroke-dasharray:1; stroke-dashoffset:1; }}
#cizim-svg .dim {{ stroke:{INK}; stroke-width:1.5; stroke-dasharray:1; stroke-dashoffset:1; }}
#cizim-svg .axis {{ stroke:rgba(214,194,154,.35); stroke-width:1; stroke-dasharray:1; stroke-dashoffset:1; }}
#cizim-svg text {{ font-family:'Inter Local',Inter,sans-serif; fill:{GOLD}; }}
#cizim-svg .lbl {{ font-size:28px; font-weight:500; letter-spacing:.08em; }}
#cizim-svg .note {{ font-size:22px; font-weight:600; letter-spacing:.3em; fill:rgba(214,194,154,.8); }}
#cizim-svg .tb {{ font-size:21px; font-weight:600; letter-spacing:.22em; fill:rgba(214,194,154,.85); }}
#cizim-svg .imza {{ font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:400; font-size:54px; fill:{GOLD}; }}
"""


def timeline(p):
    """Çizim grupları sırayla çizilir: a ön görünüş, b iç hatlar ve ölçüler, c sap/menteşe, d eğri ve antet."""
    start = {"a": 0.15, "b": 2.6, "c": 11.4, "d": 15.0}
    dur = {"ln": 1.6, "thin": 1.2, "dim": 0.8, "axis": 1.0}
    out, k = [], {}
    for i, _, c, g in p:
        n = k.get(g, 0); k[g] = n + 1
        t = start[g] + n * 0.35
        out.append(f'tl.fromTo("#{i}",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{dur[c]},ease:"power2.inOut"}},{t:.2f});')
    out.append('tl.fromTo("#cz-labels",{opacity:0},{opacity:1,duration:0.8},3.4);')
    out.append('tl.fromTo("#cz-asetat",{opacity:0,y:30},{opacity:1,y:0,duration:1.0,ease:"power2.out"},18.6);')
    out.append('tl.fromTo("#cz-imza",{opacity:0},{opacity:1,duration:1.0,ease:"power2.out"},29.6);')
    out.append('tl.fromTo("#cizim-svg",{scale:1.0},{scale:1.06,duration:31,ease:"none",transformOrigin:"50% 35%"},0);')
    return "\n".join(out)
