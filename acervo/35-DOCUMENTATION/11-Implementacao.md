# Implementação

```python
from engine.volumes import DOCUMENTATION
result = DOCUMENTATION.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
