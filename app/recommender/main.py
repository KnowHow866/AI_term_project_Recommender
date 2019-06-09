
from app.model.db_manager import DBManager
from app.model.models import ModelManager, User, Food, UserRecommendationReview, FoodPurchaseRecord
# native module
import random

class Application():
    '''
    Instance of App Service, it's so called ** Application **
    Manage all resource
    '''
    session = None
    db_name = None
    _user_id = None

    def __init__(self, db_name='db', *args, **kwrags):
        if db_name is None or not isinstance(db_name, str): raise Exception('please provide DB name to init service')
        self.db_name = db_name
        DBManager.init_db(db_name=db_name, is_echo=kwrags.get('db_is_echo', True))
        self.session = DBManager.get_session()

    def __enter__(self):
        return self

    def __exit__(self,  exc_type, exc_val, exc_tb):
        DBManager.detach_db()

    @property
    def user(self):
        if self._user_id is None: return None
        else:
            return self.session.query(User).filter(User.id==self._user_id).first()

    def login(self, user : 'User'):
        self._user_id = user.id

    def logout(self):
        self._user_id = None

    def get_foods(self, max_length=None) -> 'Food[]':
        return self.session.query(Food).order_by(Food.id.desc())[:max_length]

    def search_foods(self, search : 'str', max_length=None) -> 'Food[]':
        return self.session.query(Food).filter(
                Food.name.like(f'%{search}%')
            ).order_by(Food.id.desc())[:max_length]

    def recommend(self, max_length=10):
        if len(list(self.session.query(Food))) == 0: return []
        return [random.choice(list(self.session.query(Food))) for _ in range(max_length)]

    def reply_recommendation(self, food=None, is_accept=True):
        review = UserRecommendationReview(
            user=self.user,
            food=food,
            is_accept=is_accept
        )
        review.save()
        
    def take_food(self, food=None):
        ''' invoke this function if user want to take this food '''
        record = FoodPurchaseRecord(
            user=self.user,
            food=food
        )
        record.save()

    def get_purchased_record(self):
        return (self.user).purchased_foods_record

    def get_review_record(self):
        return (self.user).reviewed_foods
