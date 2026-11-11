# Kurulum Rehberi
## Binary Image Generator

Bu doküman, projeyi **sıfırdan** çalıştırmak için gereken her adımı içerir. Daha önce
hiç Python projesi kurmamış biri bile takip edebilmeli.

---

## 1. Ön Koşullar

Bilgisayarında şunlar kurulu olmalı. Kurulu mu diye kontrol etmek için terminal
(veya komut istemi) açıp şu komutları çalıştır:

| Araç | Minimum | Kontrol komutu | Yoksa ne yapmalı |
|------|---------|----------------|-------------------|
| Python | 3.10+ | `python --version` | python.org'dan indir |
| pip | 22+ | `pip --version` | Python ile birlikte gelir |
| Git | 2.30+ | `git --version` | git-scm.com'dan indir |

**Windows kullanıyorsan:** Python'u kurarken "Add Python to PATH" seçeneğini
işaretlemeyi unutma. Aksi halde `python` komutu tanınmaz.

**Node.js gerekli mi?** Sadece web bileşenini "minify" etmek istersen gerekli.
Geliştirme aşamasında gerekmiyor.

---

## 2. Projeyi İndir

```bash
git clone https://github.com/<kullanıcıadı>/binary-img-generator.git
cd binary-img-generator
```

Henüz repo yoksa, kendi klasörünü oluştur:

```bash
mkdir binary-img-generator
cd binary-img-generator
git init
```

---

## 3. Klasör Yapısını Oluştur

Aşağıdaki klasörler olmalı. Yoksa oluştur:

```bash
mkdir -p src/binary_img_generator src/tests
mkdir -p web
mkdir -p input output/samples
mkdir -p data scripts
mkdir -p analysis
mkdir -p .github/workflows
```

**Windows PowerShell'de** `mkdir -p` yerine tek tek:

```powershell
New-Item -ItemType Directory -Force -Path src/binary_img_generator, src/tests, web, input, output/samples, data, scripts, analysis, .github/workflows
```

Nihai yapı şöyle olmalı:

```
binary-img-generator/
├── analysis/                    ← dokümanlar
├── src/
│   ├── binary_img_generator/    ← Python kodu
│   └── tests/                   ← testler
├── web/                         ← JS bileşeni
├── input/                       ← fotoğraflar (gitignore'da)
├── output/
│   └── samples/                 ← örnek çıktılar (commit edilecek)
├── data/                        ← karakter matrisi (opsiyonel)
├── scripts/                     ← yardımcı scriptler
└── .github/workflows/           ← CI ayarları
```

---

## 4. `.gitignore` Dosyasını Oluştur

Proje köküne `.gitignore` adında bir dosya oluştur. İçine şunu koy:

```gitignore
# Kişisel fotoğraflar (asla commit edilmemeli)
input/*
!input/.gitkeep

# Üretilen çıktılar (örnekler hariç)
output/*
!output/samples/
!output/.gitkeep

# Python
__pycache__/
*.pyc
.venv/
*.egg-info/
.pytest_cache/
.coverage
htmlcov/

# Node
node_modules/
web/*.min.js

# IDE ve işletim sistemi
.vscode/
.idea/
.DS_Store
Thumbs.db

# Ortam dosyaları
.env
```

**Neden önemli:** `input/*` satırı olmadan kişisel fotoğrafların yanlışlıkla GitHub'a
gidebilir. Bu satırı **silmeyin.**

---

## 5. Python Sanal Ortamı

Sanal ortam, projenin bağımlılıklarını sistem Python'undan izole eder. Yani "bu projeye
özel bir Python kurulumu" gibi düşünebilirsin.

### 5.1 Oluştur

```bash
python -m venv .venv
```

### 5.2 Aktive Et

**Linux / macOS:**

```bash
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows komut istemi (cmd):**

```bat
.venv\Scripts\activate.bat
```

Aktive olduğunu nasıl anlarsın: Terminal satırının başında `(.venv)` yazar.

```
(.venv) user@machine:~/binary-img-generator$
```

### 5.3 Aktifleştirmeyi Kapatmak

İşin bitince: `deactivate`

---

## 6. Bağımlılıkları Yükle

Proje köküne `requirements.txt` dosyası oluştur:

```txt
Pillow>=10.0.0
numpy>=1.24.0
pytest>=7.4.0
pytest-cov>=4.1.0
ruff>=0.4.0
black>=24.0.0
pip-audit>=2.7.0
```

Sonra yükle:

```bash
pip install -r requirements.txt
```

**Ne yüklendi:**

- `Pillow` — görüntü açma, kaydetme, boyutlandırma
- `numpy` — piksel matrisleri üzerinde hızlı işlem
- `pytest` — test çalıştırma
- `pytest-cov` — test kapsamı ölçümü
- `ruff` — hızlı lint
- `black` — otomatik format
- `pip-audit` — bağımlılık güvenlik taraması

---

## 7. Python Paketini "Editable" Modda Kur

Bu adım, kodu değiştirdiğinde yeniden kurulum yapmadan çalıştırmanı sağlar.

`pyproject.toml` dosyasını proje köküne oluştur:

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "binary-img-generator"
version = "0.1.0"
description = "Fotoğrafı 0/1 portresine çeviren araç"
requires-python = ">=3.10"
dependencies = ["Pillow>=10.0.0", "numpy>=1.24.0"]

[project.scripts]
big = "binary_img_generator.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.black]
line-length = 100
target-version = ["py310"]

[tool.pytest.ini_options]
testpaths = ["src/tests"]
addopts = "--cov=binary_img_generator --cov-report=term-missing"
```

