mkdir -p ~/app/log
mkdir -p ~/app/mysql

# dependency 
docker run --name mysql-db -v ~/app/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=password -d mysql:5.7
docker run -d --hostname mq-host --name mq-stock rabbitmq:3

# main app
docker run -d --link mysql-db:mysql --link mq-stock:rabbit -v ~/app:/root/app --name backend_service  ningy/stock_tracer:1.2 service
docker run -d --link mysql-db:mysql --link mq-stock:rabbit -v ~/app:/root/app --name worker ningy/stock_tracer:1.2 worker 
docker run -d --link mysql-db:mysql --link mq-stock:rabbit -p 80:5000 -v ~/app:/root/app --name frontend_ui ningy/stock_tracer:1.2 ui 

# build
docker build -t ningy/stock_tracer:1.0 --no-cache=true .
