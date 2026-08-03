# Implementação

```python
from engine.volumes import TESTING
result = TESTING.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
