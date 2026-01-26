# 🎓 Kariyer Danışmanı Discord Botu – CareerSensei

Bu proje, gençler ve kariyer değişikliği düşünen bireyler için  
**kişiselleştirilmiş meslek ve kariyer önerileri** sunmayı amaçlayan  
bir Discord botunun geliştirilmesini kapsamaktadır.

Proje, henüz adı belirlenmemiş bir girişim şirketi için  
geliştirilen **örnek (demo) bir freelance çalışma** senaryosu üzerinden
ele alınmıştır.

CareerSensei, kullanıcıların kendilerini daha iyi tanımalarına yardımcı
olmayı ve farklı kariyer yollarını keşfetmelerini sağlamayı hedefler.

---

## 📌 Proje Tanımı

CareerSensei, Discord üzerinde çalışan bir **kariyer danışmanı botudur**.  
Kullanıcılardan alınan bilgiler doğrultusunda, farklı meslek gruplarını
ve kariyer yollarını analiz eder ve en uygun seçenekleri sunar.

Bot, özellikle:
- kariyerine yeni başlayacak gençler
- alan değiştirmeyi düşünen bireyler
- farklı meslekleri keşfetmek isteyen kullanıcılar

için tasarlanmıştır.

---

## 🎯 Projenin Temel Amaçları

- Kullanıcıların ilgi alanlarını ve güçlü yönlerini analiz etmek  
- Farklı sektörlerdeki kariyer yollarını tanıtmak  
- Kullanıcıya özel, anlaşılır ve yönlendirici öneriler sunmak  
- Discord üzerinde etkileşimli ve erişilebilir bir danışmanlık deneyimi sağlamak  

---

## 🧠 Projenin Temel Felsefesi

CareerSensei, “tek doğru kariyer” anlayışını reddeder.

Bunun yerine:
- farklı yolların
- farklı rollerin
- farklı meslek dallarının

kullanıcıya açık ve şeffaf bir şekilde sunulmasını amaçlar.

Amaç, karar vermek değil; **karar verebilecek bilgi ve farkındalığı kazandırmaktır**.

---

## 🛠 Kullanılan Teknolojiler ve Araçlar

- **Python 3.11**
- **discord.py**
- **pytest**
- **pytest-html**
- **Git & GitHub**
- Kural tabanlı öneri sistemleri

---

## 🧩 Projenin Genel Yapısı

Proje aşağıdaki ana bileşenlerden oluşmaktadır:

- Discord bot çekirdeği  
- Kullanıcıdan veri toplayan komut sistemi  
- Kariyer veri yapısı  
- Kariyer öneri (eşleştirme) algoritması  
- Yardım ve tanıtım modülleri  
- Test altyapısı  

---

## 👤 Kullanıcıdan Alınan Bilgiler (Mevcut Durum)

Demo ve MVP++ kapsamında kullanıcıdan aşağıdaki bilgiler alınmaktadır:

- İlgi alanı  
  - yazılım  
  - tasarım  
  - iletişim  

- Güçlü olduğu yön  
  - analitik  
  - yaratıcı  
  - iletişim  

Bu bilgiler, kariyer öneri algoritmasının temel girdilerini oluşturur.

---

## 🧠 Kariyer Öneri Sistemi

CareerSensei, **kural tabanlı bir puanlama sistemi** kullanır.

Örnek yaklaşım:
- İlgi alanı eşleşmesi → yüksek ağırlık  
- Güçlü yön eşleşmesi → destekleyici ağırlık  

Bu sayede:
- birden fazla kariyer önerisi üretilebilir  
- öneriler uyum düzeyine göre sıralanabilir  

Bu yapı, ileride daha karmaşık algoritmalarla genişletilmeye uygundur.

---

## 🧑‍💻 Mevcut Kariyer Dalları (MVP++)

Şu anki sürümde örnek olarak aşağıdaki alanlar bulunmaktadır:

### Yazılım
- Yazılım Geliştirici  
- Veri Analisti  
- Oyun Programcısı  

### Tasarım
- Grafik Tasarımcı  
- UI/UX Tasarımcısı  

### İletişim
- Dijital Pazarlama Uzmanı  

---

## 🚀 Gelecek Geliştirmeler (2 Haftalık Plan)

Bu proje **tamamlanmış bir MVP++** olmakla birlikte,
önümüzdeki 2 haftalık süreçte aşağıdaki geliştirmelerin yapılması planlanmaktadır.

### Yeni Kariyer Dalları
- Yapay Zeka ve Veri Bilimi  
- Siber Güvenlik  
- Oyun ve Eğlence Sektörü  
- Medya ve İçerik Üretimi  
- İşletme ve Girişimcilik  

### Yeni Roller
- Junior / Mid / Senior seviyeleri  
- Teknik roller  
- Yaratıcı roller  
- Yönetim ve liderlik rolleri  

### Kullanıcıdan Alınacak Ek Bilgiler
- Eğitim durumu  
- Çalışma tercihi (uzaktan / ofis / hibrit)  
- Risk alma isteği  
- Öğrenme hızı ve ilgi derinliği  

---

## 🗄️ Veri Yapısı ve Genişleme Planı

İlerleyen aşamalarda proje:

- Veritabanı (SQLite / PostgreSQL)
- Kullanıcı profili kayıt sistemi
- Kariyer geçmişi ve öneri geçmişi

gibi özelliklerle genişletilecektir.

Bu sayede bot:
- kullanıcıyı zaman içinde tanıyabilecek
- daha isabetli öneriler sunabilecektir.

---

## 🧪 Testler

Projedeki testler, Discord arayüzünden bağımsız olarak
**iş mantığını** test etmek amacıyla yazılmıştır.

- `pytest` kullanılmıştır  
- Temel senaryolar test edilmiştir  
- `pytest-html` ile HTML test raporu oluşturulmuştur  

### Testleri çalıştırmak için:
```bash
python -m pytest
