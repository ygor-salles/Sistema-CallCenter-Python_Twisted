import cmd,sys

class commands(cmd.Cmd):
    intro = 'Welcome a simulated call center application.\nType help or ? list commands. Type "end" to exit.\n'
    prompt = "Type: "
    data = None
    def do_call(self, arg):
        ' call <id> Makes application receive a call whose id is <id>.'
        data = {"command": "call","id": arg}
        print(data)

    def do_answer(self, arg):
        ' answer <id> Makes operator <id> answer a call being delivered to it.'
        data = {"command":" answer","id": arg}
        print(data)

    def do_reject(self, arg):
        ' reject <id> Makes operator <id> reject a call being delivered to it.'
        data = {"command": "reject","id": arg}
        print(data)

    def do_hangup(self, arg):
        ' hangup <id> Makes call whose id is <id> be finished'
        data = {"command": "hangup","id": arg}
        print(data)

    def do_end(self,arg):
        ' ends the application'
        exit()
        return True

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

if __name__ == '__main__':
    commands().cmdloop()