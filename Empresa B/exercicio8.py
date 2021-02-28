import threading
import timeit
import random
import numpy
import pylab 

tamanhoVetor= [10**5, 10**6, 10**7, 10**8, 10**9] 
quantidadesThreads = [1, 2, 4, 8, 16]

def gerandoVetor(tamanhoVetor):
    vetor = numpy.zeros(tamanhoVetor)

    for posicao in range(tamanhoVetor):
        sinal = 1 if random.random() < 0.5 else -1
        valorRandom = random.random()*50*sinal
        vetor[posicao] = valorRandom
    return vetor

class myThread (threading.Thread):

    def __init__(self, threadID, nome, soma, lista):

        threading.Thread.__init__(self)
        self.threadID = threadID
        self.nome = nome
        self.soma = soma
        self.lista = lista
        #self.threadLock = threadLock

    def run(self):

        print("Iniciando " + self.nome+"\n")

            # Trava para sicronizar threads
            #threadLock.acquire()

        for numero in self.lista:
            self.soma+=numero
    
            # Bloqueio livre para liberar próxima thread
            #threadLock.release()

#threadLock = threading.Lock()


def criarThreads(quantidadeThreads, tamanhoVetor):

    #vetor=gerandoVetor(tamanhoVetor)
    tempoInicial = timeit.default_timer()

    threads = []
    divisaoVetor = tamanhoVetor/quantidadeThreads
    
    inicio=0
    fim = 0

    for i in range(quantidadeThreads):
        
        inicio = fim
        fim += int(divisaoVetor)

        if(i==(quantidadeThreads-1)):
            fim = tamanhoVetor

        fatia = gerandoVetor(fim-inicio)
        #fatia=vetor[inicio:fim]
        print(fatia)


        thread = myThread(i, "Thread-"+str(i), 0, fatia)
        thread.start()
        threads.append(thread)
    
    somaTotal = 0

    # Espera threads terminarem ciclo

    for thread in threads:
        thread.join()
        somaTotal+=thread.soma

    print("A soma total do vetor é %f" % (somaTotal))

    tempoFinal = timeit.default_timer()
    return(tempoFinal - tempoInicial)

def criarGrafico(tamanhoVetor, quantidadesThreads):
    
    times = []
    
    for quantidadeThread in quantidadesThreads:
        time = criarThreads(quantidadeThread, tamanhoVetor)
        times.append(time)

    pylab.plot(times, quantidadesThreads, 'o')
    pylab.title('Tempo x Threads para N = '+str(tamanhoVetor),fontsize=15)

    pylab.xlabel('Tempo (sec)', fontsize=12)

    pylab.grid(True)
    pylab.savefig('Tempo x Threads para N = '+str(tamanhoVetor)+'.png',dpi=600) 
    pylab.show()

for n in tamanhoVetor:
    criarGrafico(n, quantidadesThreads)