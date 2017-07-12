import datetime
import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configuration'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'monitor_service'))

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

import mongodb_client
import news_topic_modeling_service_client
from cloudAMQP_client import CloudAMQPClient
from config_parser import config
from graphite_client import graphite
from sys_log_client import logger

DEDUPE_NEWS_TASK_QUEUE_URL = str(config['cloudAMQP']['dedupe_news_task_queue_url'])
DEDUPE_NEWS_TASK_QUEUE_NAME = str(config['cloudAMQP']['dedupe_news_task_queue_name'])

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

SLEEP_TIME_IN_SECONDS = int(config['cloudAMQP']['dedupe_news_task_queue_sleep_time_in_seconds_at_deduper'])

SAME_NEWS_SIMILARITY_THRESHOLD = float(config['news_deduper']['same_news_similarity_threshold'])

NEWS_TABLE_NAME = str(config['mongodb']['table_news'])

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        return
    task = msg
    text = task['text'].encode('utf8')
    if text is None:
        return

    # get all recent news based on publishedAt
    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year,
                                               published_at.month,
                                               published_at.day,
                                               0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    db = mongodb_client.get_db()
    same_day_news_list = list(db[NEWS_TABLE_NAME].find({
        'publishedAt': {
            '$gte': published_at_day_begin,
            '$lt': published_at_day_end
        }
    }))

    if same_day_news_list is not None and len(same_day_news_list) > 0:
        documents = [news['text'].encode('utf8') for news in same_day_news_list]
        documents.insert(0, text)

        # calculate similarity matrix
        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T

        #print pairwise_sim

        rows, _ = pairwise_sim.shape

        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                logger.debug("News_deduper : Duplicated news. Ignore")
                return

    # need to transfer string to datetime format when storing in MongoDB
    task['publishedAt'] = parser.parse(task['publishedAt'])

    # classify news
    title = task['title']
    if title is not None:
        topic = news_topic_modeling_service_client.classify(title)
        task['class'] = topic

    # if there is the same news, then replace
    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)

    # Send the metrics to graphite
    metrics = 'news.' + task['source'] + '.' + task['class'].split(' ')[0]
    graphite.send(metrics, 1)

while True:
    if dedupe_news_queue_client is not None:
        msg = dedupe_news_queue_client.getMessage()
        if msg is not None:
            # Parse and process the task
            try:
                handle_message(msg)
            except Exception as e:
                logger.error("News deduper error : %s" % e)
                pass

        dedupe_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
