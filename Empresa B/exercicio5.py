import numpy

#QUICK SORT
# Dividir para conquistar

def quickSort(array, extremoEsquerdo=0, extremoDireito=None):

    if extremoDireito is not None:
        extremoDireito = extremoDireito 
    else:
        extremoDireito = len(array)

    if extremoEsquerdo < extremoDireito:
        parteParticionada = particao(array, extremoEsquerdo, extremoDireito)
        quickSort(array, extremoEsquerdo, parteParticionada)
        quickSort(array, parteParticionada + 1, extremoDireito)
    return array

def particao(array, extremoEsquerdo, extremoDireito):

    pivo = array[extremoDireito - 1]
    for i in range(extremoEsquerdo, extremoDireito):
        if array[i] > pivo:
            extremoDireito += 1
        else:
            extremoDireito += 1
            extremoEsquerdo += 1
            array[i], array[extremoEsquerdo - 1] = array[extremoEsquerdo - 1], array[i]
    return extremoEsquerdo - 1

#MERGE SORT
#merge você ordena duas metades e uni. Dividindo em duas metades até ter array 

def merge(array, vetorAuxiliar, extremoEsquerdo, meio, extremoDireito):

    for k in range(extremoEsquerdo, extremoDireito + 1):
        vetorAuxiliar[k] = array[k]

    i , j = extremoEsquerdo, meio + 1

    for k in range(extremoEsquerdo, extremoDireito + 1):
        if i > meio:
            array[k] = vetorAuxiliar[j]
            j += 1
        elif j > extremoDireito:
            array[k] = vetorAuxiliar[i]
            i += 1
        elif vetorAuxiliar[j] < vetorAuxiliar[i]:
            array[k] = vetorAuxiliar[j]
            j += 1
        else:
            array[k] = vetorAuxiliar[i]
            i += 1

def mergesort(array, extremoEsquerdo, extremoDireito):

    if extremoDireito <= extremoEsquerdo: #quando o tamanho da parte a ser ordenada é um
        return

    vetorAuxiliar = numpy.zeros(len(array), dtype=int)
    meio = (extremoEsquerdo + extremoDireito)// 2

    mergesort(array,extremoEsquerdo, meio) # Ordena a primeira metade do arranjo.
    mergesort(array, meio + 1, extremoDireito) # Ordena a segunda metade do arranjo.

    merge(array, vetorAuxiliar, extremoEsquerdo, meio, extremoDireito) # Mescla as duas metades ordenadas
