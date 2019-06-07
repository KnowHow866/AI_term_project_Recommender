
from app.recommender.main import Main
from app.model.db_manager import DBManager
from app.model.models import User, Food, FoodPurchaseRecord, UserRecommendationReview

def test_init_project():
    DBManager.init_db(db_name='test', is_echo=False)
    Food(name='Apple').save()

def test_main():
    service = Main()

    USER_NAME = 'serviceUser'
    user = User(name=USER_NAME).save()
    
    # login
    service.login(user=user)
    assert service.user.name == USER_NAME

    # method test
    food_for_test = service.get_foods(max_length=1)[0]
    assert type(food_for_test) is Food
    assert type(service.recommend()[0]) is Food
    service.reply_recommendation(food=food_for_test)
    service.take_food(food=food_for_test)
    assert type(service.get_review_record()[0]) is UserRecommendationReview
    assert type(service.get_purchased_record()[0]) is FoodPurchaseRecord

    # logout
    service.logout()
    assert service.user is None
    
def test_detach_db():
    DBManager.detach_db(db_name='test')
