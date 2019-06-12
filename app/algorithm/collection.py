
'''
Provide a algorithm collection for client to 
** access all algorithms**
'''
from .collaborative_filtering import CollaborativeFiltering
from .random_algo import RandomAlgorithm
from .composite import FairAlgorithmComposite
from .lose_one_kg import LoseOneKgSchedule
from .markov_lose_one_kg import ModelBasedAgentOfMarkovVerionLoseOneKg

class AlgorithmCollection():
    default_algo = FairAlgorithmComposite
    algos = (
        RandomAlgorithm, 
        CollaborativeFiltering,
        LoseOneKgSchedule,
        ModelBasedAgentOfMarkovVerionLoseOneKg,
        FairAlgorithmComposite
    )
