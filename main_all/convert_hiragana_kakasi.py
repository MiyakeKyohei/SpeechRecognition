def convert_hiragana(node,kakasi):
    print(node.surface)#テキスト化されたワード
    
    result = kakasi.convert(node.surface)#変換
    
    text = result[0]['hira']#平仮名を取り出す
    return text