# Format Rehberi: Reklam ve Organik İçerik

Her reklam kreatifi **tek bir ana tasarımdan** tüm formatlara uyarlanır. Kampanyalar bu set eksiksiz hazırlanmadan kurulmaz. Böylece Meta ve Google, her yerleşimde (akış, hikâye, Reels, YouTube, Discover, Gmail) doğru boyutu kullanır, otomatik kırpma olmaz.

## Üretim kuralı

| Ana format | Türetilenler |
|---|---|
| **Video:** 9:16 (1080×1920) | 4:5 (1080×1350), 1:1 (1080×1080), 16:9 (1920×1080) |
| **Görsel:** 4:5 (1080×1350) | 1:1 (1080×1080), 9:16 (1080×1920), 1.91:1 (1200×628) |

Metin ve logo her formatta **güvenli alan** içinde kalır (aşağıda). Videolar sessiz izlenebilir; altyazı her zaman eklenir.

## Meta (Facebook + Instagram) reklamları

| Yerleşim | Oran | Boyut (px) | Not |
|---|---|---|---|
| Akış (Feed) | 4:5 | 1080×1350 | Akışta en çok alan kaplayan format |
| Akış | 1:1 | 1080×1080 | Yedek |
| Reels, Hikâye | 9:16 | 1080×1920 | Reels'te üst ~%14 ve alt ~%35 metinsiz bırakılır (arayüz öğeleri) |
| Sağ sütun, bağlantı | 1.91:1 | 1200×628 | Düşük öncelik |
| Carousel | 1:1 veya 4:5 | 1080×1080 / 1080×1350 | 2–10 kart, her kart ayrı ürün veya mesaj |
| Katalog (dinamik) | feed görselleri | — | Ürün görsellerine marka çerçevesi ve fiyat etiketi eklenir |

**Video süresi:** Reklamda 6–15 sn ideal; ilk 2 saniyede ürün ve kanca. Reels organikte 15–30 sn.
**Metin:** Birincil metin ilk 125 karakterde mesajı vermeli. Başlık ≤ 40 karakter.

## Google reklamları

| Kampanya | Varlık | Oran / boyut | Adet |
|---|---|---|---|
| **Performance Max** | Yatay görsel | 1.91:1 · 1200×628 | 3–5 |
| | Kare görsel | 1:1 · 1200×1200 | 3–5 |
| | Dikey görsel | 4:5 · 960×1200 | 2–3 |
| | Logo | 1:1 · 1200×1200 ve 4:1 · 1200×300 | 1+1 |
| | Video | 16:9, 1:1, 9:16 (≥10 sn) | her orandan 1 |
| | Başlık | ≤ 30 karakter | 3–15 |
| | Uzun başlık | ≤ 90 karakter | 1–5 |
| | Açıklama | 1 adet ≤ 60, diğerleri ≤ 90 karakter | 2–5 |
| **Arama (RSA)** | Başlık | ≤ 30 karakter | 15 |
| | Açıklama | ≤ 90 karakter | 4 |
| | Görsel öğe | 1:1 ve 1.91:1 | 2–4 |
| **Demand Gen / YouTube** | Görsel | 1.91:1, 1:1, 4:5 (ve 9:16) | 3+ |
| | Video | 16:9 (YouTube), 9:16 (Shorts) | 1+ |

> PMax'e video yüklenmezse Google görsellerden otomatik video üretir; kalitesi düşüktür. Her PMax varlık grubuna kendi videomuzu koyacağız.

## Organik sosyal medya

| Platform | Format | Boyut (px) |
|---|---|---|
| Instagram gönderi / carousel | 4:5 (profil ızgarasında 3:4 görünür, kritik öğeler ortada) | 1080×1350 |
| Instagram Reels / Hikâye | 9:16 | 1080×1920 |
| Instagram Reels kapağı | 9:16, ızgarada 3:4 kırpılır | 1080×1920 |
| Facebook gönderi | 4:5 veya 1:1 | 1080×1350 |
| **Facebook kapak (banner)** | Masaüstü ve mobilde farklı kırpılır | 1640×624 tasarım; logo ve metin ortadaki güvenli alanda |
| Facebook / Instagram profil fotoğrafı | 1:1, daire içinde görünür | 1080×1080 |
| Instagram öne çıkan kapakları | 1:1, daire içinde görünür | 1080×1080 (ikon merkezde) |
| YouTube Shorts / TikTok | 9:16 | 1080×1920 |

## API ile neler otomatik, neler elle?

| İş | Otomatik mi? |
|---|---|
| Facebook gönderi, Reels, hikâye paylaşımı | ✅ API ile |
| Instagram gönderi, carousel, Reels, hikâye paylaşımı | ✅ API ile (zamanlanmış görevle, belirlenen saatte) |
| **Facebook kapak fotoğrafı (banner)** | ✅ API ile güncellenebilir (Meta bağlantısı kurulunca ilk iş test edilecek) |
| Facebook profil fotoğrafı | ✅ API ile |
| Instagram profil fotoğrafı, biyografi, öne çıkan kapakları | ❌ API desteklemiyor. Görselleri ve metni hazırlarım, yükleme telefondan ~1 dakika. |
| Reklam kampanyaları, kreatif yükleme | ✅ API ile (duraklatılmış kurulur, onayla açılır) |

## Kuz İstanbul geçiş paketi (Ocak sonu)

Tek seferde hazırlanacak set: Facebook kapak + profil, Instagram profil + 6–8 öne çıkan kapağı, biyografi metni, sabitlenmiş 3 gönderi (lansman), Google Business Profile kapak ve logo, PMax logoları (1:1 ve 4:1), e-posta imzası.
