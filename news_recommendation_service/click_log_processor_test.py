import click_log_processor
import os
import sys

from datetime import datetime
from sets import Set

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configuration'))

import mongodb_client
from config_parser import config

PREFERENCE_MODEL_TABLE_NAME = str(config['mongodb']['table_preference'])
NEWS_TABLE_NAME = str(config['mongodb']['table_test'])

NUM_OF_CLASSES = int(config['mongodb']['news_topics']['number_of_topics'])

# Start MongoDB before running following tests.
def test_basic():
    db = mongodb_client.get_db()
    print db.collection_names()
    if (NEWS_TABLE_NAME not in db.collection_names()):
        db.createCollection(NEWS_TABLE_NAME)
        news = {
            'digest': 'test_news',
            'class': 'Other'
        }
        db[NEWS_TABLE_NAME].insert(news)

    db[PREFERENCE_MODEL_TABLE_NAME].delete_many({"userId": "test_user"})

    msg = {"userId": "test_user",
           "newsId": "test_news",
           "timestamp": str(datetime.utcnow())}

    click_log_processor.handle_message(msg)

    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId':'test_user'})
    assert model is not None
    assert len(model['preference']) == NUM_OF_CLASSES

    db[NEWS_TABLE_NAME].drop()

    print 'test_basic passed!'


if __name__ == "__main__":
    test_basic()
