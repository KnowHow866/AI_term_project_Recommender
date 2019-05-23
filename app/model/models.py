
# native module
import hashlib
import sys, inspect
# orm
from sqlalchemy import Column, Integer, String
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
            if inspect.isclass(obj) and type(obj) == type(ModelManager.ModelBase):
                models.append(obj)
        return models

    @classmethod
    def init_model_base(cls, engine=None):
        cls.ModelBase.metadata.create_all(engine)

class User(ModelManager.ModelBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)

    def __repr__(self):
        return "User('{}','{}', '{}')".format(
            self.name,
            self.username,
            self.password
        )
