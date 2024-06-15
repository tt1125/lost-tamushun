#pip install translate

from translate import Translator

def translate_2en_text(text):#オフライン対応
    translater = Translator(from_lang='ja',to_lang='en')
    return translater.translate(text)

#テスト
# print(translate_2en_text('AI とコグニティブ サービスを使用して、顧客の興味や行動に基づいた、クラウドに接続されたモバイル エクスペリエンスを構築できます。'))