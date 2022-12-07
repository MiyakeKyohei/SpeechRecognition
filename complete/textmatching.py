import os
cmd_file = "0.bat"   # .cmdファイルへのパス
command = cmd_file

def match(text,datalist):
    print(text)
    for index in range(len(datalist)):
        if text == datalist[index].split('\n',1)[0]:#datalistに\nが含まれているから
            print('音量を0にしました。')
            os.system(command)#音量0
            return 1
    return 0


    