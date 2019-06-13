
from .user_proxy_abstraction import UserProxyAbstract
import random

class SimpleUserproxy(UserProxyAbstract):
    '''
    A proxy that always take a const value of possibility to accept recommendation
    '''
    _description = '(Randomly accept food with posiibility = 0.3)'
    accept_possibility = 0.2

    def __init__(self, accept_possibility=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if accept_possibility:
            if accept_possibility < 0 or accept_possibility > 1:
                raise Exception('accept_possibility must between [0, 1]')
            self.accept_possibility = accept_possibility
    
    def utility(self, food=None):
        random.seed(random.randint(0, 999))
        if random.randint(0, 9) > self.accept_possibility*10:
            return (False, 0.1)
        else:
            return (True, 1.0)

