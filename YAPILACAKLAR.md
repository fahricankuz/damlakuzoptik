# Yapılacaklar: Şirket Tarafı

Sırayla ilerleyin. Bir adım bitmeden sonrakine geçmeyin. Her adımın sonunda **"Bana iletin"** satırındakileri sohbete yazın.
Token, şifre ve API anahtarlarını **asla sohbete yazmayın**. Bunlar için size güvenli bir form açılacak.

Son güncelleme: 19 Kasım 2026

---

## AŞAMA 0: Mevcut ajanstan devir (bu hafta, Black Friday'i bozmadan)

> Mevcut ajans Black Friday kampanyasını (27 Kasım) ve Cyber Monday'i (30 Kasım) yönetirken hesaplarda değişiklik yapmıyoruz. Devir **1 Aralık** itibarıyla başlar. Bu hafta sadece hazırlık yapılır.

- [ ] **0.1 Sahiplik kontrolü.** Aşağıdaki her varlığın **sahibinin kim olduğunu** kontrol edin: Damla Kuz Optik mi, ajans mı?
  - Meta Business Portfolio, Facebook Sayfası, Instagram hesabı, Reklam Hesabı, Pixel (`1032130095734490`)
  - Google Ads, Google Analytics 4 (`G-8BTM6DPJRS`), Google Tag Manager (`GTM-5VJ9GD74`), Merchant Center, Google Business Profile (Atrium AVM)
  - Kontrol yeri: Meta için business.facebook.com → İşletme Ayarları → Hesaplar. Google için her ürünün "Yönetici / Kullanıcı erişimi" ekranı.
  - **Ajansın sahibi olduğu bir varlık varsa**, devir için ajanstan şunu isteyin: varlık Damla Kuz Optik Business Portfolio'suna taşınsın, ajans "partner" olarak kalsın.
- [ ] **0.2 Ajanstan arşiv talebi** (yazılı, e-posta ile):
  - Son 12 ayın Meta ve Google reklam raporları (kampanya bazında harcama, satış, ROAS)
  - Tüm kreatiflerin açık dosyaları (PSD/AI/Figma/Canva bağlantıları), video projeleri
  - Logo ve kurumsal kimlik dosyaları (vektör: SVG/AI/PDF)
  - Kullanılan özel kitleler / benzer kitle tanımları
  - Varsa marka kılavuzu, içerik takvimi, hashtag listeleri
- [ ] **0.3 Sözleşme.** Ajans sözleşmesinin fesih/bildirim süresini kontrol edin. Önerilen geçiş: 1–31 Aralık paralel dönem, ajans erişimi **en son** kaldırılır.
- [ ] **0.4 Yetkili kişi.** Onayları kimin vereceğini belirleyin: içerik onayı ve bütçe onayı (aynı kişi olabilir).

**Bana iletin:** 0.1 sonucu (hangi varlık kimde), onay yetkilisi, ajans fesih tarihi.

---

## AŞAMA 1: Meta (Facebook + Instagram)

- [ ] **1.1** business.facebook.com → İşletme Ayarları'nda şunların **aynı portföyde** olduğunu doğrulayın: Facebook Sayfası, Instagram profesyonel hesabı (Sayfaya bağlı), Reklam Hesabı (ödeme yöntemi tanımlı), Pixel.
- [ ] **1.2 Katalog.** ikas paneli → Satış Kanalları → **Facebook & Instagram** entegrasyonunu açın. Ürünler Meta kataloğuna otomatik aktarılır.
- [ ] **1.3 Alan adı doğrulama.** İşletme Ayarları → Marka Güvenliği → **Alan Adları** → damlakuzoptik.com ekleyin. Verilen meta etiketini ikas panelinden sitenin `<head>` alanına ekleyin ve "Doğrula"ya basın.
- [ ] **1.4 Uygulama.** developers.facebook.com → **My Apps → Create App**.
  - Ad: `Damla Kuz Ajans`
  - Kullanım alanları: *Create & manage ads with Marketing API*, *Manage everything on your Page*, *Manage messaging & content on Instagram*
  - İşletme portföyü: Damla Kuz Optik
- [ ] **1.5 Sistem kullanıcısı.** İşletme Ayarları → Kullanıcılar → **Sistem Kullanıcıları → Ekle**.
  - Ad: `claude-ajans`, rol: **Admin**
  - **Varlık Ata**: Sayfa (tam kontrol), Instagram hesabı (tam), Reklam Hesabı (kampanyaları yönet), Pixel (tam), Katalog (tam)
  - Uygulamalar bölümünden 1.4'teki uygulamayı da bu kullanıcıya atayın.
