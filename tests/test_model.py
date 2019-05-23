
'''
Write all test of system here
If it become too large later, we would split this file 
'''

from app.model.models import User

def test_model():
    user = User(name='user', username='username', password='userpassword'.encode('utf-8'))
    assert user.name == 'user'
    