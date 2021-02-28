import tkinter as tk
from functools import partial
import os
import time
import datetime
import asyncio
from datetime import datetime
from datetime import timedelta


############################################## CONSTRUÇÃO DA JANELA INICIAL ###########################################################################

janela = tk.Tk()

janela.title("Banco Mobits") #Titulo da janela


#Definições do fundo

janela["bg"] = "#F0F0F0" #Cor de background

#Largura x Altura + Distância do topo do vídeo + Distância da esquerda do video
janela.geometry("280x500+100+100")

#Logo
imagem = tk.PhotoImage(file="imagens/logo.png")
logo= tk.Label(janela, image=imagem)
logo.imagem=imagem
logo.pack()

################################################################# FUNÇÃO DOS BOTÕES ############################################################

def comecar():
    diglogin=txlogin.get() #pega o que foi digitado no login
    digsenha=txsenha.get() #pega o que foi digitado na senha
    if(diglogin in CLIENTES): #Procura login nas chaves do dicionário CLIENTES
        if(CLIENTES[diglogin]==digsenha): #Verifica se a senha é correspondente
            login.place(x=5000, y=5000) #Para mover box da tela
            txlogin.place(x=5000, y=5000) #Para mover box da tela
            senha.place(x=5000, y=5000) #Para mover box da tela
            txsenha.place(x=5000, y=5000) #Para mover box da tela
            erro.place(x=5000, y=5000) #Para mover box da tela
            entrar.place(x=5000, y=5000) #Para mover box da tela
            msg = tk.Label(janela, text="Olá "+DONOCONTA[diglogin],foreground='#058787') #mensagem de boas vindas
            msg.place(x=80, y=110)
            CADASTRO[diglogin].iniciado()
        else:
            erro["text"] = "Sua senha está errada"
    else:
        erro["text"]="Não encontramos esse cadastro"


############################################## BOTÕES LOGIN ######################################

#Login/senha
login = tk.Label(janela, text="Login",foreground='#058787') #caixa com texto
login.place(x=80, y=210)
txlogin = tk.Entry(janela)
txlogin.place(x=80, y=240)
senha = tk.Label(janela, text="Senha",foreground='#058787') #caixa com texto
senha.place(x=80, y=280)
txsenha = tk.Entry(janela, show="*")
txsenha.place(x=80, y=310)
entrar = tk.Button(janela, text="entrar", command=comecar, bg='Orange',activebackground='#058787', foreground='White')
entrar.place(x=110, y=350)
erro = tk.Label(janela, text=" ")
erro.place(x=60, y=380)

################################################ BOTÕES MENU ############################################################

funcao = tk.Label(janela)
funcao.place(x=5000, y=5000)
btnsaldo = tk.Button(janela, text="Saldo", bg='Orange',activebackground='#058787', foreground='White')
btnsaldo.place(x=5000, y=5000)
btnextrato = tk.Button(janela, text="Extrato", bg='Orange',activebackground='#058787', foreground='White')
btnextrato.place(x=5000, y=5000)
btnsaque = tk.Button(janela, text="Saque", bg='Orange',activebackground='#058787', foreground='White')
btnsaque.place(x=5000, y=5000)
btndeposito = tk.Button(janela, text="Depósito", bg='Orange',activebackground='#058787', foreground='White')
btndeposito.place(x=5000, y=5000)
btntransferencia = tk.Button(janela, text="Transferência", bg='Orange',activebackground='#058787', foreground='White')
btntransferencia.place(x=5000, y=5000)
btnvisita = tk.Button(janela, text="Solicitar visita do gerente", bg='Orange',activebackground='#058787', foreground='White')
btnvisita.place(x=5000, y=5000)
btnsair = tk.Button(janela, text="Sair da sua conta", bg='Orange',activebackground='#058787', foreground='White')
btnsair.place(x=5000, y=5000)
btnajuda = tk.Button(janela, text="Ajuda", bg='Orange',activebackground='#058787', foreground='White')
btnajuda.place(x=5000, y=5000)
btnvoltar = tk.Button(janela, text="Voltar", bg='Orange',activebackground='#058787', foreground='White')
btnvoltar.place(x=5000, y=5000)

