
# native module
import hashlib
import sys, inspect, abc, random, datetime
# orm
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
# local module
from . import db_manager

class ModelManager():
    '''
    A singleton used to auto manage models in app
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
    _not_loaded_fields = list()

    @classmethod
    def get_loader_fields(cls) -> 'dict':
        return dict(
            loader_fields=cls._loader_fields,
            not_loaded_fields=cls._not_loaded_fields
        )

class UtilMixin():
    ''' mixin that provide convience utilities for ORM Model '''

    def save(self) -> 'instance':
        ''' save to db and return saved instance '''
        session = db_manager.DBManager.get_session()
        session.add(self)
        session.commit()

        ModelClass = type(self)
        if self.id is None:
            return session.query(ModelClass).order_by(ModelClass.id.desc()).first()
        else:
            return session.query(ModelClass).filter(ModelClass.id==self.id).first()

class User(ModelManager.ModelBase, LoaderMixin, UtilMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    name = Column(String, unique=True)
    height = Column(Integer) # cm
    weight = Column(Integer) # kg
    body_fat = Column(Integer) # percent
    gender_is_male = Column(Boolean, default=True)

    reviewed_foods = relationship('UserRecommendationReview', back_populates='user')

    _loader_fields = ('age', 'name', 'height', 'weight')

    diet_schedule = None

    def __str__(self):
        return '[User, %s] (%s)' % (self.id, self.name)

    def show_detail(self):
        print()
        print(' User: %s (id: %s)'.ljust(5, '-') % (self.name, self.id))
        figures = ['gender', 'age', 'height', 'weight', 'basal_metabolic_rate']
        for n in figures:
            print('<%s> : %s' % (n, getattr(self, n)))

    @property
    def gender(self) -> 'male / female':
        if self.gender_is_male is True: return 'male'
        else: return 'female'

    @property
    def bmi(self):
        return round(float( self.weight / (self.height / 100)**2 ), 2)

    @property
    def basal_metabolic_rate(self):
        if self.gender_is_male:
            return int(
                (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
            )
        else:
            return int(
                (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 162
            )

    def set_diet_schedule(self, diet_schedule : 'DietSchedule'):
        self.diet_schedule = diet_schedule(user=self)

class Food(ModelManager.ModelBase, LoaderMixin, UtilMixin):
    __tablename__ = 'food'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    calories = Column(Float)
    carbohydrate = Column(Float)
    protein = Column(Float)
    fat = Column(Float)

    reviewed_users = relationship('UserRecommendationReview', back_populates='food')
    
    _loader_fields = ('name', 'calories')

    def __str__(self):
        return '[Food, %s] (%s, %s, %s)' % (self.id, self.name, self.price, self.calories)

    def show_detail(self):
        print()
        print(' Food: %s (id: %s), price: %s '.ljust(5, '-').rjust(5, '-') % (self.name, self.id, self.price))
        nutritions = ['calories', 'carbohydrate', 'protein', 'fat']
        for n in nutritions:
            print('<%s> : %s' % (n, getattr(self, n)))

class UserRecommendationReview(ModelManager.ModelBase, LoaderMixin, UtilMixin):
    ''' User's review of recommendation '''
    __tablename__ = 'user_review'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), back_populates='users')
    food_id = Column(Integer, ForeignKey('food.id'), back_populates='foods')
    user = relationship('User', back_populates='reviewed_foods')
    food = relationship('Food', back_populates='reviewed_users')

    is_accept = Column(Boolean, default=False)
    created_datetime = Column(DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
        return '[UserReview, %s] Accept: %s (%s comment to %s)' % (self.id, self.is_accept, self.user, self.food)

    _loader_fields = ('user_id', 'food_id', 'is_accept')
    _not_loaded_fields = ('created_datetime',)
