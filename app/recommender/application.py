
from app.model.db_manager import DBManager
from app.model.models import ModelManager, User, Food, UserRecommendationReview
from app.algorithm.collection import AlgorithmCollection
from app.algorithm.evaluation.user_proxy_collection import UserProxyCollection
# native module
import random, traceback

class Application():
    '''
    Instance of App Service, it's so called ** Application **
    Manage all resource
    '''
    session = None
    db_name = None
    _user_id = None
    algorithm = AlgorithmCollection.default_algo()
    
    recommendation_count = 0

    def __init__(self, db_name='db', *args, **kwrags):
        if db_name is None or not isinstance(db_name, str): raise Exception('please provide DB name to init service')
        self.db_name = db_name

        DBManager.init_db(db_name=db_name, is_echo=kwrags.get('db_is_echo', True))
        self.session = DBManager.get_session()

    def set_algorithm(self, Algorithm : 'Algorithm'):
        algorithm = Algorithm()
        algorithm.init_instance()
        self.algorithm = algorithm

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
        self.recommendation_count += 1
        if self.algorithm is None:
            if len(list(self.session.query(Food))) == 0: return []
            return [random.choice(list(self.session.query(Food))) for _ in range(max_length)]
        else:
            try:
                return self.algorithm.recommend(user=self.user)[:max_length]
            except Exception as e:
                traceback.print_exc()
                return list()

    def reply_recommendation(self, food=None, is_accept=True):
        ''' User feedback to recommendation '''
        review = UserRecommendationReview(
            user=self.user,
            food=food,
            is_accept=is_accept
        )
        review.save()
        self.algorithm.user_take_food_hook(recommendation_review=review)
        
        if is_accept:
            print(f'{self.user.name} \taccept food \t{food.name}')

    def get_review_record(self):
        return (self.user).reviewed_foods
