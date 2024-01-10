#!/bin/bash

if [ "$1" = "--no-cache" ]; then
    echo "📦️ Building without cache"
    ssh idsg1 'cd /mnt/um-share-drive/vemonet/libre-chat ; git pull ; docker compose build --no-cache ; docker compose down ; docker compose up --force-recreate -d'
else
    echo "♻️  Building with cache"
    ssh idsg1 'cd /mnt/um-share-drive/vemonet/libre-chat ; git pull ; docker compose up --force-recreate --build -d'
fi
