import datetime
import os
import sys
# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

import mongodb_client
from cloudAMQP_client import CloudAMQPClient

DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://ddxjsoen:O4EHrjcK90QrpxEv738_3p-GUKayDoUB@donkey.rmq.cloudamqp.com/ddxjsoen"
DEDUPE_NEWS_TASK_QUEUE_NAME = "personalized-news-feed-dequpe-news-task-queue"

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

SLEEP_TIME_IN_SECONDS = 1

SAME_NEWS_SIMILARITY_THRESHOLD = 0.8

NEWS_TABLE_NAME = "news"

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

        print pairwise_sim

        rows, _ = pairwise_sim.shape

        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                print "News_deduper : Duplicated news. Ignore"
                return

    # need to transfer string to datetime format when storing in MongoDB
    task['publishedAt'] = parser.parse(task['publishedAt'])
    # if there is the same news, then replace
    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)

while True:
    if dedupe_news_queue_client is not None:
        msg = dedupe_news_queue_client.getMessage()
        if msg is not None:
            # Parse and process the task
            try:
                handle_message(msg)
            except Exception as e:
                print 'News deduper error : %s' % e
                pass

        dedupe_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
