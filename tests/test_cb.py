from app.algorithm.content_based_filtering import ContentBasedFiltering
from app.model.models import User, Food, UserRecommendationReview
from app.model.db_manager import DBManager
from app.algorithm.abstract import AlgorithmAbstraction

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

import os.path

def _find_similar_food(food_id, food, positive=1):
    count = CountVectorizer()
    count_matrix = count.fit_transform(food['name'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    if positive == 1:
        score_series = pd.Series(cosine_sim[food_id]).sort_values(ascending = False)
    else: # finds the least similar
        score_series = pd.Series(cosine_sim[food_id]).sort_values(ascending = True)
    similar_food = list(score_series.iloc[1:11].index)

    return similar_food
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
        usre_review = review
        top_5_food = user_review.iloc[0:5]["food_id"]
        recommendation_list = []
        for food_id in top_5_food:
            recommendation_list.extend(_find_similar_food(food_id, food, 1))
        final_recommendation = pd.Series(recommendation_list).value_counts().index.to_list()[:10]
    return final_recommendation



def test_cb_recommend():
    ''' Everytime client ask for recommendation will invoke this method, return a python object '''
    db_path = "./test.sqlite"
    # If db created then connect, otherwise, load test data.
    if os.path.exists(db_path):
        DBManager.init_db(db_name='test', is_echo=False)
    else:
        DBManager.init_db(db_name='test', is_echo=False)
        Loader.load(file_path='./tests/food.json')
        Loader.load(file_path='./tests/user.json')
        Loader.load(file_path='./tests/review.json')

    user_id = 20

    session = DBManager.get_session()
    food = pd.read_sql(session.query(Food).statement,session.bind).rename(columns={'id': 'food_id'})
    review = pd.read_sql(session.query(UserRecommendationReview).filter(user_id==UserRecommendationReview.user_id).statement,session.bind)
    review['is_accept'] = np.where(review['is_accept']==True, 1, 0)
    review = review.groupby(['food_id'])['is_accept'].mean().reset_index().sort_values(by = ["is_accept"], ascending = False)

    final_recommendation = _recommend_food(review, food)
    print(final_recommendation)
