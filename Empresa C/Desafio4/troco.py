import copy

'Programação dinâmica'

u'''É uma estratégia de resolução que visa otimizar resoluções. Isso é realizado através da memorização de ramos 
comuns. É importante visar que ela não pode ser aplicada para problemas ciclícos'''

def troca(x, b):  #x é o valor e b uma list das moedas válidas
    l_escolhida=[0]*(x+1)
    cont=[0]*(x+1)
    valor = x
    moedas=[]
    listatupla=[]
    for i in range(1,x+1):
      contador=i
      escolhida=1 # possibilidade de trocar tudo em moedas de 1
      for j in b:
          if j<=i: 
              if cont[i-j]+1<contador: 
                  contador=cont[i-j]+1 
                  escolhida=j 
          l_escolhida[i]=escolhida 
          cont[i]=contador 
    while valor>0: # repetir até que o valor zere
        pegar_essa=l_escolhida[valor] 
        moedas.append(pegar_essa) 
        valor=valor-pegar_essa
    for Bi in set(moedas):
        Ni=0
        tmp = copy.copy(moedas)
        while Bi in tmp:
            Ni+=1
            tmp.remove(Bi)
        listatupla.append((Ni,Bi))
    listatupla.sort(key=lambda x: x[1])
    listatupla.reverse()
    print(listatupla) 

#testes

troca(17, [1, 5, 10, 25, 50, 100])
#[(1, 10), (1, 5), (2, 1)]
troca(14, [1, 7, 10])
#[(2, 7)]
troca(10, [2, 3])
#[(2, 3), (2, 2)]