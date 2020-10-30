#import os
fila = [] #array para fila de espera de chamadas
status = {"A": "available", "B": "available"} #dicionario para validar o status do respectivo operador.
#CASO QUEIRA ADICIONAR MAIS OPERADORES BASTA ALIMENTAR O DICIONARIO, INSERINDO O OPERADOR E DECLARANDO SEU STATUS COMO AVAILABLE
atendeu = {} #dicionario para identificar a ultima chamada atendida pelo respectivo operador. Exemplo: {"A": 1, "B": 2}
rejeicao = {} #dicionario para identificar a ultima chamada rejeitada pelo operador. Exemplo: {"A": 1, "B": 2}
tocando = {} #dicionario para identificar as chamadas que estão tocando para o respectivo operador. Exemplo: {"A": 1, "B": 2}

while True:
    print('\n-------------------------------------------------------------')
    print('Queue = '+str(fila))
    for i in status:
        if(status[i] == 'ringing'):
            print('Status {}: {}-> call {}'.format(i, status[i], tocando[i]))
        elif(status[i] == 'busy'):
            print('Status {}: {}-> call {}'.format(i, status[i], atendeu[i]))
        else:
            print('Status {}: {}'.format(i, status[i]))
        
    opcao = str(input('\nOpção:..>> '))

    ##################################  LIGAR   ############################################
    if ('call' in opcao):
        elemento = int(opcao[5:])
        print('Call {} received'.format(elemento))

        encontrou=False
        for i in status:
            if (status[i] == 'available'):    
                print('Call {} ringing for operator {}'.format(elemento, i))
                status[i] = 'ringing'
                tocando[i] = elemento
                encontrou=True
                break
        if encontrou == False:
            fila.append(elemento)
            print('Call {} waiting in queue'.format(elemento))        
        
    ##################################  RESPOSTA   ############################################
    elif ('answer' in opcao):
        elemento = opcao[7:]

        encontrou=False
        for i in tocando:
            if (i==elemento and status[i]=='ringing'):       
                atendeu[i] = tocando[i]
                print('Call {} answered by operator {}'.format(atendeu[i], i))
                status[i]='busy'
                encontrou=True
        if encontrou==False:
            print('NO CONNECTIONS TO THE OPERATOR {}'.format(elemento))

    ##################################  REJEITAR   ############################################
    elif ('reject' in opcao):
        elemento = opcao[7:]

        encontrou=False
        for i in tocando:
            if(i==elemento and status[i]=='ringing'):
                rejeicao[i] = tocando[i]
                print('Call {} rejected by operator {}'.format(rejeicao[i], i))
                status[i]='available'
                tocando[i]=' '
                encontrou=True
        
        if encontrou == False:
            print('THERE ARE NO CALLS RINING FOR OPERATOR {}'.format(elemento))
        else:
            encontrou=False
            for i in status:
                if (i!=elemento and status[i]=='available'):
                    print('Call {} ringing for operator {}'.format(rejeicao[i], i))
                    status[i]='ringing'
                    tocando[i]=rejeicao[i]
                    encontrou=True
                    break
            if(encontrou==False):
                for i in status:
                    if (elemento==i):
                        print('Call {} ringing for operator {}'.format(rejeicao[i], i))
                        status[i]='ringing'
                        tocando[i]=rejeicao[i]

    ##################################  DESLIGAR   ############################################
    elif ('hangup' in opcao):
        elemento = int(opcao[7:])

        encontrou=False
        for i in atendeu:
            if(atendeu[i]==elemento and status[i]=='busy'):
                encontrou=True
                print('Call {} finished and operator {} available'.format(atendeu[i], i))
                status[i] = 'available'
                tocando[i] = ' '
                if not len(fila) == 0:
                    tocando[i]=fila[0]
                    print('Call {} ringing for operator {}'.format(fila.pop(0), i))
                    status[i]='ringing'
                break

        if (encontrou == False):
            print('Call {} missed'.format(elemento))
            if not len(fila) == 0:
                for i in status:
                    if (status[i]=='ringing' and (elemento==tocando[i])):
                        tocando[i]=fila[0]
                        print('Call {} ringing for operator {}'.format(fila.pop(0), i))
                        status[i]='ringing'
                        encontrou=True
                        break
                if(encontrou==False):
                    if elemento in fila:
                        fila.remove(elemento)
                    else:
                        print('THERE IS NO CALL IN THE QUEUE')
            else:
                for i in status:
                    if (status[i]=='ringing' and (elemento==tocando[i])):
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

"""Deixar o codigo comentado"""