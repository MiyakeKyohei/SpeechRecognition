#完成品
import databaseload
import voice_to_recognition
import pykakasi
import MeCab
import convert_hiragana_kakasi
import textmatching
#import mecab_split

#テキストファイルopen
datalist = databaseload.fopen()

try:
    voice_text = voice_to_recognition.convert_text()#音声認識のファイル呼び込み
    print(voice_text)

    #node = mecab_split.msplit(voice_text)
    
    mecab = MeCab.Tagger()
    node = mecab.parseToNode(voice_text)#MeCab無理
 
    kakasi = pykakasi.kakasi()#インスタンス用
    
    while node:
        
        text = convert_hiragana_kakasi.convert_hiragana(node,kakasi)#ひらがな変換
        
        flag = textmatching.match(text,datalist)#テキストマッチングの結果

        if flag == 1:
            print('終了しました。')
            break
        else:node = node.next#次の単語
 
except:
    print('sorry I could not listen')
