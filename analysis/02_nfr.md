# Fonksiyonel Olmayan Gereksinimler
## Binary Image Generator

Bu doküman "sistem **nasıl** çalışacak" sorusuna cevap verir. Ne yapacağı `01_brd.md`'de
anlatıldı; burada performans, güvenlik, mimari gibi konular var.

---

## 1. Sistem Mimarisi

Sistem **iki bağımsız parçadan** oluşur:

```
┌──────────────────────────────┐     ┌──────────────────────────────┐
│  PYTHON TARAFI (yerel)       │     │  JAVASCRIPT TARAFI (tarayıcı)│
│                              │     │                              │
│  input/fotoğraf.jpg          │     │  <canvas>                    │
│         ↓                    │     │       ↑                      │
│  gri tonlama                 │     │  karakter matrisi            │
│         ↓                    │     │       ↑                      │
│  dithering (opsiyonel)       │     │  gömülü JSON                 │
│         ↓                    │     │                              │
│  piksel → karakter           │     │                              │
│         ↓                    │     │                              │
│  output/portre.png ──────────┼─────┼──► (build sırasında JSON'a    │
│                              │     │     dönüştürülür)            │
└──────────────────────────────┘     └──────────────────────────────┘
```

**İki parça birbirinden bağımsız çalışır.** Aralarında sunucu, API, veritabanı yok.
Python tarafı PNG üretir; web tarafı o PNG'deki karakter matrisini JSON olarak alıp
tarayıcıda canlandırır.

### 1.1 Neden Bu Mimari

- **Sunucusuz:** Kişisel site GitHub Pages'te duruyor, sunucu maliyeti/bakımı yok.
- **Yerel işleme:** Fotoğraf hiçbir yere yüklenmiyor. Gizlilik açısından en güvenli yol.
- **Bağımlılıksız web:** Vanilla JS, tek dosya. `npm install` gerekmiyor.

---

## 2. Python Tarafı — İç Yapı

Kod, küçük ve tek sorumluluklu modüllere bölünür. Her modül **tek bir iş** yapar:

```
src/binary_img_generator/
├── image_loader.py      → Dosyayı açar, boyut kontrolü yapar
├── grayscale.py         → Renkli → gri ton
├── dithering.py         → Floyd–Steinberg uygular
├── ascii_mapper.py      → Piksel → karakter
├── png_exporter.py      → Karakterleri PNG'ye çizer, EXIF temizler
├── pipeline.py          → Yukarıdakileri sırayla çalıştırır
└── cli.py               → Komut satırı arayüzü
```

### 2.1 Veri Akışı

```
Dosya → image_loader → grayscale → dithering → ascii_mapper → png_exporter → Diske yaz
```

Her adım bir öncekinin çıktısını alır. **Ara dosya yazılmaz** — her şey bellekte
tutulur. Bu hem daha hızlı hem de daha temiz.

### 2.2 Neden Modüllere Bölüyoruz

- **Test edilebilirlik:** Her modülü tek başına test edebilirim.
- **Okunabilirlik:** 500 satırlık tek dosya yerine 7 küçük dosya.
- **Değiştirilebilirlik:** Dithering algoritmasını değiştirmek istersem sadece
  `dithering.py`'ye dokunurum, diğerleri etkilenmez.

---

## 3. JavaScript Tarafı — İç Yapı

Web bileşeni de tek dosya ama içinde üç sorumluluk var:

```
web/binary-portrait.js
├── init(options)         → Public fonksiyon, kullanıcı bunu çağırır
├── renderer              → Canvas'a karakter çizer
└── animator              → Belirme efektini yönetir
```

Harici bağımlılık **yok.** Tek dosya, `defer` ile yüklenir.

**Not:** JS class adı `BinaryPortrait` kalıyor. `BinaryImageGenerator` çok uzun
olurdu; JS tarafında kısa isim daha pratik.

---

## 4. Performans Hedefleri

Abartılı hedefler değil, ölçülebilir makul hedefler:

