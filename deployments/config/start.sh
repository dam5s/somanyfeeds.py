#!/usr/bin/env bash

set -e

mkfifo /tmp/logs

echo "Starting python backend on port 8081"
PORT=8081 python -m backend.apps.api_server 2>&1 | tee /tmp/logs &

echo "Starting nginx on port 8080"
nginx -p /app -c /app/nginx.conf 2>&1 | tee /tmp/logs &

tail -f /tmp/logs
