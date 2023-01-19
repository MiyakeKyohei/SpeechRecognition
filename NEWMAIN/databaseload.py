def fopen():
    f = open('database.txt', 'r', encoding='UTF-8')
    
    datalist = f.readlines()
    
    f.close()
    return datalist
