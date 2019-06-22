import random
from .user_proxy_abstraction import UserProxyAbstract
from app.model.models import User, Food

class ProxyForRememberPreference(UserProxyAbstract):
    '''
    這個proxy 會記錄下每次接受食物時，
    accept_index_list 是在哪一個順位被接受的，是有序排列，理應越後面越少100(沒接受推薦)，越多靠前的數字(0,1,2)
    recommend_dict 是推薦食物清單的有序統計 food_id%5 的次數， 理應recommend_dict[0] 將越來越多1跟2，
    '''

    def __init__(self,  *args, **kwargs):    
        super().__init__(*args, **kwargs)
        
        self.recommend_dict = dict() # a dict 把推薦食物清單內0,1,2,3~9 分別推薦food_id 尾數的次數統計
        
        self.counter = 0 # 讓我知道目前是推薦到哪一個食物(will reset everytime accepting a food)
        
        for i in range(1,11):
            for j in range(0,5):
                self.recommend_dict[i] = {j: 0 }
                
        self.accept_index_list = []#記住每次accept食物的時候 是推薦到哪一個index時才接受的
            
        
    def accept(self, satisfication_ratio):
        self.accept_index_list.append(self.counter)
        return (True, satisfication_ratio)
        
    def reject(self,satisfication_ratio):
        self.accept_index_list.append(100) #沒接受就塞進去100
        return (False, satisfication_ratio)
        
    def utility(self, food=None) -> '(is_accept : boolean, satisfication_ratio : float [0-1])':
        the_id_mod_five = food.id % 5
        self.counter +=1
        self.recommend_dict[self.counter][the_id_mod_five] += 1

        if the_id_mod_five == 1:
            if random.random() >= 0.85:
                return self.accept(0.8)

            return    self.reject(0.3)
            
        elif the_id_mod_five == 2:
            if random.random() >= 0.9:
                return self.accept(0.6)
                
            return   self.reject(0.2)
            
        else:
            if random.random() >= 0.99:
                return self.accept(0.4)
                
            return   self.reject(0.1)
        

        
                