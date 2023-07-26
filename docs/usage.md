This page explains how to create a FAIR metrics test API with `libre-llm`.

## 📥 Install the package

Install the package from [PyPI](https://pypi.org/project/libre-llm/){:target="_blank"}:

```bash
pip install libre-llm
```

## Start the server

```bash
libre-llm
```

## Or use docker

Clone the repository:

```
git clone https://github.com/vemonet/libre-llm
cd libre-llm
```

Start the server:

```bash
docker compose up
```


<!--
```bash
docker run -it ghcr.io/vemonet/libre-llm
```

## 📝 Define the API

Create a `main.py` file to declare the API, you can provide a different folder than `metrics` here, the folder path is relative to where you start the API (the root of the repository):

```python title="main.py"
from libre_llm import Api

api = API()
print(api.get_hello_world())
```
-->
