
'''
Write all test of system here
If it become too large later, we would split this file
'''
# local module
from app.model.db_manager import DBManager
from app.model.models import ModelManager, User, Food, UserRecommendationReview, FoodPurchaseRecord
from app.model.loader import Loader
# native
import random, string, os

def test_init_project():
    random_db_name_seed = ''.join([random.choice(string.ascii_lowercase) for _ in range(10)])
    DBManager.init_db(db_name='test_%s' % random_db_name_seed, is_echo=False)

def test_model():
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
    file_path = os.path.join('tests', 'load.json')
    Loader.load(file_path=file_path)
    Loader.traverse_database()

def test_detach_db():
    DBManager.detach_db()

def show_detail(self):
    print()
    print(' User: %s (id: %s)'.ljust(5, '-') % (self.name, self.id))
    figures = ['gender', 'age', 'height', 'weight', 'basal_metabolic_rate']
    for n in figures:
        print('<%s> : %s' % (n, getattr(self, n)))

def test_show_detail():
    session = DBManager.get_session()
    user = session.query(User).first()
    print(user.__str__())
    show_detail(user)
    assert user.basal_metabolic_rate > 0 
