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

class ContentBasedFiltering(AlgorithmAbstraction):
    def _find_similar_food(food_id, food):
        count = CountVectorizer()
        count_matrix = count.fit_transform(food['name'])
        cosine_sim = cosine_similarity(count_matrix, count_matrix)
        score_series = pd.Series(cosine_sim[food_id]).sort_values(ascending = False)
        similar_food = list(score_series.iloc[1:11].index)

        return similar_food

    def _id_to_food_list(self, session, recommendation_list):
        result = session.query(Food).filter(Food.id.in_(recommendation_list)).all()
        food_map = {food.id: food for food in result}
        food_list = [food_map[id] for id in recommendation_list]

        return food_list

    def _recommend_food(review, food):
        user_review = review[review['is_accept']!=0]
        if user_review.shape[0] == 0:
            usre_review = review
            top_5_food = user_review.iloc[0:5]["food_id"]
            recommendation_list = []
            for food_id in top_5_food:
                recommendation_list.extend(_find_similar_food(food_id, food, 0))
            final_recommendation = pd.Series(recommendation_list).value_counts().index.to_list()[:10]
        else:
            top_5_food = user_review.iloc[0:5]["food_id"]
            recommendation_list = []
            for food_id in top_5_food:
                recommendation_list.extend(_find_similar_food(food_id, food, 1))
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
