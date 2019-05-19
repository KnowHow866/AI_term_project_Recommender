
class BaseModel():
    def __init__(self, *args, **kwargs):
        '''
        Init Model

        1. Init model fields, delegate to _set_attrs
        Model have to define all field in advance, it mean all model need to have FIELDS attr
        FIELDS = dict(
            fieldname: ()
        )
        '''
        if hasattr(self, 'FIELDS') is False: raise Exception('Model fields must be defined')
        self._set_attrs(**kwargs)
        super().__init__()
        
    def _set_attrs(self, **kwargs):
        for key in self.FIELDS:
            setattr(self, key, kwargs.get(key, None))

    def serialize(self):
        data = dict()
        for key in self.FIELDS: data[key] = getattr(self, key)
        return data
            
class TestModel(BaseModel):
    FIELDS = dict(
        name=()
    )
