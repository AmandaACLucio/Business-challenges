#Exercicio 6

#i = taxa em porcentagem; t=tempo; a=depositos mensais; montante = valor desejado
# montante=(a*(1+(i/100))*(((((1+(i/100)))**t)-1)/(i/100)))
# a=(montante)/((1+(i/100))*(((((1+(i/100)))**t)-1)/(i/100)))


def depositaMensalmente():
    
    print("Calculadora de depósitos mensais\n")
    
    while True:
        try:
            idadeAtual = int(input("Qual a sua idade atual? "))
            if not 0 < idadeAtual:
                raise ValueError(idadeAtual)
        except ValueError as e:
            print("Invalid value:", e)
        else:
            break

    while True:
        try:
            idadeFutura = int(input("Em qual idade irá retirar o dinheiro da aplicação? "))
            if not 0 < idadeFutura:
                raise ValueError(idadeFutura)
        except ValueError as e:
            print("Invalid value:", e)
        else:
            break

    while True:
        try:
            quantiaFinal = float(input("Qual a quantia desejada no final? "))
            if not 0 < quantiaFinal:
                raise ValueError(quantiaFinal)
        except ValueError as e:
            print("Invalid value:", e)
        else:
            break

    while True:
        try:
            taxaJuros = float(input("Qual a taxa de juros? (use ponto e não vírgula) "))
            if not 0 < taxaJuros:
                raise ValueError(taxaJuros)
        except ValueError as e:
            print("Invalid value:", e)
        else:
            break

    tempo = (idadeFutura-idadeAtual)*12

    depositosMensais=(quantiaFinal)/((1+(taxaJuros/100))*(((((1+(taxaJuros/100)))**tempo)-1)/(taxaJuros/100)))
   
    depositosMensais=("%.2f" % depositosMensais).replace(".",",")
    quantiaFinal=("%.2f" % quantiaFinal).replace(".",",")

    print("\nVocê precisa depositar R$" + depositosMensais + " mensalmente para obter R$" + quantiaFinal + " no futuro\n")
    
    repetirOperacao = input("Deseja realizar uma nova operação?[sim/não] ")
    if(repetirOperacao==sim):
        return depositaMensalmente()

depositaMensalmente()  





