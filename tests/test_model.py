
'''
Write all test of system here
If it become too large later, we would split this file 
'''
# local module
from app.model.db_manager import DBManager
from app.model.models import User, Food, ModelManager
from app.model.loader import Loader
# native
import random, string

def test_init_project():
    DBManager.init_db(db_name='test', is_echo=False)

def test_model():
    session = DBManager.get_session()

    random_name = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(6)])
    user = User(name=random_name)
    session.add(user)
    session.commit()
    user = session.query(User).filter(User.name==random_name).first()

    assert user.name == random_name
    
def test_loader():
    file_path = './tests/load.txt'
    Loader.load(file_path=file_path)
    Loader.traverse_database()

def test_detach_db():
    DBManager.detach_db(db_name='test')
