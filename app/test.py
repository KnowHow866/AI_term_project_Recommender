
'''
Write all test of system here
If it become too large later, we would split this file 
'''

from .models import TestModel

def test_model():
    person = TestModel(name='Marry')
    assert person.name == 'Marry'
    