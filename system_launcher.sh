#!/bin/bash
fuser -k 3000/tcp

service redis_6379 start
service mongod start

mydir="${PWD}"

# build
pip install -r requirements.txt

cd $mydir/web_server/client
npm run build

cd $mydir/web_server/server
npm build

# start
cd $mydir/web_server/server
npm start &

cd $mydir/backend_server
python service.py &

cd $mydir/news_recommendation_service
python news_recommendation_service.py &

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)

fuser -k 3000/tcp
service redis_6379 stop
