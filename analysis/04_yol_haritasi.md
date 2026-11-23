# Proje Yol Haritası

Bu yol haritası, Binary Image Generator projesinin mevcut durumunu ve geliştirme aşamalarını gösterir.

## 1. Python CLI

Fotoğrafları komut satırı üzerinden karakter tabanlı portrelere dönüştüren temel uygulama.

- [x] Python paket yapısının oluşturulması
- [x] Fotoğraf yükleme ve gri tonlamaya dönüştürme
- [x] Karakter tabanlı çıktı oluşturma
- [x] PNG olarak dışa aktarma
- [ ] 0, 1 ve boşluk karakterleriyle dönüşümün tamamlanması

**Tamamlanma ölçütü:** CLI üzerinden verilen bir fotoğrafın istenen karakterlerle dönüştürülerek PNG olarak kaydedilebilmesi.

## 2. Görüntü Kalitesi

Farklı fotoğraflarda tanınabilir ve dengeli sonuçlar elde edilmesi.

- [ ] Karakter eşlemesinin iyileştirilmesi
- [ ] Kontrast ve parlaklık ayarlarının değerlendirilmesi
- [ ] Dithering seçeneklerinin test edilmesi
- [ ] Farklı fotoğraf ve çözünürlüklerle çıktı kalitesinin karşılaştırılması

**Tamamlanma ölçütü:** Yüz hatlarının ve önemli görsel detayların mümkün olduğunca korunması.

## 3. Web Uygulaması

Kullanıcıların herhangi bir kurulum yapmadan fotoğraflarını dönüştürebileceği arayüz.

- [ ] Fotoğraf yükleme alanı
- [ ] Görselin tarayıcıda dönüştürülmesi
- [ ] Dönüştürülmüş sonucun önizlenmesi
- [ ] PNG olarak indirme
- [ ] Farklı ekran boyutlarında kullanılabilir arayüz

**Tamamlanma ölçütü:** Kullanıcının fotoğrafını yükleyip sonucu görebilmesi ve PNG olarak indirebilmesi.

## 4. Test ve Güvenilirlik

Uygulamanın farklı koşullarda doğru ve güvenilir çalışmasının sağlanması.

- [ ] Görsel işleme adımlarının test edilmesi
- [ ] Geçersiz veya desteklenmeyen dosyaların kontrol edilmesi
- [ ] Farklı boyutlardaki görsellerin test edilmesi
- [ ] Hata mesajlarının ve kullanıcı geri bildirimlerinin iyileştirilmesi
- [ ] Performans ve kaynak kullanımının değerlendirilmesi

**Tamamlanma ölçütü:** Yaygın kullanım senaryolarında uygulamanın beklenen şekilde çalışması ve hataların anlaşılır biçimde ele alınması.

## 5. Yayına Hazırlık

Projenin kullanıcılarla paylaşılabilecek ve sürdürülebilecek duruma getirilmesi.

- [ ] README dosyasının Türkçe ve İngilizce hazırlanması
- [ ] Kullanım örneklerinin ve örnek çıktıların eklenmesi
- [ ] Lisans ve kullanım koşullarının belirlenmesi
- [ ] Son testlerin ve güvenlik kontrollerinin yapılması
- [ ] Yayın ortamının hazırlanması

**Tamamlanma ölçütü:** Projenin kurulumu, kullanımı ve sınırları açıkça belgelenmiş; yayınlanmaya hazır olması.
