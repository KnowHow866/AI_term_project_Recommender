from app.algorithm.abstract import AlgorithmAbstraction
from app.model.db_manager import DBManager
from app.model.models import ModelManager, User, Food, UserRecommendationReview
from sqlalchemy import desc
import numpy as np


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
        
            # update target_cal
            last_requirement = self.cal_requirement(self.time - 1)
            try:
                self.target_cal +=  cal - last_requirement 
            except:
                self.target_cal += self.session.query(Food).filter(Food.id == food_taken_id).first().calories - last_requirement 

        # 開始處理
        
        requirement = self.cal_requirement(self.time)
        this_meal_target = int( self.target_cal / self.meals_left )
        r_list = self.recommend_food_with_possibility(this_meal_target, requirement, self.foodlist)

        # update 
        self.meals_left -= 1
        self.time += 1
        self.list = r_list
        return r_list    