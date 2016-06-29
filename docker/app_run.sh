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

if [ $1 = "ui" ]; then
    start_ui
else
    echo 'update db...'
    alembic upgrade head

    if [ $1 = 'service' ]; then
        start_service
    else 
        start_worker
    fi
fi
