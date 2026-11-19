# Damla Kuz Optik: İletişim, Sosyal Medya ve Performans Pazarlaması

Bu repo, Damla Kuz Optik'in (Ocak 2027 sonundan itibaren **Kuz İstanbul**) sosyal medya, içerik ve reklam yönetiminin tek merkezidir. Mevcut ajans hizmetinin yerini alacak şekilde yapılandırılmıştır.

## Çalışma kuralları

1. **Gizli bilgi yok.** Token, API anahtarı ve şifre bu repoya asla yazılmaz. Erişimler güvenli kimlik bilgisi formu ile ortam düzeyinde saklanır.
2. **Para harcatan her adım onaylıdır.** Kampanyalar her zaman *duraklatılmış* kurulur. Yayına alma, bütçe artışı ve yeni kampanya yalnızca yazılı onayla yapılır.
3. **Şirket ayrımı.** Hostinger hesabı ve "Anahtar için Anahtar" ayrı bir şirkettir. Bu repoda ve bu işte kullanılmaz.
4. **Sahiplik şirkette kalır.** Tüm reklam hesapları, pikseller, kataloglar ve sayfalar Damla Kuz Optik'in kendi Business Portfolio / Google hesaplarında durur. Ajans ya da üçüncü taraflar yalnızca "partner" erişimi alır.
5. **Rebranding.** Ocak 2027 sonunda **Kuz İstanbul**'a geçilecek. Aralık–Ocak döneminde üretilen her şablon, yeni marka kimliğine kolayca uyarlanabilecek biçimde kurulur.

## Klasörler

| Klasör | İçerik |
|---|---|
| `YAPILACAKLAR.md` | Şirket tarafının sırayla yapacağı adımlar (canlı kontrol listesi) |
| `marka/` | Marka analizi, renk/font değerleri, ton kılavuzu, rebranding notları |
| `strateji/` | İletişim stratejisi, içerik ayakları, bütçe dağılımı, KPI'lar |
| `rakip-analizi/` | Rakip karşılaştırmaları ve fırsat alanları |
| `seo/` | SEO denetimleri ve düzeltme listeleri |
| `baglantilar/` | Meta, Google Ads ve ElevenLabs kurulum rehberleri |
| `takvim/` | Aylık ve haftalık içerik takvimleri |
| `icerik/` | Görsel, video ve ses çıktıları, metinler |
| `reklam/` | Kampanya planları, reklam metinleri, test kayıtları |
| `raporlar/` | Haftalık ve aylık performans raporları |

## Skill'ler (video, hareket ve tasarım)

`.claude/skills/` klasöründe 37 skill kuruludur: HyperFrames, motion-design, GSAP, Three.js, design-dna, cast/paint/bunshin, brag-slim, find-skills. Repo bir Claude oturumuna bağlandığında **otomatik yüklenir**; her oturumda yeniden kurmaya gerek yoktur. Sürümler `skills-lock.json` dosyasında tutulur. Güncelleme komutu: `npx skills update -p`.

Gerekli araçlar (bulut ortamında hazır): Node 18+, ffmpeg, Playwright + Chromium, Python (numpy, Pillow).

> Başka projelere ait sahne şablonları, marka varlıkları ve render betikleri (ör. "Anahtar için Anahtar" işleri) bu repoya **alınmaz**. Damla Kuz / Kuz İstanbul şablonları burada sıfırdan, bu markanın kimliğiyle kurulur.

## Hesap kimlikleri (gizli değildir)

| Varlık | Kimlik |
|---|---|
| Meta Pixel | `1032130095734490` |
| Google Analytics 4 | `G-8BTM6DPJRS` |
| Google Tag Manager | `GTM-5VJ9GD74` |
| Meta Conversion API | ikas üzerinden açık (sunucu tarafı). Token yalnızca ikas panelinde. |
| GA4 Measurement Protocol | ikas üzerinden açık. Gizli anahtar yalnızca ikas panelinde. |
| Ürün feed'leri | ikas paneli → Satış Kanalları (Google XML, Meta CSV). Denetim: `reklam/feed-denetimi.md` |
| Meta Business ID | _bekleniyor_ |
| Meta Reklam Hesabı | _bekleniyor_ |
| Facebook Sayfa ID | _bekleniyor_ |
| Instagram hesap ID | _bekleniyor_ |
| Meta Katalog ID | _bekleniyor_ |
| Google Ads müşteri no | _bekleniyor_ |
| Merchant Center ID | _bekleniyor_ |
