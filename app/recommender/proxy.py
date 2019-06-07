from .main import Main

class CommandLineMainProxy(Main):
    '''
    This is a proxy of Main Class
    To make it can be access and manipuated from command line
    '''
        
    def run(self):
        while True:
            command = input('> ')
        
