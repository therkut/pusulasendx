# Haftalık Otomatik Sabit Tweet Gönderici

Bu proje, Twitter hesabınıza **her hafta Pazartesi günü Türkiye saati ile 10:00'da** otomatik olarak sabit tweet göndermek için hazırlanmıştır.

## Özellikler

- Eski sabit tweet'i otomatik siler
- Dinamik tarih içeren yeni tweet oluşturur
- Sabit bir Google Sheets linki ekler
- Sabit bir görsel (static.jpg) yükler
- Yeni tweet'i otomatik olarak sabitler

## Kurulum

1. Twitter API v2 erişim bilgilerini alın.
2. Bu bilgileri GitHub Secrets kısmına ekleyin:
   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_SECRET`
   - `TWITTER_BEARER_TOKEN`
3. Depoya `static.jpg` dosyasını ekleyin.
4. Workflow dosyası otomatik olarak çalışacaktır.

## Çalıştırma

Manuel tetiklemek için:  
**Actions → Weekly Tweet → Run workflow**
