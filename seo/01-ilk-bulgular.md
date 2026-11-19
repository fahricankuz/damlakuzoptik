# SEO: İlk Bulgular

Kapsam: Ana sayfa, Hakkımızda, İletişim, Markalarımız, SSS, Güneş Gözlüğü kategorisi, Tom Ford marka sayfası, Tom Ford TF 1182 ürün sayfası, bir blog yazısı, "Sadece Damla Kuz Optik'te" koleksiyonu, robots.txt ve sitemap. Tarih: 19 Kasım 2026.
Altyapı: **ikas** (Next.js tabanlı). Düzeltmelerin çoğu ikas panelindeki SEO alanlarından yapılabilir.

## Genel durum

| Alan | Durum |
|---|---|
| Dil etiketi (`lang="tr"`) | ✅ |
| Canonical | ✅ |
| Open Graph | ✅ |
| robots.txt | ✅ Doğru (sepet, hesap ve ödeme sayfaları kapalı) |
| Sitemap | ✅ 342 ürün, 67 koleksiyon, 12 sayfa, 47 blog |
| Ürün schema (Product, Offer, Brand, Breadcrumb) | ✅ Ürün ve kategori sayfalarında var |
| Görsel alt metinleri | ✅ Ana sayfada 524 görselden yalnızca 1'i eksik |
| Blog | ✅ 47 yazı, düzenli üretim. Güçlü bir temel. |

## Düzeltilmesi gerekenler (öncelik sırasıyla)

| # | Sorun | Etki | Düzeltme |
|---|---|---|---|
| 1 | **Store schema'da adres boş.** `PostalAddress` alanı var ama içi doldurulmamış. | Yerel arama ve Maps görünürlüğü | Tam adres: Ataköy Atrium AVM, mahalle, ilçe, posta kodu, il. Ayrıca `openingHours` ve `geo`. Schema kodunu ben hazırlarım. |
| 2 | **Telefonlar tutarsız.** Schema'da +90 551 212 16 49, İletişim sayfasında 0212 529 33 33. | Google'ın işletme bilgisine güveni (NAP tutarlılığı) | Tek bir ana numara seçilip site, schema ve Google Business Profile'da aynı yazılmalı. |
| 3 | **Marka sayfalarında çok sayıda H1.** Tom Ford sayfasında 21 H1 var; her ürün kartı H1 olarak işaretlenmiş. | Sayfa konusunun bulanıklaşması | ikas temasında ürün kartı başlığı H3 veya div olmalı. Temayı kim kurduysa (ajans ya da ikas) onunla düzeltilir. |
| 4 | **Hakkımızda, İletişim ve SSS aynı title + description'ı kullanıyor.** | Yinelenen içerik sinyali, düşük tıklama oranı | Her sayfaya özgün başlık ve açıklama yazılır (aşağıda öneriler). |
| 5 | **Hakkımızda ve Markalarımız'da H1 yok. Ana sayfa H1'i sadece "GÜNEŞ GÖZLÜĞÜ".** | Zayıf anahtar kelime sinyali | Ana sayfa H1'i: "Orijinal Lüks Güneş Gözlüğü ve Optik Gözlük: 1960'tan Beri Damla Kuz Optik" |
| 6 | **"Güneş Gözlüğü" kategorisinin açıklaması "2025 Yaz Trend Güneş Gözlükleri".** | Güncel değil, en önemli kategori | "Tom Ford, Prada, Miu Miu, Ray-Ban ve 30'dan fazla markanın orijinal güneş gözlükleri. Ücretsiz kargo, 2 yıl garanti, vade farksız taksit." |
| 7 | **Blog açıklamaları başlığın kopyası.** | Tıklama oranı | Her yazıya 140–155 karakterlik özgün açıklama yazılır. |
| 8 | **Yazım hatası:** Footer'da "Blue Protecters" (doğrusu "Blue Protectors"). | Güven algısı | Menüden düzeltilir. |
| 9 | Yapılandırılmış veride `Organization` (logo, sosyal profiller `sameAs`) ve SSS sayfasında `FAQPage` yok. | Zengin sonuç fırsatı | Schema kodları hazırlanacak. |

## Önerilen title ve description'lar

| Sayfa | Title (≤60) | Description (≤155) |
|---|---|---|
| Hakkımızda | Hakkımızda: 1960'tan Beri Fahri Kuz Uzmanlığı \| Damla Kuz Optik | Yenikapı'daki ilk mağazadan bugüne: Türkiye'nin ilk optik zincirinin hikâyesi, optisyen uzmanlığı ve seçkin markalar. |
| İletişim | İletişim ve Mağaza: Ataköy Atrium AVM \| Damla Kuz Optik | Ataköy Atrium AVM mağazamızın adresi, telefon ve çalışma saatleri. Optik gözlük seçimi için randevu alın. |
| SSS | Sıkça Sorulan Sorular: Kargo, İade, Garanti \| Damla Kuz Optik | Sipariş, kargo, iade, orijinallik ve garanti hakkında merak ettikleriniz. Ücretsiz kargo, kolay iade, 2 yıl garanti. |
| Markalarımız | Güneş Gözlüğü Markaları: Tom Ford, Prada, Miu Miu \| Damla Kuz Optik | 30'dan fazla dünya markasının orijinal güneş gözlükleri: Tom Ford, Prada, Miu Miu, Chopard, Maybach, Ray-Ban ve daha fazlası. |

## Sonraki adım

Tam teknik denetim: Core Web Vitals (ana sayfa HTML'i 3 MB, mobil hızı ölçülecek), tüm kategori sayfaları, iç linkleme ve anahtar kelime boşlukları. Bu denetim `seo/02-teknik-denetim.md` dosyasına yazılacak.
