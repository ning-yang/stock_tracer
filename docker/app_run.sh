#!/bin/sh
start_worker() 
{
    echo 'start worker...'
    python scheduler/worker.py 
}

start_service()
{
    echo 'start service...'
    python stock_tracer_service.py
}

start_ui()
{
    echo 'start UI....'
    export FLASK_APP=stock_tracer.UI.home
    export FLASK_DEBUG=1
    flask run --host 0.0.0.0
}

start_test()
{
    echo 'start running py.test'
    py.test -v
}

case "$1" in
"ui")
    start_ui
    ;;
"service")
    alembic upgrade head
    start_service
    ;;
"worker")
    alembic upgrade head
    start_worker
    ;;
"test")
    start_test
    ;;
*)
    echo 'error command'
    exit 1
    ;;
esac
