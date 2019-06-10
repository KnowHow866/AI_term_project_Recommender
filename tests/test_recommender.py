
from app.recommender.application import Application
from app.model.db_manager import DBManager
from app.model.models import User, Food, UserRecommendationReview


def test_application():
    with Application(db_name='test_application', db_is_echo=False) as service:
        # pre-prepared data
        Food(name='Apple').save()
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
        assert type(service.get_review_record()[0]) is UserRecommendationReview
        
        search_foods = service.search_foods(search='a')
        assert type(search_foods) is list
        assert type(search_foods[0]) is Food

        # logout
        service.logout()
        assert service.user is None
    