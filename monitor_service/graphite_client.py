import os
import socket
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configuration'))
from config_parser import config
from sys_log_client import logger

CARBON_SERVER = str(config['graphite_carbon']['carbon_server'])
CARBON_RECEIVER_PORT = int(config['graphite_carbon']['carbon_receiver_port'])
CARBON_AGGREGATOR_PORT = int(config['graphite_carbon']['carbon_aggregator_port'])

class GraphiteClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        logger.info("Graphite client is created at %s:%d" % (host, port))

    def send(self, metrics, val):
        timestamp = int(time.time())
        msgs = '\n%s %f %d\n' % (metrics, val, timestamp)
        sock = socket.socket()
        sock.connect((self.host, self.port))
        sock.sendall(msgs)
        sock.close()
        logger.debug("Metrics '%s' with value %f is sent to %s" % (metrics, val, self.port))

graphite_receiver = GraphiteClient(CARBON_SERVER, CARBON_RECEIVER_PORT)
graphite_aggregator = GraphiteClient(CARBON_SERVER, CARBON_AGGREGATOR_PORT)
