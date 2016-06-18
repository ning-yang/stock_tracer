mkdir -p ~/app/log
mkdir -p ~/app/mysql

docker run --name mysql-db -v ~/app/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=password -d mysql:5.7

docker run -d --link mysql-dev:mysql -v ~/app:/root/app  ningy/stock_tracer:1.0
