# nllb mergen bağlam v1

nllb-200 distilled 1.3b tabanlı, **ingilizce–türkçe bağlamlı çeviri** için lora uyarlaması ve yerel çalıştırma kodu.

- güncel replik, önceki en fazla üç kaynak replikle birlikte değerlendirilir.
- encoder geçmişi okur; decoder her repliğin güncel metnine özel dikkat maskesi kullanır.
- gpu üzerinde lora bellekte birleştirilir ve en fazla üç replik birlikte işlenir. diskteki ağırlıklar değiştirilmez.
- geçmiş açıkça verilir; birbirinden bağımsız konuşmaların bağlamı otomatik karıştırılmaz.

## kullanım

python 3.12 ve cihazına uygun pytorch kurulumu gerekir. cpu ile başlamak için:

```console
python -m pip install torch==2.11.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
python prepare_model.py
python translate.py --device cpu --text "I will protect her." --previous "Hana is my little sister."
```

nvidia için pytorch'un cihazına ve sürücüne uygun cuda paketini kur, ardından `--device cuda:0` kullan. model hazırlama sabit sürüm dosyalarını indirir, kayıpsız açar ve sha256 özetlerini doğrular. yaklaşık 2 gb indirme ve açılan ağırlıklarla geçici dosyalar için ek disk alanı gerekir. ilk hazırlamadan sonra çeviri çevrimdışı çalışır.

```python
from mergen_context import Translator

translator = Translator("weights", device="cuda:0")
result = translator.translate(
    ["I will protect her.", "She can count on me."],
    previous_sources=["Hana is my little sister."],
)
print(result)
```

her konuşma için yalnızca o konuşmaya ait `previous_sources` ver. giriş geçmişi değiştirilmez. en fazla üç geçmiş replik ve 384 kaynak tokenı kullanılır; sınır aşılırsa en eski geçmiş çıkarılır. güncel replik tek başına sınırı aşarsa hata döner. çıktı sınırı 192 token ve arama genişliği 4'tür.

## kapsam ve lisans

uyarlama ingilizce–türkçe için eğitilmiştir; diğer dillerde aynı kalite garanti edilmez. ocr bu repoya dahil değildir. gerçek ekran gecikmesi ocr, replik uzunluğu, balon sayısı ve donanıma bağlıdır.

taban model: [meta ai / nllb team, nllb-200 distilled 1.3b](https://huggingface.co/facebook/nllb-200-distilled-1.3B), “no language left behind: scaling human-centered machine translation”, 2022. değişiklikler: bf16 taban kopyası, lora uyarlaması, kaynak geçmişi biçimi, güncel repliğe özel cross-attention maskesi ve başlangıç kekelemesini koruyan çıktı işlemesi.

model ağırlıkları ve türev uyarlama **cc-by-nc-4.0** koşullarına tabidir; ticari kullanım izni verilmez. bkz. [model lisansı](MODEL-LICENSE.txt). bu repodaki çalıştırma kodu [mit](LICENSE) lisanslıdır. masaüstü uygulaması: [mergen](https://github.com/tu5j4/mergen).
