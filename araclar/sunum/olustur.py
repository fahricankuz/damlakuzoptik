"""Denetim ve devir sunumunu üretir: Meta verisinden grafikler + HTML slaytlar -> PDF.

Kullanım: python3 araclar/sunum/olustur.py <meta.json> <font_dir> <cikti.html>
PDF'e çevirme: node araclar/sunum/pdf.mjs <cikti.html> <cikti.pdf>
"""
import json
import sys
import html as H

meta_path, font_dir, out_html = sys.argv[1], sys.argv[2], sys.argv[3]
ikas_path = sys.argv[4] if len(sys.argv) > 4 else None
R = json.load(open(meta_path, encoding="utf-8"))
# ikas aylık özet: ay -> [web sipariş adedi, brüt ciro, iade tutarı, tam iade adedi]  (kişisel veri içermez)
IK = json.load(open(ikas_path, encoding="utf-8")) if ikas_path else {}


def A(r, k, key="actions"):
    return sum(float(x["value"]) for x in r.get(key, []) if x["action_type"] == k)


def tl(x):
    return f"{x:,.0f}".replace(",", ".") + " TL"


def d(x, k=2):
    return f"{x:.{k}f}".replace(".", ",")


def n(x):
    return f"{x:,.0f}".replace(",", ".")


# ---------- veriler ----------
camps = R["campaigns"]
tot_spend = sum(float(r["spend"]) for r in camps)
tot_pur = sum(A(r, "purchase") for r in camps)
tot_val = sum(A(r, "purchase", "action_values") for r in camps)
old_spend = sum(float(r["spend"]) for r in R["monthly2"])
boost = [r for r in camps if r["objective"] == "LINK_CLICKS"]
boost_spend = sum(float(r["spend"]) for r in boost)
sales = [r for r in camps if r["objective"] == "OUTCOME_SALES"]
sales_zero = [r for r in sales if A(r, "purchase") == 0]
funnel = {k: sum(A(r, k) for r in camps) for k in
          ["landing_page_view", "add_to_cart", "initiate_checkout", "add_payment_info", "purchase"]}

monthly = [(r["date_start"][:7], float(r["spend"]), A(r, "purchase", "action_values"), A(r, "purchase"))
           for r in R["monthly"]]
AYLAR = {"01": "Oca", "02": "Şub", "03": "Mar", "04": "Nis", "05": "May", "06": "Haz",
         "07": "Tem", "08": "Ağu", "09": "Eyl", "10": "Eki", "11": "Kas", "12": "Ara"}

placement = sorted(R["placement"], key=lambda r: -float(r["spend"]))
an_spend = sum(float(r["spend"]) for r in placement if r["publisher_platform"] == "audience_network")
an_atc = sum(A(r, "add_to_cart") for r in placement if r["publisher_platform"] == "audience_network")

