# Yapılandırılmış Veri (JSON-LD)

| Dosya | Nereye | Ne sağlar |
|---|---|---|
| `organizasyon-ve-magaza.json` | **Tüm sayfalar** (sitenin `<head>` bölümü) | Google'a markayı (1960, kurucu, logo, sosyal hesaplar) ve Atrium mağazasını (`Optician` türü: adres, saat, konum) tanıtır. Yerel aramalar, Maps ve bilgi paneli için. |
| `sss-faqpage.json` | **Yalnızca** `/pages/sss` | SSS'deki 16 soru-cevap. Not: Google 2023'ten beri SSS zengin sonucunu yalnızca resmi ve sağlık sitelerinde gösteriyor. Bu kod zengin sonuç için değil, Google'ın ve yapay zekâ asistanlarının (ChatGPT, Gemini, Perplexity) içeriği doğru anlaması içindir. |

## Doldurulacak alanlar (`__...__` ile işaretli)

| Alan | Örnek / açıklama |
|---|---|
| `__ANA_TELEFON__` | Site, schema ve Google Business Profile'da **aynı** olacak ana numara. Şu an iki farklı numara kullanılıyor (0212 529 33 33 ve 0551 212 16 49). |
| `__MAGAZA_TELEFON__` | Mağazanın sabit hattı (ana numarayla aynı olabilir) |
| `__EPOSTA__` | İletişim sayfasındaki adres |
| `__KAT_MAGAZA_NO__`, `__POSTA_KODU__` | Atrium AVM içindeki kat ve mağaza numarası, posta kodu. Google Business Profile'daki adresle birebir aynı olmalı. |
| `__ENLEM__`, `__BOYLAM__` | Google Maps'te mağazaya sağ tık → koordinatlar |
| `__GOOGLE_MAPS_LINKI__` | Business Profile → Paylaş bağlantısı |
| `__FACEBOOK_SAYFA_ADI__` | facebook.com/... kısmı |
| Çalışma saatleri | AVM saatleriyle doğrulayın (taslakta 10:00–22:00 yazıyor) |

## Kurulum (ikas)

1. Alanları doldurun ya da bilgileri bana iletin, dosyaları ben güncelleyeyim.
2. ikas paneli → Tema/Mağaza ayarları → **Özel kod / Head kodu** alanına şu biçimde ekleyin:
   ```html
   <script type="application/ld+json">
   { ...dosyanın içeriği... }
   </script>
   ```
3. ikas'ın kendi `Store` schema'sı (adresi boş olan) da sayfada kalacak. İkisinin çakışmaması için ikas desteğine "varsayılan Store schema'sında adres alanını doldurma veya kapatma" talebi iletin.
4. Doğrulama: https://search.google.com/test/rich-results ve https://validator.schema.org adreslerinde sayfayı test edin.

## Sonraki adım

Kuz İstanbul geçişinde `name`, `logo`, `url` ve `alternateName` alanları güncellenecek. Eski ad "Damla Kuz Optik" `alternateName` içinde korunacak, böylece arama motorları iki markayı aynı işletme olarak tanır.
