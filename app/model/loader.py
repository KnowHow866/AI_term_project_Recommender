
# native module
import os, json, traceback, operator
# local module
from .models import ModelManager
from .db_manager import DBManager

class LoaderDescriptor():
    '''
    This Class describe the fields that will be load by loader
    '''
    def __init__(self, ORMClass=None, *args, **kwargs):
        self.ORMClass = ORMClass
        self.loader_fields = kwargs.get('loader_fields', list())

    def is_identical_data_in_db(self, target_dict=None):
        copy_dict = dict((k.lower(), v) for k, v in target_dict.items())
        filters = [
            operator.eq(getattr(self.ORMClass, field), target_dict.get(field, None))
            for field in self.loader_fields
        ]
        
        session = DBManager.get_session()
        obj = session.query(self.ORMClass).filter(*filters).first()
        if obj is not None: 
            print('Class <%s> instance id %s have exist in DB'.ljust(120, '-') % (self.ORMClass.__name__, obj.id))
            return True
        else: return False

    def is_loadable_dict(self, target_dict=None):
        '''
        Check this dict can be loaded to database
        A dict is loadable iff it has all loader_fields and not have identically existed in database
        '''
        copy_dict = dict((k.lower(), v) for k, v in target_dict.items())

        for field_name in self.loader_fields:
            if field_name.lower() not in copy_dict: return False
        
        if self.is_identical_data_in_db(target_dict=target_dict):
            return False

        return True

class Loader():
    '''
    A Singleton to load data to database
    Now only support json format
    '''
    RunTimeExceptions = type(
        'RunTimeExceptions', (object,), dict(
            LoadFileFailException = type('LoadFileFailException', (Exception,), dict()),
        )       
    )
    
    # loader depend on an method in ORM class to get loader_fields
    # ORM class want to be load by this loader have to implement this method 
    # the data this function return will be used to instantiate **"LoaderDescriptor"**
    DEPENDED_ORM_METHOD = 'get_loader_fields'

    @classmethod
    def _get_loader_descriptor(cls, ORMClass=None) -> 'LoaderDescriptor':
        if not hasattr(ORMClass, cls.DEPENDED_ORM_METHOD): 
            return None
        else:
            return LoaderDescriptor(
                ORMClass=ORMClass,
                **getattr(ORMClass, cls.DEPENDED_ORM_METHOD)()
            )

    @classmethod
    def load(cls, file_path=None):
        try:
            with open(os.path.join(os.getcwd(), file_path)) as f:
                try:
                    data_list = json.loads(f.read())
                    if isinstance(data_list, dict): data_list = [data_list]
                except Exception as e:
                    raise cls.RunTimeExceptions.LoadFileFailException()

                loaded_class = ModelManager.get_orm_model_classes()
                session = DBManager.get_session()

                for ORMClass in loaded_class:
                    loader_descriptor = cls._get_loader_descriptor(ORMClass=ORMClass)
                    if loader_descriptor is None: continue

                    for data in data_list:
                        if loader_descriptor.is_loadable_dict(target_dict=data):
                            session.add(ORMClass(**data))
                    session.commit()
                            
        except Exception as e:
            if isinstance(e, cls.RunTimeExceptions.LoadFileFailException): 
                print('\nLoad file fail, please check file is in legal json format'.ljust(60, '-'))
            else:
                traceback.print_exc()

    @classmethod
    def traverse_database(cls):
        ''' Go through data base and print the data '''
        session = DBManager.get_session()
        classes = ModelManager.get_orm_model_classes()
        for ORMClass in classes:
            print('\n Model: %s'.ljust(120, '-') % ORMClass.__name__)
            data = session.query(ORMClass)
            for element in data: print(element)