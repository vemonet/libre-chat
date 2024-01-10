#!/bin/bash

if [ "$1" = "--no-cache" ]; then
    echo "📦️ Building without cache"
    ssh idsg1 'cd /mnt/um-share-drive/vemonet/libre-chat ; git pull ; docker compose build --no-cache ; docker compose down ; docker compose up --force-recreate -d'
else
    echo "♻️ Building with cache"
    ssh idsg1 'cd /mnt/um-share-drive/vemonet/libre-chat ; git pull ; docker compose up --force-recreate --build -d'
fi


# Build with cache:
# ssh ids2 'cd /data/deploy-services/knowledge-collaboratory ; git pull ; docker compose -f docker compose.yml -f docker compose.prod.yml up --force-recreate --build -d'

# Build without cache:
# ssh ids2 'cd /data/deploy-services/knowledge-collaboratory ; git pull ; docker compose -f docker compose.yml -f docker compose.prod.yml build ; docker compose -f docker compose.yml -f docker compose.prod.yml down ; docker compose -f docker compose.yml -f docker compose.prod.yml up --force-recreate -d'
