
from app.model.db_manager import DBManager
from app.model.models import Food

class FoodFrequencyMixin():
    '''
    This mixin provide util function to exploit statistic data of Food in database
    '''
    _pattern = dict()
    
    @property
    def food_name_pattern_dict(self) -> 'dict(pattern : count_time)':
        '''
        Put all element of Food.name in a dict (self._pattern)
        and the value is the referenced time
        '''
        if any(self._pattern): return self._pattern

        session = DBManager.get_session()
        foods = session.query(Food).all()
        for food in foods:
            name_seq = food.name.lower().split(' ')

            for pattern in name_seq:
                if pattern in ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']:
                    continue
                if pattern in self._pattern: self._pattern[pattern] += 1
                else:
                    self._pattern[pattern] = 1

        return self._pattern
