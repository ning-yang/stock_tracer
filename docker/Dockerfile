FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    python2.7 \
    ipython \
    python-pip \
    python-dev \
    mysql-client \
    python-mysqldb \
    libmysqlclient-dev \
    vim \
    git

RUN ["git", "clone", "https://github.com/ning-yang/stock_tracer", "/root/stock_tracer"]
ENV PYTHONPATH /root
WORKDIR /root/stock_tracer
EXPOSE 5000
RUN ["pip", "install", "-r", "requirements.txt"]
COPY app_run.sh / 
ENTRYPOINT ["/app_run.sh"]
