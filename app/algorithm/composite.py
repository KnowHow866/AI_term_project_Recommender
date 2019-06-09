
'''
*** Composite is how algorithm will be access in this app ***

Algorithm Composite is a class that implement algorithm abstraction
But it self not a algo and in the other hand, include many algo
Client can invoke composite as an algo but actually many algo work underline

about Composite pattern, you can ref:
    1.https://openhome.cc/Gossip/DesignPattern/CompositePattern.htm
'''
from .abstract import AlgorithmAbstraction
from .random_algo import RandomAlgorithm

class FairAlgorithmComposite(AlgorithmAbstraction):
    ''' Most recommeded foods by algos will be uesed, or it will random choice '''
    algorithms = list()

    def __init__(self, algorithms=list(), *args, **kwargs):
        if len(algorithms) == 0:
            self.algorithms = [
                RandomAlgorithm(),
            ]
        else:
            self.algorithms = algorithms

    def recommend(self, max_length=10, *args, **kwargs):
        reply_list = list()
        recommendation_list = [ algo.recommend() for algo in self.algorithms ]

        while recommendation_list:
            for recommendation in recommendation_list:
                if len(reply_list) == max_length: break
                if not recommendation:
                    recommendation_list.remove(recommendation)
                    continue
                
                reply_list.append(recommendation.pop(0))

        return reply_list
