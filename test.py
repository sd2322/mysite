to_translate = "Кліторальний бальзам від бренду Bijoux Indiscrets допоможе жінці досить швидко відчути збудження за рахунок ефекту зігрівання та як наслідок - приливу крові до інтимних органів. Використовуйте його самостійно для пестощів клітора пальчиками, під час використання секс-іграшок або ж в парі, для незабутнього сексу"

from deep_translator import GoogleTranslator


translated_ge = GoogleTranslator(source='uk', target='de').translate(to_translate)
translated_ru = GoogleTranslator(source='uk', target='ru').translate(to_translate)
translated_eng = GoogleTranslator(source='uk', target='en').translate(to_translate)

print(translated_ge)
print(translated_ru)
print(translated_eng)