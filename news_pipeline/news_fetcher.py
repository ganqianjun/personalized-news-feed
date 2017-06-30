import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configuration'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

from newspaper import Article
from cloudAMQP_client import CloudAMQPClient
from config_parser import config

SCRAPE_NEWS_TASK_QUEUE_URL = str(config['cloudAMQP']['scrape_news_task_queue_url'])
SCRAPE_NEWS_TASK_QUEUE_NAME = str(config['cloudAMQP']['scrape_news_task_queue_name'])
DEDUPE_NEWS_TASK_QUEUE_URL = str(config['cloudAMQP']['dedupe_news_task_queue_url'])
DEDUPE_NEWS_TASK_QUEUE_NAME = str(config['cloudAMQP']['dedupe_news_task_queue_name'])

scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

SLEEP_TIME_IN_SECONDS = int(config['cloudAMQP']['scrape_news_task_queue_sleep_time_in_seconds_at_fetcher'])

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
