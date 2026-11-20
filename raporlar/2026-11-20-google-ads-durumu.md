# Google Ads Başlangıç Durumu

Tarih: 20 Kasım 2026. Kaynak: Adspirer bağlayıcısı (Google Ads API), yalnızca okuma. Hiçbir ayar değiştirilmedi.
Hesap: **Damla Kuz Optik İkas** `919-709-9903` (aktif). Eski hesap: `405-297-4129` "Damla Kuz Optik" (bağlayıcıda etkin değil).

> **Kapsam:** Bağlayıcı 9 Ağustos – 19 Kasım 2026 dönemini veriyor (~3,5 ay). Daha eski dönem için Google Ads panelinden rapor dışa aktarımı gerekiyor. Kampanya adları Temmuz 2025'ten beri Google'da harcama olduğunu gösteriyor.
> **Kota:** Bağlayıcı planında ayda 15 işlem hakkı var; 20 Kasım'da 2'si kullanıldı.

## 1. Özet (9 Ağustos – 19 Kasım 2026)

| Gösterge | Değer |
|---|---|
| Harcama | **46.920 TL** (ayda ~11–13,5 bin TL) |
| Tıklama / gösterim | 5.310 / 467.375 (tıklama oranı %1,14) |
| Ortalama tıklama maliyeti | 8,84 TL |
| Google'ın saydığı satış | **3** |
| ROAS (Google'ın ölçümü) | **0,37** |
| Satış başı maliyet | 15.640 TL |

## 2. Kampanyalar

| Kampanya | Tür | Harcama | Satış | ROAS | Not |
|---|---|---|---|---|---|
| All Placement PMax (Kas 2025'ten beri) | Performance Max | 23.852 TL | 2 | 0,42 | Bütçe yüzünden gösterim kaybı %19 |
| Ray-Ban & Vogue PMax (Mar 2026'dan beri) | Performance Max | 13.743 TL | 1 | 0,53 | Fiyat rekabetinin en yoğun olduğu markalar |
| Marka araması (Tem 2025'ten beri) | Arama | 8.096 TL | **0** | 0 | Tıklama oranı %15, gösterim payı %92 |
| Güneş gözlüğü araması | Arama | 1.229 TL | 0 | 0 | "güneş gözlüğü" kalite puanı 3/10 |

Marka araması anahtar kelimeleri: "fahri kuz optik" 2.328 TL, "fahri kuz" 2.150 TL, "damla kuz optik" 1.828 TL, "damla kuz" 871 TL; hepsinde 0 satış.

## 3. Dönüşüm ölçümü: kritik sorun

Denetim notu: **C (73/100)**.
- Tek birincil dönüşüm (`purchase`) tanımlı, ama **son 7 günde hiç dönüşüm kaydetmemiş**. Ağustos'tan bu yana yalnızca 3 satış kaydı var.
- Markanızı arayıp tıklayan kişiler (8.096 TL, tıklama oranı %15) normalde en çok satın alan kitledir. Bunlardan 0 satış kaydedilmesi, büyük olasılıkla **satın alma ölçümünün bozuk ya da eksik** olduğunu gösterir.
- Sonuç: Performance Max kampanyaları neredeyse hiç satış sinyali almadan, yani körlemesine teklif veriyor.
- Gelişmiş dönüşümlerin (enhanced conversions) açık olup olmadığı API'den doğrulanamadı.

**Doğrulama (şirket veya Claude, talimatla):** Google Ads → Hedefler → Dönüşümler → `purchase` satırında durum "Dönüşüm kaydediliyor" mu? Etiketin kaynağı GA4 içe aktarımı mı, Google Ads etiketi mi? Tag Assistant ile bir test siparişinde etiket tetikleniyor mu?

## 4. Meta + Google birlikte (Ağustos – Kasım 2026)

| | Tutar |
|---|---|
| Meta harcaması | 71.295 TL |
| Google harcaması (9 Ağu'dan itibaren) | 46.920 TL |
| **Toplam reklam harcaması** | **118.215 TL** |
| ikas net online ciro (14 Kasım'a kadar) | 70.914 TL |
| **Net ciro / toplam reklam** | **0,60** |

Son dört ayda reklama harcanan her 1 TL'ye karşılık 0,60 TL net online ciro gelmiş. Ürün maliyeti düşülmeden bile zarar.

## 5. Öneriler (uygulama talimatla)

| # | Öneri | Neden |
|---|---|---|
| 1 | **Satın alma dönüşümünü onarmak** (GA4 içe aktarımı veya Google Ads etiketi + gelişmiş dönüşümler; ikas Google entegrasyonu kontrolü) | Ölçüm olmadan PMax öğrenemez; diğer her optimizasyonun önkoşulu |
| 2 | Marka aramasının bütçesini ve kelimelerini gözden geçirmek: tam eşleme, negatif kelimeler, tıklama başı tavan | 8 bin TL; marka koruma için gerekenden fazla olabilir |
| 3 | Ray-Ban & Vogue PMax'i yeniden yapılandırmak: düşük öncelik veya üst lüks markalarla değiştirmek | En yoğun fiyat rekabeti; ROAS 0,53 |
| 4 | Merchant Center ek feed'ini yüklemek (başlık, renk, cinsiyet) | PMax'in ürün eşleşmesi |
| 5 | Ölçüm onarıldıktan sonra 2–3 hafta veri toplamak, ardından kampanya planı G1–G4'e geçiş | Plan, sunum Bölüm 6 |
| 6 | Eski Google Ads hesabının (405-297-4129) durumunu kontrol etmek | Açık bakiye veya aktif harcama olmamalı |

## 6. Dönüşüm ekranı incelemesi (20 Kasım, şirketin ekran görüntüsü)

| Dönüşüm | Kaynak | Durum | Rol | Not |
|---|---|---|---|---|
| **purchase** | Web sitesi (Google Ads etiketi) | ❌ **Hatalı yapılandırılmış** | **Birincil** (teklif buna göre veriliyor) | 0 dönüşüm |
| add_to_cart | Web sitesi | ✅ Etkin | İkincil | 2 dönüşüm |
| view_item, view_item_list | Web sitesi | ✅ Etkin | İkincil | Sayfa görüntüleme olayları çalışıyor |
| begin_checkout, view_cart, remove_from_cart | Web sitesi | ⏳ Dönüşümler bekleniyor | İkincil | Hiç veri yok |
| add_shipping_info, add_payment_info | Web sitesi | ❌ Hatalı yapılandırılmış | İkincil | |
| Yol tarifi, tıklayarak arama, web sitesi ziyareti, diğer yerel işlemler, mağaza ziyaretleri | Google | ❌ **Kaldırıldı** | Birincil | Mağaza yönlendirmesi ölçülmüyor |

**Teşhis:** Ürün ve liste sayfalarındaki etiket çalışıyor, ama **ödeme ve satın alma adımlarında etiket çalışmıyor**. En olası neden ikas'ın ödeme sayfalarında Google Ads etiketinin tetiklenmemesi veya satın alma olayının gerekli bilgileri (tutar, para birimi, sipariş no) taşımaması. Mağaza işlemleri (yol tarifi, arama) ise tamamen kaldırılmış; Business Profile bağlantısı kopmuş olabilir.

**Önerilen onarım (uygulama talimatla; Black Friday/Cyber Monday sonrası, 1 Aralık önerilir):**
1. GA4'te satın almaların kaydedildiğini doğrulamak (ikas, Measurement Protocol ile sunucu tarafından GA4'e satın alma gönderiyor). GA4 → Raporlar → Para kazanma → E-ticaret satın alımları.
2. Google Ads'e **GA4 `purchase` olayını içe aktarmak** ve birincil dönüşüm yapmak. Sunucu tarafı veri olduğu için tarayıcı ve ödeme sayfası sorunlarından etkilenmez.
3. Hatalı `purchase` (web sitesi) dönüşümünü **silmeden ikincile almak** (çift sayımı önler, geçmiş korunur).
4. Gelişmiş dönüşümleri (enhanced conversions) açmak.
5. Google Ads ↔ Business Profile bağlantısını yeniden kurup **yol tarifi ve arama** dönüşümlerini geri açmak (mağaza hedefi için şart).
6. ikas desteğine sormak: Google Ads entegrasyonunun ödeme ve teşekkür sayfasında etiketi tetikleyip tetiklemediği.

Not: Birincil dönüşümün değişmesi Performance Max'te öğrenme sürecini yeniden başlatır. Bu yüzden Black Friday dönemi bitince yapılması önerilir. Şu an kampanyalar zaten neredeyse hiç satış sinyali almıyor, bu yüzden değişiklik büyük olasılıkla olumlu etki eder.
