from .application import Application
from app.model.db_manager import DBManager
from app.model.models import User
from app.algorithm.collection import AlgorithmCollection
from app.algorithm.evaluation.user_proxy_collection import UserProxyCollection
from app.model.diet_schedule import DietScheduleCollection
# native module
import os, sys, random

class Command():
    ''' Encapulation of command '''
    name = None
    patterns = list()
    func = None

    def __init__(self, name=None, patterns=list(), invoke_function=lambda : True):
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

class CommandLineApplicationProxy():
    '''
    This is a proxy of Main Class
    To make it can be access and manipuated from command line
    '''
    command_composite = None # CommandComposite
    application = None
    user_proxy = None 

    def __init__(self, db_name=DBManager.DEFAULT_DB_NAME ,*args, **kwargs):
        super().__init__()
        self.application = Application(db_name=db_name, db_is_echo=kwargs.get('db_is_echo', True))
        commands = [
            Command(name='set Algorithm', patterns=['a'], invoke_function=self._set_algorithm),
            Command(name='set User Proxy', patterns=['p'], invoke_function=self._set_user_proxy),
            Command(name='run Proxy Evaulation', patterns=['r'], invoke_function=self._run_proxy_evaulation),
            # Command(name='view_recommendation', patterns=['r'], invoke_function=self._view_recommandation),
            # Command(name='view_foods', patterns=['v'], invoke_function=lambda : Cmd.get_input('view_foods !!!')),
            # Command(name='edit_user_data', patterns=['e'], invoke_function=lambda : Cmd.get_input('edit_user_data !!!')),
            # Command(name='purchase_food', patterns=['p'], invoke_function=lambda : Cmd.get_input('purchase_food !!!')),
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
            print('\nRandom User List')
            for user in random.choices(session.query(User).all(), k=10):
                print(user)

            username = Cmd.get_input('Please enter user name to login')
            user = session.query(User).filter(User.name==username).one_or_none()
            if user is None:
                print('User not found !')
            else:
                self.application.login(user)
                break

    def _exit_app(self):
        sys.exit()

    def _show_main_page(self):
        Cmd.clear()
        Cmd.title(' Welcome to AI Eat ! ')
        self.application.user.show_detail()
        for command in self.command_composite.commands:
            print('press \t%s to \t%s' % (command.patterns[0], command.name))
    
    def _view_recommandation(self):
        recommended_foods = self.application.recommend()[:3]
        Cmd.title('RECOMMENDATIONS')
        for food in recommended_foods:
            food.show_detail()
        Cmd.get_input('press <enter> to leave')

    def _view_foods(self):
        # choice order key
        # pagination
        pass

    def _set_algorithm(self):
        Cmd.clear()
        Cmd.title('Choice an algorithm to use')
        for idx, algo in enumerate(AlgorithmCollection.algos):
            print('(%s): %s' % (idx, algo.__name__))

        try:
            choice_idx = int(Cmd.get_input('Enter number to choice algo to apply'))
            AlgoClass = AlgorithmCollection.algos[choice_idx]
            self.application.set_algorithm(Algorithm=AlgoClass)
        except Exception as e:
            Cmd.get_input('Choice Fail, presse <enter> to continue (error: %s)' % e.__str__())
            self._set_algorithm()

    def _set_user_proxy(self):
        # 1. choice diet schedule
        Cmd.clear()
        Cmd.title('First choice an diet_schedule to apply')
        DietSchedule = None
        for idx, schdule in enumerate(DietScheduleCollection.schedules):
            print('(%s): %s' % (idx, schdule.__name__))

        try:
            choice_idx = int(Cmd.get_input('Enter number to choice diet schedule'))
            DietSchedule = DietScheduleCollection.schedules[choice_idx]
        except Exception as e:
            Cmd.get_input('Choice Fail, presse <enter> to continue (error: %s)' % e.__str__())
            return self._set_user_proxy()

        # 2. choice user proxy
        Cmd.clear()
        Cmd.title('Then choice an userproxy to proxy')
        for idx, proxy in enumerate(UserProxyCollection.proxys):
            print('(%s): %s' % (idx, proxy.__name__))

        try:
            choice_idx = int(Cmd.get_input('Enter number to choice proxy'))
            UserProxyClass = UserProxyCollection.proxys[choice_idx]
            self.user_proxy = UserProxyClass(user=self.application.user, diet_schedule=DietSchedule, application=self.application)
        except Exception as e:
            Cmd.get_input('Choice Fail, presse <enter> to continue (error: %s)' % e.__str__())
            return self._set_user_proxy()

    def _run_proxy_evaulation(self):
        '''
        UserProxy will interact will this app 
        1. avaiable food is defined in UserProxy
        2. UserProxy will choice from avaiable food and recommended food
        3. UserProxy will give satisfication
        '''
        interaction_times = 30

        if self.user_proxy is None: self._set_user_proxy()

        for idx in range(interaction_times):
            print('\n%s time pickUp food'.ljust(10, '.') % idx)
            self.user_proxy.choice_food(is_echo=True)

        self.user_proxy.report()
        Cmd.get_input('Presse <enter> to leave')
