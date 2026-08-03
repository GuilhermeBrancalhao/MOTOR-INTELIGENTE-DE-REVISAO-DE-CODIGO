# Implementação

```python
from engine.volumes import DIAGRAMS
result = DIAGRAMS.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
