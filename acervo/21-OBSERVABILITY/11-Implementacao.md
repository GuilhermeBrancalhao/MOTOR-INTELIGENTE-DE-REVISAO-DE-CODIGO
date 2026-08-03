# Implementação

```python
from engine.volumes import OBSERVABILITY
result = OBSERVABILITY.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
