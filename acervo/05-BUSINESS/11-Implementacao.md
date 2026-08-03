# Implementação

```python
from engine.volumes import BUSINESS
result = BUSINESS.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
