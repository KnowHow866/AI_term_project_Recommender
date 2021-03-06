
'''
Here define the abstraction of algorithm
abstraction will be the interface which component beyond this module work with this module used
so if your want to expose your function to be access, define it in abstraction in this file
'''

import abc

class AlgorithmAbstraction(abc.ABC):
    '''
    Interface component beyond this module use to interact with algorithm
    add any function here if you want to expose it
    '''
    _description = ''

    def __str__(self):
        return f'{self.__class__.__name__} \t{self._description}'

    def init_instance(self, *args, **kwargs) -> 'default to void':
        ''' every time algorithm instance is created will call this to init '''
        pass

    @abc.abstractmethod
    def recommend(self, user : 'User',*args, **kwargs) -> 'Food[] , high recommendation prority in lower index ':
        ''' Everytime client ask for recommendation will invoke this method, return a python object '''
        raise NotImplementedError

    def user_take_food_hook(self, recommendation_review : 'UserRecommendationReview') -> 'void':
        '''
        This hook will be invoked when user take a food
        UserRecommendationReview will be pass in
        inform Algorithm user take thier recommendation or not
        '''
        pass
