
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

class SimpleCaloriesControlDiet(DietScheduleAbstract):
    nutirtion_ratio = dict(
        carbohydrate=0.4,
        protein=0.4,
        fat=0.2
    )

    @property
    def calories(self):
        return int(self.user.basal_metabolic_rate * 1.2)

    @property
    def carbohydrate(self): 
        return (self.calories * self.nutirtion_ratio['carbohydrate']) / 4 

    @property
    def protein(self):
        return (self.calories * self.nutirtion_ratio['protein']) / 4 

    @property
    def fat(self):
        return (self.calories * self.nutirtion_ratio['fat']) / 9

class DietScheduleCollection():
    defautl_schedule = SimpleCaloriesControlDiet
    schedules = (SimpleCaloriesControlDiet, )
