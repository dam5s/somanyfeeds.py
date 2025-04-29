#!/usr/bin/env bash

set -e

if [[ -z "${SERVER_PORT}" ]]; then
  echo "SERVER_PORT is no set, exiting"
  exit 1
fi

mkfifo /tmp/logs

echo "Starting python backend on port 8081"
PORT=8081 python -m backend.apps.api_server 2>&1 | tee /tmp/logs &

echo "Starting nginx on port $SERVER_PORT"
sed -i s/SERVER_PORT/$SERVER_PORT/ nginx.conf
nginx -p /app -c /app/nginx.conf 2>&1 | tee /tmp/logs &

tail -f /tmp/logs