##################################################### BOTÕES CLASSES ##########################################################


####### SALDO ##########

titlesaldo = tk.Label(janela, text="saldo",foreground='#058787') #caixa com texto
titlesaldo.place(x=5000, y=5000)
valsaldo = tk.Label(janela, text="teste", foreground='#058787') #caixa com texto
valsaldo.place(x=5000, y=5000)

############################################# CRIAÇÃO DE CLASSE ############################################################################

class Cliente:

    def __init__(self, nome, sobrenome, cpf):
        self.nome = nome
        self.sobrenome = sobrenome
        self.cpf = cpf

class Conta(Cliente):

    def __init__(self, ide, cliente, perfil, dinheiro, horario=datetime.now(), nota=[]):
        self.ide = ide #numero da conta e do objeto da classe
        self.titular = cliente #importa objeto da classe cliente
        self.dinheiro = dinheiro #saldo bancário
        self.perfil = perfil #VIP ou Normal
        self.horario = horario #atributo utilizado para saques acima do saldo para clientes vips
        self.nota = nota #lista com movimentações feitas na conta
    
    def atualsaldo(self):
        "Essa função irá atualizar o valor do saldo negativo de acordo com o tempo passado"

        if(self.dinheiro<0):
            agora=datetime.now() #Qual hora é agora?
            passado=agora-self.horario #Quanto tempo passou
            minutos=int(int(passado.seconds)/60) #Conversão de segundos para minutos
            self.dinheiro -= 0.001*minutos*abs(self.dinheiro) #multiplica por 0.001*|self.dinheiro|
            self.getextrato('Taxa por saque especial', -0.001*minutos*abs(self.dinheiro)) #adiciona debito no extrato


    def saldo(self):
        "Função indica o saldo atual na conta"

        self.atualsaldo() #Atualiza o saldo, caso esse seja negativo
        self.limpamenu()
        titlesaldo.place(x=80, y=130)
        valsaldo["text"]="R$"+ str(round(int(self.dinheiro),2))
        valsaldo.place(x=80, y=150)
        btnvoltar.place(x=110, y=180)
        self.voltar()


    def getextrato(self, descricao, movimentacao ):
        "Função envia para o atributo extrato a descrição da movimentação e seu valor"

        data_e_hora_atuais = datetime.now() #Horário da transação
        data_e_hora = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M') #Conversão de formato da hora
        if(movimentacao>0): #se o valor é maior que zero não necessita parênteses
            self.nota+=[data_e_hora+'   '+descricao+'   '+str(movimentacao)]
        else:  #se o valor é menor que zero coloca parênteses
            self.nota+=[data_e_hora+'   '+descricao+'   '+ '('+str(movimentacao)+')']
    

    def extrato(self):
        "Função que imprimi extrato com data-hora, descrição e valor da movimentação"

        print('     Data             Descrição              Valor\n')
        for i in self.nota:
            print(str(i)+'\n')


    def saque(self, valor):
        '''Função que permite saque. Para clientes Vips, esse saque pode ser maio que o saldo. Sendo no entanto
        cobrada uma taxa de 0.1% por minuto, até o valor negativo seja coberto'''

        self.atualsaldo()
        if(self.perfil=='VIP'): #Se o cliente é vip
            if(self.dinheiro>=valor): #se o saldo é maior que o saque
                self.dinheiro-=valor
                print(u'Seu saque foi realizado com sucesso')
                return True
            else: #se o saldo é menor que o saque
                resposta=input('Seu saldo está menor que o valor de saque, gostaria de ainda sim continuar o procedimento.\n'
                +'Lembre-se que terá seu saldo reduzido em 0.1% por minuto até que sejam feitos depósitos suficientes para\n'+
                    'cobrir o saldo negativo. Sim/ Não ')
                if(resposta=='Sim'): #se o cliente quer entrar no cheque especial
                    self.dinheiro-=valor
                    self.horario=datetime.now()
                    self.getextrato('         Saque         ', -valor)
                #else: #se o cliente não quer entrar no cheque especial
                    #self.restaura()
        else:
            if(self.dinheiro>=valor): #se o saldo é maior que o saque
                self.dinheiro-=valor
                self.getextrato('         Saque         ', -valor)
                print('Seu saque foi realizado com sucesso')
                return True
            else:
                print('Infelizmente o valor de saque é menor que seu saldo.')
                return False


    def debita(self, valor):
        "Funçao que debita valores da conta"

        self.atualsaldo()
        self.dinheiro-=valor


    def credita(self, valor):
        "Funçao que credita valores da conta"

        self.atualsaldo()
        self.dinheiro+=valor


    def deposito(self, valor):
        "Depósito irá fazer uma transação positiva para a própria conta"

        self.atualsaldo()
        self.credita(valor)
        self.getextrato('        Depósito       ', valor)
        print('Depósito realizado com sucesso')
    

    def transferencia(self, valor, identificacao):
        '''Transferência é realizada através da passagem de determinado valor da conta para outra. Sendo a mesma limitada
        para clientes perfil Normal, em 1000 reais. A operação cobra taxas de acordo  com o perfil do cliente. Clientes 
        'VIPS' pagam 0.8% do valor transferido, enquanto 'Normais' pagam 8 reais por operação'''

        self.atualsaldo() #atualiza saldo
        def retirada(valor): #função interna que indica se é possível ou não fazer uma transação
            retirada = self.dinheiro-valor
            if(retirada>=0):
                return True
            else:
                return False
        if (retirada(valor) == False):
            print(u'Infelizmente a transação não pôde ser realizada') #saldo inferior a transferência
        else:    
            if(str(self.ide)==identificacao): #erro de transferência para própria conta
                print('Erro! Você não pode transferir para própria conta')
            else:
                if(self.perfil=='Normal'):
                    if(valor>1000): #limitação para clientes perfil 'Normal'
                        print('Infelizmente você não pode fazer uma transação superior a 1000 reais')
                    else:
                        self.debita(8)
                        self.debita(valor)
                        idconta=CONTAS[identificacao] #Buscando no dicionário class conta correspondente a da str
                        idconta.credita(valor)
                        self.getextrato('Taxa de transferência', -8)
                        self.getextrato('   Transferência     ', -valor)
                        print('Você será debitado em 8 reais por essa operação')
                        print(u'Transação realizada com sucesso')
                else:
                    self.debita(0.008*valor)
                    self.debita(valor)
                    idconta=CONTAS[identificacao] #Buscando no dicionário class conta correspondente a da str
                    idconta.credita(valor)
                    self.getextrato(' Taxa de transferência ', -0.008*valor)
                    self.getextrato('    Transferência      ', -valor)
                    print('Você será debitado em'+ str(0.008*valor)+'reais por essa operação')
                    print(u'Transação realizada com sucesso')


    def visita(self):
        "Funcionalidade disponível somente para clientes VIPS, que após confirmação debita em 50 reais a conta do cliente"
        
        self.atualsaldo()
        if(self.perfil=='VIP'):
            confirma = input('Essa operacao irá debitar 50 reais da sua conta. Gostaria de continuar? Sim/ Não ')
            if(confirma==('Sim')):
                self.debita(50) #Caso seja confirmado será realizado o débito
                self.getextrato('  Visita do gerente    ', -50) #Registro no extrato
            else:
                print('Obrigada por ser nosso cliente!')


    def trocaruser(self):
        "Função que faz logout"

        self.atualsaldo() #Atualiza saldo

    def limpamenu(self):
        funcao.place(x=5000, y=5000)
        btnsaldo.place(x=5000, y=5000)
        btnextrato.place(x=5000, y=5000)
        btnsaque.place(x=5000, y=5000)
        btndeposito.place(x=5000, y=5000)
        btntransferencia.place(x=5000, y=5000)
        btnvisita.place(x=5000, y=5000)
        btnsair.place(x=5000, y=5000)
        btnajuda.place(x=5000, y=5000)

    def acertamenuvip(self):
        self.limpabtnclasses()
        funcao.place(x=80, y=130)
        btnsaldo.place(x=110, y=160)
        btnextrato.place(x=110, y=190)
        btnsaque.place(x=110, y=210)
        btndeposito.place(x=110, y=240)
        btntransferencia.place(x=110, y=270)
        btnvisita.place(x=110, y=300)
        btnsair.place(x=110, y=330)
        btnajuda.place(x=110, y=360)
    
    def acertamenunormal(self):
        self.limpabtnclasses()
        funcao.place(x=80, y=130)
        btnsaldo.place(x=110, y=160)
        btnextrato.place(x=110, y=190)
        btnsaque.place(x=110, y=210)
        btndeposito.place(x=110, y=240)
        btntransferencia.place(x=110, y=270)
        btnsair.place(x=110, y=300)
        btnajuda.place(x=110, y=330)


    def limpabtnclasses(self):
        titlesaldo.place(x=5000, y=5000)
        valsaldo.place(x=5000, y=5000)
        btnvoltar.place(x=5000, y=5000)


    def voltar(self):
        if(self.perfil=="VIP"):
            btnvoltar["command"]=partial(self.acertamenuvip)

        else:
            btnvoltar["command"]=partial(self.acertamenunormal)





    def iniciado(self):
        "Função que mostra menu de opções e direciona o usuário de acordo com o seu desejo"
        self.atualsaldo() #Atualiza saldo
        if(self.perfil=='VIP'):
            #menu de funcionalidades para clientes VIPS
            funcao.place(x=80, y=130)
            btnsaldo.place(x=110, y=160)
            btnsaldo["command"]=partial(self.saldo)
            btnextrato.place(x=110, y=190)
            btnsaque.place(x=110, y=210)
            btndeposito.place(x=110, y=240)
            btntransferencia.place(x=110, y=270)
            btnvisita.place(x=110, y=300)
            btnsair.place(x=110, y=330)
            btnajuda.place(x=110, y=360)

        else:
            #menu de funcionalidades para clientes NORMAIS
            funcao.place(x=80, y=130)
            btnsaldo.place(x=110, y=160)
            btnextrato.place(x=110, y=190)
            btnsaque.place(x=110, y=210)
            btndeposito.place(x=110, y=240)
            btntransferencia.place(x=110, y=270)
            btnsair.place(x=110, y=300)
            btnajuda.place(x=110, y=330)

############################################ CRIAÇÃO DE OBJETOS NAS CLASSES ###############################################################################

cliente1 = Cliente('João', 'Silva', '1111111111-1') #Joao
conta1 = Conta('conta1', cliente1, 'Normal', 120.0) #numero, cliente, perfil, dinheiro
cliente2 = Cliente('Maria', 'Silva', '222222222-2') #Maria
conta2 = Conta('conta2', cliente2, 'VIP', 500.0) #numero, cliente, perfil, dinheiro

######################################################## DICT DE LOGIN/ SENHA E CONTAS #########################################################

CLIENTES={'01234': '1234', '56789': '5678'} #login: senha
CADASTRO={'01234': conta1, '56789': conta2} #Cadastro, relação login/ conta
CONTAS={'conta1': conta1, 'conta2': conta2} #conta(str): conta
DONOCONTA={'01234':'João', '56789':'Maria'}
#conta1 é o João e conta2 é a Mária


##################### LOOP ###########################

janela.mainloop()