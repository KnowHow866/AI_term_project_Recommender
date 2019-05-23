
'''
This is entry point of the recommender project.
Provide interface of all functionality
'''

from app.model.db_manager import DBManager

from argparse import ArgumentParser
parser = ArgumentParser(description=__doc__)
parser.add_argument('-c', '--check_db', dest='c', help='check DB health or create DB, provide args is DB name')

if __name__ == '__main__':
    args = parser.parse_args()

    if args.c is not None:
        DBManager.init_db(db_name=args.c)
    else:
        parser.print_help()
