
import abc

class UserProxyAbstract(abc.ABC):
    '''
    User proxy abstraction aim to evaluate algorithm

    Concept:
        1. provide 'utility function' to measure how a recommendtion match the proxy's preference
        2. explore 'accpet ratio' for recommendations algorithms apply
    '''
    _accepted_recommendation_count = 0
    _recommendation_viwed_count = 0
    _total_food_viewed_count = 0
    _recommendation_accepted_ratio_snapshot = list()

    _description = ''

    def __str__(self):
        return f'{self.__class__.__name__} \t{self._description}'

    def __init__(self, user : 'User', diet_schedule : 'DietSchedule' , application=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user is None or diet_schedule is None: raise Exception('User and DietSchedule and must be provide')
        self.user = user
        self.user.set_diet_schedule(diet_schedule=diet_schedule)
        self.application = application

    def set_application(self, application=None):
        ''' Application is instance of app.recommender.application.Application '''
        self.application = application

    @abc.abstractmethod
    def utility(self, food=None) -> '(is_accept : boolean, satisfication_ratio : float [0-1])':
        ''' return (True, 0.7) '''
        raise NotImplementedError

    def get_avaiable_foods(self) -> 'Food[]':
        '''
        Return foods that is avaiable for proxyUser
        Or just the foods that proxyUser will be interested in
        '''
        return self.application.get_foods()

    def choice_food(self, is_echo=False) -> '(Food, is_recommendation_choiced, recommendation_view_count, total_food_view_count)':
        '''
        This function descript the process user decide to take food
        You can override if need it

        *** BEHAVIOR
        first consider recommded foods
        if none can statisfied proxyUser, then see avaiable foods

        return
        1. Food (be choiced)
        2. is_recommendation_accepted
        3. recommendation viwed count
        4. total food viewed count
        5. satisfication_ratio
        '''
        # first consider recommended food
        recommended_foods = self.application.recommend()
        food_in_recommendation, recommendation_food_view_count, satisfication_ratio = self._try_choice_food(food_list=recommended_foods)
        if food_in_recommendation is not None:
            self._accepted_recommendation_count += 1
            self._recommendation_viwed_count += recommendation_food_view_count
            self._total_food_viewed_count += recommendation_food_view_count
            self._perform_recommendation_accepted_ratio_snapshot()
            return (food_in_recommendation, True, recommendation_food_view_count, recommendation_food_view_count, satisfication_ratio)

        # second consider available food
        avaiable_foods = self.get_avaiable_foods()
        food_choiced, food_view_count, satisfication_ratio = self._try_choice_food(food_list=avaiable_foods, force=True)
        if food_choiced is not None:
            self._total_food_viewed_count += food_view_count
            self._perform_recommendation_accepted_ratio_snapshot()
            return (food_choiced, False, recommendation_food_view_count, recommendation_food_view_count + food_view_count, satisfication_ratio)

        raise Exception('No food be take from proxy')

    def _try_choice_food(self, food_list=list(), force=False) -> '(Food (sucessfully choice food) or None, food_view_count, satisfication_ratio)':
        '''
        return 
        1. Food
        2. food_view_count
        3. satisfication_ratio
        '''
        food_view_count = 0

        for food in food_list:
            food_view_count += 1
            is_accept, satisfication_ratio = self.utility(food=food)
            if is_accept:
                self.application.reply_recommendation(food=food, is_accept=True)
                return (food, food_view_count, satisfication_ratio)
            else:
                self.application.reply_recommendation(food=food, is_accept=False)
        # no food be choiced, if force is True, take the food with hightest satisfication_ratio
        if force: 
            values = list(map(lambda f: self.utility(food=f)[1], food_list))
            max_satisfication_ratio = max(values)
            idx = values.index(max_satisfication_ratio)
            self.application.reply_recommendation(food=food_list[idx], is_accept=True)
            return (food_list[idx], food_view_count, max_satisfication_ratio)
        else:
            return (None, food_view_count, 0.0)

        return (None, food_view_count, 0.0)

    def _perform_recommendation_accepted_ratio_snapshot(self):
        self._recommendation_accepted_ratio_snapshot.append(
            round(float(100*self._accepted_recommendation_count / (self._recommendation_viwed_count or 1.0)) ,2)
        )

    def report(self):
        print()
        print(' %s Report '.rjust(15, '-').ljust(15, '-') % self.__class__.__name__)
        print(f'Algorithm: \t{self.application.algorithm}')
        print('Recommendation accept ratio: \t%s percent' % self._recommendation_accepted_ratio_snapshot[-1])
        print('Recommendation accept ratio hsitory: ')
        print(self._recommendation_accepted_ratio_snapshot)
