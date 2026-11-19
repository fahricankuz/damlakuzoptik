"""Google Merchant Center için ek (supplemental) feed üretir.

ikas'ın Google feed'inde başlıklar zayıf ("714 - Siyah" gibi), renk, cinsiyet,
yaş grubu ve varyant grubu (item_group_id) eksik. Bu bilgiler ikas'ın Meta
(CSV) feed'inde mevcut. Bu araç iki feed'i birleştirerek, Merchant Center'a
ek feed olarak yüklenecek bir TSV dosyası üretir.

Kullanım:
    python3 araclar/ek_feed_olustur.py <facebook_feed.csv> <cikti.tsv> [rapor.txt]

Feed bağlantıları gizli değildir ama herkese açık paylaşılmamalıdır; bu yüzden
repoya yazılmamıştır. Feed'i ikas panelinden alınan bağlantıyla indirin.
"""

import csv
import re
import sys

KATEGORI_ADI = {
    "Erkek Güneş Gözlüğü": ("Erkek Güneş Gözlüğü", "male", "adult"),
    "Kadın Güneş Gözlüğü": ("Kadın Güneş Gözlüğü", "female", "adult"),
    "Çocuk Güneş Gözlüğü": ("Çocuk Güneş Gözlüğü", "unisex", "kids"),
}


GOZLUK_DISI = {"Aksesuar", ""}


def sinifla(product_type: str, link: str):
    """(ürün adı eki, gender, age_group) döndürür.

    Önce product_type, o yetmezse ürün URL'si (…-kadin-gunes-gozlugu gibi)
    kullanılır. "Çok Satanlar" / "Limited Edition" gibi koleksiyonlarda
    yalnızca koleksiyon adı geldiği için URL yedeği gereklidir.
    """
    for anahtar, deger in KATEGORI_ADI.items():
        if anahtar in product_type:
            return deger
    if "Blue Protectors" in product_type:
        return ("Mavi Işık Filtreli Gözlük", "unisex", "adult")
    yol = link.split("?", 1)[0].lower()
    if "-cocuk-" in yol:
        return KATEGORI_ADI["Çocuk Güneş Gözlüğü"]
    if "-kadin-" in yol:
        return KATEGORI_ADI["Kadın Güneş Gözlüğü"]
    if "-erkek-" in yol:
        return KATEGORI_ADI["Erkek Güneş Gözlüğü"]
    if "gozlug" in yol or "Güneş Gözlüğü" in product_type:
        return ("Güneş Gözlüğü", "unisex", "adult")
    if product_type.strip() in GOZLUK_DISI or "Aksesuar" in product_type:
        return (None, None, None)  # aksesuar vb.: başlığa ek yapılmaz
    return ("Güneş Gözlüğü", "unisex", "adult")


def renk_bul(satir: dict) -> str:
    """Renk: önce varyant özelliğinden, yoksa başlıktaki ' - ' sonrasından."""
    attr = satir.get("additional_variant_attribute", "")
    if ":" in attr:
        renk = attr.split(":", 1)[1].strip()
        if renk:
            return renk
    parcalar = satir["title"].split(" - ", 1)
    return parcalar[1].strip() if len(parcalar) == 2 else ""


def baslik_olustur(satir: dict, ek: str | None, renk: str) -> str:
    model = satir["title"].split(" - ", 1)[0].strip()
    marka = satir.get("brand", "").strip()
    if marka and not model.lower().startswith(marka.lower()):
        model = f"{marka} {model}"
    baslik = f"{model} {ek}" if ek else model
    if renk:
        baslik = f"{baslik} - {renk}"
    return re.sub(r"\s+", " ", baslik)[:150]


def main():
    giris, cikti = sys.argv[1], sys.argv[2]
    rapor_yolu = sys.argv[3] if len(sys.argv) > 3 else None
    satirlar = list(csv.DictReader(open(giris, encoding="utf-8")))

    uyarilar = []
    with open(cikti, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["id", "title", "item_group_id", "color", "gender", "age_group"])
        for s in satirlar:
            if s["title"].strip().lower() in {"kargo"}:
                uyarilar.append(f"KARGO ürün olarak feed'de: '{s['title']}' fiyat {s['price']} -> ikas'ta feed dışı bırakılmalı")
                continue
            if s["title"].strip().lower() in {"deneme", "test"}:
                uyarilar.append(f"TEST ÜRÜNÜ YAYINDA: '{s['title']}' fiyat {s['price']} -> ikas'ta silinmeli/gizlenmeli")
                continue
            ek, cinsiyet, yas = sinifla(s.get("product_type", ""), s.get("link", ""))
            renk = renk_bul(s)
            if ek is None:
                uyarilar.append(f"Gözlük dışı ürün (ek yapılmadı): {s['title']} [{s.get('product_type','')}]")
                w.writerow([s["id"], baslik_olustur(s, None, ""), s["item_group_id"], "", "", ""])
                continue
            w.writerow([s["id"], baslik_olustur(s, ek, renk), s["item_group_id"], renk[:100], cinsiyet, yas])

    if rapor_yolu:
        open(rapor_yolu, "w", encoding="utf-8").write("\n".join(uyarilar) + "\n")
    print(f"{len(satirlar)} satır işlendi, {len(uyarilar)} uyarı.")


if __name__ == "__main__":
    main()
