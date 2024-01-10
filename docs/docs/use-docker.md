[![Image size](https://ghcr-badge.egpl.dev/vemonet/libre-chat/size)](https://github.com/vemonet/libre-chat/pkgs/container/libre-chat)

Libre Chat is available as a [docker image](https://github.com/vemonet/libre-chat/pkgs/container/libre-chat) that will use CUDA when available. It is recommended to use docker for deploying in production as it uses gunicorn to run multiple workers.

## ⚡ Quickstart

If you just want deploy it using the pre-trained Mixtral model, you can use docker:

```bash
docker run -it -p 8000:8000 ghcr.io/vemonet/libre-chat:main
```

!!! Warning "Loading the model takes time"

    Downloading the model will take time the first time, you can also pre-download it manually.
    If you are using GPU, loading the model when the application starts also takes some time (can take a few minutes)

## ⚙️ Configure with docker compose

1. Create a `chat.yml` file with your chat web service configuration.
2. Create the `docker-compose.yml` in the same folder:

    ```yaml title="docker-compose.yml"
    version: "3"
    services:
      libre-chat:
        image: ghcr.io/vemonet/libre-chat:main
        volumes:
          # ⚠️ Share files from the current directory to the /data dir in the container
          - ./chat.yml:/data/chat.yml
          - ./models:/data/models
          - ./documents:/data/documents
          - ./embeddings:/data/embeddings
          - ./vectorstore:/data/vectorstore
        ports:
          - 8000:8000
        environment:
          - LIBRECHAT_WORKERS=1
    ```

3. Start your chat web service with:

    ```bash
    docker compose up
    ```

??? warning "Using multiple workers"

    Using multiple worker is still experimental. When using a documents-based QA chatbot you will need to restart the API after adding new documents to make sure all workers reload the newly built vectorstore.
