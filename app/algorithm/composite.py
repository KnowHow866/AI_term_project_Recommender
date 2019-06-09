
'''
*** Composite is how algorithm will be access in this app ***

Algorithm Composite is a class that implement algorithm abstraction
But it self not a algo and in the other hand, include many algo
Client can invoke composite as an algo but actually many algo work underline

about Composite pattern, you can ref:
    1.https://openhome.cc/Gossip/DesignPattern/CompositePattern.htm
'''
from .abstract import AlgorithmAbstraction

class VotingAlgorithmComposite(AlgorithmAbstraction):
    ''' Most recommeded foods by algos will be uesed, or it will random choice '''
    def __init__(self, algorithms=list(), *args, **kwargs):
        pass
