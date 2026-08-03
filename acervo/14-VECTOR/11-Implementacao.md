# Implementação

```python
from engine.volumes import VECTOR
result = VECTOR.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
