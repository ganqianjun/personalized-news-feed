import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configuration'))

from config_parser import config
from pymongo import MongoClient
from sys_log_client import logger

MONGO_DB_HOST = str(config['mongodb']['host'])
MONGO_DB_PORT = int(config['mongodb']['port'])
DB_NAME = str(config['mongodb']['db'])

client = MongoClient("%s:%s" % (MONGO_DB_HOST, MONGO_DB_PORT))

# make the database be singleton, could only be accessed by 'get_db'
def get_db(db=DB_NAME):
    db = client[db]
    return db
