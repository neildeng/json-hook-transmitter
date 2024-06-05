
## json-hook-transmitter

WIP...

---

## Note...

WIP...

## How to ...

1. creat a transformer using python, for example transformer/sample.py

```python
import json
import os

def transform(raw):
    return {
        "new_field_1": "A",
        "new_field_2": "B",
        "new_field_3": "C"
    }
```

2. run as container

```shell
otherWebHookServer=http://localhost:5000/transformed
sudo podman run --name json-hook-transmitter --rm -it \
  -p 5001:5000 \
  -v ${PWD}/transformer/sample.py:/app/sample.py \
  -e WEBHOOK_PROXY_TRANSFORMER=sample \
  -e WEBHOOK_PROXY_DEBUG=true \
  -e REWRITE_ENDPOINT=${otherWebHookServer} \
  docker.io/neildeng/json-hook-transmitter:latest
```

3. try run

```shell
#health
curl http://localhost:5001/health | jq

#info
curl http://localhost:5001/info | jq

#webhook
curl -L -X POST http://localhost:5001/webhook -H "Content-Type: application/json" -d '{ "original_field_1": "A", "original_field_2": "B"}'

> {"response":{"new_field_1":"A","new_field_2":"B","new_field_3":"C"},"status":"success"}
```
