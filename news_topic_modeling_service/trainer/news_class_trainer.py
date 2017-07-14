import news_cnn_model
import numpy as np
import os
import pandas as pd
import pickle
import shutil
import sys
import tensorflow as tf

sys.path.append(os.path.join(os.path.dirname(__file__), '../..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..', 'configuration'))

from config_parser import config
from sklearn import metrics
from sys_log_client import logger

learn = tf.contrib.learn

REMOVE_PREVIOUS_MODEL = True

DATA_SET_FILE = str(config['news_topic_modeling']['data_set_file'])
MODEL_OUTPUT_DIR = str(config['news_topic_modeling']['model_output_dir'])
VARS_FILE = str(config['news_topic_modeling']['vars_file'])
VOCAB_PROCESSOR_SAVE_FILE = str(config['news_topic_modeling']['vocab_processor_save_file'])
MAX_DOCUMENT_LENGTH = int(config['news_topic_modeling']['max_document_length_trainer'])
N_CLASSES = int(config['news_topics']['number_of_topics'])

# Training parms
STEPS = 200

def main(unused_argv):
    if REMOVE_PREVIOUS_MODEL:
        # Remove old model
        shutil.rmtree(MODEL_OUTPUT_DIR)
        os.mkdir(MODEL_OUTPUT_DIR)

    # Prepare training and testing data
    df = pd.read_csv(DATA_SET_FILE, header=None)
    train_df = df[0:400]
    test_df = df.drop(train_df.index)

    # x - news title, y - class
    x_train = train_df[1]
    y_train = train_df[0]
    x_test = test_df[1]
    y_test = test_df[0]

    # Process vocabulary - embedding
    vocab_processor = learn.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
    x_train = np.array(list(vocab_processor.fit_transform(x_train)))
    x_test = np.array(list(vocab_processor.transform(x_test)))

    n_words = len(vocab_processor.vocabulary_)
    logger.debug('News topic trainer : Total words: %d' % n_words)

    # Saving n_words and vocab_processor:
    with open(VARS_FILE, 'w') as f:
        pickle.dump(n_words, f)

    vocab_processor.save(VOCAB_PROCESSOR_SAVE_FILE)

    # Build model
    classifier = learn.Estimator(
        model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_OUTPUT_DIR)

    # Train and predict
    classifier.fit(x_train, y_train, steps=STEPS)

    # Evaluate model
    y_predicted = [
        p['class'] for p in classifier.predict(x_test, as_iterable=True)
    ]

    score = metrics.accuracy_score(y_test, y_predicted)
    logger.info('News topic trainer accuracy: {0:f}'.format(score))

if __name__ == '__main__':
    tf.app.run(main=main)
