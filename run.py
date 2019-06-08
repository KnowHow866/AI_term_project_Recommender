
'''
This is entry point of the recommender project.
Provide interface of all functionality
'''
# native module
import os
# local module
from app.model.db_manager import DBManager
from app.model.loader import Loader
from app.recommender.proxy import CommandLineMainProxy

from argparse import ArgumentParser
parser = ArgumentParser(description=__doc__)
parser.add_argument('-c', '--connect_to_db', dest='connection_db', help='check DB health or create DB, provide args is DB name')
parser.add_argument('-l', '--load_data', dest='data_path', help='Load given path data to db (json format only) and traverse database')
parser.add_argument('-e', '--echo_database', dest='echo_database', help='true or false, echo database opperation')
parser.add_argument('-t', '--traverse_database', dest='traverse_database', help='true or false, traverse_database and print all data')

if __name__ == '__main__':
    args = parser.parse_args()

    parser.print_help()

    # init DB
    DB_NAME = args.connection_db or DBManager.DEFAULT_DB_NAME
    DB_IS_ECHO = True if args.echo_database in (None, 'true', 'True') else False
    print('\n Init database : %s.sqlite' % DB_NAME)
    DBManager.init_db( 
        db_name=DB_NAME,
        is_echo=DB_IS_ECHO
    )
        
    # auto load data in /data
    auto_load_path = os.path.join(os.getcwd(), 'data')
    for root, dirs, files in os.walk(auto_load_path):
        for file_name in files:
            Loader.load(file_path=os.path.join(auto_load_path, file_name))

    # optional args
    if args.data_path is not None: 
        Loader.load(file_path=args.data_path)
        Loader.traverse_database()

    if args.traverse_database in ('true', 'True', 't', 'T'): Loader.traverse_database()

    recommander = CommandLineMainProxy(db_is_echo=DB_IS_ECHO)
    recommander.run()
