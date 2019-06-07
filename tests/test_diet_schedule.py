
# from app.model.db_manager import DBManager
from app.model.diet_schedule import SimpleDiet
from app.model.models import User

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