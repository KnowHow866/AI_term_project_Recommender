
'''
Provide a algorithm collection for client to 
** access all algorithms**
'''
from .collaborative_filtering import CollaborativeFiltering
from .random_algo import RandomAlgorithm
from .composite import FairAlgorithmComposite

class AlgorithmCollection():
    default_algo = FairAlgorithmComposite
    algos = (
        RandomAlgorithm, CollaborativeFiltering,
        FairAlgorithmComposite
    )
