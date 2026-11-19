# Ürün Feed Denetimi (Google + Meta)

Tarih: 19 Kasım 2026. Kaynak: ikas'ın ürettiği Google (XML) ve Meta (CSV) feed'leri. Feed bağlantıları ikas panelinde. Herkese açık paylaşılmaması için repoya yazılmadı.

## Özet

| | Google feed | Meta feed |
|---|---|---|
| Ürün (varyant) | 514 | 514 |
| Ürün grubu | yok (`item_group_id` eksik) | 342 |
| Stokta / stok dışı | 418 / 96 | 418 / 96 |
| İndirimli | 509 (470'i %30, 38'i %46–47) | aynı |
| Fiyat (indirimli medyan) | 9.450 TL · en yüksek 54.247 TL | aynı |
| Marka sayısı | 33 (en çok: Ray-Ban 71, Tom Ford 59, Chopard 46, Löla 36, Vogue 35) | aynı |

Ölçüm altyapısı iyi durumda. ikas üzerinden **Meta Conversion API** (sunucu tarafı) ve **GA4 Measurement Protocol** zaten açık. Tarayıcı engellerine rağmen satın almalar Meta'ya ve GA4'e iletiliyor.

## Kritik sorunlar

| # | Sorun | Etki | Çözüm | Kim |
|---|---|---|---|---|
| 1 | **"deneme" adlı test ürünü 2,06 TL'ye satışta**, stokta 91 adet. damlakuzoptik.com/deneme adresinden satın alınabiliyor ve reklam feed'lerinde de var. | Gerçek sipariş riski, reklamda görünme riski, güven kaybı | ikas'ta ürünü **silin** veya yayından kaldırın | Şirket, **hemen** |
| 2 | **"Kargo" ürün olarak feed'de** (1,03 TL) | Shopping reklamında 1 TL'lik "ürün" | ikas'ta bu ürünü satış kanallarından (Google, Meta) çıkarın | Şirket |
| 3 | **Google feed'de başlıklar zayıf:** "714 - Siyah", "AR 8211", "SZ3001". Ortalama 25 karakter, marka ve "güneş gözlüğü" ifadesi yok. | Shopping/PMax'te ürün aramalarla eşleşmez. **En büyük performans kaybı burada.** | Ek feed ile düzeltildi: "Persol PER 8002S Erkek Güneş Gözlüğü - Siyah" | Claude, hazır |
| 4 | **GTIN (barkod) hatalı.** Meta feed'deki `gtin` alanında barkod yerine ürün kodu var ("gunes-gozlugu-Persol-1013-S-Z-1149/58"); 511 değerin hiçbiri geçerli barkod değil. Google feed'de GTIN hiç yok. | Google, markalı ürünlerde GTIN ister; yoksa görünürlük düşer. Meta geçersiz GTIN'i hata olarak işaretler. | Gerçek **EAN-13 barkodları** (kutu etiketinde ya da distribütör faturasında yazan 13 haneli numara) ikas'ta ürünlerin **barkod** alanına girilmeli. Kısa vadede: ikas'taki o alan boşaltılmalı. | Şirket (distribütör listesiyle) |
| 5 | Google feed'de **renk, cinsiyet, yaş grubu, varyant grubu** yok | Filtreli aramalarda (ör. "kadın güneş gözlüğü") görünmeme | Ek feed ile eklendi | Claude, hazır |
| 6 | Meta feed'de renk, cinsiyet ve beden yok | Dinamik reklamlarda filtreleme ve kitle eşleşmesi zayıf | Meta katalogda ek veri kaynağı olarak aynı dosya kullanılacak (Meta bağlantısından sonra) | Claude |
| 7 | Google feed'de 2 üründe görsel, 3 üründe açıklama, 5 üründe marka eksik | O ürünler reddedilir | ikas'ta tamamlanmalı (liste aşağıdaki çıktıda) | Şirket |
| 8 | Görseller WebP formatında | Google destekliyor. Meta katalog kabul etmezse JPG'ye çevrilecek. | Meta bağlanınca katalog teşhis ekranından kontrol edilecek | Claude |

## Ek feed: Merchant Center'a yükleme

Dosya: `reklam/google/merchant-ek-feed.tsv`. 512 ürün; alanlar: `id`, `title`, `item_group_id`, `color`, `gender`, `age_group`.

1. Merchant Center → **Ürünler → Veri kaynakları → Ek kaynak ekle** (Add supplementary source)
2. Yöntem: **Dosya yükle**. `merchant-ek-feed.tsv` dosyasını seçin.
3. Bağlanacak birincil kaynak: ikas Google feed'i
4. İşlem 30–60 dakika sürer. Sonra Ürünler → Tüm ürünler'de başlıklar yeni hâliyle görünür.

> Ürün eklendikçe veya değiştikçe dosya yeniden üretilmeli. Komut: `python3 araclar/ek_feed_olustur.py <meta_feed.csv> reklam/google/merchant-ek-feed.tsv`. Bu işi haftalık rutine ekliyorum. Kalıcı çözüm: ikas'ın Google feed'ine bu alanları ekletmek (ikas destek talebi).

## Fiyat ve indirim notu

Ürünlerin %92'si sürekli "%30 indirimli" görünüyor. Bu üç soruna yol açar:

- **Yasal:** Ticaret Bakanlığı'nın haksız ticari uygulamalar ve indirimli satış düzenlemesine göre indirimden önceki fiyat, son 30 gün içindeki en düşük fiyat olmalıdır. Sürekli indirim bu kurala aykırı sayılabilir; hukuk ya da mali müşavir görüşü alınmalı.
- **Google:** İndirimli fiyat (`sale_price`) çok uzun süre sabit kalırsa Google "indirim" rozetini göstermeyebilir.
- **Marka:** Kalıcı indirim, lüks ve "uzmanlık" konumlandırmasını zayıflatır.

**Öneri:** Black Friday sonrası (1 Aralık) liste fiyatlarını gerçek satış fiyatına çekmek ve indirimi yalnızca dönemsel kampanyalarda (yılbaşı, sevgililer günü, yaz sonu) kullanmak. Kuz İstanbul geçişi bunun için doğal bir an.
