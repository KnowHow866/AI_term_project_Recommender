
'''
Write all test of system here
If it become too large later, we would split this file 
'''
# local module
from app.model.db_manager import DBManager
from app.model.models import ModelManager, User, Food, UserRecommendationReview, FoodPurchaseRecord
from app.model.loader import Loader
from app.algorithm.abstract import AlgorithmAbstraction
from datetime import datetime
from sqlalchemy import desc
import numpy as np
# pytest C:\Users\User\Documents\GitHub\AI_term_project_Recommender\tests\test_review.py     -s

# pytest C:\Users\User\Documents\GitHub\AI_term_project_Recommender\tests\test_model.py
    

def test_loader():
    DBManager.init_db(db_name = 'db4')

    # Loader.load(file_path= './data/food.json')
    # Loader.load(file_path= './data/user.json')
    # Loader.load(file_path= './data/review.json')
    # Loader.traverse_database()
    
def test_of_food_data():

    session = DBManager.get_session()

    
    food_list = session.query(Food).order_by(Food.id.asc()).all()


    assert len(food_list) == 295

    user_list = session.query(User).all()

    assert len(user_list) == 201
    review_list = session.query(UserRecommendationReview).all()
    assert len(review_list) > 0 

	
	
class ModelBasedAgentOfMarkovVerionLoseOneKg(AlgorithmAbstraction):

    def __init__(self, days=1, target_cal = 0):
        self.requirement = 1600
        self.first_time = True
        self.a_dict_take_or_not = dict()
        self.time = 0
        self.meals_left = 90
        self.list = []
    def cal_requirement(self, time):
        if time %3 ==1:
            return self.requirement * 0.4
        else:
            return self.requirement * 0.3
            

    
    def prob_of_favor_a_food(self, food):
        if food.id in self.a_dict_take_or_not:
            total, accepted = self.a_dict_take_or_not[food.id]
            return (1+accepted)/ (2+total)
        else:
            return 0.33
            
    def recommend_food_with_possibility(self, target_calories, requirement, food_list):
        
        min_cal, max_cal = requirement*0.5, requirement*1.5
        
        
        
        score_list = []
        for food in food_list:
            cal = food.calories


            if not ( min_cal< cal <max_cal ):
                score_list.append(-1000)
            else:
                possibility_of_accept_the_food = self.prob_of_favor_a_food(food)
                score = ( 100 - abs( cal - requirement + target_calories ) ) * possibility_of_accept_the_food
                score_list.append(score)
                
        index = np.argsort(score_list)[-1:-11:-1]
        return_list = []
        for i in index:
            return_list.append(food_list[i])

        return return_list
        
    def recommend(self, user=None):
        if self.first_time:
            self.first_time = False
            try:
                self.requirement = user.basal_metabolic_rate
            except:
                pass
            self.min_cal, self.max_cal = self.requirement * 0.15, self.requirement * 0.6
            self.session = DBManager.get_session()
            self.foodlist = self.session.query(Food).filter(self.min_cal<Food.calories).filter( Food.calories < self.max_cal).order_by(Food.calories.asc()).all()
            self.target_cal = self.requirement * 4.8
            

        
        else:
            # update a_dict_take_or_not, 第二次以後被呼叫才會計算
            Last_review = self.session.query(UserRecommendationReview).order_by(UserRecommendationReview.created_datetime.desc()).first()
            food_taken_id = Last_review.food_id
            for food in self.list:
                if food.id not in self.a_dict_take_or_not:
                    self.a_dict_take_or_not[food.id] = [0,0]

                self.a_dict_take_or_not[food.id][0] += 1
                if food.id == food_taken_id:
                    cal = food.calories
                    self.a_dict_take_or_not[food.id][1] += 1
                    break
        
            # update
            last_requirement = self.cal_requirement(self.time - 1)
            try:
                self.target_cal +=  cal - last_requirement 
            except:
                
                self.target_cal += self.session.query(Food).filter(Food.id == food_taken_id).first().calories - last_requirement 
            
            
            
            
            
                # 開始處理
        
        requirement = self.cal_requirement(self.time)
        this_meal_target = int( self.target_cal / self.meals_left )

        r_list = self.recommend_food_with_possibility(this_meal_target, requirement, self.foodlist)

        
        self.meals_left -= 1
        self.time += 1
        self.list = r_list
        return r_list	
	
	
	
def test_of_review_data():
    
    x = ModelBasedAgentOfMarkovVerionLoseOneKg()
    r_f = x.recommend()
    assert r_f[0].id > 0
    assert len(r_f) == 10
    assert x.time == 1
    target = x.target_cal
	
	
	
    r_f = x.recommend()
    assert len(r_f) == 10
    assert x.time == 2
    assert x.target_cal < target
    
    
    
    
    
    
    
# calories summary(nobs=295, minmax=(10.0, 829.0), mean=286.1423728813559, variance=21193.598708635996, skewness=0.7518591197686839, kurtosis=0.6468584853671056)
# median calories = 260.0
