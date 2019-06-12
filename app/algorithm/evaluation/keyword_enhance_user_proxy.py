
from .user_proxy_abstraction import UserProxyAbstract
from .mixins import FoodFrequencyMixin
from app.model.models import Food

class KeywordEnhanceUserProxy(UserProxyAbstract, FoodFrequencyMixin):
    '''
    Enhanced KeywordUserProxy
    accept food match one off multiple buildin keywords
    the keywordf are the word highest appear in Food.name
    '''
    _consider_patterns = list()
    CONSIDER_NUMBER = 10
    ACCEPT_RANK = 3 # index of element in _consider_patterns smaller than ACCEPT_RANK will be accept

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sorted_food_pattern_tuple = sorted(
            self.food_name_pattern_dict.items(), 
            key=lambda item: item[1], 
            reverse=True
        )
        self._consider_patterns = [tup[0] for tup in sorted_food_pattern_tuple[:self.CONSIDER_NUMBER]]
        print('Consieder pattern')
        print(self._consider_patterns)

    @property
    def satisfication_degree(self):
        return float(1.0 / self.CONSIDER_NUMBER)

    def utility(self, food=None):
        for idx in range(self.CONSIDER_NUMBER):
            is_accept = idx < self.ACCEPT_RANK,
            satisfication_ratio = 1.0 - (idx * self.satisfication_degree)

            if self._consider_patterns[idx] in food.name.lower():
                return (is_accept, satisfication_ratio)

        return (False, 0.0)
