import json
import os
import pickle
import random
import redis
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configuration'))

from bson.json_util import dumps
from cloudAMQP_client import CloudAMQPClient
from config_parser import config
from datetime import datetime
from sys_log_client import logger
import customized_news_list_client
import mongodb_client
import news_recommendation_service_client

REDIS_HOST = str(config['redis']['host'])
REDIS_PORT = int(config['redis']['port'])

NEWS_TABLE_NAME = str(config['mongodb']['table_news'])
CLICK_LOGS_TABLE_NAME = str(config['mongodb']['table_clicks'])

NEWS_LIMIT = int(config['backend']['news_limit'])
NEWS_LIST_BATCH_SIZE = int(config['backend']['news_list_batch_size'])
USER_NEWS_TIME_OUT_IN_SECONDS = int(config['backend']['user_news_time_out_in_seconds'])

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)

LOG_CLICKS_TASK_QUEUE_URL = str(config['cloudAMQP']['log_clicks_task_queue_url'])
LOG_CLICKS_TASK_QUEUE_NAME = str(config['cloudAMQP']['log_clicks_task_queue_name'])
cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    if page_num == 1:
        redis_client.delete(user_id)

    sliced_news = []

    if redis_client.get(user_id) is not None:
        news_digests = pickle.loads(redis_client.get(user_id))

        # If begin_index is out of range, this will return empty list;
        # If end_index is out of range (begin_index is within the range), this
        # will return all remaining news ids.
        sliced_news_digests = news_digests[begin_index:end_index]
        #print sliced_news_digests
        db = mongodb_client.get_db()
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest':{'$in':sliced_news_digests}}))

    if not sliced_news:
        db = mongodb_client.get_db()
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).skip(begin_index).limit(NEWS_LIMIT))
        latest_total_news_digests = map(lambda x:x['digest'], total_news)

        if page_num == 1:
            total_news_digests = latest_total_news_digests
        else:
            total_news_digests = pickle.loads(redis_client.get(user_id))
            total_news_digests.extend(latest_total_news_digests)

        redis_client.set(user_id, pickle.dumps(total_news_digests))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)
        news_digests = pickle.loads(redis_client.get(user_id))

        sliced_news = total_news[0: NEWS_LIST_BATCH_SIZE]

    # get click_predict list to customize news list
    # The lower the number in 'click_predict', the higher probability to click
    news_description = []
    for news in sliced_news:
        if news['description'] and news['description'].strip():
            news_description.append(news['description'])
        elif news['title'] and news['title'].strip():
            news_description.append(news['title'])
        else:
            news_description.append("This is an empty description")

    if news_description:
        click_predict = customized_news_list_client.predict_news_click(user_id, news_description)
    else:
        click_predict = []

    # get user preference for news
    preference = news_recommendation_service_client.getPreferenceForUser(user_id)
    topPreference = None
    if preference is not None and len(preference) > 0:
        topPreference = preference[0]

    for news in sliced_news:
        # Remove text field to save bandwidth.
        del news['text']
        if 'class' in news and news['class'] == topPreference:
            news['reason'] = 'Recommend'
            click_predict[sliced_news.index(news)] = 0.0
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'Today'

    # sort the news based on the sort order of click_predict
    sliced_news = [x for (y,x) in sorted(zip(click_predict, sliced_news))]

    return json.loads(dumps(sliced_news))

def logNewsClickForUser(user_id, news_id):
    # Send log task to machine learning service for prediction
    message = {
        'userId': user_id,
        'newsId': news_id,
        'timestamp': str(datetime.utcnow())
    }
    cloudAMQP_client.sendMessage(message)

    logger.debug("logNewsClickForUser: send message %s" % message)
