
from .abstract import AlgorithmAbstraction
from app.model.db_manager import DBManager
from app.model.models import Food
# native 
import random

class RandomAlgorithm(AlgorithmAbstraction):
    _description = '(this algorithm just recommend RANDOM food)'

    def recommend(self, max_lenght=10, *args, **kwargs):
        session = DBManager.get_session()
        avaiable_foods = session.query(Food).all()
        random.seed(random.randint(0, 999))

        if not avaiable_foods: return list()
        return [random.choice(avaiable_foods) for _ in range(max_lenght)]
