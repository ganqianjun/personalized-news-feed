import news_click_predictor
import os
import pyjsonrpc
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configuration'))

from config_parser import config
from sys_log_client import logger

SERVER_HOST = str(config['customized_news_list']['host'])
SERVER_PORT = int(config['customized_news_list']['port'])

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """ Predict News Click """
    @pyjsonrpc.rpcmethod
    def predict_news_click(self, user_id, news_description):
        return news_click_predictor.predict_news_click(user_id, news_description)

# Threading HTTP Server
http_server = pyjsonrpc.ThreadingHttpServer(
  server_address = (SERVER_HOST, SERVER_PORT),
  RequestHandlerClass = RequestHandler
)

logger.info("Starting customized news list server on %s:%d" % (SERVER_HOST, SERVER_PORT))

http_server.serve_forever()
