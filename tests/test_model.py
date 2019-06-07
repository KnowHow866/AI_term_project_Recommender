
'''
Write all test of system here
If it become too large later, we would split this file 
'''
# local module
from app.model.db_manager import DBManager
from app.model.models import ModelManager, User, Food, UserRecommendationReview, FoodPurchaseRecord
from app.model.loader import Loader
# native
import random, string

def test_init_project():
    DBManager.init_db(db_name='test', is_echo=False)

def test_model():
    session = DBManager.get_session()

    random_name = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(6)])
    user = User(name=random_name)

    user.id = 11
    # ORMModelInstance.save() is customized method, not sqlalchemy native
    # please see @UtilMixin
    saved_user = user.save()

    assert saved_user.name == random_name
    assert saved_user.id == 11

def test_many_to_many_relationship():
    session = DBManager.get_session()
    user = User(name='Kevein')
    food = Food(name='Noodle')
    session.add(user)
    session.add(food)
    session.commit()

    record = FoodPurchaseRecord(
        user=user,
        food=food
    )
    session.add(record)
    review = UserRecommendationReview(
        user=user,
        food=food,
        is_accept=False
    )
    session.add(review)
    
    assert review.user is user
    assert review.food is food
    assert review.is_accept is False
    
def test_loader():
    file_path = './tests/load.json'
    Loader.load(file_path=file_path)
    Loader.traverse_database()

def test_detach_db():
    DBManager.detach_db()
