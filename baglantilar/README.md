# Bağlantılar: Teknik Notlar

Şirket tarafının yapacağı adımlar `../YAPILACAKLAR.md` dosyasındadır (Aşama 1–3). Bu dosya, bağlantıların nasıl çalıştığını ve sınırlarını açıklar.

## Güvenlik modeli

- Token ve API anahtarları **sohbete veya repoya yazılmaz.** Bunlar güvenli kimlik bilgisi formuyla, çalışma ortamının ağ katmanında saklanır.
- Anahtar yalnızca ilgili sunucuya giden isteklere otomatik eklenir: Meta için `graph.facebook.com`, ElevenLabs bağlayıcısı ise kendi yetkilendirmesini kullanır. Claude anahtarın değerini hiçbir zaman görmez.
- Anahtar iptal edilmek istenirse: Meta'da sistem kullanıcısının token'ı İşletme Ayarları'ndan iptal edilir; ElevenLabs bağlantısı claude.ai → Ayarlar → Bağlayıcılar bölümünden kaldırılır.

## Meta (doğrudan Graph / Marketing API)

| Konu | Not |
|---|---|
| Yöntem | Sistem kullanıcısı token'ı (süresiz) |
| Facebook paylaşımı | API ile ileri tarihli planlanabilir |
| Instagram paylaşımı | API ileri tarih desteklemez. Paylaşım, zamanlanmış görevle belirlenen saatte yapılır. Görsel ve videonun herkese açık bir URL'de bulunması gerekir (Canva dışa aktarma bağlantısı veya ikas CDN). |
| Instagram müzik | API'den Instagram müzik kütüphanesi eklenemez. ElevenLabs müzik veya telifsiz müzik kullanılır. |
| Reklamlar | Kampanya, reklam seti ve reklam her zaman **PAUSED** (duraklatılmış) oluşturulur. Yayına alma yazılı onayla yapılır. |
| Raporlama | Insights API: harcama, ROAS, CPA, erişim, kreatif bazında performans |
| Gerekli ek ağ izinleri | `graph.facebook.com`, `graph-video.facebook.com` (video yükleme), `rupload.facebook.com` (Reels yükleme) |

## Google Ads (bağlayıcı üzerinden)

| Konu | Not |
|---|---|
| Neden bağlayıcı | Google Ads API'nin developer token'ı onaya tabi ve başta yalnızca test hesaplarında çalışır. Ayrıca OAuth erişim anahtarı saatlik yenilenir; sabit anahtar yöntemi bunu desteklemez. |
| Seçenekler | **Adspirer Search Ads** (Google + Bing arama) veya **Windsor.ai for Paid Media** (Google + Meta + diğerleri). İkisi de üçüncü taraf ve ücretli olabilir. |
| Alternatif | İleride gerekirse doğrudan API: MCC hesabı → developer token başvurusu (Basic Access) → Google Cloud OAuth istemcisi. |
| Hazırlık | GA4 ↔ Ads bağlantısı, `purchase` dönüşümü, Merchant Center + ikas feed'i, Business Profile konum öğesi |

## ElevenLabs (bağlayıcı üzerinden)

| Konu | Not |
|---|---|
| Yöntem | claude.ai ElevenLabs bağlayıcısı (20 Kasım 2026'da bağlandı ve doğrulandı). API anahtarı gerekmez. |
| Plan | Creator: aylık 131.000 karakter, 30 ses yuvası |
| Kullanım | Türkçe seslendirme (TTS), ses efektleri, müzik, ses tasarımı, ses kaydını yazıya çevirme (altyazı), görsel/video üretimi ve sesli asistan |
| Çıktı | `icerik/ses/` klasörüne kaydedilir (büyük dosyalar Drive'da). Üretimler ayrıca ElevenLabs'taki "flow" sayfasında da durur. |
| Maliyet | Her üretim kredi harcar. Metin ve ses önce kullanıcıya sunulur, onayla üretilir. |
| Sınır | Fahri Kuz'un sesi klonlanmaz veya taklit edilmez; yalnızca anlatıcı sesi, müzik ve efekt. |
