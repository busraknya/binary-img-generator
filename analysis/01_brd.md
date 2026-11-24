# İş Gereksinimleri Dokümanı
## Binary Image Generator

## 1. Projenin Tanımı

Binary Image Generator, kullanıcının yüklediği bir fotoğrafı yalnızca `0` ve `1` karakterlerinden oluşan bir portreye dönüştüren bir araçtır.

Projenin amacı, fotoğrafları yalnızca siyah-beyaz hâle getirmek değil, fotoğraftaki yüz hatlarını, gölgeleri ve önemli görsel detayları mümkün olduğunca koruyarak estetik bir binary portre oluşturmaktır.

Ürün iki kullanım şekli sunar:

- **Web uygulaması:** Kullanıcı fotoğrafını yükler, dönüştürülmüş portresini görüntüler ve PNG olarak indirir.
- **Yerel kullanım:** Geliştirici, bilgisayarındaki fotoğrafları komut satırı üzerinden dönüştürerek PNG çıktısı alabilir.

## 2. Projenin Amacı

Projenin üç temel amacı vardır:

1. **Kullanılabilir bir araç geliştirmek:** Herhangi bir kullanıcının fotoğrafını kolayca binary portreye dönüştürebilmesini sağlamak.
2. **Kaliteli sonuç üretmek:** Fotoğrafın tanınabilirliğini ve önemli görsel detaylarını koruyan çıktılar oluşturmak.
3. **Açık kaynak olarak paylaşmak:** Projeyi GitHub üzerinden yayınlayarak başkalarının da kullanabilmesini ve geliştirebilmesini sağlamak.

## 3. Ürün Kapsamı

### 3.1 Kapsam Dahilinde

- JPEG, PNG ve WebP formatlarında fotoğraf kabul etmek.
- Fotoğrafı yalnızca `0` ve `1` karakterlerinden oluşan bir portreye dönüştürmek.
- Fotoğrafın en-boy oranını mümkün olduğunca korumak.
- Yüz hatlarını ve önemli görsel detayları korumaya odaklanmak.
- Kullanıcıya dönüştürülmüş portrenin önizlemesini göstermek.
- Görsel kalitesini iyileştirmek için temel ayarlar sunmak.
- Oluşturulan portreyi PNG olarak indirmek.
- Yerel kullanım için komut satırı üzerinden PNG üretimini desteklemek.
- Türkçe ve İngilizce anlaşılır kullanım ve hata açıklamaları sağlamak.
- Projeyi GitHub üzerinde açık kaynak olarak yayınlamak.

### 3.2 Kapsam Dışında

İlk sürümde aşağıdaki özellikler bulunmayacaktır:

- Kullanıcı hesabı ve giriş sistemi.
- Veritabanı ve kullanıcı verilerinin kalıcı olarak saklanması.
- Fotoğrafların sunucuya yüklenerek işlenmesi.
- Birden fazla fotoğrafı toplu dönüştürme.
- Renkli binary portre üretimi.
- `0` ve `1` dışında farklı karakter setleriyle ASCII sanat üretimi.
- Mobil uygulama.
- Kullanıcılar arasında görsel paylaşımı veya sosyal özellikler.

## 4. Kullanıcılar ve Kullanım Amaçları

| Kullanıcı | İhtiyaç |
|---|---|
| Web uygulaması ziyaretçisi | Fotoğraf yükleyip binary portresini oluşturmak ve indirmek. |
| Geliştirici | Fotoğrafları yerel ortamında dönüştürmek ve projeyi geliştirmek. |
| GitHub ziyaretçisi | Projeyi incelemek, çalıştırmak ve açık kaynak koddan yararlanmak. |

## 5. Ürün Gereksinimleri

### 5.1 Fotoğraf Yükleme (BR-01)

Kullanıcı, web uygulamasına veya yerel araca bir fotoğraf sağlayabilmelidir.

- JPEG, PNG ve WebP formatları desteklenmelidir.
- Desteklenmeyen veya bozuk dosyalar kabul edilmemelidir.
- Çok küçük veya işlenmesi uygun olmayan görseller için anlaşılır hata mesajı verilmelidir.
- Fotoğrafın yönü doğru algılanmalıdır.
- Görselin en-boy oranı korunmalıdır.

### 5.2 Binary Portre Oluşturma (BR-02)

Sistem, yüklenen fotoğrafı yalnızca `0` ve `1` karakterleriyle temsil edilen bir portreye dönüştürmelidir.

- `0` ve `1` görselin iki farklı ton seviyesini temsil etmelidir.
- Karakterlerin kullanımı sonucunda fotoğrafın önemli detayları mümkün olduğunca korunmalıdır.
- Yüz, göz, burun ve ağız gibi belirgin hatların tanınabilir olması hedeflenmelidir.
- Tüm satırlar tutarlı bir karakter düzenine sahip olmalıdır.
- Görselin oranı bozulmamalıdır.
- Çıktıda boşluk veya başka karakter kullanılmamalıdır.

### 5.3 Görsel Kalitesi (BR-03)

Kaliteli çıktı, ürünün temel gereksinimlerinden biridir.

Sistem:

- Fotoğrafın aydınlık ve karanlık bölgelerini ayırt edebilmelidir.
- İki ton arasındaki geçişleri mümkün olduğunca başarılı temsil etmelidir.
- Yüz hatlarının kaybolmasına neden olan aşırı kontrasttan kaçınmalıdır.
- Görsel detayları korumak için uygun ton dağılımı ve dithering yöntemlerini desteklemelidir.
- Farklı fotoğraf türlerinde kabul edilebilir sonuçlar üretmelidir.

