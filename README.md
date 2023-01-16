# Eye-Tracking
Çok disiplinli tasarım projesi kapsamında göz hareketlerine göre bir robot arabanın kontrolünün gerçekleştirilmesi sağlanmıştır. Bu projenin amacı omurilik felci yaşayarak alt ekstremitenin kas gücünü kaybeden insanların göz hareketleri ile yönlendirebilecekleri bir sistem tasarlanmasıdır.
Bu amaç doğrultusunda gerçekleştirilen göz takibi sistemi, göz hareketlerinin yön bilgisinin algılanmasını içermektedir. Bu kapsamda projede sağ, sol, yukarı, aşağı ve merkez konumlarının gerçek zamanlı olarak tespit edilmesi sağlanmıştır.
Bu işlem dlib kütüphanesi yardımıyla yüzdeki landmark'ların bulunması ve göz bölgesinin elde edilip threshold yöntemi ile göz bebeğinin konumunun tespit edilmesine dayanmaktadır.

### Requirements

Projenin çalıştırılabilmesi için bilgisyarınızda Python 3.x versiyonu kurulu olmalıdır.

### Kütüphaneler
- OpenCV
- Numpy
- Dlib
- Time

Projede bulunan eye_tracking kodu içerisinde kameradan alınan yüz görüntüsünden gözün konum bilgisi ekrana yazdırılmaktadır. Bir diğer eye_trackinksajk kodunda ise ekstra olarak bluetooth ile haberleşme kodu da bulunmaktadır.

