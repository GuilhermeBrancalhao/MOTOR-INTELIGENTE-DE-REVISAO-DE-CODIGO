# Implementação

```python
from engine.volumes import CLOUD
result = CLOUD.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
