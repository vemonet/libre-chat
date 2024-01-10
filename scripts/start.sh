#!/usr/bin/env sh
set -e

# Adapted from https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/master/docker-images/start.sh

export BIND=${BIND:-"0.0.0.0:8000"}
export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}

if [ ! -f "/data/main.py" ]; then
    cp /app/scripts/main.py /data/main.py
fi

if [ -f /data/main.py ]; then
    DEFAULT_MODULE_NAME=main
elif [ -f /app/scripts/main.py ]; then
    DEFAULT_MODULE_NAME=scripts.main
elif [ -f /app/app/main.py ]; then
    DEFAULT_MODULE_NAME=app.main
elif [ -f /app/main.py ]; then
    DEFAULT_MODULE_NAME=main
fi
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}
export TIMEOUT=${TIMEOUT:-600} # 10min
export NUMEXPR_MAX_THREADS=${NUMEXPR_MAX_THREADS:-$LIBRECHAT_WORKERS}

if [ -n "$LIBRECHAT_CONF_URL" ]; then
    # Do something when the environment variable is not null
    echo "📋 LIBRECHAT_CONF_URL provided, downlading it to chat.yml: $LIBRECHAT_CONF_URL"
    curl -L -o chat.yml $LIBRECHAT_CONF_URL
fi

# Initialize the Llm (ddl files if not present, build vectors) runs before the API to avoid running on multiple workers
python3 /app/scripts/init.py

# Wait for Qdrant to start
sleep 10

echo "🦄 Starting gunicorn with $LIBRECHAT_WORKERS workers on $BIND for the module $APP_MODULE with a timeout of $TIMEOUT sec"
exec gunicorn -w "$LIBRECHAT_WORKERS" -k "$WORKER_CLASS" -b "$BIND" --timeout "$TIMEOUT" "$APP_MODULE"
# exec uvicorn --host "0.0.0.0" --port 8000 "$APP_MODULE"

# -w: number of worker processes for handling requests [1]
# --threads: number of worker threads for handling requests. [1]



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
