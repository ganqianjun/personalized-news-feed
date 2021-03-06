import operations
import os
import pyjsonrpc
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configuration'))

from config_parser import config
from sys_log_client import logger

SERVER_HOST = str(config['backend']['host'])
SERVER_PORT = int(config['backend']['port'])

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """Test Method"""
    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        print "Service.py : add is called with %d and %d" % (a, b)
        return a + b

    """ Get news summaries for a user """
    @pyjsonrpc.rpcmethod
    def getNewsSummariesForUser(self, user_id, page_num):
        return operations.getNewsSummariesForUser(user_id, page_num)

    """ Log user news clicks """
    @pyjsonrpc.rpcmethod
    def logNewsClickForUser(self, user_id, news_id):
        return operations.logNewsClickForUser(user_id, news_id)

# Threading HTTP Server
http_server = pyjsonrpc.ThreadingHttpServer(
  server_address = (SERVER_HOST, SERVER_PORT),
  RequestHandlerClass = RequestHandler
)

logger.info("Starting Backend HTTP server on %s:%d" % (SERVER_HOST, SERVER_PORT))

http_server.serve_forever()
