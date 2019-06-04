
'''
Here define the abstraction of algorithm
abstraction will be the interface which component beyond this module work with this module used
so if your want to expose your function to be access, define it in abstraction in this file
'''

import abc

class AlgorithmAbstraction(abc.ABC):
    '''
    Interface component beyond this module use to interact with algorithm
    add ant function here if you want to expose it
    '''

    @abc.abstractclassmethod
    def init_instance(*arg, **kwargs) -> 'default to void':
        ''' every time algorithm instance is created will call this to init '''
        pass

    @abc.abstractmethod
    def run(*arg, **kwargs) -> 'return python object':
        raise NotImplemented
