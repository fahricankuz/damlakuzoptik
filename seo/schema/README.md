# Yapılandırılmış Veri (JSON-LD)

| Dosya | Nereye | Ne sağlar |
|---|---|---|
| `organizasyon-ve-magaza.json` | **Tüm sayfalar** (sitenin `<head>` bölümü) | Google'a markayı (1960, kurucu, logo, sosyal hesaplar) ve Atrium mağazasını (`Optician` türü: adres, saat, konum) tanıtır. Yerel aramalar, Maps ve bilgi paneli için. |
| `sss-faqpage.json` | **Yalnızca** `/pages/sss` | SSS'deki 16 soru-cevap. Not: Google 2023'ten beri SSS zengin sonucunu yalnızca resmi ve sağlık sitelerinde gösteriyor. Bu kod zengin sonuç için değil, Google'ın ve yapay zekâ asistanlarının (ChatGPT, Gemini, Perplexity) içeriği doğru anlaması içindir. |

## Kullanılan bilgiler (20 Kasım 2026, şirketten)

| Alan | Değer |
|---|---|
| Ana telefon | 0 212 529 33 33 (site, schema ve Google Business Profile'da **tek numara** bu olmalı) |
| Adres | Ataköy Atrium AVM, Zemin Kat, Ana Giriş, 34158 Bakırköy / İstanbul |
| Saatler | Her gün 09:00–22:00 |
| E-posta | info@damlakuzoptik.com (İletişim sayfasından) |
| Google Maps | https://share.google/CkJ2tgsbVcgiOh8KV |
| Facebook | facebook.com/damlakuzoptic.by.fahrikuz |

Koordinat (`geo`) bilinçli olarak eklenmedi; Google adres ve Maps bağlantısından konumu çıkarır. **Yapılacak:** İkas'taki varsayılan `Store` schema'sında görünen 0551 212 16 49 numarası ikas mağaza ayarlarından 0 212 529 33 33 olarak değiştirilmeli.

## Kurulum (ikas)

1. ikas paneli → Tema/Mağaza ayarları → **Özel kod / Head kodu** alanına şu biçimde ekleyin:
   ```html
   <script type="application/ld+json">
   { ...dosyanın içeriği... }
   </script>
   ```
2. ikas'ın kendi `Store` schema'sı (adresi boş olan) da sayfada kalacak. İkisinin çakışmaması için ikas desteğine "varsayılan Store schema'sında adres alanını doldurma veya kapatma" talebi iletin.
3. Doğrulama: https://search.google.com/test/rich-results ve https://validator.schema.org adreslerinde sayfayı test edin.

## Sonraki adım

Kuz İstanbul geçişinde `name`, `logo`, `url` ve `alternateName` alanları güncellenecek. Eski ad "Damla Kuz Optik" `alternateName` içinde korunacak, böylece arama motorları iki markayı aynı işletme olarak tanır.
