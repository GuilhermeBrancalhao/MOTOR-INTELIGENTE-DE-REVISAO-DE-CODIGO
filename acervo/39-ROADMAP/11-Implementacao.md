# Implementação

```python
from engine.volumes import ROADMAP
result = ROADMAP.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
