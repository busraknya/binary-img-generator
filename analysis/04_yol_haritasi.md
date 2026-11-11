# Yol Haritası
## Binary Image Generator

Bu doküman, projeyi **hangi sırayla** yapacağımızı gösterir. Bir backlog değil —
sprint planı, story point, atama yok. Sadece "bugün ne yapacağım" listesi.

Her fazın sonunda **bitmiş sayılma kriteri** var. Bir sonraki faza geçmeden önce
o kriterlerin hepsi doğru olmalı.

Durum sembolleri:

- `[ ]` yapılmadı
- `[~]` devam ediyor
- `[x]` bitti

---

## Faz 0 — İskelet (tahmini: yarım gün)

Projenin iskeletini kur. Kod yok, sadece ortam.

- [ ] GitHub'da repo aç (public, MIT lisans): `binary-img-generator`
- [ ] `git clone` ile yerele indir (veya boş klasörde `git init`)
- [ ] Klasör yapısı (`03_kurulum.md` Bölüm 3'teki gibi)
- [ ] `.gitignore` yaz (`03_kurulum.md` Bölüm 4)
- [ ] `requirements.txt` yaz
- [ ] `pyproject.toml` yaz
- [ ] Sanal ortam oluştur, bağımlılıkları yükle
- [ ] İlk commit: `chore: proje iskeleti`

**Bitmiş sayılır eğer:** `git status` temiz, `python --version` doğru, klasör yapısı
`03_kurulum.md`'deki gibi.

---

## Faz 1 — Çalışan MVP (tahmini: 1 hafta sonu)

Hedef: **ilk PNG'yi görmek.** Kalite değil, "vay be çalıştı" anı.

Bu fazda dithering yok, sadece en basit hâli. Dithering Faz 2'de.

### 1.1 Gri tonlama

- [ ] `src/binary_img_generator/image_loader.py`
  - `Pillow` ile fotoğrafı aç
  - Boyut kontrolü (64×64'ten küçükse `ValueError`, Türkçe mesaj)
  - Format kontrolü (JPEG/PNG/WebP dışındakileri reddet)
- [ ] `src/binary_img_generator/grayscale.py`
  - `numpy` dizisine çevir
  - BT.601 formülüyle gri tona çevir
- [ ] `src/tests/test_grayscale.py`
  - Kırmızı `(255,0,0)` → `76`
  - Yeşil `(0,255,0)` → `150`
  - Mavi `(0,0,255)` → `29`
  - Beyaz → `255`, siyah → `0`
  - ±1 tolerans kullan

### 1.2 Karakter eşleme

- [ ] `src/binary_img_generator/ascii_mapper.py`
  - `threshold` parametresi al (varsayılan 128)
  - Her pikseli `1` veya boşluğa çevir
  - `invert` desteği ekle
- [ ] `src/tests/test_ascii_mapper.py`
  - `grid_width` kadar sütun var mı?
  - Tüm satırlar eşit uzunlukta mı?
  - `invert` çalışıyor mu?

### 1.3 CLI

- [ ] `src/binary_img_generator/cli.py`
  - `argparse` ile basit komut satırı
  - En az: fotoğraf yolu, `--grid-width`, `--invert`
  - `--verbose` ile aşamaları logla
- [ ] `src/binary_img_generator/pipeline.py`
  - Yukarıdaki modülleri sırayla çalıştır

### 1.4 PNG çıktısı (basit)

- [ ] `src/binary_img_generator/png_exporter.py`
  - Karakterleri monospace fontla PNG'ye çiz
  - `Pillow` ile siyah zemin üstüne beyaz karakter
  - `output/portre_<zaman>.png` olarak kaydet

### 1.5 İlk çalıştırma

- [ ] `input/`'a bir portre fotoğrafı koy
- [ ] `python -m binary_img_generator.cli input/ben.jpg` çalıştır
- [ ] `output/`'daki PNG'yi aç, gözle kontrol et
- [ ] README'ye "şu komutla çalışıyor" yaz
- [ ] Commit: `feat: MVP - fotoğraftan PNG portre üretimi`

**Bitmiş sayılır eğer:** Çıktıda yüz tanınıyor (kaba da olsa). Yani "evet bu benim"
diyebiliyorum.

---

## Faz 2 — Kalite (tahmini: 1 hafta)

MVP çalışıyor ama "güzel" değil. Bu fazda düzeltiyoruz.

### 2.1 Dithering

- [ ] `src/binary_img_generator/dithering.py`
  - Floyd–Steinberg algoritması
  - Hata dağıtım katsayıları: `7/16, 3/16, 5/16, 1/16`
  - Kayan nokta hatası birikmesin diye `float` kullan
- [ ] `src/tests/test_dithering.py`
  - **Golden test:** sabit bir gri gradient üzerinde üretilen matris,
    `src/tests/fixtures/expected/gradient_dither.txt` ile birebir eşleşmeli
  - Dithering kapalıyken saf threshold çalışmalı
  - Threshold `0` → hepsi beyaz
  - Threshold `255` → hepsi siyah

### 2.2 Parametre doğrulama

- [ ] `cli.py`'de tüm parametreler için aralık kontrolü
  - `grid_width` 40–400
  - `char_aspect` 0.3–1.0
  - `threshold` 0–255
- [ ] Geçersiz değer → `ValueError` + Türkçe mesaj
- [ ] `src/tests/test_cli.py` — her parametre için geçerli/geçersiz test

### 2.3 EXIF temizliği

- [ ] `png_exporter.py`'de `exif` verisini açıkça sil

  ```python
  img.save(path, exif=b'')  # boş EXIF
  ```

- [ ] Test: `exiftool output/test.png` → GPS/kamera bilgisi yok

### 2.4 Örnek çıktılar

- [ ] `output/samples/` altına 3 farklı fotoğraftan çıktı üret
- [ ] README'ye bu örnekleri ekle (görsel olarak)
- [ ] Commit: `feat: dithering, doğrulama, EXIF temizliği`

### 2.5 Test ve kapsam

- [ ] `pytest --cov=binary_img_generator --cov-report=term-missing` çalıştır
- [ ] Kapsam %80'in üstünde mi? Değilse test ekle

**Bitmiş sayılır eğer:** Dithering açık/kapalı arasındaki fark gözle net görülüyor.
Geçersiz parametre Türkçe hata veriyor. Örnekler repoda.

---

## Faz 3 — Web Bileşeni (tahmini: 1–2 hafta)

En uzun faz. JavaScript'e yabancıysan daha uzun sürebilir, normal.

### 3.1 Statik render (animasyon yok)

- [ ] `web/binary-portrait.js`
  - `BinaryPortrait.init({ target, dataUrl })` public fonksiyonu
  - `fetch` ile JSON al
  - Canvas'a karakterleri çiz (monospace font)
  - Boyut responsive olsun
- [ ] `web/demo.html`
  - Basit HTML, canvas + script tag
  - `python -m http.server` ile test et

### 3.2 Karakter matrisini gömme

- [ ] `scripts/build_web.py`
  - PNG'deki karakter matrisini oku
  - JSON olarak `web/data.json`'a yaz (veya doğrudan JS'e göm)
- [ ] `web/demo.html`'de `dataUrl: './data.json'` ile çalıştır

### 3.3 Animasyon

- [ ] `animator` modülü ekle
  - `requestAnimationFrame` ile soldan sağa belirme
  - `duration` parametresi (varsayılan 2500 ms)
  - Karakterler arası gecikme: `duration / totalChars`

### 3.4 Erişilebilirlik

- [ ] `prefers-reduced-motion` kontrolü
  - Aktifse `renderStatic()` çağır, animasyonu atla
- [ ] Canvas'a `aria-label` ekle (JS içinden veya HTML'den)
- [ ] Test: OS ayarını değiştir, animasyon duruyor mu?

