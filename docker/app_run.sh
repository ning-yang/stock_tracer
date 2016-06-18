#!/bin/sh
echo 'update db...'
alembic upgrade head

echo 'start service...'
python worker.py
