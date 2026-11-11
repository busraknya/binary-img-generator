# İş Gereksinimleri Dokümanı
## Binary Image Generator

Bu doküman projenin **ne yaptığını** ve **neden yapıldığını** anlatır. Kod detayı
içermez. Bir arkadaşın "bu proje ne işe yarıyor?" diye sorduğunda bu dokümanı okuması
yeterli olmalı.

---

## 1. Proje Nedir

Binary Image Generator, bir fotoğrafı alıp onu **0 ve 1 rakamlarından oluşan bir
portreye** dönüştüren küçük bir araçtır. Aynı portrenin iki farklı çıktısı vardır:

1. **PNG dosyası:** Python ile üretilir, diske kaydedilir. Statik görsel.
2. **Web bileşeni:** Tarayıcıda Canvas üzerinde animasyonla beliren hâli.

Kısaca: fotoğrafını ver, sana "binary portreni" versin.

---

## 2. Neden Yapıyoruz

Üç sebep var, üçü de gerçek:

1. **Öğrenmek.** Görüntü işleme (fotoğraf → siyah beyaz), algoritmik düşünme
   (dithering, karakter eşleme) ve frontend (Canvas, animasyon) konularını tek bir
   projede birleştirmek istiyorum.
2. **Kullanmak.** Kişisel sitemde sıradan bir fotoğraf yerine, kodla ürettiğim bir
   portre dursun istiyorum. Yani proje "demo" değil, gerçekten kullanılacak.
3. **Paylaşmak.** GitHub'da yayınlayınca hem kendi portfolyom için somut bir iş
   olacak, hem de benzer bir şey yapmak isteyen biri bu repodan faydalanabilecek.

---

## 3. Kapsam

### 3.1 Kapsamda Olanlar

