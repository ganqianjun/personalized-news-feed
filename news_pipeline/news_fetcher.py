import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

from newspaper import Article

from cloudAMQP_client import CloudAMQPClient

SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://lidfgojb:e2ZxaQS3nDRqgXHBq5mHrxyqjl9K3_uG@donkey.rmq.cloudamqp.com/lidfgojb"
SCRAPE_NEWS_TASK_QUEUE_NAME = "personalized-news-feed-scrape-news-task-queue"
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://ddxjsoen:O4EHrjcK90QrpxEv738_3p-GUKayDoUB@donkey.rmq.cloudamqp.com/ddxjsoen"
DEDUPE_NEWS_TASK_QUEUE_NAME = "personalized-news-feed-dequpe-news-task-queue"

scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

SLEEP_TIME_IN_SECONDS = 5

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print 'News fetcher : message is broken'
        return

    task = msg
    text = None

    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text.encode('utf-8')
    dedupe_news_queue_client.sendMessage(task)

while True:
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            try:
                handle_message(msg)
            except Exception as e:
                print 'News fetcher error : %s' % e
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
