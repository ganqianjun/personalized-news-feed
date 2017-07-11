# Personalized-news-feed

## Installation
### Install NodeJs
```
sudo apt-get update
curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Install mongoose for ubuntu 16.04
```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org
```

For other version of ubuntu, please check [this link](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/).

### Install Redis
```
wget http://download.redis.io/releases/redis-3.2.6.tar.gz
tar xzf redis-3.2.6.tar.gz
cd redis-3.2.6
make
sudo make install
cd utils
sudo ./install_server.sh
```

### Install python 2.7: This is installed already in Ubuntu
### Install pip and python dependencies
```
sudo apt-get update
sudo apt install python-pip
```

### Install dependency for newspaper package
```
sudo apt-get install python-dev
sudo apt-get install libxml2-dev libxslt-dev
sudo apt-get install libjpeg-dev zlib1g-dev libpng12-devpip
sudo install —upgrade setuptools
```
## Build and start the monitor system
This system uses graphite for monitor and grafana to show the data.  
The docker image for graphite and grafana is based on [this link](https://github.com/kamon-io/docker-grafana-graphite).    
And the graph could be checked under `localhost:80`.  
The username and password are both `admin` by default.    

To start monitor system :
```
sudo ./news_monitor_installation.sh
```

## Build and start the system
```
sudo system_launcher.sh
```
Press 'Enter' to stop this system. If press other buttons, run:  
```
sudo killall python
```

## Start news_pipeline to fetch and process news
```
sudo news_pipeline_launcher.sh
```
## System log file
The system log file lives under directory 'common'.  
The default logging level is 'info'. If you need more information, please change  
the log level to 'debug'.
```
logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)
```
