import os
import pandas as pd
import random
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '../..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..', 'configuration'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..', 'monitor_service'))

import mongodb_client
from config_parser import config
from graphite_client import graphite
from sys_log_client import logger

CLICK_LOGS_TABLE_NAME = str(config['mongodb']['table_clicks'])
NEWS_TABLE_NAME = str(config['mongodb']['table_news'])
# how many news got from database which will be labaled as 'unclicked'
UNCLICK_NEWS_LIMIT = 10
CLICK_NEWS_LIMIT = 5

db = mongodb_client.get_db()

training_data_path = os.path.dirname(__file__) + '/training_data/'

class NewsListTrainingDataGenerator:
    def get_unclicked_news(self):
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(UNCLICK_NEWS_LIMIT))
        news_unclicked_list = {news['digest']: news['description'] for news in total_news}
        logger.debug("Customized - unclicked_list :\n %s " % (' '.join(news for news in news_unclicked_list)))
        return news_unclicked_list

    def get_clicked_news(self, user):
        clicks_list = list(db[CLICK_LOGS_TABLE_NAME].find({'userId': user}).sort([('timestamp', -1)]).limit(CLICK_NEWS_LIMIT))
        clicked_news_count = len(clicks_list)

        news_clicked_count = []
        news_clicked_digest = set()

        for click in clicks_list:
            news_clicked_count.append({
                k : v for k, v in click.items() if k == 'clicked' or k == 'description'
            })
            news_clicked_digest.add(click['newsId'])

        logger.debug("Customized - clicked_list:\n %s " % (' '.join(news for news in news_clicked_digest)))
        return news_clicked_count, news_clicked_digest

    def export_training_data(self, user_list):
        news_unclicked_list = self.get_unclicked_news()

        for user in user_list:
            news_clicked_count, news_clicked_digest = self.get_clicked_news(user)

            for news_digest in news_unclicked_list.keys():
                if news_digest not in news_clicked_digest:
                    news_clicked_count.append({
                        'clicked': 0,
                        'description': news_unclicked_list[news_digest]
                    })

            random.shuffle(news_clicked_count)

            my_df = pd.DataFrame(news_clicked_count)
            training_data_file_name = 'labeled_' + user + '.csv'
            training_data_file = os.path.join(training_data_path, training_data_file_name)
            my_df.to_csv(
                training_data_file,
                index = False,
                header = False,
                encoding = 'utf-8'
            )
            logger.debug("Customized - generate click training file for %s" % user)

training_data_generator = NewsListTrainingDataGenerator()
