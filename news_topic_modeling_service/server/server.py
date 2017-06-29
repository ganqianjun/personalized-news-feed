#import news_classes
import ast
import numpy as np
import os
import pandas as pd
import pickle
import pyjsonrpc
import sys
import tensorflow as tf
import time

# import packages in trainer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'trainer'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..', 'configuration'))

from config_parser import config
from tensorflow.contrib.learn.python.learn.estimators import model_fn
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import news_cnn_model

learn = tf.contrib.learn

NEWS_TOPICS = ast.literal_eval(config['news_topics']['topics'])
print '======= topic server ====='
print NEWS_TOPICS
print '============================'
SERVER_HOST = config['news_topic_modeling']['host']
SERVER_PORT = int(config['news_topic_modeling']['port'])

MODEL_DIR = '../model'
MODEL_UPDATE_LAG_IN_SECONDS = 60

N_CLASSES = int(config['news_topics']['total_number'])

VARS_FILE = '../model/vars'
VOCAB_PROCESSOR_SAVE_FILE = '../model/vocab_procesor_save_file'

n_words = 0

MAX_DOCUMENT_LENGTH = 500
vocab_processor = None

classifier = None

def restoreVars():
    with open(VARS_FILE, 'r') as f:
        global n_words
        n_words = pickle.load(f)
    global vocab_processor
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(VOCAB_PROCESSOR_SAVE_FILE)
    print vocab_processor
    print 'Vars updated.'

def loadModel():
    global classifier
    classifier = learn.Estimator(
        model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_DIR)
    # Prepare training and testing
    df = pd.read_csv('../training_data/labeled_news.csv', header=None)

    # TODO: fix this until https://github.com/tensorflow/tensorflow/issues/5548 is solved.
    # We have to call evaluate or predict at least once to make the restored Estimator work.
    train_df = df[0:400]
    x_train = train_df[1]
    x_train = np.array(list(vocab_processor.transform(x_train)))
    y_train = train_df[0]
    classifier.evaluate(x_train, y_train)

    print "Model updated."

restoreVars()
loadModel()

print "Model loaded"

class ReloadModelHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Reload model
        print "Model update detected. Loading new model."
        time.sleep(MODEL_UPDATE_LAG_IN_SECONDS)
        restoreVars()
        loadModel()


class RequestHandler(pyjsonrpc.HttpRequestHandler):
    @pyjsonrpc.rpcmethod
    def classify(self, text):
        text_series = pd.Series([text])
        predict_x = np.array(list(vocab_processor.transform(text_series)))
        print predict_x

        y_predicted = [
            p['class'] for p in classifier.predict(
                predict_x, as_iterable=True)
        ]
        print y_predicted[0]
        #topic = news_classes.class_map[str(y_predicted[0])]
        topic = NEWS_TOPICS[y_predicted[0]]
        return topic

# Setup watchdog
observer = Observer()
observer.schedule(ReloadModelHandler(), path=MODEL_DIR, recursive=False)
observer.start()

# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print "Starting predicting server ..."
print "URL: http://" + str(SERVER_HOST) + ":" + str(SERVER_PORT)

http_server.serve_forever()
