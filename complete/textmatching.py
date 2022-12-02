import os
cmd_file = "0.bat"   # .cmdファイルへのパス
command = cmd_file

def match(text,datalist):
    for w in datalist:
        if text == w.split('\n',1)[0]:#wに\nが含まれているから
            print('音量を0にしました。')
            os.system(command)#音量0
            return 1
        return 0


    