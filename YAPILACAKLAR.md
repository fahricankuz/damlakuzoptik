# Yapılacaklar: Şirket Tarafı

Sırayla ilerleyin. Bir adım bitmeden sonrakine geçmeyin. Her adımın sonunda **"Bana iletin"** satırındakileri sohbete yazın.
Token, şifre ve API anahtarlarını **asla sohbete yazmayın**. Bunlar için size güvenli bir form açılacak.

Son güncelleme: 19 Kasım 2026

---

## ACİL (bugün)

- [~] **A.1 Test ürününü kaldırın.** _(19 Kas: satış kanallarından kaldırıldı. Feed ikas tarafında güncellenince Claude kontrol edecek. Sitedeki /deneme sayfası hâlâ açık; web mağazası kanalından da kaldırılmalı.)_ ikas'taki **"deneme"** adlı ürün 2,06 TL fiyatla satışta ve stokta görünüyor: damlakuzoptik.com/deneme. Ürünü silin veya yayından kaldırın.
- [~] **A.2 "Kargo" ürününü feed'den çıkarın.** _(19 Kas: kaldırıldı, feed güncellemesi bekleniyor.)_ 1,03 TL'lik "Kargo" ürünü Google ve Meta feed'lerinde var. ikas'ta bu ürünün Google ve Facebook satış kanallarındaki işaretini kaldırın.
- [ ] **A.3 Telefon tutarlılığı.** ikas → Mağaza ayarlarındaki iletişim telefonunu **0 212 529 33 33** yapın. Şu an sitenin arka planda Google'a gönderdiği kodda 0551 212 16 49 görünüyor.

---

## AŞAMA 0: Mevcut ajanstan devir (bu hafta, Black Friday'i bozmadan)

> Mevcut ajans Black Friday kampanyasını (27 Kasım) ve Cyber Monday'i (30 Kasım) yönetirken hesaplarda değişiklik yapmıyoruz. Devir tarihi **şirket sahibinin talimatıyla** belirlenecek; o güne kadar Claude hiçbir kampanyaya dokunmaz, yalnızca veri okur.

- [~] **0.1 Sahiplik kontrolü.** _(19 Kas durumu)_
  | Varlık | Durum |
  |---|---|
  | Facebook Sayfası | ✅ Bizde |
  | Instagram | ✅ Bizde |
  | Reklam hesabı | ✅ Sahibi DamlaKuzOptik (API ile doğrulandı) |
  | Pixel `1032130095734490` | ✅ Sahibi DamlaKuzOptik (API ile doğrulandı) |
  | Ürün kataloğu | ✅ Sahibi DamlaKuzOptik, 512 ürün (API ile doğrulandı) |
  | Google Tag Manager | ✅ Yönetici şirkette |
  | Google Business Profile | ✅ Bizde |
  | Google Ads | ❓ Görünmüyor, ajansa sorulacak |
  | Merchant Center | ❓ Görünmüyor, ajansa sorulacak |
  | Google Analytics 4 | ❓ Kontrol edilecek: analytics.google.com → Yönetici → Hesap erişim yönetimi |

  **Pixel kontrolü:** business.facebook.com → İşletme Ayarları → **Veri kaynakları → Veri setleri** (eski adı Pikseller). Listede `1032130095734490` var mı? Varsa üzerine tıklayın, sağ tarafta "Sahibi" satırında hangi işletme yazıyor? Listede yoksa pixel ajansın veya ikas'ın oluşturduğu başka bir portföydedir. ikas "otomatik kurulan Pixel" ifadesini kullandığı için ikas entegrasyonunu kimin yaptığına da bakın (ikas → Satış Kanalları → Facebook → bağlı hesap).
  **Katalog kontrolü:** İşletme Ayarları → **Veri kaynakları → Kataloglar**. Bir katalog görünüyor mu, ürün sayısı ~514 mü, sahibi kim? Alternatif yol: business.facebook.com/commerce (Commerce Manager).
  **Reklam hesabı sahipliği:** İşletme Ayarları → Hesaplar → Reklam hesapları → hesabın yanında "Sahibi" kim yazıyor?

  **Ajansta olanlar için:** `strateji/ajans-devir-epostasi.md` taslağını gönderin (1 Aralık'tan sonra işlem yapılmasını ister, Black Friday'i etkilemez).
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

## AŞAMA 1: Meta (Facebook + Instagram) ✅ BAĞLANDI (19 Kasım)

> Bağlantı kuruldu ve test edildi. Kalan: 1.3 alan adı doğrulama, **işletme doğrulaması** (Güvenlik Merkezi), eski reklam hesabının (`act_640771468722072`) ödenmemiş bakiyesi. Ayrıntılar: `raporlar/2026-11-19-meta-baslangic-durumu.md`

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
- [ ] **2.2 Merchant Center.** ikas'ın Google feed bağlantısını (ikas paneli → Satış Kanalları → Google) Merchant Center'a **birincil veri kaynağı** olarak ekleyin. Merchant Center'da damlakuzoptik.com'u **doğrulayıp sahiplenin**, sonra Google Ads hesabına bağlayın.
- [ ] **2.2b Ek feed.** Repodaki `reklam/google/merchant-ek-feed.tsv` dosyasını Merchant Center'a **ek veri kaynağı** olarak yükleyin. Bu dosya ürün başlıklarını, renk ve cinsiyet bilgisini düzeltir. Adımlar `reklam/feed-denetimi.md` dosyasında.
- [ ] **2.2c Barkodlar.** Distribütörlerden (Luxottica, Kering, Safilo vb.) ürünlerin **EAN-13 barkod** listesini isteyin. Barkodların ikas'taki ürünlere girilmesi Google Shopping performansını belirgin artırır. Şu an barkod alanında ürün kodları var; bunlar geçersizdir.
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
- [ ] **4.4** ⏰ **25 Kasım'a kadar: Fahri Kuz fotoğrafları** (eski ve yeni; liste `takvim/2026-12-aralik.md` içinde). Çekim gerekmez. **Arşiv:** 1960'lardan bu yana Fahri Kuz, Yenikapı ilk mağaza, eski reklamlar, gazete kupürleri. Marka mirası içeriklerinin en değerli kaynağı budur.
- [ ] **4.5** **Kuz İstanbul** rebranding dosyaları: logo taslakları, renkler, fontlar, ajans sunumu (hazır olduğunda)

---

## AŞAMA 5: Onay rutini

- [ ] **5.1** Haftalık içerik planı **pazartesi** gönderilir. Onay için **salı 17:00**'ye kadar yanıt verilir.
- [ ] **5.2** Reklam kampanyaları duraklatılmış kurulur, özet gönderilir. Onay mesajı ("onaylıyorum, yayına al") gelmeden açılmaz.
- [ ] **5.3** Haftalık performans raporu her **pazartesi** sabah gönderilir. Aylık rapor her ayın ilk iş günü gönderilir.
