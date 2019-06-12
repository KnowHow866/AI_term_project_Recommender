
from .user_proxy_abstraction import UserProxyAbstract
from .mixins import FoodFrequencyMixin
from app.model.models import Food

class KeywordUserProxy(UserProxyAbstract, FoodFrequencyMixin):
    '''
    This proxy only accept food with specific keyword
    And the keyword is the string pattern with hightest appear-frequency within all Foods
    ''' 
    _desired_pattern = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sorted_food_pattern_tuple = sorted(
            self.food_name_pattern_dict.items(), 
            key=lambda item: item[1], 
            reverse=True
        )
        self._desired_pattern = sorted_food_pattern_tuple[0][0]

    def utility(self, food=None):
        if self._desired_pattern in food.name.lower():
            return (True, 1.0)
        else:
            return (False, 0.0)
            