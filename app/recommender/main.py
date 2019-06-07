
from app.model.db_manager import DBManager
from app.model.models import ModelManager, User, Food, UserRecommendationReview, FoodPurchaseRecord
# native module
import random

class Main():
    '''
    Instance of App Service
    Manage all resource
    '''
    session = None
    _user_id = None

    def __init__(self, *args, **kwrags):
        self.session = DBManager.get_session()

    @property
    def user(self):
        if self._user_id is None: return None
        else:
            return self.session.query(User).filter(User.id==self._user_id).first()

    def login(self, user : 'User'):
        self._user_id = user.id

    def logout(self):
        self._user_id = None

    def get_foods(self, max_length=-1):
        return self.session.query(Food).order_by(Food.id.desc())[:max_length]

    def recommend(self, max_length=10):
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

    