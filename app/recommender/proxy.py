from .main import Main
from app.model.db_manager import DBManager
from app.model.models import User
# native module
import os, sys

class Command():
    ''' Encapulation of command '''
    name = None
    patterns = list()
    func = None

    def __init__(self, name=None, patterns=list(), invoke_function=lambda _ : True):
        self.name = name
        self.patterns = patterns
        self.func = invoke_function
        
    def support(self, text : 'str') -> 'boolean':
        ''' Is this command supported ? '''
        for p in self.patterns:
            if text.lower() == p.lower(): return True
        return False

    def invoke(self, *args, **kwargs):
        return self.func(*args, **kwargs)

class CommandComposite():
    commands = list()
    def __init__(self, commands=list()):
        self.commands = commands
        
    def _get_command(self, text : 'str') -> 'Command':
        for command in self.commands:
            if command.support(text): return command
        return None

    def support(self, text : 'str') -> 'boolean':
        if self._get_command(text) is None: return False
        return True

    def invoke(self, text=None, *args, **kwargs):
        command = self._get_command(text)
        if command is not None: command.invoke(*args, **kwargs)

class Cmd():
    ''' a util class for command line operation '''
    @classmethod
    def get_input(cls, text=''):
        return input('\n(%s) >' % text)

    @classmethod
    def clear(cls):
        # clear console different from OS platform
        if sys.platform.startswith('win32'): os.system('cls')
        else: os.system('clear')

    @classmethod
    def title(cls, text=''):
        print(f'{text}'.rjust(30, '-').ljust(30, '-'))
        print()

class CommandLineMainProxy(Main):
    '''
    This is a proxy of Main Class
    To make it can be access and manipuated from command line
    '''
    command_composite = None # CommandComposite

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        commands = [
            Command(name='view_recommendation', patterns=['r'], invoke_function=self._view_recommandation),
            Command(name='view_foods', patterns=['v'], invoke_function=lambda : Cmd.get_input('view_foods !!!')),
            Command(name='edit_user_data', patterns=['e'], invoke_function=lambda : Cmd.get_input('edit_user_data !!!')),
            Command(name='purchase_food', patterns=['p'], invoke_function=lambda : Cmd.get_input('purchase_food !!!')),
            Command(name='exit', patterns=['q'], invoke_function=self._exit_app),
        ]
        self.command_composite = CommandComposite(commands=commands)

    def run(self):
        '''
        *** Run this function to start Command Line Interaction ***
        '''
        self._login()
        while True:
            self._show_main_page()
            text = Cmd.get_input()
            if self.command_composite.support(text):
                self.command_composite.invoke(text)

    def _login(self):
        session = DBManager.get_session()
        while True:
            username = Cmd.get_input('Please enter user name to login')
            user = session.query(User).filter(User.name==username).one_or_none()
            if user is None:
                print('User not found !')
            else:
                self.login(user)
                break

    def _exit_app(self):
        sys.exit()

    def _show_main_page(self):
        Cmd.clear()
        Cmd.title(' Welcome to AI Eat ! ')
        for command in self.command_composite.commands:
            print('press \t%s to \t%s' % (command.patterns[0], command.name))
    
    def _view_recommandation(self):
        recommended_foods = self.recommend()[:3]
        Cmd.title('RECOMMENDATIONS')
        for food in recommended_foods:
            food.show_detail()
        Cmd.get_input('press <enter> to leave')

    def _view_foods(self):
        # choice order key
        # pagination
        pass