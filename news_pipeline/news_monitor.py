import datetime
import hashlib
import os
import redis
import sys

# because news_api_client is at anohter folder
# we could also use  '__init__.py'
# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import news_api_client

from cloudAMQP_client import CloudAMQPClient

NEWS_SOURCES = [
    'cnn'
]

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

NEWS_TIME_OUT_IN_SECONDS = 3600 * 24 * 1
SLEEP_TIME_IN_SECONDS = 10

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)

SCRAPE_NEWS_TASK_QUEUE_URL = 'amqp://lidfgojb:e2ZxaQS3nDRqgXHBq5mHrxyqjl9K3_uG@donkey.rmq.cloudamqp.com/lidfgojb'
SCRAPE_NEWS_TASK_QUEUE_NAME = 'test'

cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

while True:
    news_list = news_api_client.getNewsFromSource(NEWS_SOURCES)
    num_of_new_news = 0

    for news in news_list:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

        if redis_client.get(news_digest) is None:
            num_of_new_news = num_of_new_news + 1
            news['digest'] = news_digest

            # if there's no published time, set it to current UTC time
            if news['publishedAt'] is None:
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

            redis_client.set(news_digest, news)
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

            cloudAMQP_client.sendMessage(news)

    print "Fetched %d news." % num_of_new_news

    cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)