Varsayılan ayarlar, kullanıcının ek bir işlem yapmasına gerek kalmadan dengeli ve estetik bir sonuç oluşturmayı hedeflemelidir. Floyd–Steinberg dithering varsayılan yöntemdir.

### 5.4 Görsel Ayarları (BR-04)

Kullanıcı, oluşturulan portrenin görünümünü iyileştirebilmelidir.

İlk sürüm için değerlendirilmesi gereken ayarlar:

- Parlaklık
- Kontrast
- Karakter yoğunluğu / detay seviyesi
- Dithering açma ve kapatma
- Açık ve koyu alanların ters çevrilmesi

Ayarlar anlaşılır isimlerle sunulmalı ve kullanıcı değişikliklerin sonucunu önizlemede görebilmelidir.

### 5.5 Önizleme (BR-05)

- Kullanıcı dönüştürülmüş portresini web uygulamasında görebilmelidir.
- Ayarlarda yapılan değişiklikler önizlemeye yansıtılmalıdır.
- Önizleme, indirilecek PNG ile aynı görsel sonucu temsil etmelidir.
- Kullanıcı isterse başlangıç ayarlarına dönebilmelidir.

### 5.6 PNG Çıktısı (BR-06)

- Oluşturulan portre PNG formatında indirilebilmelidir.
- Çıktı yüksek çözünürlüklü olmalıdır.
- Görselin en-boy oranı korunmalıdır.
- Arka plan ve karakter renkleri okunabilir olmalıdır.
- Kullanıcının özel fotoğraf bilgileri veya EXIF verileri çıktı dosyasına taşınmamalıdır.
- İndirilen dosya, önizlemede görülen karakter düzeniyle tutarlı olmalıdır.
- Çıktı yalnızca `0` ve `1` karakterlerini içermelidir.

### 5.7 Gizlilik (BR-07)

- Kullanıcının fotoğrafı izni olmadan başka bir yerde saklanmamalıdır.
- Fotoğrafın işlenmesi için sunucuya gönderilmesi gerekmemelidir.
- Kullanıcı fotoğrafı üzerinde işlem yaparken gizliliği korunmalıdır.
- Kullanıcı hesabı veya veritabanı gerektiren bir işlem bulunmamalıdır.

### 5.8 Yerel Kullanım (BR-08)

Geliştirici, projeyi kendi bilgisayarında çalıştırarak fotoğrafları PNG formatında dönüştürebilmelidir.

- İşlem tek bir komutla başlatılabilmelidir.
- Kullanıcı giriş dosyasını ve desteklenen ayarları belirleyebilmelidir.
- Oluşturulan çıktı belirtilen klasöre kaydedilmelidir.
- Hatalı girişlerde anlaşılır hata mesajı verilmelidir.

### 5.9 Açık Kaynak Yayını (BR-09)

GitHub deposunda aşağıdakiler bulunmalıdır:

- Projeyi açıklayan README.
- Kurulum ve çalıştırma talimatları.
- Kullanım örnekleri.
- Örnek binary portre çıktıları.
- Açık kaynak lisansı.

## 6. Başarı ve Kabul Kriterleri

İlk sürümün tamamlanmış sayılması için:

- [ ] Kullanıcı JPEG, PNG veya WebP fotoğrafı yükleyebilmelidir.
- [ ] Sistem fotoğrafı yalnızca `0` ve `1` karakterleriyle dönüştürebilmelidir.
- [ ] Çıktıda boşluk veya başka karakter bulunmamalıdır.
- [ ] Oluşturulan portrede yüz hatları mümkün olduğunca tanınabilir olmalıdır.
- [ ] Farklı ışık ve kontrast koşullarındaki fotoğraflarda kabul edilebilir sonuç alınmalıdır.
- [ ] Kullanıcı temel görsel ayarlarını değiştirebilmelidir.
- [ ] Önizleme yapılan değişiklikleri doğru göstermelidir.
- [ ] Kullanıcı sonucu yüksek çözünürlüklü PNG olarak indirebilmelidir.
- [ ] Önizleme ve indirilen dosya birbiriyle tutarlı olmalıdır.
- [ ] Fotoğraflar sunucuya gönderilmeden işlenebilmelidir.
- [ ] Geçersiz dosyalarda anlaşılır hata mesajları verilmelidir.
- [ ] Yerel kullanım komut satırı üzerinden çalışmalıdır.
- [ ] README, projeyi yeni bir kullanıcının kurup çalıştırmasına yetecek açıklıkta olmalıdır.

## 7. Terimler Sözlüğü

| Terim | Açıklama |
|---|---|
| Binary portre | Bir fotoğrafın yalnızca 0 ve 1 karakterleriyle temsil edilen görsel hâli. |
| Grayscale | Fotoğrafın renklerden arındırılarak gri tonlarla temsil edilmesi. |
| Karakter yoğunluğu | Kullanılan karakterlerin görselde oluşturduğu koyuluk ve doluluk seviyesi. |
| Dithering | Ara tonları küçük desenlerle temsil ederek görsel detayları korumaya yardımcı olan teknik. |
| Önizleme | Kullanıcının indirmeden önce oluşturulan sonucu görebildiği alan. |
| PNG | Kayıpsız görsel dosyası formatı. |
| EXIF | Fotoğraflarda bulunabilen çekim tarihi, konum ve kamera bilgileri gibi meta veriler. |
| MVP | Ürünün temel ihtiyaçları karşılayan ilk kullanılabilir sürümü. |
