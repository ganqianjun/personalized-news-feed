# -*- coding: utf-8 -*-

'''
Time decay model:

If selected:
p = (1-α)p + α

If not:
p = (1-α)p

Where p is the selection probability, and α is the degree of weight decrease.
The result of this is that the nth most recent selection will have a weight of
(1-α)^n. Using a coefficient value of 0.05 as an example, the 10th most recent
selection would only have half the weight of the most recent. Increasing epsilon
would bias towards more recent results more.
'''

import ast
import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configuration'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'monitor_service'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient
from config_parser import config
from datetime import datetime
from graphite_client import graphite
from sys_log_client import logger

NEWS_TOPICS = ast.literal_eval(config['news_topics']['topics'])
# Don't modify this value unless you know what you are doing.
NUM_OF_TOPICS = int(config['news_topics']['number_of_topics'])
INITIAL_P = 1.0 / NUM_OF_TOPICS
ALPHA = float(config['news_recommendation']['alpha'])

PREFERENCE_MODEL_TABLE_NAME = str(config['mongodb']['table_preference'])
NEWS_TABLE_NAME = str(config['mongodb']['table_news'])
CLICK_LOGS_TABLE_NAME = str(config['mongodb']['table_clicks'])

LOG_CLICKS_TASK_QUEUE_URL = str(config['cloudAMQP']['log_clicks_task_queue_url'])
LOG_CLICKS_TASK_QUEUE_NAME = str(config['cloudAMQP']['log_clicks_task_queue_name'])
cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

SLEEP_TIME_IN_SECONDS = int(config['cloudAMQP']['log_clicks_task_queue_sleep_time_in_seconds'])

def handle_message(msg):
    if msg is None or not isinstance(msg, dict) :
        return

    if ('userId' not in msg
        or 'newsId' not in msg
        or 'timestamp' not in msg):
        return

    userId = msg['userId']
    newsId = msg['newsId']

    # Update user's preference
    db = mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId': userId})

    # If model not exists, create a new one
    if model is None:
        logger.debug('Click log processor: Creating preference model for new user: %s' % userId)
        new_model = {'userId' : userId}
        preference = {}
        for i in NEWS_TOPICS:
            preference[i] = float(INITIAL_P)
        new_model['preference'] = preference
        model = new_model

    logger.info('Click log processor: Updating preference model for new user: %s' % userId)

    # Update model using time decaying method
    news = db[NEWS_TABLE_NAME].find_one({'digest': newsId})
    if (news is None
        or 'class' not in news
        or news['class'] not in NEWS_TOPICS):
        logger.error("Click log prrocessor: news doesn't exist or news topic doesn't exist")
        return

    click_class = news['class']

    # Send the metrics to graphite
    metrics = 'backend.click.' + userId.replace('.', '') + '.' + newsId.replace('.', '').replace('\n','') + '.' + click_class.split(' ')[0]
    graphite.send(metrics, 1)

    # Update the clicked one.
    old_p = model['preference'][click_class]
    model['preference'][click_class] = float((1 - ALPHA) * old_p + ALPHA)

    # Update not clicked classes.
    for i, prob in model['preference'].iteritems():
        if not i == click_class:
            model['preference'][i] = float((1 - ALPHA) * model['preference'][i])

    # update to mongodb
    db[PREFERENCE_MODEL_TABLE_NAME].replace_one({'userId': userId}, model, upsert=True)

    # add news title to click log table
    click_logs = db[CLICK_LOGS_TABLE_NAME].find({
        "$and": [
            {'userId': userId},
            {'newsId': news['digest']}
        ]
    })

    if click_logs.count() == 0:
        if news['description'] is not None:
            click_log = {
                'userId': userId,
                'newsId': news['digest'],
                'description': news['description'],
                'timestamp': datetime.utcnow(),
                'clicked': 1
            }
            db[CLICK_LOGS_TABLE_NAME].insert(click_log)
            logger.info("Click log processor: add click log")
            logger.info(news['description'])
        else:
            logger.info('==== empty news description ==== ')
    else:
        for click_log in click_logs:
            click_log['timestamp'] = datetime.utcnow()
            db[CLICK_LOGS_TABLE_NAME].replace_one(
                {"$and": [
                    {'userId': userId},
                    {'newsId': news['digest']}
                ]},
                click_log,
                upsert = True
            )
            logger.info("Click log processor: find duplicated click and update the time")
            logger.info(news['description'])

def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.getMessage()
            if msg is not None:
                # Parse and process the task
                try:
                    handle_message(msg)
                except Exception as e:
                    logger.error("Click log processor : handle message has error %s" % e)
                    pass
            # Remove this if this becomes a bottleneck.
            cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ ==  "__main__":
    run()
