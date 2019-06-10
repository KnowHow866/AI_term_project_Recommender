
import abc

class UserProxyAbstract(abc.ABC):
    '''
    User proxy abstraction aim to evaluate algorithm

    Concept:
        1. provide 'utility function' to measure how a recommendtion match the proxy's preference
        2. explore 'accpet ratio' for recommendations algorithms apply
    '''
    def __init__(self, user : 'User', diet_schedule : 'DietSchedule' , application=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user is None or diet_schedule is None: raise Exception('User and DietSchedule and must be provide')
        self.user = user
        self.diet_schedule = diet_schedule
        self.application = application

    def set_application(self, application=None):
        ''' Application is instance of app.recommender.application.Application '''
        self.application = application

    @abc.abstractmethod
    def utility(self, food=None) -> '(is_accept : boolean, satisfication_ratio : float [0-1])':
        ''' return (True, 0.7) '''
        raise NotImplementedError

    def accpet_ratio(self) -> 'float [0-1]':
        accpet_ratio = float(self.application.acception_count / self.application.recommendation_count)
        return round(accpet_ratio ,2)
        
    def get_avaiable_foods(self) -> 'Food[]':
        '''
        Return foods that is avaiable for proxyUser
        Or just the foods that proxyUser will be interested in
        '''
        return self.application.get_foods()

    def choice_food(self):
        '''
        This function descript the process user decide to take food
        You can override if need it

        *** BEHAVIOR
        first consider recommded foods
        if none can statisfied proxyUser, then see avaiable foods
        '''
        # first consider recommended food
        recommended_foods = self.application.recommend()
        food_in_recommendation = self._try_choice_food(food_list=recommended_foods)
        if food_in_recommendation is not None:
            self.application.reply_recommendation(food=food_in_recommendation, is_accept=True)
            return 

        # second consider available food
        avaiable_foods = self.get_avaiable_foods()
        if self._try_choice_food(food_list=avaiable_foods, force=True) is not None: 
            return

        raise Exception('No food be take from proxy')

    def _try_choice_food(self, food_list=list(), force=False) -> 'Food (is sucessfully choice food) or None':
        for food in food_list:
            is_accept, satisfication_ratio = self.utility(food=food)
            if is_accept:
                self.application.take_food(food=food)
                return food
        # no food be choiced, if force is True, take the food with hightest satisfication_ratio
        if force: 
            values = list(map(lambda f: self.application.take_food(food=f)[1], food_list))
            idx = values.index(max(values))
            self.application.take_food(food=food_list[idx])
            return food_list[idx]
        else:
            return None