ig = R["igacc"]
media = R["igmedia"]
posts60 = media[:60]
likes = sorted(m.get("like_count", 0) for m in posts60)
med_like = likes[len(likes) // 2]
comments = sum(m.get("comments_count", 0) for m in posts60)
reels_share = sum(1 for m in media if m.get("media_product_type") == "REELS") / len(media) * 100
er = sum((m.get("like_count", 0) + m.get("comments_count", 0)) for m in posts60) / len(posts60) / ig["followers_count"] * 100
reach_vals = []
for m in posts60:
    for x in R["igins"].get(m["id"], []):
        if isinstance(x, dict) and x.get("name") == "reach":
            reach_vals.append(x["values"][0]["value"] if "values" in x else x["total_value"]["value"])
reach_vals.sort()
med_reach = reach_vals[len(reach_vals) // 2]
igins = {x["name"]: x.get("total_value", {}).get("value") for x in R["igacc_ins"]}
demo = R["igdemo"][0]["total_value"]["breakdowns"][0]["results"]
g_unknown = sum(x["value"] for x in demo if x["dimension_values"][1] == "U")
g_total = sum(x["value"] for x in demo)

# ---------- grafikler (SVG) ----------
GOLD, INK, MUTED, LINE, RED, GREEN = "#B08D3C", "#121212", "#7A7670", "#E4DED3", "#B4483C", "#3F7D5A"


def chart_monthly(w=1100, h=330):
    pad_l, pad_b, pad_t = 70, 46, 20
    mx = max(max(s, v) for _, s, v, _ in monthly) * 1.08
    bw = (w - pad_l - 20) / len(monthly)
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="Montserrat" font-size="13">']
    for i in range(5):
        y = pad_t + (h - pad_t - pad_b) * i / 4
        val = mx * (1 - i / 4)
        out.append(f'<line x1="{pad_l}" x2="{w-10}" y1="{y:.1f}" y2="{y:.1f}" stroke="{LINE}"/>')
        out.append(f'<text x="{pad_l-10}" y="{y+4:.1f}" text-anchor="end" fill="{MUTED}">{val/1000:.0f}b</text>')
    for i, (m, s, v, p) in enumerate(monthly):
        x = pad_l + i * bw
        hs = (h - pad_t - pad_b) * s / mx
        hv = (h - pad_t - pad_b) * v / mx
        base = h - pad_b
        out.append(f'<rect x="{x+bw*0.14:.1f}" y="{base-hs:.1f}" width="{bw*0.34:.1f}" height="{hs:.1f}" fill="{INK}" rx="2"/>')
        out.append(f'<rect x="{x+bw*0.52:.1f}" y="{base-hv:.1f}" width="{bw*0.34:.1f}" height="{hv:.1f}" fill="{GOLD}" rx="2"/>')
        lab = AYLAR[m[5:]] + (" '" + m[2:4] if m[5:] in ("01", "07") or i == 0 else "")
        out.append(f'<text x="{x+bw/2:.1f}" y="{h-24}" text-anchor="middle" fill="{INK}">{lab}</text>')
        out.append(f'<text x="{x+bw/2:.1f}" y="{h-6}" text-anchor="middle" fill="{MUTED}" font-size="11">{int(p)} satış</text>')
    out.append("</svg>")
    return "".join(out)


def chart_funnel(w=1100, h=280):
    steps = [("Site ziyareti (sayfa yüklendi)", funnel["landing_page_view"]),
             ("Sepete ekleme", funnel["add_to_cart"]),
             ("Ödeme başlatma", funnel["initiate_checkout"]),
             ("Ödeme bilgisi", funnel["add_payment_info"]),
             ("Satış", funnel["purchase"])]
    import math
    mx = math.log10(steps[0][1])
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="Montserrat" font-size="15">']
    rowh = h / len(steps)
    for i, (lab, v) in enumerate(steps):
        y = i * rowh
        bwid = (w - 520) * (math.log10(max(v, 1)) / mx)
        out.append(f'<text x="0" y="{y+rowh/2+5:.1f}" fill="{INK}">{lab}</text>')
        out.append(f'<rect x="300" y="{y+8:.1f}" width="{bwid:.1f}" height="{rowh-16:.1f}" fill="{INK if i < 4 else GOLD}" rx="3"/>')
        rate = "" if i == 0 else f'  ·  %{d(v/steps[i-1][1]*100,1)} bir önceki adımdan'
        out.append(f'<text x="{310+bwid:.1f}" y="{y+rowh/2+5:.1f}" fill="{INK}" font-weight="700">{n(v)}<tspan fill="{MUTED}" font-weight="400">{rate}</tspan></text>')
    out.append("</svg>")
    return "".join(out)


def spend_by_month():
    sp = {r["date_start"][:7]: float(r["spend"]) for r in R["monthly"]}
    for r in R["monthly2"]:
        m = r["date_start"][:7]; sp[m] = sp.get(m, 0) + float(r["spend"])
    return sp


def chart_ikas(w=1100, h=330):
    sp = spend_by_month()
    ms = [m for m in sorted(set(sp) | set(IK)) if m >= "2025-07"]
    vals = [(m, sp.get(m, 0), IK.get(m, [0, 0, 0, 0])[1] - IK.get(m, [0, 0, 0, 0])[2], IK.get(m, [0])[0]) for m in ms]
    pad_l, pad_b, pad_t = 70, 46, 20
    mx = max(max(s, v) for _, s, v, _ in vals) * 1.08
    bw = (w - pad_l - 20) / len(vals)
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="Montserrat" font-size="13">']
    for i in range(5):
        y = pad_t + (h - pad_t - pad_b) * i / 4
        out.append(f'<line x1="{pad_l}" x2="{w-10}" y1="{y:.1f}" y2="{y:.1f}" stroke="{LINE}"/>')
        out.append(f'<text x="{pad_l-10}" y="{y+4:.1f}" text-anchor="end" fill="{MUTED}">{mx*(1-i/4)/1000:.0f}b</text>')
    for i, (m, s_, v, o) in enumerate(vals):
        x = pad_l + i * bw; base = h - pad_b
        hs = (h - pad_t - pad_b) * s_ / mx; hv = (h - pad_t - pad_b) * v / mx
        out.append(f'<rect x="{x+bw*0.14:.1f}" y="{base-hs:.1f}" width="{bw*0.34:.1f}" height="{hs:.1f}" fill="{INK}" rx="2"/>')
        out.append(f'<rect x="{x+bw*0.52:.1f}" y="{base-hv:.1f}" width="{bw*0.34:.1f}" height="{hv:.1f}" fill="{GREEN}" rx="2"/>')
        lab = AYLAR[m[5:]] + ("\u00a0'" + m[2:4] if m[5:] in ("01", "07") else "")
        out.append(f'<text x="{x+bw/2:.1f}" y="{h-24}" text-anchor="middle" fill="{INK}">{lab}</text>')
        out.append(f'<text x="{x+bw/2:.1f}" y="{h-6}" text-anchor="middle" fill="{MUTED}" font-size="11">{o} sipariş</text>')
    out.append("</svg>")
    return "".join(out)


def ikas_period(a, b):
    sp = spend_by_month()
    S = sum(v for m, v in sp.items() if a <= m <= b)
    N = sum(v[1] - v[2] for m, v in IK.items() if a <= m <= b)
    O = sum(v[0] for m, v in IK.items() if a <= m <= b)
    G = sum(v[1] for m, v in IK.items() if a <= m <= b)
    Rf = sum(v[2] for m, v in IK.items() if a <= m <= b)
    F = sum(v[3] for m, v in IK.items() if a <= m <= b)
    return dict(spend=S, net=N, orders=O, gross=G, refund=Rf, fullref=F)


def chart_split(w=1100, h=90):
    parts = [("Satış kampanyaları", tot_spend - boost_spend - sum(float(r['spend']) for r in camps if r['objective'] == 'OUTCOME_AWARENESS'), INK),
             ("Öne çıkarılan gönderiler (tıklama hedefli)", boost_spend, RED),
             ("Bilinirlik", sum(float(r['spend']) for r in camps if r['objective'] == 'OUTCOME_AWARENESS'), MUTED)]
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="Montserrat" font-size="14">']
    x = 0
    for lab, v, c in parts:
        ww = w * v / tot_spend
        out.append(f'<rect x="{x:.1f}" y="0" width="{ww:.1f}" height="40" fill="{c}"/>')
        x += ww
    x = 0
    for i, (lab, v, c) in enumerate(parts[:2]):
        out.append(f'<rect x="{x}" y="58" width="14" height="14" fill="{c}"/><text x="{x+22}" y="70" fill="{INK}">{lab}: <tspan font-weight="700">{tl(v)}</tspan> (%{d(v/tot_spend*100,1)})</text>')
        x += 560
    out.append("</svg>")
    return "".join(out)


# ---------- tablolar ----------
def top_campaigns_rows():
    rows = []
    for r in sorted(sales, key=lambda r: -float(r["spend"]))[:9]:
        sp = float(r["spend"]); pv = A(r, "purchase", "action_values"); pu = A(r, "purchase")
        roas = pv / sp if sp else 0
        cls = "neg" if roas < 1 else ("pos" if roas >= 2 else "")
        name = r["campaign_name"].replace("_", " ").replace("Damla Kuz Optik ", "").replace("Damla Kuz ", "")
        rows.append(f"<tr><td>{H.escape(name[:48])}</td><td class='r'>{tl(sp)}</td><td class='r'>{int(pu)}</td><td class='r'>{tl(pv)}</td><td class='r {cls}'>{d(roas)}</td><td class='r'>{d(float(r.get('frequency',0)),1)}</td></tr>")
    return "".join(rows)


def placement_rows():
    rows = []
    for r in placement[:8]:
        sp = float(r["spend"])
        pos = r["platform_position"].replace("instagram_", "").replace("_", " ")
        plat = {"instagram": "Instagram", "facebook": "Facebook", "audience_network": "Audience Network"}[r["publisher_platform"]]
        ctr = float(r.get("ctr", 0))
        cls = "neg" if ctr > 10 else ""
        rows.append(f"<tr><td>{plat} · {pos}</td><td class='r'>{tl(sp)}</td><td class='r {cls}'>%{d(ctr,1)}</td><td class='r'>{int(A(r,'add_to_cart'))}</td><td class='r'>{int(A(r,'purchase'))}</td></tr>")
    return "".join(rows)


pf_dir = font_dir.replace("montserrat", "playfair-display")
fonts = f"""
@font-face{{font-family:Montserrat;font-weight:400;src:url('{font_dir}/montserrat-latin-ext-400-normal.woff2')}}
@font-face{{font-family:Montserrat;font-weight:500;src:url('{font_dir}/montserrat-latin-ext-500-normal.woff2')}}
@font-face{{font-family:Montserrat;font-weight:600;src:url('{font_dir}/montserrat-latin-ext-600-normal.woff2')}}
@font-face{{font-family:Montserrat;font-weight:700;src:url('{font_dir}/montserrat-latin-ext-700-normal.woff2')}}
@font-face{{font-family:Montserrat;font-weight:800;src:url('{font_dir}/montserrat-latin-ext-800-normal.woff2')}}
@font-face{{font-family:Playfair;font-weight:400;src:url('{pf_dir}/playfair-display-latin-ext-400-normal.woff2')}}
@font-face{{font-family:Playfair;font-weight:400;font-style:italic;src:url('{pf_dir}/playfair-display-latin-ext-400-italic.woff2')}}
@font-face{{font-family:Playfair;font-weight:600;src:url('{pf_dir}/playfair-display-latin-ext-600-normal.woff2')}}
"""
# Montserrat latin (temel) dosyaları da eklenir; latin-ext yalnızca Türkçe ek karakterleri kapsar
fonts += "".join(
    f"@font-face{{font-family:Montserrat;font-weight:{w};src:url('{font_dir}/montserrat-latin-{w}-normal.woff2');unicode-range:U+0000-00FF}}"
    for w in (400, 500, 600, 700, 800))
fonts += "".join(
    f"@font-face{{font-family:Playfair;font-weight:{w};src:url('{pf_dir}/playfair-display-latin-{w}-normal.woff2');unicode-range:U+0000-00FF}}"
    for w in (400, 600))

CSS = fonts + f"""
@page{{size:1280px 720px;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#F6F3EE}}
body{{font-family:Montserrat,sans-serif;color:{INK};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.s{{width:1280px;height:720px;padding:56px 72px 48px;position:relative;overflow:hidden;page-break-after:always;background:#F6F3EE}}
.s.dark{{background:{INK};color:#F6F3EE}}
.s.dark .k,.s.dark .foot{{color:#C9B27A}}
.k{{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:{GOLD};font-weight:700;margin-bottom:14px}}
h1{{font-family:Playfair,serif;font-weight:400;font-size:64px;line-height:1.05;letter-spacing:-.01em}}
h2{{font-family:Playfair,serif;font-weight:400;font-size:38px;line-height:1.15;margin-bottom:22px;max-width:1080px}}
h3{{font-size:15px;font-weight:700;margin-bottom:8px}}
p,li{{font-size:15px;line-height:1.55}}
.lead{{font-size:19px;line-height:1.5;max-width:960px;color:#3A3733}}
.dark .lead{{color:#D9D4CB}}
.foot{{position:absolute;left:72px;right:72px;bottom:22px;display:flex;justify-content:space-between;font-size:11px;color:{MUTED};letter-spacing:.06em}}
.grid{{display:grid;gap:22px}}
.g2{{grid-template-columns:1fr 1fr}}.g3{{grid-template-columns:repeat(3,1fr)}}.g4{{grid-template-columns:repeat(4,1fr)}}
.kpi{{border-top:2px solid {INK};padding-top:12px}}
.dark .kpi{{border-color:#C9B27A}}
.kpi .v{{font-family:Playfair,serif;font-size:44px;line-height:1.05}}
.kpi .l{{font-size:13px;color:{MUTED};margin-top:6px;line-height:1.4}}
.dark .kpi .l{{color:#B9B3A8}}
.card{{background:#fff;border:1px solid {LINE};border-radius:10px;padding:18px 20px}}
.card p,.card li{{font-size:14px}}
ul{{padding-left:18px}} li{{margin-bottom:6px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:{MUTED};font-weight:600;border-bottom:1.5px solid {INK};padding:7px 8px}}
td{{padding:7px 8px;border-bottom:1px solid {LINE};vertical-align:top;line-height:1.4}}
td.r,th.r{{text-align:right;white-space:nowrap}}
.neg{{color:{RED};font-weight:700}} .pos{{color:{GREEN};font-weight:700}}
.tag{{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.06em;padding:3px 8px;border-radius:20px;text-transform:uppercase}}
.t-red{{background:#F3DCD8;color:{RED}}} .t-amb{{background:#F2E7CF;color:#8A6A1E}} .t-grn{{background:#DCEBE1;color:{GREEN}}}
.note{{font-size:12px;color:{MUTED};line-height:1.5;margin-top:12px}}
.num{{font-family:Playfair,serif;font-size:30px;color:{GOLD};line-height:1}}
.reason{{display:grid;grid-template-columns:44px 1fr;gap:10px;padding:11px 0;border-bottom:1px solid {LINE}}}
.reason:last-child{{border:none}}
.reason p{{font-size:14px}}
.phase{{border-left:3px solid {GOLD};padding:4px 0 4px 14px}}
.phase .when{{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:{GOLD};font-weight:700}}
.phase li{{font-size:13px;margin-bottom:3px}}
.small td,.small th{{font-size:12px;padding:5px 7px}}
.cover-line{{width:80px;height:2px;background:{GOLD};margin:28px 0}}
"""

FOOT = "Damla Kuz Optik · Dijital Pazarlama Denetimi ve Devir Planı · Kasım 2026 · Gizli"
slides = []


def S(body, cls="", page=True):
    num = len(slides) + 1
    foot = f'<div class="foot"><span>{FOOT}</span><span>{num:02d}</span></div>' if page else ""
    slides.append(f'<section class="s {cls}">{body}{foot}</section>')


roas_all = tot_val / tot_spend
cpa = tot_spend / tot_pur
first_month = AYLAR[monthly[0][0][5:]] + " " + monthly[0][0][:4]

# 1 Kapak
S(f"""<div class="k">Gizli · Yönetim için</div>
<h1>Dijital Pazarlama<br>Denetimi ve<br><i>Devir Planı</i></h1>
<div class="cover-line"></div>
<p class="lead">Damla Kuz Optik · Temmuz 2025 – Kasım 2026 dönemi<br>Meta reklamları, Instagram, web sitesi, ürün feed'leri ve ajans devri</p>
<p class="note" style="position:absolute;bottom:56px;left:72px">Hazırlanma tarihi: 19 Kasım 2026 · Veri: Meta Marketing API (yalnızca okuma), damlakuzoptik.com, ikas feed'leri</p>""", "dark", page=False)

# 2 Yönetici özeti
S(f"""<div class="k">Yönetici özeti</div>
<h2>Nisan 2025'ten bu yana {tl(tot_spend + old_spend)} Meta harcaması. İlkbahar ve yazda reklam satış getirdi; son dört ayda harcama kadar ciro bile gelmedi.</h2>
<div class="grid g4" style="margin-bottom:28px">
<div class="kpi"><div class="v">126</div><div class="l">Online sipariş (ikas, Tem 2025 – 14 Kas 2026). Meta yalnızca {int(tot_pur)}'unu ölçebilmiş</div></div>
<div class="kpi"><div class="v">985.150 TL</div><div class="l">Net online ciro (iadeler düşülmüş)</div></div>
<div class="kpi"><div class="v">2,98</div><div class="l">Net ciro / Meta harcaması, tüm dönem (Google harcaması hariç)</div></div>
<div class="kpi"><div class="v" style="color:#B4483C">0,99</div><div class="l">Net ciro / Meta harcaması, Ağustos – Kasım 2026</div></div>
</div>
<div class="grid g2">
<div><h3>Temel bulgular</h3><ul>
<li>ikas'a göre aynı dönemde <b>126 online sipariş, 985 bin TL net ciro</b>; Meta bunların yalnızca 39'unu ölçebilmiş. Ölçüm ve raporlama zayıf.</li><li>Ağustos–Kasım 2026: 71 bin TL harcama, <b>13 sipariş</b>, net ciro harcamaya eşit (0,99).</li>
<li>Bütçenin <b>{tl(boost_spend)}</b>'si satış hedefi olmayan "öne çıkarılan gönderi"lere gitti: <b>0 satış</b>.</li>
<li>Siparişlerin %21'i tamamen iade edilmiş; iade tutarı brüt cironun %16'sı.</li>
<li>Instagram etkileşimi %{d(er,2)}; gönderi başına ortalama {med_like} beğeni, 60 gönderide {comments} yorum.</li>
<li>Site ve feed hijyeni ihmal edilmiş: test ürünü 2,06 TL'ye satışta, barkodlar geçersiz, başlıklar zayıf.</li>
</ul></div>
<div><h3>Önerilen kararlar</h3><ul>
<li>Ajans ilişkisinin planlı bir devirle sonlandırılması (bu belgenin 6. bölümü).</li>
<li>Devir öncesi <b>tüm erişimlerin şirkete alınması</b>: Google Ads, Merchant Center ve Analytics öncelikli.</li>
<li>Devirden sonra kampanya yapısının sadeleştirilmesi, kreatif ve feed'in yenilenmesi.</li>
<li>Sitede dönüşüm engellerinin giderilmesi: kalıcı indirim algısı, taksit ve ürün sayfası güveni.</li>
</ul></div></div>""")

# 3 Kapsam
S(f"""<div class="k">Kapsam ve yöntem</div>
<h2>Neye baktık, neye bakamadık</h2>
<div class="grid g2">
<div class="card"><h3>İncelenen</h3><ul>
<li>Meta reklam hesabı "Damla Kuz Optik İkas": 52 kampanya, 389 reklam, aylık kırılım, yerleşim, yaş ve cinsiyet, bölge</li>
<li>Eski reklam hesabı "Damla Kuz Optik" (Nisan–Eylül 2025): {tl(old_spend)} harcama</li>
<li>Instagram @damlakuzoptik: son 100 gönderi, 60 gönderinin erişim verisi, takipçi demografisi</li>
<li>İşletme portföyü erişim yapısı ve hesap etkinlik kaydı</li>
<li>damlakuzoptik.com: 10 sayfa SEO, yapılandırılmış veri, ölçüm etiketleri</li>
<li>ikas Google ve Meta ürün feed'leri (514 varyant)</li>
<li>7 rakip sitesi</li></ul></div>
<div class="card"><h3>Erişilemeyen (ajansta)</h3><ul>
<li><b>Google Ads</b>: hesap şirkette görünmüyor, harcama ve sonuç bilinmiyor</li>
<li><b>Google Merchant Center</b>: hesap şirkette görünmüyor</li>
<li><b>Google Analytics 4</b>: erişim teyit edilmedi</li>
<li>Ajansın kreatif arşivi, raporları, sözleşme kapsamı</li></ul>
<p class="note">Notlar: (1) Meta yalnızca kendi ölçebildiği satışları gösterir; gerçek online satış ve mağaza satışları daha yüksek olabilir. Sonuçlar ikas sipariş verisiyle karşılaştırılmalıdır. (2) Tutarlar KDV hariç reklam harcamasıdır.</p></div>
</div>""")

# 4 Bölüm başlığı
S("""<div class="k">Bölüm 1</div><h1 style="margin-top:160px">Meta reklamları:<br><i>geçmiş performans</i></h1>""", "dark")

# 5 Aylık
S(f"""<div class="k">Aylık harcama ve ölçülen ciro</div>
<h2>Meta'nın kendi ölçtüğü satış, harcamanın çok gerisinde kaldı; son üç ayda neredeyse sıfıra indi.</h2>
<div style="display:flex;gap:22px;font-size:13px;margin-bottom:8px"><span><b style="color:{INK}">■</b> Reklam harcaması</span><span><b style="color:{GOLD}">■</b> Ölçülen satış cirosu</span></div>
{chart_monthly()}
<p class="note">Eylül–Ekim 2025'te harcama yok. Aralık 2025'teki yüksek ciro tek bir yüksek tutarlı siparişten geliyor (1 satış, 89.627 TL); bu ay hariç tutulduğunda dönemin ROAS'ı {d((tot_val-89627)/(tot_spend-20907),2)}.</p>""")

# 6 Bütçe dağılımı ve kampanyalar
S(f"""<div class="k">Bütçe nereye gitti</div>
<h2>52 kampanyanın 34'ü öne çıkarılmış gönderi. Satış amaçlı 14 kampanyanın {len(sales_zero)}'inde hiç satış yok.</h2>
{chart_split()}
<table style="margin-top:14px"><tr><th>Satış kampanyası (ömür boyu)</th><th class="r">Harcama</th><th class="r">Satış</th><th class="r">Ciro</th><th class="r">ROAS</th><th class="r">Sıklık</th></tr>{top_campaigns_rows()}</table>""")

# 7 Huni
S(f"""<div class="k">Dönüşüm hunisi (ömür boyu, Meta reklamlarından gelen trafik)</div>
<h2>Trafik geliyor, ürün sayfasında karar verilmiyor: 100 ziyaretçiden 1,5'i sepete ekliyor.</h2>
{chart_funnel()}
<div class="grid g3" style="margin-top:18px">
<div class="card"><h3>Sepete ekleme %{d(funnel['add_to_cart']/funnel['landing_page_view']*100,1)}</h3><p>E-ticaret sektör ortalaması genellikle %3 ile %7 arasındadır. Ürün sayfası güveni, fiyat algısı ve taksit seçenekleri birlikte incelenmeli.</p></div>
<div class="card"><h3>Ödeme adımları kayıplı</h3><p>193 ödeme başlatmadan 39 satış (%{d(39/193*100,0)}). Ödeme adımında sürtünme var: kargo ve taksit bilgisi, güven rozetleri, ödeme seçenekleri.</p></div>
<div class="card"><h3>Ölçüm eksik</h3><p>Aynı dönemde ikas'ta 126 online sipariş var; Meta yalnızca 39'unu kendisine bağlayabilmiş. Bir sonraki sayfada gerçek satış verisi.</p></div>
</div>""")

# 8 Yerleşim ve kitle
S(f"""<div class="k">Yerleşim, kitle ve kreatif</div>
<h2>Düşük kaliteli yerleşimler, yorgun kitleler, az sayıda kreatife yaslanan bir hesap.</h2>
<div class="grid g2">
<div><table class="small"><tr><th>Yerleşim (son 12 ay)</th><th class="r">Harcama</th><th class="r">Tıklama oranı</th><th class="r">Sepet</th><th class="r">Satış</th></tr>{placement_rows()}</table>
<p class="note">Audience Network'te %18–36 tıklama oranı, kaza tıklamaları ve düşük kaliteli trafik için tipik bir işarettir. {tl(an_spend)} harcamadan {int(an_atc)} sepete ekleme, 0 satış.</p></div>
<div>
<div class="card" style="margin-bottom:14px"><h3>Remarketing kampanyasında sıklık 12,1</h3><p>Aynı kişiye ortalama 12 kez aynı reklamlar gösterilmiş. En çok harcanan reklam ("Rayban") 27.925 TL harcamada 7,3 sıklığa ulaşmış. Kreatif yenilenmemiş, kitle yorulmuş.</p></div>
<div class="card" style="margin-bottom:14px"><h3>Kreatif çeşitliliği dar</h3><p>389 reklamın ilk 10'u harcamanın %34'ünü alıyor. Satış getiren reklamlar: video UGC, "Rayban" ve "Police" ürün videoları. Marka mirası, uzmanlık ve Kuz AI hikâyesi reklamda neredeyse hiç kullanılmamış.</p></div>
<div class="card"><h3>Kitle yaşı ve marka uyumu</h3><p>Harcamanın en büyük payı 35–54 yaş kadın. Sepete ekleme oranı 55+ yaşta belirgin biçimde daha yüksek. Lüks ürün için bu segment ayrıca test edilmeli.</p></div>
</div></div>""")

# ikas karşılaştırması
if IK:
    T = ikas_period("2025-07", "2026-11"); P1 = ikas_period("2026-02", "2026-07"); P2 = ikas_period("2026-08", "2026-11")
    S(f"""<div class="k">Gerçek satış verisi · ikas</div>
<h2>Meta satışların yalnızca üçte birini görüyor; gerçek tablo daha iyi ama son dört aydaki çöküş gerçek.</h2>
<div class="grid g4" style="margin-bottom:14px">
<div class="kpi"><div class="v">{T['orders']}</div><div class="l">Online sipariş (Tem 2025 – 14 Kas 2026). Meta bunların {int(tot_pur)}'unu (%{d(tot_pur/T['orders']*100,0)}) görmüş</div></div>
<div class="kpi"><div class="v">{tl(T['net'])}</div><div class="l">Net online ciro (iadeler düşülmüş). Brüt {tl(T['gross'])}</div></div>
<div class="kpi"><div class="v">{d(T['net']/T['spend'],2)}</div><div class="l">Net ciro / Meta harcaması. Google harcaması bilinmediği için gerçek oran daha düşük</div></div>
<div class="kpi"><div class="v">{tl(T['spend']/T['orders'])}</div><div class="l">Sipariş başına Meta harcaması</div></div>
</div>
<div style="display:flex;gap:22px;font-size:13px;margin-bottom:4px"><span><b style="color:{INK}">■</b> Meta reklam harcaması</span><span><b style="color:{GREEN}">■</b> ikas net online ciro</span></div>
{chart_ikas(h=255)}
<p class="note">Mağaza içi kayıtlar (ADMIN) ve 5 TL altı siparişler hariç; Kasım 2026 verisi 14 Kasım'a kadar. Net ciro organik, Google ve doğrudan satışları da içerir.</p>""")

    S(f"""<div class="k">İki dönem, iki tablo</div>
<h2>İlkbahar ve yazda sistem çalıştı; Ağustos'tan sonra harcama sürdü, satış durdu.</h2>
<div class="grid g2" style="margin-bottom:20px">
<div class="card"><h3>Şubat – Temmuz 2026</h3><table class="small">
<tr><td>Meta harcaması</td><td class="r">{tl(P1['spend'])}</td></tr><tr><td>Online sipariş</td><td class="r">{P1['orders']}</td></tr>
<tr><td>Net ciro</td><td class="r">{tl(P1['net'])}</td></tr><tr><td>Net ciro / harcama</td><td class="r pos">{d(P1['net']/P1['spend'],2)}</td></tr>
<tr><td>Sipariş başına harcama</td><td class="r">{tl(P1['spend']/P1['orders'])}</td></tr></table></div>
<div class="card"><h3>Ağustos – Kasım 2026</h3><table class="small">
<tr><td>Meta harcaması</td><td class="r">{tl(P2['spend'])}</td></tr><tr><td>Online sipariş</td><td class="r">{P2['orders']}</td></tr>
<tr><td>Net ciro</td><td class="r">{tl(P2['net'])}</td></tr><tr><td>Net ciro / harcama</td><td class="r neg">{d(P2['net']/P2['spend'],2)}</td></tr>
<tr><td>Sipariş başına harcama</td><td class="r neg">{tl(P2['spend']/P2['orders'])}</td></tr></table></div>
</div>
<div class="grid g3">
<div class="card"><h3>Sezon etkisi var</h3><p>Güneş gözlüğü talebi yaz sonunda düşer; düşüşün bir kısmı doğaldır. Ancak harcama Ağustos'ta 30 bin TL ile Temmuz seviyesinde sürdü, yapı ve mesaj sezona göre uyarlanmadı.</p></div>
<div class="card"><h3>Kasım kampanyası sonuç vermedi</h3><p>“Net %30” Kasım kampanyası ve 13 bin TL harcamaya karşın 14 Kasım'a kadar 1 online sipariş.</p></div>
<div class="card"><h3>İadeler yüksek</h3><p>{T['fullref']} sipariş tamamen iade (%{d(T['fullref']/T['orders']*100,0)}); iade tutarı brüt cironun %{d(T['refund']/T['gross']*100,0)}'sı. Haziran'da %35. Ürün beklentisi, renk ve beden uyumu incelenmeli.</p></div>
</div>""")

# 9 Organik bölüm
S("""<div class="k">Bölüm 2</div><h1 style="margin-top:160px">Instagram:<br><i>organik görünüm</i></h1>""", "dark")

S(f"""<div class="k">Instagram @damlakuzoptik</div>
<h2>Düzenli paylaşım var ama içerik ilgi uyandırmıyor; hesap konuşmuyor.</h2>
<div class="grid g4" style="margin-bottom:26px">
<div class="kpi"><div class="v">{n(ig['followers_count'])}</div><div class="l">Takipçi · son 28 günde net +{sum(v['value'] for v in R['igfollow'][0]['values'])}</div></div>
<div class="kpi"><div class="v">%{d(er,2)}</div><div class="l">Etkileşim oranı (son 60 gönderi). Sağlıklı seviye genellikle %1'in üzeri</div></div>
<div class="kpi"><div class="v">{n(med_reach)}</div><div class="l">Gönderi başına ortanca erişim; takipçinin %{d(med_reach/ig['followers_count']*100,1)}'i</div></div>
<div class="kpi"><div class="v">%{d(reels_share,0)}</div><div class="l">Reels oranı (son 100 paylaşım). Kalanı tekil fotoğraf</div></div>
</div>
<div class="grid g3">
<div class="card"><h3>Ne görüyoruz</h3><ul><li>Ayda ~11 paylaşım, %88'i tekil ürün fotoğrafı</li><li>Ortanca {med_like} beğeni, 60 gönderide {comments} yorum, kaydetme ve paylaşım neredeyse sıfır</li><li>Metinler kalıp: "zamansız", "ikonik", "şıklık detaylarda"</li></ul></div>
<div class="card"><h3>Ne eksik</h3><ul><li>İnsan yüzü, optisyen, mağaza ve ekip yok</li><li>Yarım asırlık hikâye Kasım'a kadar hiç anlatılmamış</li><li>Kuz AI yalnızca Nisan'da iki gönderide geçiyor</li><li>Soru, anket, rehber gibi konuşma başlatan format yok</li></ul></div>
<div class="card"><h3>Takipçi kalitesi</h3><p>Takipçilerin %{d(g_unknown/g_total*100,0)}'inin cinsiyeti bilinmiyor; yaygın olarak pasif veya işletme hesaplarına işaret eder. Son 28 günde {n(igins.get('profile_views') or 0)} profil ziyaretinden yalnızca {n(igins.get('website_clicks') or 0)} siteye tıklama geldi.</p></div>
</div>""")

# 11 Site ve ölçüm
S("""<div class="k">Bölüm 3</div><h1 style="margin-top:160px">Site, feed<br><i>ve ölçüm</i></h1>""", "dark")

S("""<div class="k">Teknik hijyen</div>
<h2>Reklamın beslendiği altyapıda, ajansın kontrol etmesi gereken temel hatalar var.</h2>
<table><tr><th>Bulgu</th><th>Etki</th><th>Önem</th></tr>
<tr><td><b>"deneme" test ürünü 2,06 TL'ye satışta</b>, Google ve Meta feed'inde de yer alıyor</td><td>Gerçek sipariş riski; reklamda 2 TL'lik ürün görünme riski</td><td><span class="tag t-red">Kritik</span></td></tr>
<tr><td>"Kargo" ürün olarak feed'de (1,03 TL)</td><td>Alışveriş reklamlarında anlamsız ürün</td><td><span class="tag t-red">Kritik</span></td></tr>
<tr><td>Google feed başlıkları zayıf ("714 - Siyah", "AR 8211"); marka ve "güneş gözlüğü" ifadesi yok</td><td>Google Alışveriş'te aramalarla eşleşme düşük</td><td><span class="tag t-red">Yüksek</span></td></tr>
<tr><td>Barkod (GTIN) alanında 511 üründe barkod yerine ürün kodu var; geçerli barkod yok</td><td>Google görünürlüğü düşer; Meta katalog uyarısı</td><td><span class="tag t-red">Yüksek</span></td></tr>
<tr><td>Ürünlerin %92'si kalıcı olarak "%30 indirimli"</td><td>Lüks algısına zarar; indirimli satış mevzuatı açısından risk</td><td><span class="tag t-amb">Yüksek</span></td></tr>
<tr><td>Site schema'sında adres boş; site ve Instagram'da farklı telefonlar</td><td>Yerel arama ve Maps görünürlüğü</td><td><span class="tag t-amb">Orta</span></td></tr>
<tr><td>Marka sayfalarında 21 adet H1, yinelenen sayfa başlıkları, güncel olmayan açıklamalar</td><td>SEO sıralamaları</td><td><span class="tag t-amb">Orta</span></td></tr>
<tr><td>Sitede doğrudan Google Ads dönüşüm etiketi görünmüyor (GTM içinden yükleniyor olabilir)</td><td>Google kampanyalarının ölçümü doğrulanamıyor</td><td><span class="tag t-amb">Teyit</span></td></tr>
</table>""")

# 13 Rakip
S("""<div class="k">Rekabet bağlamı</div>
<h2>Rakipler indirimle konuşuyor; Damla Kuz'un sahiplenebileceği alan uzmanlık ve miras.</h2>
<div class="grid g3">
<div class="card"><h3>Fiyat savaşı</h3><p>Özkan, Gürel ve Ersun Optik; Miu Miu, Prada ve Ray-Ban'da %25–50 indirim yapıyor. Atasun 5 taksit veriyor. Fiyat üzerinden kazanmak marjı eritir.</p></div>
<div class="card"><h3>En yakın rakip: Kuvars Optik</h3><p>Aynı segment, İstanbul AVM'leri (Akmerkez, Akbatı, Tersane), kendi premium markası Movitra, Google Ads'te aktif.</p></div>
<div class="card"><h3>Boş alan</h3><p>Hiçbir rakip yarım asırlık bir optisyen hikâyesi, Kuz AI gibi bir seçim asistanı ya da "Sadece Damla Kuz'da" seçkisi sunmuyor. Ajans bu farkları iletişimde kullanmamış.</p></div>
</div>
<table class="small" style="margin-top:22px"><tr><th>Rakip</th><th>Segment</th><th>Fiziksel</th><th>Fiyat iletişimi</th><th>Reklam altyapısı (sitede görülen)</th></tr>
<tr><td><b>Atasun</b></td><td>Kitlesel zincir</td><td>Türkiye geneli</td><td>İndirim, 5 taksit, kendi markaları %50</td><td>Meta Pixel, Insider, Criteo</td></tr>
<tr><td><b>Kuvars Optik</b></td><td>Premium / lüks</td><td>İstanbul AVM'leri</td><td>%10–18 indirim, Movitra</td><td>Meta Pixel, Google Ads</td></tr>
<tr><td><b>Opmar</b></td><td>Orta-üst zincir</td><td>İstanbul, Ankara, Kayseri</td><td>Ücretsiz kargo, pazaryeri</td><td>Insider, Criteo</td></tr>
<tr><td><b>Özkan Optik</b></td><td>Online, fiyat odaklı</td><td>Ankara</td><td>%25–50 indirim</td><td>Meta Pixel, Google Ads</td></tr>
<tr><td><b>Bilge Karga</b></td><td>Kendi markası</td><td>—</td><td>%25–45 indirim, pazaryerleri</td><td>Meta Pixel, Insider, Criteo</td></tr>
<tr><td><b>Damla Kuz</b></td><td>Lüks + miras</td><td>Ataköy Atrium</td><td>Kalıcı %30, 3 taksit</td><td>Meta Pixel + CAPI, GA4 (Google Ads etiketi görülmedi)</td></tr></table>
<p class="note">Ayrıntılı analiz: repo · rakip-analizi/01-rakip-analizi.md</p>""")

# 14 Ayrılık gerekçeleri
S("""<div class="k">Bölüm 4</div><h1 style="margin-top:160px">Ajanstan ayrılma<br><i>gerekçeleri</i></h1>""", "dark")

S(f"""<div class="k">Gerekçeler · veriye dayalı</div>
<h2 style="font-size:32px;margin-bottom:12px">Ayrılık kararı kişisel değil, ölçülebilir sonuçlara dayanıyor.</h2>
<div class="grid g2" style="gap:6px 40px">
<div class="reason"><div class="num">1</div><div><h3>Son dört ayda geri dönüş yok</h3><p>Ağustos–Kasım 2026'da Meta'ya 71 bin TL harcandı; ikas'ta 13 sipariş, 71 bin TL net ciro. Ürün maliyeti düşülünce zarar.</p></div></div>
<div class="reason"><div class="num">2</div><div><h3>Bütçe yanlış hedefe harcandı</h3><p>{tl(boost_spend)} (%{d(boost_spend/tot_spend*100,1)}), satış değil tıklama hedefli 34 öne çıkarmaya gitti: 0 satış. Uygulama bugün de sürüyor.</p></div></div>
<div class="reason"><div class="num">3</div><div><h3>Sezona uyum ve müdahale yok</h3><p>Yaz sonunda talep düşerken harcama ve yapı aynı kaldı. Kasım “net %30” kampanyası 14 Kasım'a kadar 1 online sipariş getirdi.</p></div></div>
<div class="reason"><div class="num">4</div><div><h3>Dağınık yapı, yorgun kreatif</h3><p>14 satış kampanyasından {len(sales_zero)}'i sıfır satış. Remarketing sıklığı 12. Kreatifler aylarca yenilenmemiş.</p></div></div>
<div class="reason"><div class="num">5</div><div><h3>Altyapı hijyeni ihmal edildi</h3><p>Test ürünü feed'de ve satışta; barkodlar geçersiz; feed başlıkları optimize edilmemiş; Audience Network kapatılmamış.</p></div></div>
<div class="reason"><div class="num">6</div><div><h3>Organik iletişimde strateji yok</h3><p>Etkileşim %{d(er,2)}, Reels %{d(reels_share,0)}. Marka mirası, uzmanlık ve Kuz AI gibi ayrıştırıcılar kullanılmamış; dil indirim ağırlıklı.</p></div></div>
<div class="reason"><div class="num">7</div><div><h3>Sahiplik ve şeffaflık riski</h3><p>Google Ads ve Merchant Center şirketin erişiminde değil. Harcama ve sonuçlar şirket tarafından denetlenemiyor.</p></div></div>
<div class="reason"><div class="num">8</div><div><h3>Ölçüm ve raporlama yetersiz</h3><p>Meta, siparişlerin yalnızca %31'ini görüyor; ikas ile karşılaştırma ve iade takibi (%16) yapılmamış. Kararlar eksik veriyle alınmış.</p></div></div>
</div>""")

# 16-18 Düzeltme önerileri
S("""<div class="k">Bölüm 5</div><h1 style="margin-top:160px">Düzeltme<br><i>önerileri</i></h1>""", "dark")

S("""<div class="k">Öneriler · Meta reklamları</div>
<h2>Az kampanya, doğru hedef, sürekli yenilenen kreatif.</h2>
<table><tr><th>#</th><th>Öneri</th><th>Neden</th><th>Öncelik</th></tr>
<tr><td>1</td><td>Tıklama hedefli öne çıkarmaları bırakmak; organik içerik yalnızca satış veya etkileşim hedefiyle desteklenir</td><td>%10,5 bütçe, 0 satış</td><td><span class="tag t-red">Hemen</span></td></tr>
<tr><td>2</td><td>Yapıyı 3 kampanyaya indirmek: Advantage+ satış (keşif), katalog yeniden pazarlama, yerel mağaza bilinirliği</td><td>14 dağınık kampanya öğrenmeyi bölüyor</td><td><span class="tag t-red">Yüksek</span></td></tr>
<tr><td>3</td><td>Audience Network'ü kapatmak</td><td>Yüksek tıklama, sıfır satış</td><td><span class="tag t-red">Yüksek</span></td></tr>
<tr><td>4</td><td>Remarketing'i katalog tabanlı dinamik reklamla yeniden kurmak; sıklık tavanı ve 2 haftalık kreatif döngüsü</td><td>Sıklık 12, yorgunluk</td><td><span class="tag t-amb">Yüksek</span></td></tr>
<tr><td>5</td><td>Her ay en az 6 yeni kreatif: UGC ve ürün videoları (kanıtlanmış), miras, optisyen uzmanlığı, Kuz AI; tüm formatlarda</td><td>Satış getiren format video; çeşitlilik dar</td><td><span class="tag t-amb">Yüksek</span></td></tr>
<tr><td>6</td><td>Katalog verisini zenginleştirmek: renk, cinsiyet, yaş grubu, gerçek barkod</td><td>Dinamik reklam eşleşmesi</td><td><span class="tag t-amb">Orta</span></td></tr>
<tr><td>7</td><td>Haftalık Meta ile ikas karşılaştırması; ROAS hedefi brüt marja göre belirlenir (ör. %40 marjda başa baş ROAS 2,5)</td><td>Gerçek kârlılık yönetimi</td><td><span class="tag t-amb">Sürekli</span></td></tr>
<tr><td>8</td><td>İşletme doğrulaması; eski reklam hesabındaki ödenmemiş bakiyenin kapatılması</td><td>Hesap güvenilirliği</td><td><span class="tag t-grn">Bu ay</span></td></tr>
</table>""")

S("""<div class="k">Öneriler · içerik, site, Google</div>
<h2>Reklamı düzeltmek tek başına yetmez; içerik ve site de aynı hikâyeyi anlatmalı.</h2>
<div class="grid g3">
<div class="card"><h3>İçerik ve Instagram</h3><ul>
<li>Haftada 3 Reels, 2 carousel; Reels oranı %60'ın üzerine</li>
<li>İçerik ayakları: ürün ve stil %40, optisyen uzmanlığı %25, miras %15, Kuz AI %10, mağaza %10</li>
<li>İnsan yüzü: optisyen, ekip, müşteri (izinli)</li>
<li>Kaydedilir rehber içerikler: yüz şekli, orijinallik, polarize</li>
<li>Ton: indirim değil, uzmanlık ve seçkinlik</li>
<li>Bio: tek telefon, Kuz AI ve mağaza bağlantısı</li></ul></div>
<div class="card"><h3>Site ve feed</h3><ul>
<li>Test ve kargo ürünlerinin tamamen kaldırılması</li>
<li>Merchant Center'a ek feed: başlık, renk, cinsiyet (hazır)</li>
<li>Distribütörlerden EAN-13 barkod listesi</li>
<li>Kalıcı %30 yerine gerçek fiyat ve dönemsel kampanya</li>
<li>6 taksit seçeneğinin değerlendirilmesi</li>
<li>Ürün sayfasına güven öğeleri: resmi distribütör, 2 yıl garanti, optisyen desteği</li>
<li>Schema, H1 ve meta düzeltmeleri (hazır)</li></ul></div>
<div class="card"><h3>Google</h3><ul>
<li>Hesapların şirkete devri (önkoşul)</li>
<li>Satın alma dönüşümünün doğrulanması</li>
<li>Performance Max: üst lüks markalara ve özel seçkiye ağırlık; fiyat savaşı olan modellerde düşük teklif</li>
<li>Marka ve model aramaları</li>
<li>Yerel arama: Ataköy, Bakırköy çevresi, yol tarifi ve arama hedefi</li>
<li>Google Business Profile: fotoğraf, yorum yönetimi, haftalık gönderi</li></ul></div>
</div>""")

# Devir planı
S("""<div class="k">Bölüm 6</div><h1 style="margin-top:160px">Devir<br><i>planı</i></h1>
<p class="lead" style="margin-top:24px">Varsayım: bugün hiçbir hesabın erişimi şirkette değil.<br>Plan, her varlığı bu en kötü senaryodan başlayarak güvenceye alır.</p>""", "dark")

S("""<div class="k">İlkeler</div>
<h2>Önce sahiplik, sonra bildirim, en son erişim kaldırma.</h2>
<div class="grid g4">
<div class="card"><div class="num">1</div><h3 style="margin-top:10px">Sahiplik şirkette</h3><p>Her hesap şirketin kendi portföyünde ve şirket e-postasıyla, iki yöneticiyle. Ajans yalnızca "partner".</p></div>
<div class="card"><div class="num">2</div><h3 style="margin-top:10px">Kesintisiz yayın</h3><p>Devir sırasında kampanyalar durmaz. Paralel dönem tamamlanmadan hiçbir şey kapatılmaz.</p></div>
<div class="card"><div class="num">3</div><h3 style="margin-top:10px">Veri kaybı yok</h3><p>Pixel, kitleler, katalog ve kampanya geçmişi aynı hesaplarda kalır; yeni hesap açılmaz.</p></div>
<div class="card"><div class="num">4</div><h3 style="margin-top:10px">Yazılı ve tarihli</h3><p>Her talep e-postayla, teslim tarihleriyle. Teslim edilen her şey kontrol listesiyle doğrulanır.</p></div>
</div>
<p class="note" style="margin-top:22px">Not: Hiçbir kampanyaya şirket sahibinin açık talimatı olmadan dokunulmaz. Devir tarihi (T günü) şirket tarafından belirlenir.</p>""")

S("""<div class="k">Varlık envanteri · 1/2</div>
<h2 style="font-size:30px">Her varlık için hedef durum ve yapılacak işlem</h2>
<table class="small"><tr><th>Varlık</th><th>Bilinen durum (19 Kasım)</th><th>Hedef</th><th>İşlem</th></tr>
<tr><td><b>Meta işletme portföyü</b></td><td>Şirkette, tek yönetici</td><td>En az 2 şirket yöneticisi, doğrulanmış işletme</td><td>İkinci yönetici eklemek, işletme doğrulaması</td></tr>
<tr><td><b>Facebook sayfası, Instagram</b></td><td>Portföyde</td><td>Portföy sahibi; ajans partner</td><td>Sayfa rollerini denetlemek, kişisel profil erişimlerini temizlemek</td></tr>
<tr><td><b>Meta reklam hesabı</b></td><td>Portföyde. Ajans, reklam hesabına atanmış <b>"Ulusal Çağdaş Çalım"</b> sistem kullanıcısıyla yönetiyor (Mayıs'tan bu yana ~1.700 işlem). "Inolyzer" kullanıcılarının da erişimi var.</td><td>Şirket sahibi; ajans erişimi T+30'da kaldırılır</td><td>Erişim listesi, kampanya dökümü, kitle listesi</td></tr>
<tr><td><b>Meta Pixel ve Conversions API</b></td><td>Portföyde; ajans sistem kullanıcıları yetkili; ikas sunucu entegrasyonu açık</td><td>Şirket sahibi; ikas entegrasyonu korunur</td><td>Özel dönüşümlerin ve olay ayarlarının belgelenmesi</td></tr>
<tr><td><b>Meta katalog</b></td><td>Portföyde, 512 ürün, ikas beslemeli</td><td>Aynı</td><td>Ek veri kaynağı (renk, cinsiyet)</td></tr>
<tr><td><b>Kitleler</b></td><td>Bilinmiyor</td><td>Şirket hesabında, belgelenmiş</td><td>Ajanstan tanım listesi; müşteri listesi kaynağı</td></tr>
<tr><td><b>Eski reklam hesabı</b></td><td>Ödenmemiş bakiye</td><td>Bakiye kapalı, hesap arşiv</td><td>Faturalar ve ödemeler bölümünden kapatmak</td></tr>
</table>""")

S("""<div class="k">Varlık envanteri · 2/2</div>
<h2 style="font-size:30px">Google, web ve içerik varlıkları</h2>
<table class="small"><tr><th>Varlık</th><th>Bilinen durum</th><th>Hedef</th><th>İşlem</th></tr>
<tr><td><b>Google Ads</b></td><td>Şirkette görünmüyor; muhtemelen ajansın yönetici hesabı (MCC) altında</td><td>Şirket e-postası "Yönetici"; fatura şirket kartında; ajans MCC bağlantısı T+30'da kaldırılır</td><td>Müşteri no, MCC bağlantısı, yönetici daveti, fatura sahibi teyidi</td></tr>
<tr><td><b>Merchant Center</b></td><td>Şirkette görünmüyor</td><td>Şirket yöneticisi; alan adı şirket adına doğrulanmış</td><td>Kimlik, yönetici daveti, feed kaynağı</td></tr>
<tr><td><b>Google Analytics 4</b></td><td>Teyit edilmedi</td><td>Hesap düzeyinde şirket yöneticisi</td><td>Erişim kontrolü, gerekirse davet</td></tr>
<tr><td><b>Google Tag Manager</b></td><td>Şirket yönetici</td><td>Ajans kullanıcıları kaldırılmış</td><td>Etiket envanteri, sürüm yedeği</td></tr>
<tr><td><b>Google Business Profile</b></td><td>Şirkette</td><td>Birincil sahip şirket</td><td>Yönetici listesini temizlemek</td></tr>
<tr><td><b>ikas paneli</b></td><td>Bilinmiyor</td><td>Ajans kullanıcıları kaldırılmış; satış kanalı entegrasyonları şirket hesaplarında</td><td>Kullanıcı listesi, entegrasyon sahipleri</td></tr>
<tr><td><b>Alan adı ve DNS</b></td><td>Bilinmiyor</td><td>Kayıt şirket adına, şifre şirkette</td><td>Kayıt firması, yetkili e-posta, yenileme tarihi</td></tr>
<tr><td><b>Kreatif arşiv</b></td><td>Ajansta</td><td>Açık dosyalar şirket Drive'ında; kullanım hakları yazılı</td><td>PSD/AI/Figma/Canva/video projeleri, font ve görsel lisansları</td></tr>
<tr><td><b>Raporlar ve şifreler</b></td><td>Ajansta</td><td>12 aylık rapor, şifre ve 2FA yöneticisi şirkette</td><td>Teslim ve şifre değişimi</td></tr>
</table>""")

S("""<div class="k">Takvim · T = devir tarihi</div>
<h2>Altı adımda devir: hazırlık, talep, transfer, paralel dönem, kapanış, doğrulama</h2>
<div class="grid g3" style="gap:20px 28px">
<div class="phase"><div class="when">T−14 · Hazırlık (ajansa haber vermeden)</div><ul><li>Envanter ve erişim kontrolü (bu belge)</li><li>Sözleşme ve bildirim süresinin incelenmesi</li><li>Şirket e-postası ve iki yönetici belirlenmesi</li><li>Yeni operasyonun hazır olması</li></ul></div>
<div class="phase"><div class="when">T−10 · Hesap envanteri talebi</div><ul><li>"Envanter güncelleme" e-postası (hazır taslak)</li><li>Google Ads, Merchant Center, GA4 yönetici davetleri</li><li>Rapor ve kreatif arşiv talebi</li></ul></div>
<div class="phase"><div class="when">T · Resmi bildirim</div><ul><li>Sözleşmeye uygun yazılı fesih bildirimi</li><li>Devir kontrol listesi ve teslim tarihleri</li><li>Gizlilik, KVKK ve veri iade maddeleri</li></ul></div>
<div class="phase"><div class="when">T → T+14 · Transfer</div><ul><li>Sahiplik ve fatura şirkete</li><li>Ajans "partner" rolüne indirilir</li><li>Kitle, dönüşüm ve kampanya belgeleri teslim</li></ul></div>
<div class="phase"><div class="when">T+14 → T+30 · Paralel dönem</div><ul><li>Ajans kampanyaları yayında, yeni yapı onayla hazırlanır</li><li>Haftalık karşılaştırmalı rapor</li><li>Kreatif ve feed yenileme</li></ul></div>
<div class="phase"><div class="when">T+30 · Kapanış ve doğrulama</div><ul><li>Ajans erişimleri kaldırılır (Meta, Google, ikas, GTM)</li><li>Tüm şifreler değiştirilir, 2FA yenilenir</li><li>Son fatura ve iade kontrolü; erişim denetimi tekrar</li></ul></div>
</div>""")

S("""<div class="k">Erişim kaldırma sırası ve riskler</div>
<h2>Yanlış sırayla kapatılan erişim, kampanyayı da veriyi de götürebilir.</h2>
<div class="grid g2">
<div><h3>Kaldırma sırası (T+30)</h3><ol style="padding-left:18px">
<li>Yeni yapının yayında ve ölçümün doğrulanmış olması</li>
<li>Google Ads: ajans MCC bağlantısının kaldırılması (hesap şirkette kalır)</li>
<li>Merchant Center ve GA4 ajans kullanıcıları</li>
<li>Meta: ajans sistem kullanıcılarının reklam hesabı ve Pixel atamaları</li>
<li>Meta: partner işletme bağlantısı</li>
<li>GTM, ikas ve Business Profile ajans kullanıcıları</li>
<li>Ortak kullanılan tüm şifrelerin değiştirilmesi</li></ol></div>
<div><table class="small"><tr><th>Risk</th><th>Önlem</th></tr>
<tr><td>Google Ads ajansın MCC'si altında oluşturulmuşsa hesap verilmeyebilir</td><td>T'den önce yönetici daveti; sözleşmede hesap sahipliği maddesi</td></tr>
<tr><td>Kampanyaların aniden durdurulması</td><td>Paralel dönem; kampanya dökümü T−10'da alınır</td></tr>
<tr><td>Kreatiflerin teslim edilmemesi</td><td>Ödeme ve fesih teslime bağlanır; yayınlanmış reklamlar API ile arşivlenir</td></tr>
<tr><td>Kitle ve dönüşüm tanımlarının kaybı</td><td>Aynı hesaplar korunur; tanımlar belgelenir</td></tr>
<tr><td>Fatura kartının ajansa ait olması</td><td>Ödeme yöntemi şirket kartına alınır</td></tr>
<tr><td>Müşteri verisinin ajansta kalması</td><td>KVKK uyarınca iade ve imha teyidi</td></tr></table></div>
</div>""")

S("""<div class="k">Ajanstan resmi teslim listesi</div>
<h2>Fesih bildirimiyle birlikte istenecekler</h2>
<div class="grid g3">
<div class="card"><h3>Hesaplar ve erişim</h3><ul><li>Google Ads müşteri no, MCC bilgisi, yönetici erişimi</li><li>Merchant Center kimliği ve yönetici erişimi</li><li>GA4 hesap düzeyinde yönetici</li><li>Kullanılan tüm araçların listesi (ör. Inolyzer) ve sözleşme sahipleri</li><li>Ortak şifrelerin listesi</li></ul></div>
<div class="card"><h3>Veri ve belgeler</h3><ul><li>12 aylık Meta ve Google raporları</li><li>Kampanya yapısı ve hedefleme belgeleri</li><li>Özel ve benzer kitle tanımları, müşteri listesi kaynakları</li><li>Özel dönüşüm ve GTM etiket açıklamaları</li><li>İçerik takvimi ve yayın arşivi</li></ul></div>
<div class="card"><h3>Kreatif ve haklar</h3><ul><li>Tüm kreatiflerin açık dosyaları</li><li>Video projeleri ve ham çekimler</li><li>Logo ve kurumsal kimlik (vektör)</li><li>Font, müzik ve stok görsel lisansları</li><li>Fikri hakların şirkete devri teyidi</li></ul></div>
</div>
<p class="note">Hazır taslak e-posta: repo · strateji/ajans-devir-epostasi.md. Fesih bildirim metni sözleşme incelendikten sonra hazırlanır.</p>""")

S("""<div class="k">Devir sonrası · ilk 90 gün</div>
<h2>Aylık 50.000 TL bütçeyle ölçülebilir, kârlılığa odaklı bir yapı</h2>
<div class="grid g3">
<div class="phase"><div class="when">0–30 gün · Temel</div><ul><li>Ölçüm doğrulama: Meta, Google ve ikas aynı rakamı söylüyor</li><li>Feed düzeltmeleri, barkod, schema</li><li>3 kampanyalık yeni Meta yapısı (onayla)</li><li>Google: PMax, marka ve model araması, yerel arama</li><li>Aralık içerik takvimi (onaylandı)</li></ul></div>
<div class="phase"><div class="when">30–60 gün · Kuz İstanbul geçişi</div><ul><li>Teaser serisi ve hesap adı geçişi</li><li>Kreatif yenileme: miras filmi, Kuz AI, hediye</li><li>Site fiyat politikası ve taksit kararı</li><li>Haftalık optimizasyon ve bütçe kaydırma</li></ul></div>
<div class="phase"><div class="when">60–90 gün · Ölçekleme</div><ul><li>Kârlı kanallara bütçe artışı önerisi</li><li>İlkbahar ve yaz sezonu hazırlığı</li><li>Influencer ve iş birliği testleri</li><li>Aylık yönetim raporu: ROAS, satış başı maliyet, mağaza yönlendirmesi</li></ul></div>
</div>
<div class="grid g4" style="margin-top:26px">
<div class="kpi"><div class="v">≥ 2,5</div><div class="l">Hedef ROAS (brüt marja göre güncellenecek)</div></div>
<div class="kpi"><div class="v">%3</div><div class="l">Hedef sepete ekleme oranı (şu an %1,5)</div></div>
<div class="kpi"><div class="v">%1+</div><div class="l">Hedef Instagram etkileşim oranı</div></div>
<div class="kpi"><div class="v">%60</div><div class="l">Reels oranı</div></div>
</div>""")

S("""<div class="k">Kararlar ve sonraki adımlar</div>
<h2>Şirket tarafından verilecek kararlar</h2>
<table><tr><th>#</th><th>Karar</th><th>Not</th></tr>
<tr><td>1</td><td>Devir tarihi (T günü) ve fesih bildirim zamanı</td><td>Sözleşme süresine göre</td></tr>
<tr><td>2</td><td>Hesap envanteri e-postasının gönderilmesi</td><td>Taslak hazır; ajansla ilişkiyi bozmadan sahipliği güvenceye alır</td></tr>
<tr><td>3</td><td>Google Ads harcama verisi (ajanstan)</td><td>ikas cirosuyla birlikte gerçek toplam getiri hesabı</td></tr>
<tr><td>4</td><td>Brüt marj oranı</td><td>ikas'ta ürün alış fiyatları boş; başa baş hedef için gerekli</td></tr>
<tr><td>5</td><td>Fiyat politikası (kalıcı %30) ve taksit sayısı</td><td>Dönüşüm ve marka algısı</td></tr>
<tr><td>6</td><td>İşletme doğrulaması ve eski hesabın bakiyesi</td><td>Meta hesap sağlığı</td></tr>
<tr><td>7</td><td>Mevcut kampanyalara müdahale zamanı</td><td>Şu an hiçbir şeye dokunulmuyor; yalnızca izleniyor</td></tr>
</table>""")

S(f"""<div class="k">Ek · tanımlar ve kaynaklar</div>
<h2 style="font-size:30px">Tanımlar</h2>
<div class="grid g2">
<div><ul>
<li><b>ROAS:</b> reklamdan ölçülen ciro / reklam harcaması. 1,00 = harcanan kadar ciro.</li>
<li><b>Satış başı maliyet:</b> harcama / ölçülen satış adedi.</li>
<li><b>Sıklık:</b> bir kişinin aynı reklamı ortalama görme sayısı.</li>
<li><b>Öne çıkarılan gönderi:</b> Instagram gönderisinin "bağlantı tıklaması" hedefiyle reklama dönüştürülmesi.</li>
<li><b>Audience Network:</b> Meta dışındaki uygulama ve sitelerde gösterilen reklam yerleşimi.</li>
<li><b>Etkileşim oranı:</b> (beğeni + yorum) / takipçi, gönderi başına ortalama.</li></ul></div>
<div><ul>
<li>Meta Marketing API v23, 19 Kasım 2026; aktif hesap {first_month}–Kas 2026, eski hesap Nis–Eyl 2025.</li>
<li>Instagram Graph API: son 100 paylaşım (27 Şub – 18 Kas 2026).</li>
<li>Hesap etkinlik kaydı: ajans sistem kullanıcılarının işlemleri.</li>
<li>damlakuzoptik.com ve ikas feed'leri, 19 Kasım 2026.</li><li>ikas sipariş dökümü (Haz 2025 – 14 Kas 2026), yalnızca toplulaştırılmış olarak kullanıldı.</li>
<li>Rakip siteleri: Atasun, Kuvars, Opmar, Özkan, Bilge Karga, Gürel, Ersun.</li>
<li>Tüm veriler okuma yetkisiyle alındı; hiçbir hesap ayarı değiştirilmedi.</li></ul>
<p class="note">Ayrıntılı çalışma dosyaları: github.com/fahricankuz/damlakuzoptik</p></div>
</div>""")

html = f"<!doctype html><html lang='tr'><head><meta charset='utf-8'><title>Damla Kuz Optik · Denetim ve Devir Planı</title><style>{CSS}</style></head><body>{''.join(slides)}</body></html>"
open(out_html, "w", encoding="utf-8").write(html)
print(len(slides), "slayt")
