import numpy as np
import os
import random
import sys

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configuration'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'monitor_service'))

import mongodb_client
from config_parser import config
from graphite_client import graphite
from sys_log_client import logger

CLICK_LOGS_TABLE_NAME = str(config['mongodb']['table_clicks'])
NEWS_TABLE_NAME = str(config['mongodb']['table_news'])
UNCLICK_NEWS_LIMIT = int(config['customized_news_list']['unclick_news_limit'])
CLICK_NEWS_LIMIT = int(config['customized_news_list']['click_news_limit'])

db = mongodb_client.get_db()

def get_unclicked_news():
    total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(UNCLICK_NEWS_LIMIT))
    news_unclicked_list = {news['digest']: news['description'] for news in total_news}
    logger.debug("Customized - unclicked_list :\n %s " % (' '.join(news for news in news_unclicked_list)))
    return news_unclicked_list

def get_clicked_news(user):
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

def get_training_data(user):
    # this is to generator training data
    # it will get the latest clicks' description and get the lastest unclicked
    # news. Combine the clicked and unclicked new together as training data
    news_unclicked_list = get_unclicked_news()

    news_clicked_count, news_clicked_digest = get_clicked_news(user)

    for news_digest in news_unclicked_list.keys():
        if news_digest not in news_clicked_digest:
            news_clicked_count.append({
                'clicked': 0,
                'description': news_unclicked_list[news_digest]
            })

    # TODO: add test data
    # random.shuffle(news_clicked_count)

    x_train = []
    y_train = []
    for news in news_clicked_count:
        x_train.append(news['description'])
        y_train.append(news['clicked'])

    logger.debug("Customized - generate click training file for %s" % user)
    return x_train, y_train

def predict_news_click(user_id, news_description):
    # this function is to predict the probability of news in x_test to be clicked
    x_test = news_description
    x_train, y_train = get_training_data(user_id)

    x_train.extend(x_test)
    x_vector = TfidfVectorizer().fit_transform(x_train).todense()

    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(x_vector[0:len(y_train)], y_train)

    y_predict = neigh.predict_proba(x_vector[len(y_train):])
    # store the 'unclicked' probability
    click_predict = [predict[0] for predict in y_predict]
    logger.info("Predict news click for %s : [%s]" % (user_id, ' '.join(map(str, click_predict))))

    return click_predict