### 3.5 Boyut optimizasyonu

- [ ] (Opsiyonel) `terser` ile minify
- [ ] `gzip -c web/binary-portrait.min.js | wc -c` → 50 KB altında mı?
- [ ] Commit: `feat: web bileşeni`

**Bitmiş sayılır eğer:** `demo.html` tarayıcıda açılıyor, portre animasyonla beliriyor.
Reduced-motion açıkken animasyon duruyor. Dosya 50 KB altında.

---

## Faz 4 — Yayın (tahmini: 2–3 gün)

Kod bitti, şimdi paketle.

- [ ] `README.md` yaz — **hem İngilizce hem Türkçe**
  - Ne olduğu, nasıl çalıştırıldığı, örnek çıktılar
  - Kurulum komutları (kopyala-yapıştır çalışsın)
- [ ] `README.tr.md` — Türkçe sürüm
- [ ] `LICENSE` — MIT
- [ ] Kişisel siteye embed et
  - `<canvas>` + `<script defer>` + `init()` çağrısı
  - Canlı test et
- [ ] `.github/workflows/test.yml`
  - Her push'ta: `pytest`, `ruff`, `black --check`
- [ ] `.github/workflows/weekly-audit.yml`
  - Pazartesi: `pip-audit`, `npm audit`
- [ ] `v1.0.0` tag at
- [ ] LinkedIn/portfolyo notu (isteğe bağlı)

