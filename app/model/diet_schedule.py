
import abc
from .models import User

class DietScheduleAbstract(abc.ABC):
    user = None

    def __init__(self, user : 'User instance', *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not isinstance(user, User): raise Exception('%s is not a instance of %s' % (user, User))
        self.user = user
    
    @property
    @abc.abstractmethod
    def calories(self) -> 'int':
        ''' recommend calories take in daily '''
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def carbohydrate(self) -> 'int':
        ''' recommend carbohydrate take in daily '''
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def protein(self) -> 'int':
        ''' recommend protein take in daily '''
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def fat(self) -> 'int':
        ''' recommend fat take in daily '''
        raise NotImplementedError

class SimpleDiet(DietScheduleAbstract):
    ''' Simple diet pattern '''

    @property
    def calories(self):
        return 1800

    @property
    def carbohydrate(self): 
        return 200

    @property
    def protein(self):
        return 60

    @property
    def fat(self):
        return 10
