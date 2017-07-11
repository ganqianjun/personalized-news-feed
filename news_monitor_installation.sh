#!/bin/bash

fuser -k 80/tcp
fuser -k 2003/tcp
fuser -k 2004/tcp

cd monitor_service/docker_graphite
docker build -t graphite .
docker run -d\
 --name graphite\
 --restart=always\
 -p 80:80\
 -p 2003-2004:2003-2004\
 -p 2023-2024:2023-2024\
 -p 8125:8125/udp\
 -p 8126:8126\
 graphite
