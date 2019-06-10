
'''
Write all test of system here
If it become too large later, we would split this file 
'''
# local module
from app.model.db_manager import DBManager
from app.model.models import ModelManager, User, Food, UserRecommendationReview, FoodPurchaseRecord
from app.model.loader import Loader

    
# pytest C:\Users\User\Documents\GitHub\AI_term_project_Recommender\tests\test_algorithm1.py -s

# pytest C:\Users\User\Documents\GitHub\AI_term_project_Recommender\tests\test_model.py
import json
    
def cal_requirement(time):
    daily_requirement =  1600
    morning_r, noon_r, night_r = daily_requirement*0.3, daily_requirement*0.4, daily_requirement*0.3
    if time == 'night':
        requirement =  night_r #480
    elif time == 'noon':
        requirement =  noon_r #640
    elif time == 'morning':
        requirement =  morning_r #480
    return requirement
        
def recommend_food(target_calories, time = 'night', food_list = []):

    requirement = cal_requirement(time)
    def find_food_closet_to_target(target, a_list, threshold = 0.5, time = 'night'):
        # a_list is a sorted list of Food instance, ascendingly sorted by calories
        min_error = 100000
        best_food = a_list[0]
        
        
        min_cal, max_cal = requirement*0.5, requirement*1.5
        for food in a_list:
            cal = food.calories
            if cal>max_cal or cal<min_cal:
                continue

            error = abs( cal - target )    

            if error < threshold:
                return food

            if error< min_error:
                min_error = error
                best_food = food

        return best_food



    best_food = find_food_closet_to_target(requirement-target_calories, food_list, 0.5, time)
    return best_food, best_food.calories - requirement + target_calories
        
def determing_what_time_it_is(number):
    if number %3 == 0:
        return 'morning'
    elif number %3 ==1 :
        return 'noon'
    elif  number %3 ==2 :
        return 'night'        
        
def get_the_score_of_a_specific_date(left_time, now, now_target_cal, path, food_list):
    
    now += 1
    left_time -= 1
    time = determing_what_time_it_is(now)
    
    if left_time == 0:
        next_food, loss = recommend_food(now_target_cal , time, food_list )
        tem_path = path + [next_food]

        return loss, tem_path

    else:
        min_score = 100000
        min_nest_loss = None
        requirement = cal_requirement(time)
        min_cal, max_cal = requirement*0.5, requirement*1.5
       
        
        for food in food_list:
            if food in path or food.calories < min_cal or food.calories > max_cal:
                continue
                
            tem_path = path + [food]
            next_loss, final_path = get_the_score_of_a_specific_date(left_time, now, food.calories - requirement + now_target_cal, tem_path, food_list)
            
            next_score = abs( food.calories - requirement + now_target_cal + next_loss )#早餐吃80 要480, target是-100, 那吃完後是-500
            
            print(food.calories, requirement, now_target_cal , next_score)
            
            if next_score <10:
                return next_loss, final_path
            
            elif next_score < min_score:
                min_score = next_score
                min_nest_loss = next_loss
                best_path = final_path

    return min_nest_loss, best_path

def get_multiday_schedule(days, target_cal, food_list):
    path = []
    tem_food_list = food_list
    while days > 1:
        today_target_cal = int( target_cal/days)
        loss, a_path = get_the_score_of_a_specific_date(3,-1, today_target_cal,[], tem_food_list)
        path += a_path
        days -=1 
        target_cal += loss - today_target_cal
        tem_food_list = []
        for x in food_list:
            if x not in path[-3:]:
                tem_food_list.append(x) 
        
    
    target_cal, a_path = get_the_score_of_a_specific_date(3,-1, target_cal,[], tem_food_list)
    path += a_path
    
    return target_cal , path    


def test_loader():
    DBManager.init_db(db_name = 'db4')

    Loader.load(file_path= './data/food.json')
    Loader.load(file_path= './data/user.json')

    Loader.traverse_database()
    
def test_of_food_data():

    session = DBManager.get_session()

    
    food_list = session.query(Food).order_by(Food.id.asc()).all()


    assert len(food_list) == 295
    
def test_of_user_data():

    session = DBManager.get_session()

    
    user_list = session.query(User).all()


    assert len(user_list) == 200
    
def test_of_last_purchase():
    session = DBManager.get_session()
    min_cal, max_cal = 240, 960
    
    food_list = session.query(Food).filter(min_cal<Food.calories).filter( Food.calories < max_cal).order_by(Food.calories.asc()).all()


    assert recommend_food(-100, 'night', food_list)[1] == 0
    assert recommend_food(-100, 'night', food_list)[0].id == 186
    
def test_of_a_day_purchase():    
    session = DBManager.get_session()
    min_cal, max_cal = 240, 960
    
    food_list = session.query(Food).filter(min_cal<Food.calories).filter( Food.calories < max_cal).order_by(Food.calories.asc()).all()
    loss, path = get_the_score_of_a_specific_date(3,-1,-100,[], food_list )
    
    total_cal_taken = -100 #多吃了100大卡
    for i in range(len(path)):
        print(path[i])
        total_cal_taken += path[i].calories
    
    
    
    assert len(path) == 3
    assert total_cal_taken - 1600 == loss
    

def test_of_many_day():
    session = DBManager.get_session()
    min_cal, max_cal = 240, 960
    
    foodlist = session.query(Food).filter(min_cal<Food.calories).filter( Food.calories < max_cal).order_by(Food.calories.asc()).all()

    loss, path =  get_multiday_schedule(3, -1000, foodlist) 
    assert abs(loss) < abs(1000)
    assert len(path) == 9
    
    
    
    
def test_rollback_db():
    session = DBManager.get_session()
    DBManager.detach_db()
    
# calories summary(nobs=295, minmax=(10.0, 829.0), mean=286.1423728813559, variance=21193.598708635996, skewness=0.7518591197686839, kurtosis=0.6468584853671056)
# median calories = 260.0
