'''
test of content filtering recommender system
'''
from app.recommender.main import Main
from app.model.db_manager import DBManager
from app.model.models import User, Food, FoodPurchaseRecord, UserRecommendationReview
from app.algorithm.abstract import AlgorithmAbstraction
import pandas as pd
import numpy as np
# native
import random, string

class CollaborativeFiltering(AlgorithmAbstraction):
    def _foo(self):
        pass

    def recommend(self, *args, **kwargs) -> 'Food[] , high recommendation prority in lower index ':
        ''' Everytime client ask for recommendation will invoke this method, return a python object '''
        session = DBManager.get_session()
        Food = pd.read_sql(session.query(Food).statement,session.bind)
        User = pd.read_sql(session.query(User).statement,session.bind)
        Review = pd.read_sql(session.query(UserRecommendationReview).statement,session.bind)



        return []