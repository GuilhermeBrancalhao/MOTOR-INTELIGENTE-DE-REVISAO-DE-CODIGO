# Implementação

```python
from engine.volumes import DEVOPS
result = DEVOPS.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