- Fotoğrafı siyah-beyaza (gri tona) çevirmek
- Gri tonlu görüntüyü 0 ve 1 karakterlerinden oluşan bir metin ızgarasına dönüştürmek
- Dithering uygulamak (görsel detayı artıran bir teknik — Bölüm 5.4'te anlatılıyor)
- Sonucu PNG olarak kaydetmek
- Portre "yoğunluğunu" ve karakter boyutunu ayarlayabilmek
- Aynı portreyi tarayıcıda animasyonlu göstermek
- Kişisel siteye tek bir `<script>` etiketiyle eklenebilmek
- GitHub'da açık kaynak olarak yayınlamak

### 3.2 Kapsamda Olmayanlar

Bunlar bilinçli olarak **v1'e dahil edilmedi.** "Acaba eklesem mi?" dürtüsüne karşı
burada dursun:

- Renkli çıktı (sadece siyah-beyaz, tema bu)
- 0/1 dışında karakter setleri (örn. `@#%*+=-` gibi ASCII sanatı — ayrı bir proje)
- Kullanıcı hesabı, giriş sistemi (tek kişisel kullanım)
- Veritabanı (saklanacak bir şey yok)
- Sunucu tarafı işlem (her şey tarayıcıda veya yerelde çalışır)
- Mobil uygulama
- Birden fazla fotoğrafı toplu işleme

---

## 4. Kim Kullanacak

| Kim | Ne için | Nerede |
|-----|---------|--------|
| **Ben (geliştirici)** | PNG üretmek, siteye gömmek | Kendi bilgisayarım |
| **Site ziyaretçisi** | Animasyonlu portreyi görmek | Tarayıcıda, sitemde |
| **Kodu inceleyen biri** | Benzer proje yapmak için örnek almak | GitHub'da |

v1'de başka kullanıcı yok. Bu yüzden kimlik doğrulama, yetkilendirme gibi şeyler
kapsam dışı.

---

## 5. İş Kuralları

Aşağıdaki maddeler "sistem neyi nasıl yapmalı" sorusuna cevap verir. Her biri kod
yazarken kontrol edilecek bir kural. Kodlayan kişi (yani ben) bu maddelere bakarak
"buna uyuyor muyum?" diye kontrol edecek.

### 5.1 Girdi (BR-01)

**Ne:** Kullanıcı bir portre fotoğrafı verir.

- Kabul edilen formatlar: **JPEG, PNG, WebP**
- Minimum boyut: **64×64 piksel.** Daha küçük görseller reddedilir.
- Reddedilirse **Türkçe** ve anlaşılır hata mesajı verilir.

**Neden minimum boyut var:** 64×64'ün altındaki görsellerde yüz hatları zaten
kaybolmuş olur; portre üretmek anlamsız.

**Örnek hata mesajı:**

```
Hata: Görsel çok küçük (32×32). En az 64×64 piksel olmalı.
```

### 5.2 Gri Tonlama (BR-02)

**Ne:** Renkli fotoğraf, siyah-beyaz tonlarına çevrilir.

Burada standart bir formül kullanılır: **BT.601**. Nedir? Her pikselin kırmızı, yeşil
ve mavi değerini belirli ağırlıklarla toplayıp tek bir "parlaklık" değeri elde etme
yöntemi. İnsan gözü yeşile daha duyarlı, maviye daha az duyarlı olduğu için ağırlıklar
eşit değildir:

```
Parlaklık = 0.299 × Kırmızı + 0.587 × Yeşil + 0.114 × Mavi
```

**Neden bu formül:** Her gri tonlama kütüphanesi bunu kullanır. Farklı bir formül
kullanmak sonucu "yanlış" yapmaz ama standarttan sapar; testlerde de bunu bekleriz.

**Örnek:** Saf kırmızı bir piksel (`R=255, G=0, B=0`), gri tonda `76` değerini alır.
Saf yeşil `150`, saf mavi `29`.

### 5.3 Karakter Eşleme (BR-03)

**Ne:** Her piksel, bir karaktere dönüştürülür.

Kural basit: piksel ne kadar koyuysa o kadar "dolu" karakter kullanılır.

- Koyu piksel (parlaklık düşük) → `1`
- Açık piksel (parlaklık yüksek) → boşluk

**Neden sadece 0 ve 1:** Projenin teması "binary". 0/1 kullanmak estetik bir tercih,
aynı zamanda başlıkla uyumlu.

**Satır uzunluğu:** Tüm satırlar **eşit uzunlukta** olmalı. Aksi halde görüntü
bozulur. Görselin en-boy oranı korunur: geniş bir fotoğraf geniş bir metin ızgarası
üretir.

### 5.4 Dithering (BR-04)

**Dithering nedir:** Gri tonlu bir görüntüyü sadece siyah-beyaz ile göstermeye
çalıştığımızda, orta tonlar kaybolur ve "bantlar" oluşur. Dithering, bu bantları
kırmak için piksellerin siyah mı beyaz mı olacağına karar verirken **hatanın bir
kısmını komşu piksellere yayar.** Sonuç: göz, gri tonları "noktacıklardan" algılar.

Kullandığımız algoritma: **Floyd–Steinberg.** En yaygın dithering algoritması.
Bir pikselin siyah mı beyaz mı olacağına karar verirken oluşan "hata"yı 4 komşu
piksele belirli oranlarda paylaştırır.

**Kural:**

- Dithering **açılıp kapatılabilir** (varsayılan: açık).
- Kapalıyken basit eşikleme (threshold) kullanılır: parlaklık `128`'in altındaysa
  siyah, üstündeyse beyaz.

**Neden opsiyonel:** Bazı fotoğraflarda dithering "gürültülü" görünebilir. Kullanıcı
kapatabilsin.

### 5.5 Ayarlanabilir Parametreler (BR-05)

Kullanıcı şu değerleri değiştirebilir:

| Parametre | Ne işe yarar | Varsayılan | Aralık |
|-----------|--------------|------------|--------|
| `grid_width` | Metin portresinin kaç karakter genişliğinde olacağı | 120 | 40–400 |
| `char_aspect` | Karakterin en/boy oranı | 0.5 | 0.3–1.0 |
| `threshold` | Siyah/beyaz eşiği (dithering kapalıyken) | 128 | 0–255 |
| `dither` | Dithering açık mı kapalı mı | `true` | `true`/`false` |
| `invert` | 0 ve 1'lerin yerini değiştir | `false` | `true`/`false` |

**`grid_width` örneği:** `grid_width=120` dersen çıktı 120 karakter genişliğinde olur.
Daha büyük değer = daha detaylı ama daha yavaş. `40` çok kaba, `400` çok yavaş.

**`char_aspect` örneği:** Monospace fontlarda bir karakterin yüksekliği genişliğinden
fazladır. Bu yüzden 1 piksel yüksekliği, 1 piksel genişliğine eşit değildir. `0.5`
demek "her karakter, 2 piksel genişliğinde 1 piksel yüksekliğinde" gibi düşünülebilir.
Ayarı bozarsan görüntü ezilir veya gerilir.

**Kural:** Geçersiz değer gelirse (örn. `grid_width=10` çünkü minimum 40), Türkçe hata
mesajı verilir. Sessizce düzeltilmez.

### 5.6 PNG Çıktısı (BR-06)

**Ne:** Sonuç bir PNG dosyası olarak kaydedilir.

- **Çözünürlük:** En az `1200×1200` piksel.
- **Font:** Monospace (eşit genişlikli) olmalı.
- **Arka plan:** Siyah zemin + beyaz karakter (varsayılan) veya tersi.
- **Dosya adı:** `portre_<zaman>.png` formatı. Örnek: `portre_20261111_1430.png`.
- **Meta veri:** Kaynak fotoğrafın EXIF bilgileri (GPS, kamera modeli vb.)
  **taşınmaz.** Bu bilinçli bir gizlilik kararı.

### 5.7 Web Bileşeni (BR-07)

**Ne:** Aynı portre, tarayıcıda animasyonla belirir.

- Canvas üzerinde çizilir (HTML5 Canvas API).
- **Animasyon:** Karakterler **soldan sağa sırayla** belirir.
- **`prefers-reduced-motion` desteği:** Kullanıcı işletim sistemi ayarlarında
  "hareketi azalt" seçtiyse animasyon otomatik olarak **kapanır**, portre statik
  gösterilir.

**Neden soldan sağa:** Soldan sağa okuma yönüyle uyumlu olduğu için seçildi.

### 5.8 Siteye Gömme (BR-08)

- Tek bir `<script>` etiketi + tek bir `<canvas>` ile çalışmalı.
- **Sayfayı bloklamamalı:** `defer` özniteliğiyle yüklenmeli.
- Harici kütüphane gerektirmemeli (vanilla JS).

**Neden harici kütüphane yok:** Kişisel siteye "tek dosya" olarak eklenmeli.

### 5.9 Yayın (BR-09)

GitHub'da yayınlanırken şunlar olmalı:

- `README.md` — projeyi tanıtan, çalıştırma adımlarını içeren
- `LICENSE` — MIT önerilir
- En az 3 örnek çıktı (`output/samples/` altında)

---

## 6. Bitmiş Sayılma Kriterleri

v1 tamamlandı diyebilmem için **hepsi** doğru olmalı:

- [ ] Bir fotoğrafı tek komutla PNG'ye çevirebiliyorum.
- [ ] Çıktıya baktığımda yüz hatları tanınıyor.
- [ ] Dithering açık ve kapalı arasındaki fark net görülüyor.
- [ ] Geçersiz parametre verdiğimde Türkçe hata alıyorum.
- [ ] Web bileşeni kişisel sitemde çalışıyor.
- [ ] `prefers-reduced-motion` açıkken animasyon duruyor.
- [ ] README'yi sıfırdan takip eden biri 30 dakikada çalıştırabiliyor.
- [ ] GitHub'da en az 3 örnek çıktı var.

---

## 7. Terimler Sözlüğü

| Terim | Anlamı |
|-------|--------|
| **Gri ton (grayscale)** | Siyah ile beyaz arasındaki tonlar. Her pikselin tek bir parlaklık değeri vardır (0–255). |
| **BT.601** | Gri tona çevirmede kullanılan standart ağırlık formülü. |
| **Eşikleme (threshold)** | Bir değeri siyah mı beyaz mı sayacağımıza karar veren sınır. |
| **Dithering** | Gri tonları siyah-beyaz noktalarla taklit etme tekniği. |
| **Floyd–Steinberg** | En yaygın dithering algoritması; hatayı komşu piksellere yayar. |
| **Monospace** | Her karakterin aynı genişlikte olduğu font. |
| **Canvas** | Tarayıcıda piksel piksel çizim yapmaya izin veren HTML5 API'si. |
| **EXIF** | Fotoğrafın içine gömülü meta bilgi (çekim tarihi, GPS, kamera modeli vb.). |
| **MVP** | Minimum Uygulanabilir Ürün — çalışan en basit hâl. |