# Implementação

```python
from engine.volumes import CORE
result = CORE.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
