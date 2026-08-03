# Implementação

```python
from engine.volumes import INTEGRATION
result = INTEGRATION.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