- [ ] **1.6 Token.** Sistem kullanıcısında **Yeni Token Oluştur**.
  - Uygulama: `Damla Kuz Ajans`, süre: **Asla sona ermez**
  - İzinler: `ads_management`, `ads_read`, `business_management`, `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`, `pages_manage_engagement`, `pages_manage_metadata`, `read_insights`, `instagram_basic`, `instagram_content_publish`, `instagram_manage_comments`, `instagram_manage_insights`, `catalog_management`
  - Token'ı bir yere **kopyalamayın, sohbete yazmayın.** Sohbete "Meta token hazır" yazın, size güvenli form açılacak.

**Bana iletin:** Business ID, Reklam Hesabı ID (`act_` ile başlar), Sayfa ID, Instagram hesap ID, Katalog ID. Hepsi İşletme Ayarları'nda ilgili varlığın üzerine tıklayınca görünür.

---

## AŞAMA 2: Google (Ads + Merchant Center + Business Profile)

- [ ] **2.1 GA4 ↔ Google Ads bağlantısı.** GA4 → Yönetici → Ürün Bağlantıları → Google Ads bağlantıları → hesabı bağlayın. Ardından Google Ads → Hedefler → Dönüşümler → **İçe aktar → GA4 → `purchase`**.
- [ ] **2.2 Merchant Center.** ikas paneli → Satış Kanalları → **Google** entegrasyonunu açın. Ürün feed'i Merchant Center'a gider. Merchant Center'da damlakuzoptik.com'u **doğrulayıp sahiplenin**, sonra Google Ads hesabına bağlayın.
- [ ] **2.3 Google Business Profile.** Ataköy Atrium AVM mağazasının profilinin sizin hesabınızda olduğunu doğrulayın. Profilde telefon, saat ve fotoğraflar güncel olsun. Google Ads → Öğeler → **Konum öğesi** ile profili bağlayın.
- [ ] **2.4 Reklam yönetim bağlantısı.** Google Ads'i Claude'a bağlamak için claude.ai → Ayarlar → Bağlayıcılar (Connectors) bölümünden **Adspirer Search Ads** veya **Windsor.ai for Paid Media**'yı ekleyin ve Google hesabınızla yetkilendirin. Ücretlendirmesini ve gizlilik koşullarını kontrol edip birini seçin.

**Bana iletin:** Google Ads müşteri numarası (xxx-xxx-xxxx), Merchant Center ID, hangi bağlayıcıyı seçtiğiniz.

---

## AŞAMA 3: ElevenLabs

- [ ] **3.1** elevenlabs.io → Profil → **API Keys → Create API Key**. İzinler: Text to Speech, Sound Effects, Music, Voices (okuma).
- [ ] **3.2** Sohbete "ElevenLabs anahtarı hazır" yazın, güvenli form açılacak.
- [ ] **3.3** Kullanmak istediğiniz seslerin **Voice ID**'lerini ve adlarını iletin. Bunlar gizli değildir. Marka sesi olarak klonlanmış bir ses varsa onu belirtin.

---

## AŞAMA 4: İçerik materyalleri

Bunları Google Drive'da bir klasöre koyup klasör bağlantısını iletin.

- [ ] **4.1** Logo: vektör (SVG/AI/PDF), beyaz ve siyah versiyon
- [ ] **4.2** Ürün fotoğrafları: yüksek çözünürlük, mümkünse model üzerinde çekimler
- [ ] **4.3** Mağaza, ekip ve optisyen çalışma anlarından fotoğraf ve video (telefon çekimi yeterli, dikey 9:16 tercih)
- [ ] **4.4** **Arşiv:** 1960'lardan bu yana Fahri Kuz, Yenikapı ilk mağaza, eski reklamlar, gazete kupürleri. Marka mirası içeriklerinin en değerli kaynağı budur.
- [ ] **4.5** **Kuz İstanbul** rebranding dosyaları: logo taslakları, renkler, fontlar, ajans sunumu (hazır olduğunda)

---

## AŞAMA 5: Onay rutini

- [ ] **5.1** Haftalık içerik planı **pazartesi** gönderilir. Onay için **salı 17:00**'ye kadar yanıt verilir.
- [ ] **5.2** Reklam kampanyaları duraklatılmış kurulur, özet gönderilir. Onay mesajı ("onaylıyorum, yayına al") gelmeden açılmaz.
- [ ] **5.3** Haftalık performans raporu her **pazartesi** sabah gönderilir. Aylık rapor her ayın ilk iş günü gönderilir.
