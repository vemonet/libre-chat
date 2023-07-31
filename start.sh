#! /usr/bin/env sh
set -e

# Copied from https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/master/docker-images/start.sh

export BIND=${BIND:-"0.0.0.0:8000"}
export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}

if [ -f /app/tests/main.py ]; then
    DEFAULT_MODULE_NAME=tests.main
elif [ -f /app/app/main.py ]; then
    DEFAULT_MODULE_NAME=app.main
elif [ -f /app/main.py ]; then
    DEFAULT_MODULE_NAME=main
fi
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

# if [ -f /app/gunicorn_conf.py ]; then
#     DEFAULT_GUNICORN_CONF=/app/gunicorn_conf.py
# elif [ -f /app/app/gunicorn_conf.py ]; then
#     DEFAULT_GUNICORN_CONF=/app/app/gunicorn_conf.py
# else
#     DEFAULT_GUNICORN_CONF=/gunicorn_conf.py
# fi
# export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}

# # If there's a prestart.sh script in the /app directory or other path specified, run it before starting
# PRE_START_PATH=${PRE_START_PATH:-/app/prestart.sh}
# echo "Checking for script in $PRE_START_PATH"
# if [ -f $PRE_START_PATH ] ; then
#     echo "Running script $PRE_START_PATH"
#     . "$PRE_START_PATH"
# else
#     echo "There is no script $PRE_START_PATH"
# fi

# Start Gunicorn -w $LIBRECHAT_WORKERS --bind 0.0.0.0:8000 -c "$GUNICORN_CONF"
# -w: number of worker processes for handling requests [1]
# --threads: number of worker threads for handling requests. [1]

echo "🦄 Starting gunicorn with $LIBRECHAT_WORKERS for module $APP_MODULE on $BIND"

exec gunicorn -w "$LIBRECHAT_WORKERS" -k "$WORKER_CLASS" -b "$BIND" "$APP_MODULE"
