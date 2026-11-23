# Teknik Tasarım ve Kalite Gereksinimleri
## Binary Image Generator

Bu belge, Binary Image Generator'ın nasıl çalışacağını ve hangi kalite koşullarını sağlaması gerektiğini açıklar.

Proje iki kullanım alanına sahiptir:

- **Python CLI:** Bilgisayarda bulunan bir fotoğrafı komut satırından dönüştürme.
- **Web uygulaması:** Kullanıcının tarayıcıdan fotoğraf yükleyip binary portresini oluşturması ve PNG olarak indirmesi.

Web uygulamasında fotoğraf sunucuya gönderilmez; mümkün olduğunca tüm görüntü işleme kullanıcının tarayıcısında yapılır.

---

## 1. Sistem Yapısı

Python ve web tarafı aynı ürünün iki farklı kullanım alanıdır.

- Python tarafı yerel görüntü işleme ve PNG çıktısı üretir.
- Web tarafı fotoğrafı tarayıcıda işler, sonucu önizler ve indirme olanağı sunar.
- Kullanıcı hesabı, veritabanı veya fotoğraf saklama sistemi bulunmaz.
- Web uygulaması bir sunucuya fotoğraf yüklemeyi gerektirmez.

Web tarafındaki teknik uygulama yöntemi, kalite ve performans denemeleri sonucunda kesinleştirilecektir.

## 2. Görüntü İşleme ve Çıktı Kalitesi

Projenin en önemli kalite ölçütü, dönüştürülen portrenin kaynak fotoğraftaki temel detayları mümkün olduğunca korumasıdır.

Dikkat edilecek noktalar:

- Fotoğrafın doğru şekilde okunması ve hazırlanması.
- Görüntünün gri tonlamaya dönüştürülmesi.
- Kontrast ve parlaklık farklılıklarının yönetilmesi.
- Yüz hatları, gölgeler ve önemli detayların korunması.
- `0`, `1` ve boşluk karakterlerinin dengeli kullanılması.
- Gerekli durumlarda dithering gibi görüntü işleme yöntemlerinin değerlendirilmesi.
- Oluşturulan portrenin PNG olarak indirilebilmesi.

En iyi sonucu veren karakter eşleme ve görüntü işleme yöntemi denemelerle belirlenecektir. Henüz kesinleşmemiş algoritmalar zorunlu teknik karar olarak kabul edilmeyecektir.

## 3. Performans, Güvenlik ve Gizlilik

- Görüntü işleme makul sürede tamamlanmalıdır.
- Büyük fotoğraflar işlenmeden önce uygun boyuta indirilebilmelidir.
- Desteklenmeyen veya bozuk dosyalarda kullanıcıya anlaşılır hata mesajı gösterilmelidir.
- Web tarafında fotoğraflar sunucuya gönderilmemeli ve kalıcı olarak saklanmamalıdır.
- Kullanıcı dosyaları gereksiz yere bellekte tutulmamalıdır.
- İndirilen PNG çıktısına kaynak fotoğrafın hassas EXIF bilgileri taşınmamalıdır.
- Kişisel fotoğraflar ve test amaçlı özel dosyalar Git deposuna eklenmemelidir.
- Kullanılmayan veya güvenlik açığı bulunan bağımlılıklar projede tutulmamalıdır.

## 4. Test ve Kod Kalitesi

Geliştirme sırasında aşağıdaki alanlar kontrol edilmelidir:

- Farklı boyut ve formatlardaki fotoğrafların işlenmesi.
- Bozuk veya desteklenmeyen dosyalarda hata yönetimi.
- Karakter eşleme ve PNG çıktısının doğruluğu.
- Web tarafında fotoğraf yükleme, önizleme ve indirme akışı.
- Farklı ekran boyutlarında kullanılabilirlik.
- Python ve web tarafındaki sonuçların görsel açıdan tutarlılığı.

Mevcut Python modülleri için otomatik testler kullanılmaya devam edilmelidir. Web tarafı geliştirildiğinde ilgili testler de eklenmelidir.

Kod okunabilir, modüler ve bakımı kolay olmalıdır. Projenin ölçeğini aşan mimari ve araçlardan kaçınılmalıdır.
