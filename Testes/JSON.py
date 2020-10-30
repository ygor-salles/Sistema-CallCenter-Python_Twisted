
import json
cont=0 #contador do JSON
i=1 #contador de ligações
while True:
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
        
        print(json.dumps(a)) 
        
    print('saindo do laço')
    if (opt1 == 'exit'):
        print('\nENDING SESSION.. \n')
        exit()