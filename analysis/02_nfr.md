# Teknik Tasarım ve Kalite Gereksinimleri
## Binary Image Generator

Bu belge, Binary Image Generator'ın nasıl çalışacağını ve hangi kalite koşullarını sağlaması gerektiğini açıklar.

Projenin mevcut kullanım alanı Python CLI aracıdır. Web uygulaması planlanan sonraki geliştirme aşamasıdır. Web sürümünde fotoğrafın sunucuya gönderilmeden tarayıcıda işlenmesi hedeflenir.

---

## 1. Sistem Yapısı

Mevcut Python CLI yerel görüntü işleme ve PNG çıktısı üretir. Web uygulaması geliştirildiğinde aynı temel dönüşüm kurallarının tarayıcı tarafında uygulanması hedeflenir. Kullanıcı hesabı, veritabanı veya fotoğraf saklama sistemi mevcut kapsamda değildir.

## 2. Görüntü İşleme ve Çıktı Kalitesi

Projenin en önemli kalite ölçütü, dönüştürülen portrenin kaynak fotoğraftaki temel detayları mümkün olduğunca korumasıdır.

Dönüşüm sırasında dikkat edilecek noktalar:

- Fotoğrafın doğru şekilde okunması ve hazırlanması.
- Görüntünün gri tonlamaya dönüştürülmesi.
- Kontrast ve parlaklık farklılıklarının yönetilmesi.
- Yüz hatları, gölgeler ve önemli detayların korunması.
- Çıktıda yalnızca `0` ve `1` karakterlerinin kullanılması; boşluk veya başka karakter eklenmemesi.
- Floyd–Steinberg dithering yönteminin varsayılan olarak kullanılması.
- Görüntünün karakter ızgarasına küçültülmesi sırasında detay kaybının azaltılması.
- Oluşturulan portrenin PNG olarak indirilebilmesi.

Karakterlerin açık ve koyu tonları nasıl temsil edeceği, PNG çıktısında kullanılan fontla tutarlı olmalıdır. Görsel kalite, farklı ışık koşulları ve detay seviyelerine sahip aynı örnek fotoğraflar üzerinde, aynı ayarlar kullanılarak karşılaştırılmalıdır.

## 3. Performans, Güvenlik ve Gizlilik

- Görüntü işleme, desteklenen görsel boyutlarında makul sürede tamamlanmalıdır.
- Büyük fotoğraflar işlenmeden önce uygun boyuta indirilebilmelidir.
- Desteklenen en yüksek dosya ve görsel boyutları, gerçek uygulama davranışı doğrulandıktan sonra belgelenmelidir.
- Desteklenmeyen veya bozuk dosyalarda kullanıcıya anlaşılır hata mesajı gösterilmelidir.
- Web tarafında fotoğraflar sunucuya gönderilmemeli ve kalıcı olarak saklanmamalıdır.
- Kullanıcı dosyaları gereksiz yere bellekte tutulmamalıdır.
- İndirilen PNG çıktısına kaynak fotoğrafın hassas EXIF bilgileri taşınmamalıdır.
- Kişisel fotoğraflar ve test amaçlı özel dosyalar Git deposuna eklenmemelidir.
- Kullanılmayan veya güvenlik açığı bulunan bağımlılıklar projede tutulmamalıdır.

## 4. Test ve Kod Kalitesi

Testler geliştirme sürecinin parçası olmalıdır. Yeni bir görüntü işleme davranışı eklendiğinde ilgili testler de güncellenmelidir.

Kontrol edilmesi gereken alanlar:

- Farklı boyut ve formatlardaki fotoğrafların işlenmesi.
- Bozuk veya desteklenmeyen dosyalarda hata yönetimi.
- Çıktıda yalnızca `0` ve `1` karakterlerinin bulunması.
- Floyd–Steinberg dithering çıktısının doğruluğu.
- Karakter eşleme ve PNG çıktısının doğruluğu.
- CLI parametreleri ve hatalı parametrelerin ele alınması.
- Web sürümü geliştirildiğinde fotoğraf yükleme, önizleme ve indirme akışı.
- Web sürümü geliştirildiğinde Python ve tarayıcı çıktılarının görsel açıdan tutarlılığı.

Kod okunabilir, modüler ve bakımı kolay olmalıdır. Projenin ölçeğini aşan mimari ve araçlardan kaçınılmalıdır.
