#!/bin/bash
fuser -k 3000/tcp

service redis_6379 start
service mongod start

mydir="${PWD}"

# build
pip install -r requirements.txt

cd $mydir/web_server/client
npm install
npm run build

cd $mydir/web_server/server
npm install
npm build

# start
cd $mydir/web_server/server
npm start &

cd $mydir/backend_server
python service.py &

cd $mydir/news_recommendation_service
python click_log_processor.py &
python news_recommendation_service.py &

cd $mydir/monitor_service
python system_monitor.py &

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)

fuser -k 3000/tcp
service redis_6379 stop
