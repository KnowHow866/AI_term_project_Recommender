
from .abstract import AlgorithmAbstraction
from app.model.db_manager import DBManager
from app.model.models import Food
# native 
import random

class RandomAlgorithm(AlgorithmAbstraction):

    def recommend(self, max_lenght=10, *args, **kwargs):
        session = DBManager.get_session()
        avaiable_foods = session.query(Food).all()
        return [random.choice(avaiable_foods) for _ in max_lenght]
        