**Bitmiş sayılır eğer:** Site canlıda animasyonlu portre görünüyor. Repo public.
README'yi sıfırdan takip eden biri 30 dakikada çalıştırabiliyor.

---

## Test Listesi

Her faz sonunda bu listeye bakacağım. Ayrı bir "test planı dokümanı" yok — çünkü
buna gerek yok. Kısa liste yeterli.

### Otomatik testler (pytest)

- [ ] BT.601 ağırlıkları doğru (kırmızı→76, yeşil→150, mavi→29)
- [ ] `grid_width` kadar sütun var
- [ ] Tüm satırlar eşit uzunlukta
- [ ] `invert` doğru çalışıyor
- [ ] Dithering golden çıktıyla eşleşiyor
- [ ] Dithering kapalıyken threshold çalışıyor
- [ ] Geçersiz parametre `ValueError` fırlatıyor (Türkçe mesaj)
- [ ] 32×32 görsel reddediliyor

### Elle kontroller

- [ ] Çıktıda yüz tanınıyor (gözle)
- [ ] Dithering açık/kapalı farkı görülüyor
- [ ] EXIF temiz: `exiftool output/*.png` → GPS yok
- [ ] `input/` gitignore'da: `git check-ignore input/test.jpg` çıktı veriyor
- [ ] Web 50 KB altında: `gzip -c web/binary-portrait.min.js | wc -c`
- [ ] Reduced-motion animasyonu durduruyor
- [ ] Mobilde animasyon akıcı (Chrome DevTools → Device Mode)

### Release öncesi

- [ ] `pytest` yeşil
- [ ] `ruff check src/` temiz
- [ ] `black --check src/` temiz
- [ ] `pip-audit` kritik CVE yok
- [ ] README komutları hâlâ çalışıyor
- [ ] `output/samples/` güncel

---

## Yapmayacaklarım (v2'ye kalanlar)

Listeye bakıp "bunu da eklesem mi" dürtüsüne karşı burada dursun. v1 kapsamı dışında:

- Renkli çıktı
- 0/1 dışında karakter setleri
- Kullanıcı hesabı, veritabanı
- API endpoint, sunucu
- Toplu (batch) işleme
- Mobil uygulama
- Docker
- CI/CD otomatik deploy (GitHub Pages zaten otomatik)
- %100 test kapsamı

İhtiyaç olursa v2'de.

---

## Zaman Tahmini

Dürüst olalım:

| Faz | Süre | Not |
|-----|------|-----|
| Faz 0 — İskelet | Yarım gün | Hızlı, sıkıcı ama gerekli |
| Faz 1 — MVP | 1 hafta sonu | En motive edici, ilk PNG burada |
| Faz 2 — Kalite | 1 hafta | Dithering'de takılabilirsin, normal |
| Faz 3 — Web | 1–2 hafta | En uzun, JS'e yabancıysan daha uzun |
| Faz 4 — Yayın | 2–3 gün | Paketleme, README, deploy |

**Toplam: 3–4 hafta** (günde 1–2 saat çalışarak).
Yoğun çalışırsan **1 haftada** biter.

---

## İlerleme Notları

Her faz bittiğinde buraya bir not düş. 6 ay sonra dönüp baktığında ne yaptığını
hatırlarsın.

- **[Tarih]** Faz 0 bitti. İskelet hazır.
- **[Tarih]** Faz 1 bitti. İlk PNG'yi gördüm, çok kaba ama çalışıyor.
- **[Tarih]** Faz 2 bitti. Dithering farkı gerçekten büyük.
- **[Tarih]** Faz 3 bitti. Sitede çalışıyor. Animasyon tam istediğim gibi.
- **[Tarih]** v1.0.0 yayında. 🎉