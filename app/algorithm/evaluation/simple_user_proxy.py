
from .user_proxy_abstraction import UserProxyAbstract
import random

class SimpleUserproxy(UserProxyAbstract):
    '''
    A proxy that always take a const value of possibility to accept recommendation
    '''
    accept_possibility = 0.1

    def __init__(self, accept_possibility=0.8, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if accept_possibility < 0 or accept_possibility > 1:
            raise Exception('accept_possibility must between [0, 1]')
        self.accept_possibility = accept_possibility
    
    def utility(self, food=None):
        reply_pool = [(True, 1.0), (False, 0.1)]
        reply_weight_pool = [float(self.accept_possibility), float(1-self.accept_possibility)]
        
        proxy_reply = random.choices(reply_pool, reply_weight_pool)[0]
        print('Proxy reply: ',proxy_reply)
        return proxy_reply
