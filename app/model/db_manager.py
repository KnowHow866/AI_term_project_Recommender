
# 3rd module
from sqlalchemy import create_engine
# local module
from .models import ModelManager, User

class DBManager():
    '''
    A singleton in app in authority of DB management
    It should not be instaniated
    '''
    _engine = None

    def __init__(self, *args, **kwargs):
        raise Exception('DBManager is singleton and should not be instaniated')

    @classmethod
    def init_db(cls, db_name=None) -> 'sqlalchemy engine':
        cls._engine = create_engine('sqlite:///%s.sqlite' % db_name, echo=True)
        ModelManager.init_model_base(engine=cls._engine)
        return cls._engine
