import MeCab

def msplit(voice):
    mecab = MeCab.Tagger()
    node = mecab.parseToNode(voice)
    return node
    