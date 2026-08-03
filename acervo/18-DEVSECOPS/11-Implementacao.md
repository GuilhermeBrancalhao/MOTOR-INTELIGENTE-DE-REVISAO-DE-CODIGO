# Implementação

```python
from engine.volumes import DEVSECOPS
result = DEVSECOPS.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