| Ne | Hedef | Neden bu |
|----|-------|----------|
| Python CLI (1200×1200 çıktı) | < 2 saniye | Orta seviye laptopta beklemek sıkıcı olmasın |
| Bellek tüketimi | < 200 MB | 1200×1200 görüntü için makul |
| Web bileşeni boyutu | < 50 KB (gzip'li) | Site yavaşlamasın |
| Animasyon akıcılığı | ≥ 30 FPS | 60 FPS için uğraşmaya değmez |
| Sayfa yüklenmesi | Bloklamasın | `defer` yeterli |

**Ölçüm yöntemleri:**

- CLI süresi: `time python -m ...`
- Bellek: `memory_profiler` veya `/usr/bin/time -v`
- Web boyutu: `gzip -c web/binary-portrait.min.js | wc -c`
- FPS: Chrome DevTools → Performance sekmesi

---

## 5. Güvenlik ve Gizlilik

Bu bölüm kısa çünkü proje zaten "yerel çalışan" bir araç. Ama yine de dikkat
edilmesi gereken noktalar var:

### 5.1 Fotoğraf Sunucuya Gitmez

Tüm işleme kullanıcının cihazında. Sunucu yok, API yok. Bu, gizlilik açısından
en güvenli yaklaşım.

### 5.2 EXIF Temizliği

Üretilen PNG, kaynak fotoğrafın meta verilerini taşımaz. Bir portre paylaştığında
fotoğrafın **nerede çekildiği** (GPS) gibi bilgilerin sızmaması önemlidir.

**Nasıl test edilir:**

```bash
exiftool output/portre.png
# Çıktıda GPS, kamera modeli gibi alanlar olmamalı
```

### 5.3 Kişisel Fotoğraflar Repoya Girmez

`input/` klasörü `.gitignore`'da. Böylece kişisel fotoğraflar yanlışlıkla GitHub'a
gitmez. Bu maddeyi **unutmamak** kritik.

**Nasıl test edilir:**

```bash
git check-ignore input/test.jpg
# Bir çıktı vermeli (yani ignore ediliyor demek)
```

### 5.4 Web Bileşeni İzleme Yapmaz

Çerez yok, analytics yok, harici font/CDN yok. Bileşen kendi kendine yeterli.

### 5.5 Bağımlılık Güvenliği

Python bağımlılıkları haftada bir `pip-audit` ile taranır. Bilinen bir zafiyeti olan
sürüm kullanılmaz.

---

## 6. Arka Plan İşleri

"Background job" dediğimiz şey burada sadece **GitHub Actions'ta zamanlanmış
kontroller.** Ağır bir iş yok, çünkü sunucu yok.

| Ne | Ne zaman | Ne yapar |
|----|----------|----------|
| Test + lint | Her push ve PR'da | `pytest`, `ruff check`, `black --check` |
| Bağımlılık taraması | Haftada bir (pazartesi) | `pip-audit`, `npm audit` |
| Örnek çıktı üretimi | Release öncesi | `output/samples/` yenilenir, repoya commit |

**Neden bunlar "arka plan":** Kullanıcı beklemez, otomatik çalışır. Ama senkron bir
uygulama değil, CI tarafında.

---

## 7. Erişilebilirlik

İki madde, ikisi de zorunlu:

### 7.1 Hareket Hassasiyeti

Kullanıcı işletim sisteminde "hareketi azalt" (`prefers-reduced-motion`) seçtiyse
animasyon **otomatik kapanır.** Bu, baş dönmesi veya dikkat sorunları yaşayan
kullanıcılar için önemli.

**CSS/JS kontrolü:**

```javascript
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (reducedMotion) {
  renderStatic();  // animasyonsuz
} else {
  animate();       // animasyonlu
}
```

### 7.2 Ekran Okuyucu Desteği

Canvas görsel bir öğe olduğu için ekran okuyucu ne olduğunu bilemez. `aria-label`
ile açıklama eklenir:

```html
<canvas aria-label="Binary portre: Ad Soyad"></canvas>
```

---

## 8. Kod Kalitesi

Basit ama tutarlı kurallar:

| Alan | Kural | Araç |
|------|-------|------|
| Python formatı | PEP 8 uyumlu | `black` |
| Python lint | Yaygın hatalar | `ruff` |
| Test | Her modül için en az 1 test | `pytest` |
| Test kapsamı | %80 hedef (zorunlu değil) | `pytest-cov` |
| Docstring | Public fonksiyonlarda zorunlu, İngilizce | — |
| Commit mesajı | Conventional Commits | — |
| Sürüm | SemVer (`v1.0.0`, `v1.1.0`) | — |

**Neden %80 kapsam:** %100 kapsam gerçek projede çok zaman alır ve marjinal faydası
düşük. %80, "kritik yollar test edilmiş" demek için yeterli.

---

## 9. Yedekleme

- **Kod:** GitHub'da. Zaten yedek.
- **Örnek çıktılar:** Repoda, sürümlü.
- **Kişisel fotoğraflar:** Sistemin sorumluluğunda değil. README'de "fotoğraflarını
  kendin yedekle" notu olacak.

---

## 10. Bilinçli Olarak Yapmadıklarımız

Over-engineering'den kaçınmak için v1'de **bilerek** olmayanlar:

| Yapmadık | Neden |
|----------|-------|
| Docker | Tek kişilik proje, ortam kurulumu basit |
| Veritabanı | Saklanacak veri yok |
| Log toplama (Sentry, Datadog) | `logging` modülü yeterli |
| Mikroservis | İki dosyalık iş |
| CI/CD ile otomatik deploy | GitHub Pages zaten otomatik |
| %100 test kapsamı | Zaman kaybı, marjinal fayda yok |

Bunlar "kötü pratik" değil; bu ölçekteki bir proje için **gereksiz.** İhtiyaç olursa
v2'de eklenir.

---

## 11. Teknoloji Seçimleri ve Nedenleri

| Teknoloji | Neden |
|-----------|-------|
| **Python 3.10+** | Görüntü işleme için zengin kütüphane ekosistemi |
| **Pillow** | Python'un standart görüntü kütüphanesi, basit ve yeterli |
| **numpy** | Piksel matrisleri üzerinde hızlı işlem |
| **Vanilla JS** | Bağımlılıksız, tek dosya, tarayıcıda doğrudan çalışır |
| **Canvas API** | Piksel seviyesinde çizim için standart |
| **pytest** | Python'un en yaygın test framework'ü |
| **ruff + black** | Hızlı, modern Python araçları |