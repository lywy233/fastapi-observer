# fastapi-observer

en：A simple request observer based on FastAPI  
zh:一个简易的基于fastapi的请求观察器

## Usage Instructions

In general, use OpenResty as the gateway service and a FastAPI service as a request observer. When the gateway forwards requests, it also sends a copy to the observer, allowing the observer to fully inspect the input of each request.  
This setup is useful for monitoring model inputs, thereby gaining insight into the execution flow of intelligent agent applications.

## Quick Start

```bash
uv sync
python main.py
```

or

```bash
docker compose up -d
```
