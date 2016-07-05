#!/bin/sh
# stop all/remove apps
docker stop backend_service
docker rm backend_service
docker stop worker
docker rm worker
docker stop frontend_ui
docker rm frontend_ui

# main app
docker run -d --link mysql-db:mysql --link mq-stock:rabbit --link elastic:elastic-host -v ~/app:/root/app --name backend_service  ningy/stock_tracer service
docker run -d --link mysql-db:mysql --link mq-stock:rabbit --link elastic:elastic-host -v ~/app:/root/app --name worker ningy/stock_tracer worker
docker run -d --link mysql-db:mysql --link mq-stock:rabbit --link elastic:elastic-host -p 80:5000 -v ~/app:/root/app --name frontend_ui ningy/stock_tracer ui
