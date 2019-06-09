
# from app.model.db_manager import DBManager
from app.model.diet_schedule import DietScheduleAbstract
from app.model.models import User

class SimpleDiet(DietScheduleAbstract):
    ''' Simple diet pattern '''

    @property
    def calories(self):
        return 1800

    @property
    def carbohydrate(self): 
        return 200

    @property
    def protein(self):
        return 60

    @property
    def fat(self):
        return 10

def test_simple_diet():
    user = User(
        name='test_user',
        age=20,
        height=170,
        weight=60
    )
    diet = SimpleDiet(user=user)

    assert isinstance(diet.calories , int)
    assert isinstance(diet.carbohydrate , int)
    assert isinstance(diet.protein , int)
    assert isinstance(diet.fat , int)
