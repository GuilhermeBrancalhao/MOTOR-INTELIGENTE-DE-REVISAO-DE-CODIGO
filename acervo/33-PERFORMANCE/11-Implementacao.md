# Implementação

```python
from engine.volumes import PERFORMANCE
result = PERFORMANCE.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
