
'''
Write all test of system here
If it become too large later, we would split this file 
'''

from app.model.models import BaseModel

class TestModel(BaseModel):
    FIELDS = dict(
        name=()
    )

def test_model():
    person = TestModel(name='Marry')
    assert person.name == 'Marry'
    