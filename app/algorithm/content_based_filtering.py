'''
Recommend food using content-based filtering
'''
from app.model.models import User, Food, UserRecommendationReview
from app.model.db_manager import DBManager
from app.algorithm.abstract import AlgorithmAbstraction

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
# native module
import random

class ContentBasedFiltering(AlgorithmAbstraction):
    _description = '(Content-based filtering aims for recommending foods similar to what the user has accepted)'

    def _find_similar_food(self, food_id, food, positive=1) -> 'food.id[]':
        try:
            count = CountVectorizer()
            count_matrix = count.fit_transform(food['name'])
            cosine_sim = cosine_similarity(count_matrix, count_matrix)
            if positive == 1:
                score_series = pd.Series(cosine_sim[food_id]).sort_values(ascending = False)
            else: # finds the least similar
                score_series = pd.Series(cosine_sim[food_id]).sort_values(ascending = True)
            similar_food = list(score_series.iloc[1:11].index)

            return similar_food
        except Exception as e:
            session = DBManager.get_session()
            random_food = random.choice(session.query(Food).all())
            return list([random_food.id])

    def _id_to_food_list(self, session, recommendation_list):
        result = session.query(Food).filter(Food.id.in_(recommendation_list)).all()
        food_map = {food.id: food for food in result}
        food_list = list()
        for food_id in recommendation_list:
            if food_id in food_map: food_list.append(food_map[food_id])

        return food_list

    def _recommend_food(self,review, food):
        user_review = review[review['is_accept']!=0]
        if user_review.shape[0] == 0:
            usre_review = review
            top_5_food = user_review.iloc[0:5]["food_id"]
            recommendation_list = []
            for food_id in top_5_food:
                recommendation_list.extend(self._find_similar_food(food_id, food, 0))
            final_recommendation = pd.Series(recommendation_list).value_counts().index.to_list()[:10]
        else:
            top_5_food = user_review.iloc[0:5]["food_id"]
            recommendation_list = []
            for food_id in top_5_food:
                recommendation_list.extend(self._find_similar_food(food_id, food, 1))
            final_recommendation = pd.Series(recommendation_list).value_counts().index.to_list()[:10]
        return final_recommendation

    def recommend(self, user=None, *args, **kwargs) -> 'Food[] , high recommendation prority in lower index ':
        ''' Everytime client ask for recommendation will invoke this method, return a python object '''
        user_id = user.id
        session = DBManager.get_session()
        food = pd.read_sql(session.query(Food).statement,session.bind).rename(columns={'id': 'food_id'})
        review = pd.read_sql(session.query(UserRecommendationReview).filter(user_id==UserRecommendationReview.user_id).statement,session.bind)
        review['is_accept'] = np.where(review['is_accept']==True, 1, 0)
        review = review.groupby(['food_id'])['is_accept'].mean().reset_index().sort_values(by = ["is_accept"], ascending = False)

        final_recommendation = self._recommend_food(review, food)
        food_list = self._id_to_food_list(session, final_recommendation)

        return food_list
