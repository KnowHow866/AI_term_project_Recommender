'''
Recommend food using content-based filtering
'''
from app.model.models import User, Food, UserRecommendationReview
from app.model.db_manager import DBManager
from app.algorithm.abstract import AlgorithmAbstraction

import pandas as pd
import numpy as np

class ContentBasedFiltering(AlgorithmAbstraction):
    def recommend(self, user=None, *args, **kwargs) -> 'Food[] , high recommendation prority in lower index ':
        ''' Everytime client ask for recommendation will invoke this method, return a python object '''
        return []
