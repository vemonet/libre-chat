## ⚡ Quickstart

If you just want to quickly deploy it using the pre-trained model `Llama-2-7B-Chat-GGML`, you can use docker:

```bash
docker run -it -p 8000:8000 ghcr.io/vemonet/libre-chat:main
```

## ⚙️ Configure with docker compose

1. Create a `chat.yml` file with your chat web service configuration.
2. Create the `docker-compose.yml` in the same folder:

    ```yaml title="docker-compose.yml"
    version: "3"
    services:
      libre-chat:
        image: ghcr.io/vemonet/libre-chat:main
        volumes:
        - ./chat.yml:/app/chat.yml
        - ./models:/app/models
        - ./vectorstore:/app/vectorstore
        ports:
          - 8000:8000
    ```

3. Start your chat web service with:

    ```bash
    docker compose up
    ```
