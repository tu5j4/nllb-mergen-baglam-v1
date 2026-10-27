# eğitim metinleri

sürüm dosyalarındaki `nllb-mergen-baglam-v1-egitim-txt.zip`, utf-8 txt dosyaları içerir. her satır bağımsız bir json kaydıdır: kaynak, türkçe hedef, önceki kaynak replikler, veri kimliği ve varsa atıf bilgisi. txt uzantısı veriyi okunabilir yapar; zip sıkıştırması dosya boyutunu azaltır. bu metinler modeli çalıştıran ağırlık dosyalarının yerine geçmez.

| dosya | kaynak ve lisans |
|---|---|
| train-tatoeba.txt | [manythings / tatoeba](https://www.manythings.org/anki/), cc-by-2.0-fr; her cümlenin yazar ve cümle kimlikleri `attribution` alanında korunur. |
| train-setimes.txt | [opus setimes v2](https://opus.nlpl.eu/legacy/SETIMES.php), cc-by-sa-3.0; nikola ljubešić tarafından derlenen setimes korpusu. |
| train-context-curriculum.txt | mergen için hazırlanmış sentetik bağlam örnekleri, cc-by-4.0. |

tatoeba atfı: www.manythings.org/anki ve tatoeba.org; cümle sahipleri kayıtların içindedir. setimes atfı: nikola ljubešić; j. tiedemann, 2012, “parallel data, tools and interfaces in opus”, lrec 2012. ön işleme: ingilizce–türkçe eğitim altkümesi seçimi, kalite filtreleme ve kaynak geçmişi alanı ekleme. txt dışa aktarımı kaynak ve hedef metinleri değiştirmez. her dosya kendi lisansını korur; bu veri paketine modelin cc-by-nc lisansı uygulanmaz.

lisanslar: [cc-by-2.0-fr](https://creativecommons.org/licenses/by/2.0/fr/) · [cc-by-sa-3.0](https://creativecommons.org/licenses/by-sa/3.0/) · [cc-by-4.0](https://creativecommons.org/licenses/by/4.0/).

bu paket tüm eğitim kaynaklarının eksiksiz kopyası değildir. ted2020 ve yeniden dağıtım koşulları doğrulanmayan altyazı/opus örnekleri, ham indirmeler, geliştirme/test kayıtları ve yerel çalışma günlükleri yayımlanmaz. bu nedenle paket, bütün eğitimi tek başına yeniden üretme garantisi vermez. kapsam ve kayıt sayıları `manifest.txt` içindedir.
