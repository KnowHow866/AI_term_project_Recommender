from .main import Main

class CommandLineMainProxy(Main):
    '''
    This is a proxy of Main Class
    To make it can be access and manipuated from command line
    '''
    COMMANDS = dict(
        view_recommendation=['r', 'rec', 'recommend', 'recommendation'],
        view_foods=['v', 'view_foods'],
        edit_user_data=['e', 'edit_data'],
        purchase_food=['p']
    )

    def get_input(self, text=''):
        return input('\n(%s) >')

    def show_main_page(self):
        help_text_collection = [
            '\n',
            ' Welcome to AI Eat ! '.rjust(30, '-').ljust(30, '-'),
            '\n'
        ]
        for s in help_text_collection: print(s)
        for k, v in self.COMMANDS.items():
            print('press \t%s to \t%s' % (v[0], k))
        
        
    def run(self):
        while True:
            self.show_main_page()
            commend = self.get_input()
        