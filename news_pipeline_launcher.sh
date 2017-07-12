#!/bin/bash
service redis_6379 start
service mongod start

mydir="${PWD}"

cd $mydir/news_topic_modeling_service/server
python server.py &

cd $mydir/news_pipeline
python news_monitor.py &
python news_fetcher.py &
python news_deduper.py &

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)

service redis_6379 stop
