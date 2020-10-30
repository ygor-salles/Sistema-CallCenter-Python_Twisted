from twisted.internet import protocol, reactor

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(data)
    
    def dataReceived(self, data):
        a = json.loads(data)
        print (a["response"])
        self.transport.loseConnection()

class EchoFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()
        
    def clientConnectionFailed(self, connector, reason):
        print ("Connection failed.")
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print ("Connection lost.")
        reactor.stop()

import json
#i=0 contador de ligações
while True:
    """ i += 1
    print('OPTIONS MENU - CHOOSE ONE OF THE OPTIONS:')
    print('("call %d") '%i)
    print('("answer A" ou "answer B")')
    print('("reject A" ou "reject B")')
    print('("hangup _")')
    print('("exit")')
    """
    opt1 = [v for v in input('Option:..>> ').split(', ')]
    for x in opt1:
        if ('call' in x):
            a = { "command" : str(x[0:4]), "id" : int(x[5:])}
        elif ('answer' in x):
            a = { "command" : str(x[0:6]), "id" : str(x[7:])}
        elif ('reject' in x):
            a = { "command" : str(x[0:6]), "id" : str(x[7:])}
        elif ('hangup' in x):
            a = { "command" : str(x[0:6]), "id" : int(x[7:])}

        data = json.dumps(a)
        reactor.connectTCP("localhost", 5678, EchoFactory())
        reactor.run()