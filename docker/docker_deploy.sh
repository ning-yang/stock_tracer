mkdir -p ~/app/log
mkdir -p ~/app/mysql

# dependency 
docker run --name mysql-db -v ~/app/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=password -d mysql:5.7
docker run --name mq-stock --hostname mq-host -d rabbitmq:3
docker run --name elastic -d elasticsearch
docker run --name kibana --link elastic:elasticsearch -p 5601:5601 -d kibana

# stop all/remove apps
docker stop backend_service 
docker rm backend_service
docker stop worker
docker rm worker
docker stop frontend_ui
docker rm frontend_ui

# main app
docker run -d --link mysql-db:mysql --link mq-stock:rabbit --link elastic:elastic-host -v ~/app:/root/app --name backend_service  ningy/stock_tracer:1.3 service
docker run -d --link mysql-db:mysql --link mq-stock:rabbit --link elastic:elastic-host -v ~/app:/root/app --name worker ningy/stock_tracer worker 
docker run -d --link mysql-db:mysql --link mq-stock:rabbit --link elastic:elastic-host -p 80:5000 -v ~/app:/root/app --name frontend_ui ningy/stock_tracer:1.3 ui 

# build
docker build -t ningy/stock_tracer:1.3 --no-cache=true .
docker push ningy/stock_tracer:1.3
