def histograma (s):
    d ={}
    for c in s:
        if c not in d:
            d[c ]=1
        else :
            d[c ]+=1
    return d


hs = histograma("Hola")
print("Ingrese una cadena de caracteres:", hs)