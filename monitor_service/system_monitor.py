import psutil
import time
from graphite_client import graphite

while True:
    graphite.send('system.cpu', psutil.cpu_percent())
    graphite.send('system.free_memory', psutil.virtual_memory().free)
    time.sleep(10)
