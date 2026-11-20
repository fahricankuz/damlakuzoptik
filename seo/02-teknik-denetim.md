# SEO: Teknik Denetim (hız ve sayfa ağırlığı)

Tarih: 20 Kasım 2026. Mobil tarayıcı kimliğiyle ölçüldü.

> **Google PageSpeed Insights ölçümü yapılamadı.** Anahtarsız kullanımın ortak günlük kotası dolu (19 ve 20 Kasım'da HTTP 429). Gerçek kullanıcı verisi (Core Web Vitals) için ücretsiz bir PageSpeed API anahtarı gerekiyor. Anahtar gelince bu bölüm tamamlanacak. Aşağıdaki ölçümler doğrudan sayfa kaynağından alınmıştır.

## Ölçümler

| Sayfa | İlk bayt süresi (TTFB) | HTML (sıkıştırılmış) | HTML (açık) | Gömülü sayfa verisi | Görsel | Geç yüklenen görsel |
|---|---|---|---|---|---|---|
| Ana sayfa | 0,79 sn | 379 KB | **2,97 MB** | **1,8 MB** | **524** | 260 |
| /gunes-gozlugu | **2,71 sn** | 328 KB | **2,02 MB** | 1,55 MB | 132 | 64 |
| Ürün (Tom Ford TF 1182) | **2,75 sn** | 121 KB | 729 KB | 487 KB | 54 | 25 |
| Blog yazısı | 1,59 sn | 106 KB | 570 KB | 408 KB | 10 | 3 |

İyi bir e-ticaret sayfasında ilk bayt süresi 0,8 saniyenin, sıkıştırılmış HTML 100 KB'ın altında olmalıdır.

## Bulgular

| # | Sorun | Etki | Öneri | Kim |
|---|---|---|---|---|
| 1 | **Ana sayfa HTML'i ~3 MB**; bunun 1,8 MB'ı sayfaya gömülü ürün verisi. Ana sayfada 524 görsel var. | Mobilde yavaş açılış, düşük Google puanı, reklam tıklamalarında kayıp ziyaretçi | Ana sayfadaki ürün vitrinlerini azaltmak (her vitrinde 8–12 ürün), tekrar eden blokları kaldırmak | Tema düzenleyen (ajans veya ikas) |
| 2 | **Kategori ve ürün sayfalarında ilk bayt süresi ~2,7 sn** | Hem SEO hem reklam açılış sayfası deneyimi | ikas önbelleği / sunucu tarafı; ikas desteğine bildirilmeli | ikas desteği |
| 3 | Görsellerin yaklaşık yarısı geç yüklenmiyor (ana sayfada 264 görsel ilk açılışta isteniyor) | Gereksiz veri, yavaş ilk görüntü | Ekranın altında kalan tüm görsellerde geç yükleme (lazy loading) | Tema |
| 4 | İlk görünen büyük görsel (LCP) için ön yükleme yok | En büyük içeriğin geç görünmesi | Ana banner görseline ön yükleme (preload) | Tema |
| 5 | **WhatsApp takip betiği iki kez yükleniyor** (ikaswhatsapp.creato.digital) | Gereksiz yük, olası çift olay kaydı | Bir kopyası kaldırılmalı | Entegrasyonu kuran |
| 6 | Harici arama betiği (backend-production-cc4b.up.railway.app/arama.js) | Dış sunucuya bağımlılık; yavaşlarsa site de yavaşlar | Kime ait olduğu (Kuz AI mı?) ve sözleşmesi netleşmeli | Şirket |

## Önceki bulgularla birlikte öncelik sırası

1. Ana sayfa ağırlığı (madde 1) ve ilk bayt süresi (madde 2): reklam trafiğinin kalitesini doğrudan etkiler.
2. Schema kurulumu (`seo/schema/`): hazır.
3. Başlık, açıklama ve H1 düzeltmeleri (`seo/01-ilk-bulgular.md`).
4. Görsel geç yükleme ve ön yükleme (madde 3–4).
5. Yinelenen betik (madde 5).

## Kuz İstanbul geçişi

Alan adı değişecekse geçişten önce bu hız sorunlarının çözülmesi, yeni alan adında temiz bir başlangıç sağlar. Geçiş planı (301 yönlendirme haritası, Search Console adres değişikliği, sitemap) ayrı bir belge olarak hazırlanacak.
