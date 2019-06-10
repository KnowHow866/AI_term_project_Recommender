
'''
This is entry point of the recommender project.
Provide interface of all functionality
'''
# native module
import os
# local module
from app.model.db_manager import DBManager
from app.model.loader import Loader
from app.recommender.application_proxy import CommandLineApplicationProxy

from argparse import ArgumentParser
parser = ArgumentParser(description=__doc__)
parser.add_argument('-c', '--connect_to_db', dest='connection_db', help='check DB health or create DB, provide args is DB name')
parser.add_argument('-l', '--load_data', dest='data_path', help='Load given path data to db (json format only) and traverse database')
parser.add_argument('-d', '--load_directory', dest='data_directory', help='Load all file in given directory to db (json format only) and traverse database')
parser.add_argument('-e', '--echo_database', dest='echo_database', help='true or false, echo database opperation')
parser.add_argument('-t', '--traverse_database', dest='traverse_database', help='true or false, traverse_database and print all data')

# algorithm related args
parser.add_argument('-a', '--algorithm', dest='algorithm', help='selected used algorithm')
parser.add_argument('-p', '--user_proxy', dest='user_proxy', help='select a userProxy to evaluate algorithm, this argument will close the command line UI')

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
        
    # optional args
    if args.data_directory is not None:
        loaad_path = os.path.join(os.getcwd(), args.data_directory)
        for root, dirs, files in os.walk(loaad_path):
            for file_name in files:
                Loader.load(file_path=os.path.join(loaad_path, file_name))
        Loader.traverse_database()

    if args.data_path is not None: 
        Loader.load(file_path=args.data_path)
        Loader.traverse_database()

    if args.traverse_database in ('true', 'True', 't', 'T'): Loader.traverse_database()

    # run command line UI
    app = CommandLineApplicationProxy(db_is_echo=DB_IS_ECHO)
    app.run()
