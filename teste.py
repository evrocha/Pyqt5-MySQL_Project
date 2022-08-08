
def buscar(palavra):
    # str(palavra).capitalize
    lista = [
        'maca',
        'banana',
        'limao'
    ]
    lista.append(palavra)
    print(lista, " -----------")
    for x in lista:
        print(len(x), " vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
        for i in x:
            print(i[0])
    # print(lista)
buscar("aooo")