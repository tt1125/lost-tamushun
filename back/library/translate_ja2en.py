#無駄に技術使ってAPIで実装してみるかも。

#pip install translate

from translate import Translator

def translate_2en_text(text):#オフライン対応
    translater = Translator(from_lang='ja',to_lang='en')
    return translater.translate(text)

#テスト
print(translate_2en_text('ディズニー風の男性'))