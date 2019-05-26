
# 3rd module
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# local module
from .models import ModelManager, User
# native module
import os, traceback

class DBManager():
    '''
    A singleton in app in authority of DB management
    It should not be instaniated

    SQLAlchemy reference doc
    1. https://www.sqlalchemy.org
    2. https://myapollo.com.tw/2016/09/28/python-sqlalchemy-orm-1/
    '''
    DEFAULT_DB_NAME = 'db'
    _engine = None
    _session = None

    def __init__(self, *args, **kwargs):
        raise Exception('DBManager is singleton and should not be instaniated')

    @classmethod
    def init_db(cls, db_name=None, is_echo=True) -> 'sqlalchemy session':
        cls._engine = create_engine('sqlite:///%s.sqlite' % db_name, echo=is_echo)
        ModelManager.init_model_base(engine=cls._engine)
        session = sessionmaker(bind=cls._engine)
        cls._session = session()
        return cls._session

    @classmethod
    def detach_db(cls, db_name=None):
        ''' Delete DB, only used in test env and sqlite database '''
        try:
            os.remove(os.path.join(os.getcwd(), '%s.sqlite' % db_name))
        except Exception as e:
            traceback.print_exc()

    @classmethod
    def get_session(cls):
        return cls._session
