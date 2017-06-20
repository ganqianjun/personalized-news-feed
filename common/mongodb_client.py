from pymongo import MongoClient

MONGO_DB_HOST = 'localhost'
MONGO_DB_PORT = '27017'
DB_NAME = 'personalized-news-feed'

client = MongoClient("%s:%s" % (MONGO_DB_HOST, MONGO_DB_PORT))

# make the database be singleton, could only be accessed by 'get_db'
def get_db(db=DB_NAME):
    db = client[db]
    return db
