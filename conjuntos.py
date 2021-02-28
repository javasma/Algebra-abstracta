"""Operaciones entre conjuntos"""

def contenido(A,B):
    val = True
    contador = 0
    while val == True:
        for i in A:
            elem = i
            if elem not in B:
                val == False
                break
            contador+=1
        if contador == len(A):
            break
    return val
