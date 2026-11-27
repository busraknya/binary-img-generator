# Proje Yol Haritası

Bu yol haritası, Binary Image Generator projesinin mevcut durumunu ve geliştirme aşamalarını gösterir.

## 1. Python CLI

Fotoğrafları komut satırı üzerinden karakter tabanlı portrelere dönüştüren temel uygulama.

- [x] Python paket yapısının oluşturulması
- [x] Fotoğraf yükleme ve gri tonlamaya dönüştürme
- [x] Karakter tabanlı çıktı oluşturma
- [x] PNG olarak dışa aktarma
- [x] Çıktının yalnızca `0` ve `1` karakterlerinden oluşturulması

**Tamamlanma ölçütü:** CLI üzerinden verilen bir fotoğrafın istenen karakterlerle dönüştürülerek PNG olarak kaydedilebilmesi.

## 2. Görüntü Kalitesi

Farklı fotoğraflarda tanınabilir ve dengeli sonuçlar elde edilmesi.

- [ ] Karakter eşlemesinin iyileştirilmesi
- [ ] Kontrast ve parlaklık ayarlarının değerlendirilmesi
- [ ] Dithering seçeneklerinin test edilmesi
- [ ] Farklı fotoğraf ve çözünürlüklerle çıktı kalitesinin karşılaştırılması

**Tamamlanma ölçütü:** Yüz hatlarının ve önemli görsel detayların mümkün olduğunca korunması.

## 3. Test ve Güvenilirlik

Görüntü işleme ve CLI davranışının farklı koşullarda doğru çalıştığından emin olmak.

- [ ] Desteklenen dosya formatlarını ve geçersiz girişleri test etme
- [ ] Çıktıda yalnızca `0` ve `1` bulunduğunu doğrulama
- [ ] Eşikleme ve dithering seçeneklerini test etme
- [ ] Farklı görsel boyutlarında çıktı kalitesini ve kaynak kullanımını kontrol etme
- [ ] Testleri ilgili her değişiklikte çalıştırma

**Tamamlanma ölçütü:** Temel dönüşüm ve hata senaryolarının otomatik testlerle kontrol edilmesi.

## 4. Web Uygulaması

Kullanıcıların herhangi bir kurulum yapmadan fotoğraflarını dönüştürebileceği arayüz.

- [ ] Fotoğraf yükleme alanı
- [ ] Görselin tarayıcıda dönüştürülmesi
- [ ] Dönüştürülmüş sonucun önizlenmesi
- [ ] PNG olarak indirme
- [ ] Farklı ekran boyutlarında kullanılabilir arayüz

**Tamamlanma ölçütü:** Kullanıcının fotoğrafını yükleyip sonucu görebilmesi ve PNG olarak indirebilmesi.

## 5. Yayına Hazırlık

Projenin kullanıcılarla paylaşılabilecek ve sürdürülebilecek duruma getirilmesi.

- [ ] README dosyasının Türkçe ve İngilizce hazırlanması
- [ ] Kullanım örneklerinin ve örnek çıktıların eklenmesi
- [ ] Lisans ve kullanım koşullarının belirlenmesi
- [ ] Son testlerin ve güvenlik kontrollerinin yapılması
- [ ] Yayın ortamının hazırlanması

**Tamamlanma ölçütü:** Projenin kurulumu, kullanımı ve sınırları açıkça belgelenmiş; yayınlanmaya hazır olması.
