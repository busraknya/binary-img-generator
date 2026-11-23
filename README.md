# Binary Image Generator

Convert your photos into text-based portraits made with `0`, `1`, and spaces.

Fotoğraflarınızı `0`, `1` ve boşluk karakterlerinden oluşan portrelere dönüştürün.

[English](#english) | [Türkçe](#turkce)

---

<a id="english"></a>

## English

### About

Binary Image Generator is a Python tool. It turns photos into text-based portraits and saves them as PNG images.

The project currently has a command-line tool. A web application is planned for a future release.

### Features

- Supports JPEG, PNG, and WebP images.
- Converts images to grayscale.
- Creates portraits with `0`, `1`, and spaces.
- Measures character density using the font selected for PNG export.
- Keeps the original image proportions.
- Uses Floyd–Steinberg dithering to keep more image details.
- Offers automatic contrast adjustment.
- Lets you change portrait width and the middle-tone setting.
- Saves the result as a PNG image with white characters on a black background.

### Requirements

- Python 3.10 or later
- Git

### Installation

Clone the project:

```bash
git clone https://github.com/busraknya/binary-img-generator.git
cd binary-img-generator
```

Create and activate a virtual environment.

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the project and its packages:

```bash
pip install -r requirements.txt
pip install -e .
```

### Usage

Run the tool with an image path:

```bash
big path/to/photo.jpg
```

You can also run it with Python:

```bash
python -m binary_img_generator.cli path/to/photo.jpg
```

The tool saves the PNG file in the `output/` folder by default.

### Options

| Option | Description | Default |
|---|---|---|
| `--grid-width` | Number of characters in each row (40–400) | `120` |
| `--char-aspect` | Character width-to-height ratio (0.3–1.0) | `0.5` |
| `--threshold` | Sets the middle tone (0–255) | `128` |
| `--invert` | Reverses the character-density mapping | Off |
| `--auto-contrast` | Adjusts image contrast automatically | Off |
| `--dither` / `--no-dither` | Turns dithering on or off | On |
| `--output` | Sets the output file path | Automatic |

### Examples

Create a portrait with more detail:

```bash
big input/photo.jpg --grid-width 200
```

Turn dithering off:

```bash
big input/photo.jpg --no-dither
```

Adjust contrast automatically:

```bash
big input/photo.jpg --auto-contrast
```

Choose where to save the image:

```bash
big input/photo.jpg --output output/my-portrait.png
```

See all options:

```bash
big --help
```

### Development and Tests

Run the tests:

```bash
pytest
```

Check code style:

```bash
black --check src/
ruff check src/
```

Check packages for known security issues:

```bash
pip-audit
```

### Privacy

The current tool works on your computer. It does not send your photos to a server.

The planned web application aims to process photos in the browser. Photos will not need to be uploaded to a server.

### Roadmap

1. Python command-line tool
2. Better image quality
3. Web application
4. Tests and reliability
5. Release preparation

See [the project roadmap](analysis/04_yol_haritasi.md) for more details.

---

<a id="turkce"></a>

## Türkçe

### Hakkında

Binary Image Generator, fotoğrafları metin tabanlı portrelere dönüştüren bir Python aracıdır. Oluşturulan portreleri PNG olarak kaydeder.

Projenin şu anda komut satırından çalışan bir sürümü vardır. Web uygulaması ise gelecek sürümler için planlanmaktadır.

### Özellikler

- JPEG, PNG ve WebP görsellerini destekler.
- Görselleri gri tonlamaya dönüştürür.
- Portreleri `0`, `1` ve boşluk karakterleriyle oluşturur.
- PNG çıktısında kullanılan fonta göre karakter yoğunluğunu ölçer.
- Görselin orijinal oranlarını korur.
- Görsel detaylarını korumaya yardımcı olan Floyd–Steinberg dithering yöntemini kullanır.
- Otomatik kontrast ayarı sunar.
- Portre genişliğini ve orta ton ayarını değiştirmeye izin verir.
- Sonucu siyah arka plan üzerinde beyaz karakterlerle PNG olarak kaydeder.

### Gereksinimler

- Python 3.10 veya üzeri
- Git

### Kurulum

Projeyi bilgisayarınıza indirin:

```bash
git clone https://github.com/busraknya/binary-img-generator.git
cd binary-img-generator
```

Bir sanal ortam oluşturun ve etkinleştirin.

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Projeyi ve gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
pip install -e .
```

### Kullanım

Aracı bir görsel yolu vererek çalıştırın:

```bash
big path/to/photo.jpg
```

Python üzerinden de çalıştırabilirsiniz:

```bash
python -m binary_img_generator.cli path/to/photo.jpg
```

Oluşturulan PNG dosyası varsayılan olarak `output/` klasörüne kaydedilir.

### Seçenekler

| Seçenek | Açıklama | Varsayılan |
|---|---|---|
| `--grid-width` | Her satırdaki karakter sayısı (40–400) | `120` |
| `--char-aspect` | Karakter genişlik/yükseklik oranı (0.3–1.0) | `0.5` |
| `--threshold` | Orta ton ayarı (0–255) | `128` |
| `--invert` | Karakter yoğunluğu sırasını tersine çevirir | Kapalı |
| `--auto-contrast` | Kontrastı otomatik ayarlar | Kapalı |
| `--dither` / `--no-dither` | Dithering özelliğini açar veya kapatır | Açık |
| `--output` | Çıktı dosyasının konumunu belirler | Otomatik |

### Örnekler

Daha detaylı bir portre oluşturun:

```bash
big input/photo.jpg --grid-width 200
```

Dithering özelliğini kapatın:

```bash
big input/photo.jpg --no-dither
```

Kontrastı otomatik ayarlayın:

```bash
big input/photo.jpg --auto-contrast
```

Görselin kaydedileceği konumu seçin:

```bash
big input/photo.jpg --output output/my-portrait.png
```

Tüm seçenekleri görüntüleyin:

```bash
big --help
```

### Geliştirme ve Testler

Testleri çalıştırın:

```bash
pytest
```

Kod biçimini kontrol edin:

```bash
black --check src/
ruff check src/
```

Paketlerde bilinen güvenlik sorunlarını kontrol edin:

```bash
pip-audit
```

### Gizlilik

Mevcut araç bilgisayarınızda çalışır. Fotoğraflarınızı bir sunucuya göndermez.

Planlanan web uygulamasında fotoğrafların doğrudan tarayıcıda işlenmesi hedeflenmektedir. Fotoğrafların bir sunucuya yüklenmesi gerekmeyecektir.

### Yol Haritası

1. Python komut satırı aracı
2. Görsel kalitesini iyileştirme
3. Web uygulaması
4. Testler ve güvenilirlik
5. Yayına hazırlık

Daha fazla bilgi için [proje yol haritasına](analysis/04_yol_haritasi.md) bakabilirsiniz.
