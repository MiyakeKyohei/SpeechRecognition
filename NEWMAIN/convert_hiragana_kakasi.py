def convert_hiragana(node,kakasi):
    
    result = kakasi.convert(node.surface)#変換
    
    text = result[0]['hira']#平仮名を取り出す
    return text