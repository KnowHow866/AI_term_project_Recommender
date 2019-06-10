
from app.model.db_manager import DBManager
from app.model.models import User, Food
from app.algorithm.collection import AlgorithmCollection
from app.algorithm.evaluation.user_proxy_collection import UserProxyCollection
from app.model.diet_schedule import DietScheduleCollection
from app.recommender.application import Application
from app.model.loader import Loader
# native module
import random, string, os

def test_init_project():
    random_db_name_seed = ''.join([random.choice(string.ascii_lowercase) for _ in range(10)])
    DBManager.init_db(db_name='test_%s' % random_db_name_seed, is_echo=False)

def test_proxy_run():
    Loader.load(file_path=os.path.join(os.getcwd(), 'data', 'user.json'))
    Loader.load(file_path=os.path.join(os.getcwd(), 'data', 'food.json'))
    Loader.load(file_path=os.path.join(os.getcwd(), 'data', 'review.json'))

    session = DBManager.get_session()
    foods =  session.query(Food).all()

    random_user_name = ''.join([random.choice(string.ascii_lowercase) for _ in range(10)])
    user = User(name=random_user_name, weight=70, height=170).save()
    application = Application(db_is_echo=False)

    user_proxy = UserProxyCollection.default_proxy(
        user=user,
        diet_schedule=DietScheduleCollection.defautl_schedule,
        application=application
    )

    pickup_food_times = 30
    for _ in range(pickup_food_times):
        user_proxy.choice_food()

    user_proxy.report()

def test_detach_db():
    DBManager.detach_db()
