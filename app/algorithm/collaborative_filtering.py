
'''
Recommend food using collaborative filtering with Singular Value Decomposition
'''
from app.model.models import User, Food, UserRecommendationReview
from app.model.db_manager import DBManager
from app.algorithm.abstract import AlgorithmAbstraction

from scipy.sparse.linalg import svds
import pandas as pd
import numpy as np

class CollaborativeFiltering(AlgorithmAbstraction):
    _description = '(Collaborative filtering aims for recommending the users items that their peers like)'

    def _recommend_for_user(self, prediction_df, user_id, food, review, num_recommendations=10):
        sorted_user_predictions = prediction_df.iloc[user_id - 1].sort_values(ascending=False)
        user_preference = pd.DataFrame(sorted_user_predictions).reset_index()
        user_preference.columns = ['food_id', 'ratings']

        user_review = review[review["user_id"] == user_id]
        food_not_yet_recommended = food[~food['food_id'].isin(user_review['food_id'])]
        recommend_list = pd.merge(food_not_yet_recommended, user_preference, on = "food_id").sort_values(by = ["ratings"], ascending = False).iloc[:num_recommendations]["food_id"].to_list()

        if len(recommend_list) < 10:
            recommend_list.extend(user_preference.iloc[:(10-len(recommend_list))]["food_id"].to_list())

        return recommend_list

    def _id_to_food_list(self, session, recommendation_list):
        result = session.query(Food).filter(Food.id.in_(recommendation_list)).all()
        food_map = {food.id: food for food in result}
        food_list = [food_map[id] for id in recommendation_list]

        return food_list

    def recommend(self, user=None, *args, **kwargs) -> 'Food[] , high recommendation prority in lower index ':
        ''' Everytime client ask for recommendation will invoke this method, return a python object '''
        user_id = user.id

        session = DBManager.get_session()
        food = pd.read_sql(session.query(Food).statement,session.bind).rename(columns={'id': 'food_id'})
        user = pd.read_sql(session.query(User).statement,session.bind).rename(columns={'id': 'user_id'})
        review = pd.read_sql(session.query(UserRecommendationReview).statement,session.bind)

        # Data processing & prepare
        review['is_accept'] = np.where(review['is_accept']==True, 1, -1)
        review = review.groupby(['user_id','food_id'])['is_accept'].sum().reset_index()
        rating_pivot = review.pivot(index='user_id',columns = 'food_id',values='is_accept').fillna(0)

        # Turn review to ratings matrix
        rating_df = rating_pivot.as_matrix()
        user_ratings_mean = np.mean(rating_df, axis = 1)
        r_demeaned = rating_df - user_ratings_mean.reshape(-1, 1)

        # Matrix factorization
        U, sigma, Vt = svds(r_demeaned, k = 20)
        sigma = np.diag(sigma)

        prediction_all= np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
        prediction_df = pd.DataFrame(prediction_all, columns = rating_pivot.columns)

        recommendation_list = self._recommend_for_user(prediction_df, user_id, food, review)
        food_list = self._id_to_food_list(session, recommendation_list)

        return food_list
