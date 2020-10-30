#import os
import json
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

class Echo(Protocol):
    def dataReceived(self, data):
        self.transport.write(data)

class EchoFactory(Factory):
    def buildProtocol(self, addr):
        return Echo()

fila = [] #para fila de espera de chamadas
i=1 #contador de ligações
c=0 #contador para chamadas atendidas
#para validar a chamada do respectivo operador
statusA = 'available'
statusB = 'available'
#para validar o identificador de chamadas de cada Operador
identificadorA=0
identificadorB=0
#para validar qual chamada foi rejeitada
rejeicao=0

while True:
    opcao = json.loads(data)

    ##################################  LIGAR   ############################################
    if (opcao == 'call %d'%i):
        a = {"response": "Call %d received"%i}
        if (statusA=='available' and statusB=='available'):    
            a = {"response": "Call %d ringing for operator A"%i}
            statusA = 'ringing'

        elif(statusA=='available' and (statusB=='ringing' or statusB=='busy')):
            a = {"response": "Call %d ringing for operator A"%i}
            statusA = 'ringing'

        elif(statusB=='available' and (statusA=='ringing' or statusA=='busy')):
            a = {"response": "Call %d ringing for operator B"%i}
            statusB = 'ringing'

        elif(statusA != 'available' and statusB != 'available'):
            fila.append(i)
            a = {"response": "Call %d waiting in queue"%i}

        else:
            a={"response": "PLEASE VALIDATE THE CORRECT CONNECTION OF THE MOMENT"}
        
        i += 1


    ##################################  RESPOSTA   ############################################
    elif (opcao=='answer A' or opcao=='answer B'):
        if(statusA=='ringing' and opcao=='answer A'):
            c += 1
            identificadorA = c
            a = {"response": "Call %d answered by operator A"%c}
            statusA='busy'
            
        elif(statusB=='ringing' and opcao=='answer B'):
            c += 1
            identificadorB = c
            a = {"response": "Call %d answered by operator B"%c}
            statusB='busy'
            
        else:
            a = {"response": "HAS NO CONNECTION TO THE QUOTE OPERATOR OR IS OCCUPIED.."}

        
    ##################################  REJEITAR   ############################################
    elif (opcao=='reject A' or opcao=='reject B'):
        if(statusA=='ringing' and opcao=='reject A'):
            a = {"response": "Call %d rejected by operator A"%(c+1)}
            statusA='available'
            fila.insert(0, int(c+1))
            rejeicao=c+1
            a = {"response": "Call %d ringing for operator A"%(c+1)}
            statusA='ringing'

        elif(statusB=='ringing' and opcao=='reject B'):
            a = {"response": "Call %d rejected by operator B"%(c+1)}
            statusB='available'
            fila.insert(0, int(c+1))
            rejeicao=c+1
            a = {"response": "Call %d ringing for operator B"%(c+1)}
            statusB='ringing'

        else:
            a = {"response": "DOES NOT HAVE A CONNECTION TO THE CITED OPERATOR.."}


    ##################################  DESLIGAR   ############################################
    elif ('hangup' in opcao):
        elemento = int(opcao[7:])

        if(identificadorA == elemento and statusA=='busy'):
            a = {"response": "Call %d finished and operator A available"%identificadorA}
            statusA = 'available'
            if not len(fila) == 0:
                a = {"response": "Call %d ringing for operator A"%fila.pop(0)}
                statusA='ringing'

        elif(identificadorB == elemento and statusB=='busy'):
            a = {"response": "Call %d finished and operator B available"%identificadorB}
            statusB = 'available'
            if not len(fila) == 0:
                a = {"response": "Call %d ringing for operator B"%fila.pop(0)}
                statusB='ringing'

        elif (elemento==rejeicao and statusA=='ringing'):
            a = {"response": "Call %d received"%fila.pop(0)}
            a = {"response": "Call %d ringing for operator A"%fila[0]}
            statusA='ringing'

        elif (elemento==rejeicao and statusB=='ringing'):
            a = {"response": "Call %d received"%fila.pop(0)}
            a = {"response": "Call %d ringing for operator B"%fila[0]}
            statusB='ringing'
        
        elif (identificadorA!=elemento and identificadorB!=elemento and not len(fila)==0):
            a = {"response": "Call %d received"%elemento}
            if (statusA=='available' and (elemento== fila[0])):
                a = {"response": "Call %d ringing for operator A"%fila.pop(0)}
                statusA='ringing'
            elif (statusB=='available' and (elemento== fila[0])):
                a = {"response": "Call %d ringing for operator B"%fila.pop(0)}
                statusB='ringing'
            elif (elemento!=fila[0]):
                fila.remove(elemento)
            else:
                del fila[0]
        
        else:
            a = {"response": "CALL %d NOT FOUND IN QUEUE"%elemento}

    ##################################  FINALIZAR / SE ERRO   ############################################

    elif (opcao == 'exit'):
        a = {"response": "\nENDING SESSION.. \n"}
        break
    else:
        a = {"response": "\nINVALID OPTION!"}

    a = {"response": "\n"}
    #os.system('pause')
    #os.system('cls') or None

data = json.dumps(a)
reactor.listenTCP(5678, EchoFactory())
reactor.run()