Sonra:

```bash
pip install -e .
```

`-e` (editable), "kodu düzenledikçe değişiklik anında yansısın" demek.

**Not:** `[project.scripts]` bölümü sayesinde kurulumdan sonra `big` kısayolu çalışır.
Yani `python -m binary_img_generator.cli` yerine sadece `big` yazabilirsin. Bu opsiyonel
bir kolaylık.

---

## 8. İlk Fotoğrafı Koy

`input/` klasörüne bir portre fotoğrafı koy:

```bash
cp ~/Pictures/ben.jpg input/
```

**Dikkat:** Fotoğraf **en az 64×64 piksel** olmalı (BR-01). Çoğu telefon fotoğrafı
zaten çok daha büyük, sorun olmaz.

---

## 9. Çalıştır

Kod yazıldıktan sonra:

```bash
python -m binary_img_generator.cli input/ben.jpg
```

Ya da kısayolla:

```bash
big input/ben.jpg
```

Çıktı `output/` klasörüne düşer.

Farklı ayarlarla denemek için:

```bash
# Daha yüksek detay
python -m binary_img_generator.cli input/ben.jpg --grid-width 200

# Dithering kapalı
python -m binary_img_generator.cli input/ben.jpg --no-dither

# Örnek çıktı klasörüne
python -m binary_img_generator.cli input/ben.jpg --output output/samples/ben.png
```

---

## 10. Web Demo'yu Aç (Faz 3'ten Sonra)

`web/` klasöründe basit bir HTTP sunucusu çalıştır:

```bash
cd web
python -m http.server 8080
```

Tarayıcıda aç: `http://localhost:8080/demo.html`

`file://` protokolü yerine HTTP kullanmak önemli — bazı tarayıcılar `file://` ile
JS yüklemeyi engeller.

---

## 11. Testleri Çalıştır

```bash
pytest
```

Kapsam raporuyla birlikte:

```bash
pytest --cov=binary_img_generator --cov-report=html
```

Rapor `htmlcov/index.html`'de açılır.

---

## 12. Kod Kalitesi Kontrolleri

```bash
# Format
black src/

# Lint
ruff check src/ --fix

# Bağımlılık güvenlik taraması
pip-audit
```

---

## 13. Sık Karşılaşılan Sorunlar

| Hata | Sebep | Çözüm |
|------|-------|-------|
| `ModuleNotFoundError: binary_img_generator` | Paket kurulmamış | `pip install -e .` |
| `python: command not found` | Python PATH'te değil | Python'u yeniden kur, "Add to PATH" işaretle |
| `.venv\Scripts\Activate.ps1` çalışmıyor | PowerShell güvenlik politikası | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| "Görsel çok küçük" hatası | Fotoğraf < 64×64 | Daha büyük fotoğraf kullan |
| Çıktı tanınmıyor | `grid_width` çok düşük | `--grid-width 160` dene |
| Tüm piksel siyah | `--invert` yanlış veya threshold düşük | `--invert` ekle/kaldır, `--threshold 100` dene |
| `exiftool` yok | Kurulu değil | Linux: `apt install libimage-exiftool-perl`, macOS: `brew install exiftool` |

---

## 14. Kurulum Kontrol Listesi

Her şeyin doğru olduğundan emin olmak için sırayla kontrol et:

- [ ] `python --version` 3.10 veya üstü gösteriyor
- [ ] `pip install -r requirements.txt` hatasız tamamlandı
- [ ] `pip install -e .` hatasız tamamlandı
- [ ] `.venv` aktive edilmiş (terminalde `(.venv)` görünüyor)
- [ ] `input/` içinde en az bir fotoğraf var
- [ ] `pytest` çalışıyor (testler olmasa bile "0 test, 0 hata" der)
- [ ] `black --check src/` hata vermiyor
- [ ] `ruff check src/` hata vermiyor

Hepsi tamamsa ortam hazır. Kod yazmaya başlayabilirsin.