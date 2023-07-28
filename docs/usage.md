This page explains how to create a FAIR metrics test API with `libre-chat`.

## 📥 Install the package

Install the package from [PyPI](https://pypi.org/project/libre-chat/){:target="_blank"}:

```bash
pip install libre-chat
```

## Start the server

```bash
libre-chat
```

## Or use docker

Clone the repository:

```
git clone https://github.com/vemonet/libre-chat
cd libre-chat
```

Start the server:

```bash
docker compose up
```


<!--
```bash
docker run -it ghcr.io/vemonet/libre-chat
```

## 📝 Define the API

Create a `main.py` file to declare the API, you can provide a different folder than `metrics` here, the folder path is relative to where you start the API (the root of the repository):

```python title="main.py"
from libre_chat import Api

api = API()
print(api.get_hello_world())
```
-->
