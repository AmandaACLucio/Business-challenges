import os
import time
import datetime
import asyncio
from datetime import datetime
from datetime import timedelta

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
        print(self.dinheiro)


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
                else: #se o cliente não quer entrar no cheque especial
                    self.restaura()
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
        time.sleep(1)
        print("\n" * os.get_terminal_size().lines) #Limpa a tela
        comecar()


    def restaura(self):
        "Função que irá auxiliar em uma escolha de nova opção"

        time.sleep(0.5)
        resposta = input('Deseja fazer outra operação? Sim/ Não ')
        if(resposta=='Sim'):
            self.iniciado() #Reaparece o menu iniciar
        else:
            comecar() #Sai da conta


    def iniciado(self):
        "Função que mostra menu de opções e direciona o usuário de acordo com o seu desejo"

        valor=0 #reseta variável valor para zero
        self.atualsaldo() #Atualiza saldo
        if(self.perfil=='VIP'):
            print('1. Ver Saldo\n'+
            '2. Extrato\n'+
            '3. Saque\n'+
            '4. Depósito\n'+
            '5. Transferencia\n'+
            '6. Solicitar visita do gerente\n' +
            '7. Sair da sua conta\n'+
            '8. Ajuda') #menu de funcionalidades para clientes VIPs

            funcao = int(input('Escolha uma funcionalidade: ')) #Local para inserir opção do menu

            if(funcao==1): #Saldo
                self.saldo()
                self.restaura()

            elif(funcao==2): #Extrato
                self.extrato()

            elif(funcao==3): #Saque
                valor=float(input('Digite o valor de saque: '))
                self.saque(valor)
                print('Seu saldo agora é '+ str(self.dinheiro))
                self.restaura()

            elif(funcao==4): #Depósito
                valor=float(input('Digite o valor de depósito: '))
                self.deposito(valor)
                print('Seu saldo agora é '+str(self.dinheiro))
                self.restaura()

            elif(funcao==5): #Transferência
                valor=float(input('Digite o valor de Tranferência: '))
                identificacao=input('Digite a identificacao do destinatário: ')
                self.transferencia(valor, identificacao)
                print('Seu saldo agora é '+str(self.dinheiro))
                self.restaura()

            elif(funcao==6 and self.perfil=='VIP'): #Solicitar Visita do Gerente
                self.visita()
                print('Seu saldo agora é '+str(self.dinheiro))
                self.restaura()

            elif(funcao==7): #Sair da conta
                self.trocaruser()

            elif(funcao==8): #Ajuda

                #Informações de funcionalidades disponiveis para os clientes
                print('1. Ver Saldo: Função indica o saldo atual na conta.\n'+
                '2. Extrato: Função que imprimi extrato com data-hora, descrição e valor da movimentação.\n'+
                '''3. Saque: Função que permite saque. Para clientes Vips, esse saque pode ser maio que o saldo. 
                Sendo no entanto cobrada uma taxa de 0.1% por minuto, até o valor negativo seja coberto.\n'''+
                '4. Depósito: Selecione para fazer uma transação positiva para a própria conta\n'+
                '''5. Transferencia: Funcionalidade realizada através da passagem de determinado valor da conta para
                 outra. Sendo a mesma limitada para clientes perfil Normal, em 1000 reais. A operação cobra taxas 
                 de acordo  com o perfil do cliente. Clientes 'VIPS' pagam 0.8% do valor transferido, enquanto 
                 'Normais' pagam 8 reais por operação\n'''+
                '6. Trocar de usuário: Função que irá sair da sua conta\n' +
                '7. Solicitar visita do gerente: Função para clientes VIPS, que debita em 50 reais a conta do cliente\n')
                
                resposta=input('Desejaria voltar para tela de menu? Sim/Não ')
                if(resposta=='Sim'):
                    self.restaura()
                else:
                    self.trocaruser()
            else:
                print('A operação digitada não é válida, tente novamente')
                self.iniciado()
        else:
            print('1. Ver Saldo\n'+
            '2. Extrato\n'+
            '3. Saque\n'+
            '4. Depósito\n'+
            '5. Transferencia\n'+
            '6. Sair da sua conta\n'+
            '7. Ajuda') #menu de funcionalidades para clientes Normais

            funcao = int(input('Escolha uma funcionalidade: ')) #Local para inserir opção do menu

            if(funcao==1): #Saldo
                self.saldo()
                self.restaura()
            
            elif(funcao==2): #Extrato
                print('Em construção')

            elif(funcao==3): #Saque
                valor=float(input('Digite o valor de saque: '))
                self.saque(valor)
                print('Seu saldo agora é '+str(self.dinheiro))
                self.restaura()

            elif(funcao==4): #Depósito
                valor=float(input('Digite o valor de depósito: '))
                self.deposito(valor)
                print('Seu saldo agora é '+str(self.dinheiro))
                self.restaura()

            elif(funcao==5): #Transferência
                valor=float(input('Digite o valor de Tranferência: '))
                identificacao=input('Digite a identificacao do destinatário: ')
                self.transferencia(valor, identificacao)
                print('Seu saldo agora é '+str(self.dinheiro))
                self.restaura()

            elif(funcao==6): #Sair da conta
                self.trocaruser()

            elif(funcao==7): #Ajuda

                #Informações de funcionalidades disponiveis para os clientes
                print('1. Ver Saldo: Função indica o saldo atual na conta.\n'+
                '2. Extrato: Função que imprimi extrato com data-hora, descrição e valor da movimentação.\n'+
                '''3. Saque: Função que permite saque. Para clientes Vips, esse saque pode ser maio que o saldo. 
                Sendo no entanto cobrada uma taxa de 0.1% por minuto, até o valor negativo seja coberto.\n'''+
                '4. Depósito: Selecione para fazer uma transação positiva para a própria conta\n'+
                '''5. Transferencia: Funcionalidade realizada através da passagem de determinado valor da conta para
                 outra. Sendo a mesma limitada para clientes perfil Normal, em 1000 reais. A operação cobra taxas 
                 de acordo  com o perfil do cliente. Clientes 'VIPS' pagam 0.8% do valor transferido, enquanto 
                 'Normais' pagam 8 reais por operação\n'''+
                '6. Trocar de usuário: Função que irá sair da sua conta\n')

                resposta=input('Desejaria voltar para tela de menu? Sim/Não ')
                if(resposta=='Sim'):
                    self.restaura()
                else:
                    self.trocaruser()
            else:
                print('A operação digitada não é válida, tente novamente')
                self.iniciado()

