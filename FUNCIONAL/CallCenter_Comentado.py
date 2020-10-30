#import os
fila = [] #array para fila de espera de chamadas
status = {"A": "available", "B": "available"} #dicionario para validar o status do respectivo operador.
#CASO QUEIRA ADICIONAR MAIS OPERADORES BASTA ALIMENTAR O DICIONARIO, INSERINDO O OPERADOR E DECLARANDO SEU STATUS COMO AVAILABLE
atendeu = {} #dicionario para identificar a ultima chamada atendida pelo respectivo operador. Exemplo: {"A": 1, "B": 2}
rejeicao = {} #dicionario para identificar a ultima chamada rejeitada pelo operador. Exemplo: {"A": 1, "B": 2}
tocando = {} #dicionario para identificar as chamadas que estão tocando para o respectivo operador. Não é tão necessário, será util na exibição do menu mais 
#como já foi criado será utilizado no decorrer do codigo  Exemplo: {"A": 1, "B": 2}

while True:
    #exibindo o menu de opções do programa durante sua execução
    print('\n-------------------------------------------------------------')
    print('Queue = '+str(fila))
    for i in status: #corre o dicionario Status e dependendo do status de cada operador, imprimi de uma forma diferente na tela
        if(status[i] == 'ringing'): 
            print('Status {}: {}-> call {}'.format(i, status[i], tocando[i])) #para status tocando
        elif(status[i] == 'busy'): 
            print('Status {}: {}-> call {}'.format(i, status[i], atendeu[i])) #para status ocupado
        else: 
            print('Status {}: {}'.format(i, status[i])) #para status disponível
        
    opcao = str(input('\nOpção:..>> '))

    ##################################  LIGAR   ############################################
    if ('call' in opcao): #se a cadeia 'call' estiver dentro da entrada de dados opcao entrar no laço abaixo 
        elemento = int(opcao[5:]) #elemento recebe a 5ª cadeia de caracter e o que tiver na frente da variavel opcao, que será a qual ligação será recebida
        #A mesma técnica acima será utilizada para capturar o caracter necessário para as outras operações: "call _, answer _, reject _, hangup _"
        
        print('Call {} received'.format(elemento))

        encontrou=False #variavel booleana que será usada para validar se tal laço foi executado. Será utilizada em todo o código
        for i in status: #Para fazer as condições será necessário correr um for com no dicionário, nesse caso correr dicionario Status para verificar quem é o primeiro a estar disponível
            if (status[i] == 'available'): #Se o status do respectivo operador estiver diponível, chamada tal estará tocando para ele   
                print('Call {} ringing for operator {}'.format(elemento, i)) #i imprime o operador do laço que está correndo
                status[i] = 'ringing' #Atualiza o status do respectivo operador
                tocando[i] = elemento #Atualiza a ligação que está tocando para o respectivo operador 
                encontrou=True #Indentifica que encontrou algum operador disponível
                break
        if encontrou == False: #Se não encontrou nenhum operador disponível adiciona a ligação na fila de espera
            fila.append(elemento)
            print('Call {} waiting in queue'.format(elemento))        
        
    ##################################  RESPOSTA   ############################################
    elif ('answer' in opcao): 
        elemento = opcao[7:] 

        encontrou=False 
        for i in tocando: #Correndo Tocando para validar qual a ligação correta que o operador digitado está atendendo
            if (i==elemento and status[i]=='ringing'): #Se operador for igual ao operador que atendeu     
                atendeu[i] = tocando[i] #Atualiza a ligação atendida pelo respectivo operador 
                print('Call {} answered by operator {}'.format(atendeu[i], i))
                status[i]='busy'  
                encontrou=True
        if encontrou==False: #Se não encontrou é pq não existe ligações tocando para o operador
            print('NO CONNECTIONS TO THE OPERATOR {}'.format(elemento))
        
        #Note que todos a referencia i do for é a mesma para todos os dicionários pois i é o operador que no dicionario Status guarda o status e 
        # nos outros dicionários as ligações. Então quando corro qualquer dicionário o i será o mesmo Operador para qualquer dicionário  

    ##################################  REJEITAR   ############################################
    elif ('reject' in opcao): 
        elemento = opcao[7:] 

        encontrou=False 
        for i in tocando: #correndo Tocando para validar qual ligação será rejeitada pelo operador
            if(i==elemento and status[i]=='ringing'): #Se operador for igual ao operador que rejeitou e status estiver tocando
                rejeicao[i] = tocando[i] #Atualiza a ligação rejeitada que estava tocando para o respectivo operador
                print('Call {} rejected by operator {}'.format(rejeicao[i], i))
                status[i]='available' 
                tocando[i]=' ' #Com status disponível nenhuma ligação está tocando para o respectivo operador
                encontrou=True
        
        if encontrou == False: #Caso o operador não esteja com o status tocando exibi a mensagem
            print('THERE ARE NO CALLS RINING FOR OPERATOR {}'.format(elemento))
        else: #Caso tenha sido algum operador que rejeitou a chamada, proucurar em Status um operador que esteja disponível para atender a ligação que foi rejeitada 
            encontrou=False
            for i in status:
                if (i!=elemento and status[i]=='available'):
                    print('Call {} ringing for operator {}'.format(rejeicao[i], i))
                    status[i]='ringing' 
                    tocando[i]=rejeicao[i] 
                    encontrou=True
                    break
            if(encontrou==False): #Se não tiver nenhum operador disponível a ligação cairá novamente para quem a rejeitou
                for i in status:
                    if (elemento==i):
                        print('Call {} ringing for operator {}'.format(rejeicao[i], i))
                        status[i]='ringing' 
                        tocando[i]=rejeicao[i] 

    ##################################  DESLIGAR   ############################################
    elif ('hangup' in opcao): 
        elemento = int(opcao[7:]) 

        encontrou=False
        for i in atendeu: #Corre Atendeu para validar as chamadas que foram finalizadas e atendidas 
            if(atendeu[i]==elemento and status[i]=='busy'): #valida se a ligação desligada se encontra no dicionario de ligações atendidas
                encontrou=True
                print('Call {} finished and operator {} available'.format(atendeu[i], i))
                status[i] = 'available' 
                tocando[i] = ' ' 
                if not len(fila) == 0: #Caso a Fila não esteja vazia, assim que um operador finalizar uma ligação a primeira ligação em espera na fila irá tocar para esse operador
                    tocando[i]=fila[0] #Vai tocar a primeira chamada da fila de espera para o operador
                    print('Call {} ringing for operator {}'.format(fila.pop(0), i)) #fila.pop(0) remove a primeira chamada da fila e exibi essa chamada removida
                    status[i]='ringing'
                break

        if (encontrou == False): #Caso a ligação desligada não estiver sido atendida quer dizer que ela foi perdida, e há 3 suposiçoes, ou ela estava tocando para algum operador ou estava em alguma posição na fila ou ela nem existe na fila.
            print('Call {} missed'.format(elemento))
            if not len(fila) == 0: #Caso a ligação desligada não estiver sido atendida e a fila não estiver vazia
                for i in status:
                    if (status[i]=='ringing' and (elemento==tocando[i])): #Caso ela esteja tocando para algum operador
                        tocando[i]=fila[0]
                        print('Call {} ringing for operator {}'.format(fila.pop(0), i))
                        status[i]='ringing'
                        encontrou=True
                        break
                if(encontrou==False): #Se não estiver tocando para nenhum operador corre laço abaixo:
                    if elemento in fila: #Caso não estiver tocando para nenhum operador e estiver na fila
                        fila.remove(elemento) #Remove a ligação da fila 
                    else: #Caso nem exista na fila
                        print('THERE IS NO CALL IN THE QUEUE')
            else: #Caso a ligação desligada não estiver sido atendida e a fila não estiver vazia
                for i in status: 
                    if (status[i]=='ringing' and (elemento==tocando[i])): #Se for uma ligação que estava tocando para o operador e foi desligada seu Status e Tocando devem ser atualizados 
                        status[i]='available'
                        tocando[i]=' '

    ##################################  FINALIZAR / SE ERRO   ############################################

    elif(opcao == 'exit'):
        print('\nENDING SESSION.. \n')
        break
    else:
        print('\nINVALID OPTION!')
    
    #os.system('pause')
    #os.system('cls') or None
