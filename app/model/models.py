
# native module
import hashlib
import sys, inspect, abc, random
# orm
from sqlalchemy import Column, Integer, String, Float
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
    This mixin provide ORM Model ability to bt load to database by loader
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

    _loader_fields = ('age', 'name', 'height', 'weight')

    def __str__(self):
        return 'User %s (%s)' % (self.id, self.name)

    @property
    def bmi(self): 
        return round(float( self.height / (self.height / 100)^2 ), 2)

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
    
    _loader_fields = ('name', 'calories')

    def __str__(self):
        return 'Food %s (%s, %s, %s)' % (self.id, self.name, self.price, self.calories)