################################################ MENSAGEM INICIAL ####################################################################

print('Bem vindo(a) ao Banco Mobits')
print(' ')

############################################ CRIAÇÃO DE OBJETOS NAS CLASSES ###############################################################################

cliente1 = Cliente('João', 'Silva', '1111111111-1')
conta1 = Conta('conta1', cliente1, 'Normal', 120.0) #numero, cliente, perfil, dinheiro
cliente2 = Cliente('Maria', 'Silva', '222222222-2')
conta2 = Conta('conta2', cliente2, 'VIP', 500.0) #numero, cliente, perfil, dinheiro

######################################### DICT DE LOGIN/ SENHA E CONTAS #########################################################

CLIENTES={'Joao': '1234', 'Maria': '5678'} #login: senha
CADASTRO={'Joao': conta1, 'Maria': conta2} #Cadastro, relação login/ conta
CONTAS={'conta1': conta1, 'conta2': conta2} #conta(str): conta
#conta1 é o João e conta2 é a Mária

############################################### INICIALIZA O SISTEMA ###############################################################

def comecar():
    "Função que irá iniciar o sistema e chamar a função que mostra o menu"

    login=input('Login: ') #inicializa o login
    print(' ')
    if(login in CLIENTES): #Procura login nas chaves do dicionário CLIENTES
        senha=input('senha: ')
        print(' ')
        if(CLIENTES[login]==senha): #Verifica se a senha é correspondente
            print('Olá '+login)
            print(' ')
            CADASTRO[login].iniciado() #Objeto no dicionário CADASTRO é encontrado pela chave 'login'
            return True
        else:
            print('A senha está errada, tente novamente')
            print(' ')
            time.sleep(1)
            print("\n" * os.get_terminal_size().lines) #Limpa tela
            comecar()
            return False
    else:
        print('Não encontramos esse cadastro no nosso resgistro, tente novamente')
        time.sleep(1)
        print("\n" * os.get_terminal_size().lines)
        comecar()
        return False

################################################# CHAMADA DE COMEÇAR #######################################################

comecar() #Chama função começar, que irá iniciar o sistema