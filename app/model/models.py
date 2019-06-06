
# native module
import hashlib
import sys, inspect, abc, random
# orm
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class ModelManager():
    '''
    A singleton used to auto mange models in app
    '''
    ModelBase = declarative_base()

    @classmethod
    def get_orm_model_classes(cls) -> 'list of all ORM class':
        models = list()
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj) and isinstance(obj, type(cls.ModelBase)):
                models.append(obj)
        return models

    @classmethod
    def init_model_base(cls, engine=None):
        cls.ModelBase.metadata.create_all(engine)

class LoaderMixin():
    '''
    This mixin provide ORM Model ability to be loaded to database by loader
    But the inherit Class must define _loader_fields by itself
    '''
    _loader_fields = list()

    @classmethod
    def get_loader_fields(cls) -> 'dict':
        return dict(
            loader_fields=cls._loader_fields
        )

class User(ModelManager.ModelBase, LoaderMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    name = Column(String)
    height = Column(Integer) # cm
    weight = Column(Integer) # kg

    foods = relationship('UserReview', back_populates='user')

    _loader_fields = ('age', 'name', 'height', 'weight')

    def __str__(self):
        return '[User, %s] (%s)' % (self.id, self.name)

    @property
    def bmi(self): 
        return round(float( self.weight / (self.height / 100)^2 ), 2)

    @property
    def basal_metabolic_rate(self):
        return None
    
class Food(ModelManager.ModelBase, LoaderMixin):
    __tablename__ = 'food'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    calories = Column(Float)
    carbohydrate = Column(Float)
    protein = Column(Float)
    fat = Column(Float)

    users = relationship('UserReview', back_populates='food')
    
    _loader_fields = ('name', 'calories')

    def __str__(self):
        return '[Food, %s] (%s, %s, %s)' % (self.id, self.name, self.price, self.calories)

class UserReview(ModelManager.ModelBase, LoaderMixin):
    __tablename__ = 'user_review'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), back_populates='users')
    food_id = Column(Integer, ForeignKey('food.id'), back_populates='foods')
    user = relationship('User', back_populates='foods')
    food = relationship('Food', back_populates='users')
    is_accept = Column(Boolean, default=False)
    
    def __str__(self):
        return '[UserReview, %s] Accept: %s (%s comment to %s)' % (self.id, self.is_accept, self.user.name, self.food.name)